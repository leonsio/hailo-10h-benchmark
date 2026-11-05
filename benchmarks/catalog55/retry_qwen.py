#!/usr/bin/env python3
"""Run the requested Qwen retry after the existing runtime-5.5 suite."""
import json
from pathlib import Path
import subprocess
import sys
import time
from suite import HERE,alive,ensure_runtime,monitor,archive_results
from evaluate import atomic_json

results=HERE/'results'
status=results/'qwen-retry-status.json'
output=results/'runtime55-zoo55-qwen4b-retry'

def run():
    try:
        pid=int((results/'suite-runtime55.pid').read_text())
        atomic_json(status,dict(phase='queued_after_both_catalog_runs',output=str(output)))
        while alive(pid): time.sleep(5)
        state=json.loads((results/'suite_status_runtime55.json').read_text())
        if state.get('phase')!='runtime55_suites_complete':
            raise RuntimeError('Previous suite did not finish; retry remains deferred')
        ensure_runtime('5.5.0')
        output.mkdir(exist_ok=True)
        reviews=results/'runtime55-zoo55/manual_reviews.json'
        if reviews.exists(): (output/'manual_reviews.json').write_bytes(reviews.read_bytes())
        with (output/'runner.log').open('a') as log:
            process=subprocess.Popen([sys.executable,str(HERE/'run.py'),'--release','v5.5.0','--mode','hailo','--models','Qwen3-4B-Instruct-2507','--repeats','3','--max-tokens','128','--no-prefetch','--output',str(output)],cwd=output,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        (output/'runner.pid').write_text(str(process.pid)+'\n')
        monitor(process.pid,output,status,'runtime55_qwen4b_retry_running')
        archive=archive_results(output,results/'archives')
        atomic_json(status,dict(phase='retry_complete_archived',output=str(output),archive=archive))
    except Exception as exc:
        atomic_json(status,dict(phase='needs_attention',error=repr(exc),output=str(output)))
        raise

if __name__=='__main__': run()
