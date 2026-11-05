#!/usr/bin/env python3
"""Sequential native chat benchmark; only owned downloads are removed.

Run with /opt/hailo-10h-services/venv/bin/python benchmarks/catalog55/run.py.
Each repetition reloads the model in a subprocess; every question has fresh KV
context. Model load timing excludes download, Python imports and VDevice creation.
"""
from __future__ import annotations
import argparse
import csv
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'src'))

def write_json(path, value):
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
    tmp.replace(path)

_APPEND_LOCK = threading.Lock()

def append(path, value):
    with _APPEND_LOCK, path.open('a') as out:
        out.write(json.dumps(value, ensure_ascii=False)+'\n')
        out.flush()
        os.fsync(out.fileno())

def chunk_text(chunk):
    if isinstance(chunk, str):
        return chunk
    if hasattr(chunk, 'to_json'):
        chunk = chunk.to_json()
    if isinstance(chunk, str):
        chunk = json.loads(chunk)
    if isinstance(chunk, dict):
        content = chunk.get('content', [])
        return content if isinstance(content, str) else ''.join(p.get('text','') for p in content if isinstance(p,dict) and p.get('type')=='text')
    return ''

SYSTEM = {
'de':'Isolierter Sprachmodell-Benchmark. Folge der Benutzeranweisung exakt. Antworte auf Deutsch, sofern die Aufgabe keine andere Sprache verlangt. Keine Präambel. Es stehen keine Wetterdaten und keine Gerätewerkzeuge zur Verfügung. Behaupte nicht, Geräteaktionen ausgeführt zu haben.',
'en':'Isolated language model benchmark. Follow the user instruction exactly. Answer in English unless the task requires another language. No preamble. No weather data or device tools are available. Do not claim to have executed device actions.'}

def worker(args):
    import yaml
    catalog = yaml.safe_load((ROOT/'src/hailo_services/model_catalog.yaml').read_text())['models']
    entry = catalog[args.worker]
    kind = entry['kind']
    questions = json.loads((HERE/'questions.json').read_text())['questions']
    if args.limit:
        questions = questions[:args.limit]
    output = Path(args.output)
    with ExitStack() as stack:
        if kind == 'litert':
            import litert_lm
            t = time.perf_counter()
            model = stack.enter_context(litert_lm.Engine(args.artifact, backend=litert_lm.Backend.CPU(), max_num_tokens=2048))
            load_s = time.perf_counter()-t
        else:
            from hailo_platform import VDevice
            from hailo_platform.genai import LLM, VLM
            from hailo_services.chat.chat_common import render_prompt
            params = VDevice.create_params()
            params.group_id = 'SHARED'
            device = stack.enter_context(VDevice(params))
            t = time.perf_counter()
            model = stack.enter_context((VLM if kind=='vlm' else LLM)(device, args.artifact, optimize_memory_on_device=args.optimize_memory))
            load_s = time.perf_counter()-t
        append(output/'loads.jsonl', dict(model=args.worker, repeat=args.repeat, load_s=load_s, kind=kind))
        for question in questions:
            for lang in ('de','en'):
                row = dict(model=args.worker, kind=kind, repeat=args.repeat, question=question['id'], category=question['category'], language=lang, prompt=question[lang], load_s=load_s)
                try:
                    messages = [{'role':'system','content':SYSTEM[lang]}, {'role':'user','content':question[lang]}]
                    first = None
                    last = None
                    pieces = []
                    if kind=='litert':
                        start = time.perf_counter()
                        with model.create_conversation(messages=messages[:1], sampler_config=litert_lm.SamplerConfig(temperature=0.1,seed=args.repeat), max_output_tokens=args.max_tokens) as conversation:
                            for chunk in conversation.send_message_async(question[lang], max_output_tokens=args.max_tokens):
                                text = chunk_text(chunk)
                                if text:
                                    now = time.perf_counter()
                                    first = first or now
                                    last = now
                                    pieces.append(text)
                    else:
                        if kind=='vlm':
                            messages = [dict(role=m['role'], content=[{'type':'text','text':m['content']}]) for m in messages]
                        prompt = render_prompt(model, messages, model_kind=kind.upper(), template_options=entry.get('prompt_template'))
                        start = time.perf_counter()
                        model.clear_context()
                        with model.generate(prompt=prompt, **({'frames':[]} if kind=='vlm' else {}), temperature=0.1, seed=args.repeat, max_generated_tokens=args.max_tokens) as generation:
                            for text in generation:
                                if text:
                                    now = time.perf_counter()
                                    first = first or now
                                    last = now
                                    pieces.append(text)
                        model.clear_context()
                    end = time.perf_counter()
                    answer = ''.join(pieces)
                    # Count using each model's own tokenizer, never streaming chunks.
                    tokens = len(model.tokenize(answer)) if answer else 0
                    first_piece_tokens = len(model.tokenize(pieces[0])) if pieces else 0
                    decode_s = last-first if last is not None and first is not None else 0
                    row.update(status='ok', answer=answer, output_tokens=tokens, token_count_source='retokenized_output', ttft_s=first-start if first else None, total_s=end-start, tokens_per_s=tokens/(end-start), decode_tokens_per_s=(tokens-first_piece_tokens)/decode_s if decode_s>0 and tokens>first_piece_tokens else None)
                except Exception as exc:
                    row.update(status='error', error=repr(exc))
                append(output/'answers.jsonl', row)
                print(f"{args.worker} run={args.repeat} {question['id']} {lang}: {row['status']}", flush=True)


def summarize(output):
    rows = [json.loads(line) for line in (output/'answers.jsonl').read_text().splitlines()] if (output/'answers.jsonl').exists() else []
    loads = [json.loads(line) for line in (output/'loads.jsonl').read_text().splitlines()] if (output/'loads.jsonl').exists() else []
    summaries = []
    planned = json.loads((output/'metadata.json').read_text()).get('models',[]) if (output/'metadata.json').exists() else []
    events = [json.loads(line) for line in (output/'events.jsonl').read_text().splitlines()] if (output/'events.jsonl').exists() else []
    for model in sorted(set(planned) | {r['model'] for r in rows}):
        for lang in ('de','en'):
            selected = [r for r in rows if r['model']==model and r['language']==lang and r['status']=='ok']
            s = dict(model=model, language=lang, successful_answers=len(selected), errors=sum(r['status']!='ok' for r in rows if r['model']==model and r['language']==lang), successful_loads=sum(r['model']==model for r in loads), failed_starts=sum(e.get('model')==model and (e.get('event')=='timeout' or (e.get('event')=='worker_exit' and e.get('returncode')!=0)) for e in events))
            for key in ('ttft_s','total_s','tokens_per_s','decode_tokens_per_s'):
                vals = [r[key] for r in selected if r.get(key) is not None]
                s[key+'_mean'] = statistics.mean(vals) if vals else None
            times = [r['load_s'] for r in loads if r['model']==model]
            s['load_s_mean'] = statistics.mean(times) if times else None
            summaries.append(s)
    write_json(output/'summary.json', summaries)
    if summaries:
        with (output/'summary.csv').open('w') as out:
            writer=csv.DictWriter(out, fieldnames=list(summaries[0]))
            writer.writeheader(); writer.writerows(summaries)
    grouped = {}
    for r in rows:
        if r['status']=='ok':
            grouped.setdefault((r['model'],r['question'],r['language']),[]).append(r)
    per_question=[]
    for (model,qid,lang),items in grouped.items():
        s=dict(model=model,question=qid,language=lang,successful_repeats=len(items))
        for key in ('ttft_s','total_s','tokens_per_s','decode_tokens_per_s'):
            vals=[r[key] for r in items if r.get(key) is not None]
            s[key+'_mean']=statistics.mean(vals) if vals else None
        per_question.append(s)
    write_json(output/'question_means.json',per_question)


def prepare_artifact(name, entry, artifact, output, local=False):
    """Download once, verify, and return a receipt; safe in one prefetch thread."""
    receipt=artifact.with_suffix(artifact.suffix+'.receipt.json')
    url=entry['url'] if entry['kind']=='litert' else entry['releases']['v5.5.0']
    reused=not local and artifact.exists() and receipt.exists()
    print(f'Existing model {name}: {artifact}' if local else f'Reuse completed download {name}: {artifact}' if reused else f'Download {name}: {url}',flush=True)
    if not local and not reused:
        # Reserve space for the largest allowed artifact plus 1 GB headroom.
        if shutil.disk_usage(artifact.parent).free < entry['maximum_bytes']+1_000_000_000:
            raise RuntimeError('Insufficient disk space for next model and safety reserve')
        command=['curl','--silent','--show-error','--fail','--location','--retry','3','--connect-timeout','30','--max-time','3600','--output',str(artifact)]
        resumed=artifact.exists() and artifact.stat().st_size>0
        if resumed:
            command+=['--continue-at','-']
        result=subprocess.run(command+[url])
        if result.returncode==33 and resumed:
            result=subprocess.run([c for i,c in enumerate(command) if i not in (len(command)-2,len(command)-1)]+[url])
        if result.returncode:
            raise RuntimeError(f'download exit {result.returncode}')
    size=artifact.stat().st_size
    if not entry['minimum_bytes']<=size<=entry['maximum_bytes']:
        raise RuntimeError(f'invalid artifact size {size}')
    with artifact.open('rb') as downloaded:
        sha=hashlib.file_digest(downloaded,'sha256').hexdigest()
    value=dict(url=url,bytes=size,sha256=sha)
    if reused and json.loads(receipt.read_text())!=value:
        raise RuntimeError('Cached artifact receipt mismatch')
    if not local:
        write_json(receipt,value)
    append(output/'events.jsonl',dict(model=name,event='existing_artifact' if local else 'cached_download' if reused else 'downloaded',**value))
    return artifact


def main(args):
    import yaml
    output=Path(args.output).resolve()
    output.mkdir(parents=True,exist_ok=True)
    lock=(HERE/'.run.lock').open('w')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if (output/'events.jsonl').exists():
        raise RuntimeError('Choose a new --output to prevent mixed measurements')
    active=subprocess.run(['systemctl','is-active','hailo-10h-services'],capture_output=True,text=True).stdout.strip()
    if active not in ('inactive','failed','unknown'):
        raise RuntimeError('Stop hailo-10h-services before running: '+active)
    users=subprocess.run(['fuser','/dev/h1x-0'],capture_output=True,text=True)
    if users.returncode==0:
        raise RuntimeError('Hailo device still in use: '+users.stdout)
    free=shutil.disk_usage(output).free
    if free<10_000_000_000:
        raise RuntimeError('At least 10 GB free disk required')
    catalog=yaml.safe_load((ROOT/'src/hailo_services/model_catalog.yaml').read_text())['models']
    models=[n for n,e in catalog.items() if e['kind'] in ('llm','vlm') and 'v5.5.0' in e.get('releases',{})]
    priority=['Qwen3-4B-Instruct-2507','Gemma4-E2B-Instruct','Qwen3-VL-4B-Instruct']
    models=priority+[n for n in models if n not in priority]
    if args.mode=='cpu': models=[]
    if args.mode!='hailo': models+=['gemma-4-E2B-it']
    if args.models:
        requested=args.models.split(',')
        if set(requested)-set(models):
            raise ValueError('Unknown or unavailable selected model')
        models=requested
    if args.local_model and len(models)!=1:
        raise ValueError('--local-model requires exactly one --models entry')
    runtime=subprocess.run(['hailortcli','--version'],capture_output=True,text=True).stdout.strip()
    write_json(output/'metadata.json',dict(started=time.strftime('%Y-%m-%dT%H:%M:%S%z'),runtime=runtime,firmware=subprocess.run(['hailortcli','fw-control','identify'],capture_output=True,text=True).stdout,free_disk_bytes=free,meminfo=Path('/proc/meminfo').read_text(),models=models,repeats=args.repeats,max_tokens=args.max_tokens,release='existing-service-artifact' if args.local_model else 'v5.5.0',temperature=0.1,context_tokens=2048,service_state=active,optimize_memory_on_device=args.optimize_memory,native_request_timeout_s=args.native_timeout,stall_timeout_s=args.stall_timeout,prefetch=not args.no_prefetch,questions_sha256=hashlib.sha256((HERE/'questions.json').read_bytes()).hexdigest(),measurements='TTFT includes context setup; tokens/s uses retokenized output. Native loads exclude download/import/VDevice creation. OS cache uncontrolled. VLM chat is text-only. One next artifact may download and hash in background during inference and later reloads.'))
    shutil.copyfile(HERE/'questions.json',output/'questions.json')
    shutil.copyfile(Path(__file__),output/'run_snapshot.py')
    cache=Path(args.download_cache).resolve() if args.download_cache else output/'downloads'
    if not cache.is_relative_to(HERE/'results') and cache!=output/'downloads':
        raise ValueError('Shared download cache must be under benchmarks/catalog55/results')
    cache.mkdir(parents=True,exist_ok=True)
    futures={}
    # One download thread; at most current + next artifact, never two native models.
    with ThreadPoolExecutor(max_workers=1,thread_name_prefix='model-download') as pool:
        try:
            for index,name in enumerate(models):
                artifact=Path(args.local_model).resolve() if args.local_model else cache/catalog[name]['filename']
                receipt=artifact.with_suffix(artifact.suffix+'.receipt.json')
                next_started=False
                try:
                    if name in futures:
                        futures.pop(name).result()
                    else:
                        prepare_artifact(name,catalog[name],artifact,output,local=bool(args.local_model))
                    for repeat in range(1,args.repeats+1):
                        command=[sys.executable,str(Path(__file__).resolve()),'--worker',name,'--artifact',str(artifact),'--repeat',str(repeat),'--output',str(output),'--max-tokens',str(args.max_tokens),'--limit',str(args.limit)]
                        if args.optimize_memory: command+=['--optimize-memory']
                        native_env=dict(os.environ,HAILO_REQUEST_TIMEOUT_SECONDS=str(args.native_timeout))
                        with (output/(name+f'-{repeat}.log')).open('w') as log:
                            process=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,env=native_env)
                            launched=progress=time.monotonic()
                            sizes=tuple((output/f).stat().st_size if (output/f).exists() else 0 for f in ('loads.jsonl','answers.jsonl'))
                            timed_out=False
                            try:
                                while process.poll() is None:
                                    current=tuple((output/f).stat().st_size if (output/f).exists() else 0 for f in ('loads.jsonl','answers.jsonl'))
                                    if current!=sizes:
                                        progress=time.monotonic()
                                    if current[0]>sizes[0] and not next_started and not args.no_prefetch and not args.local_model and index+1<len(models):
                                        next_name=models[index+1]
                                        append(output/'events.jsonl',dict(model=next_name,event='prefetch_started',while_testing=name))
                                        futures[next_name]=pool.submit(prepare_artifact,next_name,catalog[next_name],cache/catalog[next_name]['filename'],output)
                                        next_started=True
                                    sizes=current
                                    if time.monotonic()-progress>args.stall_timeout or time.monotonic()-launched>args.timeout:
                                        process.kill(); process.wait()
                                        timed_out=True
                                        append(output/'events.jsonl',dict(model=name,repeat=repeat,event='timeout',elapsed_s=time.monotonic()-launched))
                                        break
                                    time.sleep(0.5)
                            finally:
                                if process.poll() is None:
                                    process.terminate()
                                    try: process.wait(timeout=15)
                                    except subprocess.TimeoutExpired: process.kill(); process.wait()
                            if not timed_out:
                                append(output/'events.jsonl',dict(model=name,repeat=repeat,event='worker_exit',returncode=process.returncode))
                        summarize(output)
                except Exception as exc:
                    append(output/'events.jsonl',dict(model=name,event='error',error=repr(exc)))
                finally:
                    if args.local_model:
                        append(output/'events.jsonl',dict(model=name,event='existing_artifact_preserved'))
                    else:
                        artifact.unlink(missing_ok=True)
                        receipt.unlink(missing_ok=True)
                        append(output/'events.jsonl',dict(model=name,event='artifact_deleted'))
        finally:
            summarize(output)
    print(f'Results: {output}',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default=str(HERE/'results'/time.strftime('%Y%m%d-%H%M%S')))
    parser.add_argument('--mode',choices=['all','hailo','cpu'],default='all')
    parser.add_argument('--no-prefetch',action='store_true',help='Disable next-model background download')
    parser.add_argument('--optimize-memory',action='store_true',help='Enable host tokenization; required for selected models on 4 GB Hailo, default off for this 8 GB device')
    parser.add_argument('--native-timeout',type=int,default=300,help='Hailo HRPC request timeout seconds')
    parser.add_argument('--download-cache',help='Reuse verified test downloads under benchmarks/catalog55/results')
    parser.add_argument('--local-model',help='Read an existing artifact for one selected model; never delete it')
    parser.add_argument('--models',default='')
    parser.add_argument('--repeats',type=int,default=3)
    parser.add_argument('--max-tokens',type=int,default=128)
    parser.add_argument('--stall-timeout',type=int,default=600,help='Kill worker after this many seconds without a load or answer')
    parser.add_argument('--timeout',type=int,default=14400,help='Timeout seconds per model repetition')
    parser.add_argument('--limit',type=int,default=0,help='Smoke test only: limit questions')
    parser.add_argument('--worker')
    parser.add_argument('--artifact')
    parser.add_argument('--repeat',type=int,default=1)
    args=parser.parse_args()
    if args.worker: worker(args)
    else: main(args)
