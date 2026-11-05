#!/usr/bin/env python3
"""Persistently download verified HTTP ranges, then run and archive Qwen4B."""
import fcntl
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from evaluate import atomic_json
from suite import HERE,ensure_runtime,monitor,archive_results

RESULTS=HERE/'results'
OUTPUT=RESULTS/'runtime55-zoo55-qwen4b-persistent'
STATUS=RESULTS/'qwen-retry-status.json'
MODEL='Qwen3-4B-Instruct-2507'
URL='https://dev-public.hailo.ai/v5.5.0/blob/'+MODEL+'.hef'
SIZE=5656354387
SHA='033e4e3b2c90d41b2f02620144f4faa0908e7333e98b8766c6c63b9cdbb93d6e'
CHUNK=32*1024*1024

def state(phase,**kwargs):
    atomic_json(STATUS,dict(phase=phase,output=str(OUTPUT),updated=time.strftime('%Y-%m-%dT%H:%M:%S%z'),**kwargs))

def download():
    cache=OUTPUT/'downloads';cache.mkdir(parents=True,exist_ok=True)
    artifact=cache/(MODEL+'.hef')
    part=cache/(MODEL+'.chunk')
    headers=cache/'range.headers'
    attempt=0
    while True:
        have=artifact.stat().st_size if artifact.exists() else 0
        if have>SIZE:
            artifact.unlink();continue
        if have==SIZE:
            state('verifying_download',bytes=have,total_bytes=SIZE)
            with artifact.open('rb') as f: actual=hashlib.file_digest(f,'sha256').hexdigest()
            if actual==SHA:
                atomic_json(artifact.with_suffix('.hef.receipt.json'),dict(url=URL,bytes=SIZE,sha256=SHA))
                state('download_verified',bytes=have,total_bytes=SIZE,sha256=actual)
                return cache
            state('download_checksum_mismatch_retrying',sha256=actual,expected=SHA)
            # A bad artifact cannot be used; preserve the failure in the log.
            print('SHA256 mismatch:',actual,'restarting download',flush=True)
            artifact.unlink();time.sleep(10);continue
        if shutil.disk_usage(cache).free<SIZE-have+1_000_000_000:
            state('waiting_for_disk_space',bytes=have,total_bytes=SIZE)
            time.sleep(30);continue
        end=min(have+CHUNK,SIZE)-1
        attempt+=1
        state('downloading_with_retries',bytes=have,total_bytes=SIZE,attempt=attempt)
        print(f'Range {have}-{end}; attempt {attempt}',flush=True)
        command=['curl','--http1.1','--silent','--show-error','--fail','--location','--connect-timeout','30','--max-time','180','--range',f'{have}-{end}','--dump-header',str(headers),'--output',str(part),URL]
        result=subprocess.run(command)
        # Accept even a truncated transfer only after its exact range is confirmed.
        content=headers.read_text() if headers.exists() else ''
        ranges=re.findall(r'(?im)^Content-Range:\s*bytes\s+(\d+)-(\d+)/(\d+)\s*$',content)
        actual_size=part.stat().st_size if part.exists() else 0
        valid=bool(ranges and tuple(map(int,ranges[-1]))==(have,end,SIZE) and 0<actual_size<=end-have+1)
        if valid:
            with artifact.open('ab') as dest,part.open('rb') as source:shutil.copyfileobj(source,dest)
            part.unlink()
            state('downloading_with_retries',bytes=have+actual_size,total_bytes=SIZE,attempt=attempt,last_curl_exit=result.returncode)
            print(f'Confirmed {have+actual_size}/{SIZE} bytes; curl exit {result.returncode}',flush=True)
        else:
            print('Unconfirmed range response; retrying, curl exit',result.returncode,flush=True)
        if result.returncode or not valid:time.sleep(10)

def run():
    OUTPUT.mkdir(parents=True,exist_ok=True)
    try:
        cache=download()
        ensure_runtime('5.5.0')
        reviews=RESULTS/'runtime55-zoo55/manual_reviews.json'
        if reviews.exists() and not (OUTPUT/'manual_reviews.json').exists():shutil.copyfile(reviews,OUTPUT/'manual_reviews.json')
        # run.py owns deletion only after testing; completed receipts avoid a new download.
        command=[sys.executable,str(HERE/'run.py'),'--release','v5.5.0','--mode','hailo','--models',MODEL,'--repeats','3','--max-tokens','128','--no-prefetch','--download-cache',str(cache),'--output',str(OUTPUT)]
        if (OUTPUT/'metadata.json').exists():command.append('--resume')
        with (OUTPUT/'runner.log').open('a') as log:
            process=subprocess.Popen(command,cwd=OUTPUT,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        (OUTPUT/'runner.pid').write_text(str(process.pid)+'\n')
        monitor(process.pid,OUTPUT,STATUS,'runtime55_qwen4b_retry_running')
        archive=archive_results(OUTPUT,RESULTS/'archives')
        state('retry_complete_archived',archive=archive)
    except Exception as exc:
        state('needs_attention',error=repr(exc))
        raise

if __name__=='__main__':
    with (RESULTS/'.qwen-persistent.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        run()
