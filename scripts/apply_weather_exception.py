#!/usr/bin/env python3
"""Apply reviewed E05 missing-data exceptions without changing measurements."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'benchmarks/catalog55'))
from evaluate import evaluate,atomic_json
from report import render

MAIN=['runtime54-prefetch','runtime54-zoo54','runtime55-zoo55','runtime55-zoo54']

def apply(results):
    decisions=json.loads((ROOT/'benchmarks/catalog55/weather_exception_reviews.json').read_text())['decisions']
    changes=[]
    for name in MAIN:
        p=results/name
        previous=json.loads((p/'correctness_summary.json').read_text())
        history=p/'evaluation_history/before_weather_exception_v1.4'
        if not history.exists():
            history.mkdir(parents=True)
            for f in ['manual_reviews.json','correctness_summary.json','correctness_summary.csv','answer_checks.jsonl','evaluation_metadata.json','review_queue.json','report.md']:
                shutil.copy2(p/f,history/f)
        hashes={f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in ('answers.jsonl','loads.jsonl')}
        reviews=json.loads((p/'manual_reviews.json').read_text());reviews.update(decisions);atomic_json(p/'manual_reviews.json',reviews)
        scores=evaluate(p);render(p)
        assert not sum(r['review_pending'] for r in scores)
        for f,value in hashes.items():assert hashlib.sha256((p/f).read_bytes()).hexdigest()==value
        before={(r['model'],r['language']):r for r in previous}
        changed=[]
        for r in scores:
            old=before[(r['model'],r['language'])]
            assert r['objective_points']==old['objective_points']
            if r['manual_quality_points']!=old['manual_quality_points']:
                changed.append(dict(model=r['model'],language=r['language'],old_editorial_points=old['manual_quality_points'],new_editorial_points=r['manual_quality_points']))
        changes.append(dict(run=name,changes=changed,measurement_hashes=hashes,review_pending=0))
    atomic_json(results/'weather_exception_v1.4_changes.json',changes)
    return changes

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--results-dir',type=Path,default=ROOT/'benchmarks/catalog55/results');args=p.parse_args()
    print(json.dumps(apply(args.results_dir),ensure_ascii=False,indent=2))
