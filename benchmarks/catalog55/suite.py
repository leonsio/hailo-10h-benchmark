#!/usr/bin/env python3
"""Evaluate live answers, archive completed runs, then run Zoo 5.4 on the selected runtime."""
import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import time
from evaluate import evaluate,atomic_json,read_records
from report import render

HERE=Path(__file__).resolve().parent

def alive(pid):
    try:
        return Path(f'/proc/{pid}/stat').read_text().split()[2] not in ('Z','X')
    except FileNotFoundError:
        return False

def ensure_runtime(version_expected):
    version=subprocess.run(['hailortcli','--version'],capture_output=True,text=True,check=True).stdout
    firmware=subprocess.run(['hailortcli','fw-control','identify'],capture_output=True,text=True,check=True).stdout
    if version_expected not in version or f'Firmware Version: {version_expected}' not in firmware:
        raise RuntimeError('Queued experiment requires unchanged HailoRT and firmware '+version_expected)

def completed(output):
    meta=json.loads((output/'metadata.json').read_text())
    names={e['model'] for e in read_records(output/'events.jsonl') if e.get('event') in ('artifact_deleted','existing_artifact_preserved')}
    return set(meta['models'])<=names

def archive_results(output,destination):
    """Copy first, then hash and verify every archived file; never remove source."""
    destination.mkdir(parents=True,exist_ok=True)
    metadata=json.loads((output/'metadata.json').read_text())
    runtime=metadata.get('runtime','HailoRT-CLI version 5.4.0').strip().split()[-1]
    label='hailort-'+runtime+'_zoo-'+metadata['release']+'_'+time.strftime('%Y%m%d-%H%M%S')
    staging=destination/(label+'.staging')
    snapshot=staging/'results'
    shutil.copytree(output,snapshot,ignore=shutil.ignore_patterns('downloads','*.tmp','*.pid'))
    tools=staging/'tools'; tools.mkdir()
    for source in HERE.glob('*.py'): shutil.copyfile(source,tools/source.name)
    for pattern in ('*.json','*.md'):
        for source in HERE.glob(pattern): shutil.copyfile(source,tools/source.name)
    shutil.copyfile(HERE.parents[1]/'src/hailo_services/model_catalog.yaml',tools/'model_catalog.yaml')
    manifest={str(p.relative_to(staging)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(staging.rglob('*')) if p.is_file()}
    atomic_json(staging/'SHA256_MANIFEST.json',manifest)
    target=destination/(label+'.tar.gz')
    if target.exists(): raise FileExistsError(target)
    temporary=destination/(label+'.tar.gz.tmp')
    with tarfile.open(temporary,'w:gz') as archive:
        for path in sorted(staging.rglob('*')):
            archive.add(path,arcname=str(path.relative_to(staging)),recursive=False)
    with tarfile.open(temporary,'r:gz') as archive:
        with archive.extractfile('SHA256_MANIFEST.json') as manifest_file:
            archived=json.load(manifest_file)
        if archived!=manifest: raise RuntimeError('Archive manifest mismatch')
        for name,expected in manifest.items():
            with archive.extractfile(name) as file:
                if hashlib.file_digest(file,'sha256').hexdigest()!=expected:
                    raise RuntimeError('Archive verification failed: '+name)
    temporary.replace(target)
    with target.open('rb') as file: checksum=hashlib.file_digest(file,'sha256').hexdigest()
    target.with_suffix(target.suffix+'.sha256').write_text(checksum+'  '+target.name+'\n')
    target.chmod(0o444)
    target.with_suffix(target.suffix+'.sha256').chmod(0o444)
    shutil.rmtree(staging)
    return dict(path=str(target),sha256=checksum,files=len(manifest),verified=True)

def matrix_state(zoo,state,archive=None,runtime="5.4.0"):
    path=HERE/'test_matrix.json'
    matrix=json.loads(path.read_text())
    for experiment in matrix['experiments']:
        if experiment['hailort']==runtime and experiment['zoo']==zoo:
            experiment['state']=state
            if archive: experiment['archive']=archive
    atomic_json(path,matrix)


def monitor(pid,output,status_path,phase):
    last=None
    while alive(pid):
        if (output/'metadata.json').exists():
            answers=output/'answers.jsonl'
            stamp=(answers.stat().st_mtime_ns if answers.exists() else 0,(output/'events.jsonl').stat().st_mtime_ns if (output/'events.jsonl').exists() else 0,(output/'manual_reviews.json').stat().st_mtime_ns if (output/'manual_reviews.json').exists() else 0)
            if stamp!=last:
                evaluate(output); render(output)
                last=stamp
        atomic_json(status_path,dict(phase=phase,runner_pid=pid,output=str(output),updated=time.strftime('%Y-%m-%dT%H:%M:%S%z')))
        time.sleep(5)
    # Allow the independent performance reporter to finish its last update.
    time.sleep(6)
    if not completed(output):
        raise RuntimeError('Benchmark stopped with uncompleted models; source results preserved at '+str(output))
    evaluate(output); render(output)


def run(args):
    tag='runtime'+args.runtime.replace('.','')[:2]
    status=HERE/('results/suite_status_'+tag+'.json') if args.runtime!='5.4.0' else HERE/'results/suite_status.json'
    archives=HERE/'results/archives'
    try:
        # The active runner owns the device; validate its recorded preflight.
        first_meta=json.loads((args.first_output/'metadata.json').read_text())
        if args.runtime not in first_meta['runtime'] or 'Firmware Version: '+args.runtime not in first_meta['firmware']:
            raise RuntimeError('First benchmark runtime/firmware mismatch')
        matrix_state('v5.5.0','running_and_evaluating',runtime=args.runtime)
        monitor(args.first_pid,args.first_output,status,tag+'_zoo55_running_and_evaluating')
        atomic_json(status,dict(phase='archiving_'+tag+'_zoo55'))
        first=archive_results(args.first_output,archives)
        atomic_json(HERE/('results/archive_'+tag+'_zoo55.json'),first)
        matrix_state('v5.5.0','complete_archived',first,runtime=args.runtime)
        # Archive verification is a mandatory prerequisite for the next run.
        ensure_runtime(args.runtime)
        second=args.second_output
        command=[sys.executable,str(HERE/'run.py'),'--release','v5.4.0','--output',str(second),'--repeats','3','--max-tokens','128']
        second.mkdir(parents=True,exist_ok=True)
        if (args.first_output/'manual_reviews.json').exists():
            shutil.copyfile(args.first_output/'manual_reviews.json',second/'manual_reviews.json')
        matrix_state('v5.4.0','running_and_evaluating',runtime=args.runtime)
        with (second/'runner.log').open('a') as log:
            process=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,cwd=str(HERE))
        (second/'runner.pid').write_text(str(process.pid)+'\n')
        monitor(process.pid,second,status,tag+'_zoo54_running_and_evaluating')
        atomic_json(status,dict(phase='archiving_'+tag+'_zoo54',first_archive=first))
        second_archive=archive_results(second,archives)
        atomic_json(HERE/('results/archive_'+tag+'_zoo54.json'),second_archive)
        matrix_state('v5.4.0','complete_archived',second_archive,runtime=args.runtime)
        atomic_json(status,dict(phase=tag+'_suites_complete',archives=[first,second_archive],next='All requested runs on HailoRT '+args.runtime+' completed; editorial review may remain pending',updated=time.strftime('%Y-%m-%dT%H:%M:%S%z')))
    except Exception as exc:
        atomic_json(status,dict(phase='needs_attention',error=repr(exc),updated=time.strftime('%Y-%m-%dT%H:%M:%S%z')))
        raise

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime',choices=['5.4.0','5.5.0'],default='5.4.0')
    parser.add_argument('--first-pid',type=int,required=True)
    parser.add_argument('--first-output',type=Path,required=True)
    parser.add_argument('--second-output',type=Path,default=HERE/'results/runtime54-zoo54')
    args=parser.parse_args()
    with (HERE/'results/.suite.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        run(args)
