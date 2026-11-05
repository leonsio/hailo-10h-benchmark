#!/usr/bin/env python3
"""Read-only local benchmark dashboard; never opens the Hailo device."""
import argparse
from collections import Counter
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
RESULTS=HERE/'results'
RUNS=['runtime55-zoo55','runtime55-zoo54','runtime54-prefetch','runtime54-zoo54']

def read_json(path, default):
    try: return json.loads(path.read_text())
    except (OSError,ValueError): return default

def records(path):
    try: lines=path.read_text().splitlines()
    except OSError: return []
    rows=[]
    for line in lines:
        try: rows.append(json.loads(line))
        except ValueError: pass
    return rows

def snapshot():
    runs=[]
    matrix=read_json(HERE/'test_matrix.json',{}).get('experiments',[])
    for name in RUNS:
        p=RESULTS/name;meta=read_json(p/'metadata.json',{})
        experiment=next((r for r in matrix if r.get('output','').endswith('/'+name)),{})
        models=meta.get('models',[])
        answers=records(p/'answers.jsonl');events=records(p/'events.jsonl');loads=records(p/'loads.jsonl')
        summary=read_json(p/'live_summary.json',[]);quality=read_json(p/'correctness_summary.json',[])
        finished={r['model'] for r in events if r.get('event') in ('artifact_deleted','existing_artifact_preserved')}
        names=list(models)
        table=[]
        for model in names:
            rows=[r for r in answers if r['model']==model]
            ls=[r for r in loads if r['model']==model and 'load_s' in r]
            qs=[r for r in quality if r['model']==model]
            ms=next((r for r in read_json(p/'model_sizes.json',[]) if r['model']==model),{})
            errors=[r.get('error',r.get('status','Fehler')) for r in events if r.get('model')==model and ('error' in r or r.get('event')=='worker_failed')]
            avg=lambda vals:sum(vals)/len(vals) if vals else None
            langs={lang:avg([r['ttft_s'] for r in rows if r.get('language')==lang and r.get('ttft_s') is not None]) for lang in ('de','en')}
            table.append(dict(model=model,answers=len(rows),loads=len(ls),done=model in finished,
                state='Abgeschlossen' if model in finished and rows else 'Fehlgeschlagen' if model in finished else 'Läuft' if rows or ls else 'Ausstehend',
                load=avg([r['load_s'] for r in ls]),ttft=langs,
                tps=avg([r['decode_tokens_per_s'] for r in rows if r.get('decode_tokens_per_s') is not None]),
                file=ms.get('artifact_bytes'),ram=ms.get('hailo_ram_loaded_bytes_mean'),
                points=sum(r.get('objective_points',0) for r in qs),scored=sum(r.get('objective_scored',0) for r in qs),
                pending=sum(r.get('review_pending',0) for r in qs),quality_points=sum(r.get('manual_quality_points',r.get('manual_quality_pass',0)) for r in qs),quality_pass=sum(r.get('manual_quality_pass',0) for r in qs),quality_reviewed=sum(r.get('manual_reviewed',0) for r in qs),errors=errors[-1:]))
        downloads=[dict(name=f.name,bytes=f.stat().st_size) for f in (p/'downloads').glob('*.hef') if f.exists()]
        runs.append(dict(name=name,runtime=meta.get('runtime'),release=meta.get('release'),state=experiment.get('state','Ausstehend'),models=len(models),finished=len(finished),answers=len(answers),expected=len(models)*198,table=table,downloads=downloads,events=events[-5:]))
    return dict(time=datetime.now().astimezone().isoformat(),suite=read_json(RESULTS/'suite_status_runtime55.json',{}),runs=runs)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path=self.path.split('?',1)[0]
        if path=='/':
            body=(HERE/'status.html').read_bytes();kind='text/html; charset=utf-8'
        elif path=='/api/status':
            body=json.dumps(snapshot(),ensure_ascii=False).encode();kind='application/json; charset=utf-8'
        else:
            self.send_error(404);return
        self.send_response(200);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(body)
    def log_message(self,*args): pass

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8090);parser.add_argument('--host',default='0.0.0.0');args=parser.parse_args()
    ThreadingHTTPServer((args.host,args.port),Handler).serve_forever()
