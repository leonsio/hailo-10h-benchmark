#!/usr/bin/env python3
"""Integrate the completed Qwen3-4B measurements into the final 5.5 experiment."""
import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT=Path(__file__).resolve().parents[1]
MODEL='Qwen3-4B-Instruct-2507'

def records(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]

def write_records(path,rows):
    path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))

def integrate(base):
    parent=base/'runtime55-zoo55';source=base/'runtime55-zoo55-qwen4b-persistent'
    meta=json.loads((parent/'metadata.json').read_text())
    if meta.get('integrated_model_measurements',{}).get(MODEL):
        return {'already_integrated':True}
    child=json.loads((source/'metadata.json').read_text())
    for field in ('runtime','firmware','release','questions_sha256','repeats','max_tokens','temperature','context_tokens','optimize_memory_on_device'):
        assert meta[field]==child[field],field
    answers=records(source/'answers.jsonl');loads=records(source/'loads.jsonl')
    assert len(answers)==198 and all(r['model']==MODEL and r['status']=='ok' for r in answers)
    keys={(r['repeat'],r['question'],r['language']) for r in answers};assert len(keys)==198
    assert Counter(r['repeat'] for r in answers)=={1:66,2:66,3:66}
    assert len(loads)==3 and {r['repeat'] for r in loads}=={1,2,3}
    provenance=parent/'provenance';before=provenance/'before-qwen-integration'
    before.mkdir(parents=True,exist_ok=False)
    # Keep an exact prior snapshot, including the failed download, for provenance.
    for path in parent.iterdir():
        if path.is_file():shutil.copy2(path,before/path.name)
    original_others=[r for r in records(parent/'answers.jsonl') if r['model']!=MODEL]
    for filename in ('answers.jsonl','loads.jsonl','events.jsonl'):
        prior=[r for r in records(parent/filename) if r.get('model')!=MODEL]
        supplement=records(source/filename)
        write_records(parent/filename,prior+supplement)
    reviews=json.loads((parent/'manual_reviews.json').read_text())
    reviews.update(json.loads((source/'manual_reviews.json').read_text()))
    (parent/'manual_reviews.json').write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+'\n')
    source_records={name:hashlib.sha256((source/name).read_bytes()).hexdigest() for name in ('answers.jsonl','loads.jsonl','events.jsonl','metadata.json')}
    meta['integrated_model_measurements']={MODEL:dict(source='provenance/qwen3-4b-measurements',original_started=child['started'],integrated_at=datetime.now().astimezone().isoformat(),prefetch=child.get('prefetch'),source_sha256=source_records,note='Same questions and inference settings; measured later after successful download, with background prefetch disabled. These are the three Qwen repetitions of this experiment.')}
    (parent/'metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    for path in source.glob(MODEL+'-*.log'):shutil.copy2(path,parent/path.name)
    shutil.move(str(source),str(provenance/'qwen3-4b-measurements'))
    failed=base/'runtime55-zoo55-qwen4b-retry'
    if failed.exists():shutil.move(str(failed),str(provenance/'qwen3-4b-download-attempt'))
    sys.path.insert(0,str(ROOT/'benchmarks/catalog55'))
    from evaluate import evaluate
    from report import render
    from run import summarize
    summarize(parent);scores=evaluate(parent);render(parent)
    merged=records(parent/'answers.jsonl')
    assert [r for r in merged if r['model']!=MODEL]==original_others
    assert len(merged)==2574 and len({(r['model'],r['repeat'],r['question'],r['language']) for r in merged})==2574
    assert sum(r['review_pending'] for r in scores)==0
    qwen=[r for r in scores if r['model']==MODEL]
    assert sum(r['objective_points'] for r in qwen)==98
    return dict(answers=len(merged),models=len(meta['models']),qwen_answers=198,qwen_loads=3,pending=0)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--results-dir',type=Path,default=ROOT/'benchmarks/catalog55/results');args=p.parse_args()
    print(json.dumps(integrate(args.results_dir)))
