"""Exercise download reuse and overlap without using accelerator hardware."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
import run as benchmark

class RunnerTests(unittest.TestCase):
    def test_prefetch_overlaps_inference_and_downloads_each_model_once(self):
        active=set()
        downloads=[]
        overlap=[]
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            source=root/'source.bin'
            source.write_bytes(b'X'*1048576)
            entry=lambda n:dict(kind='llm',filename=n+'.hef',minimum_bytes=1048576,maximum_bytes=2097152,releases={'v5.5.0':source.as_uri()})
            catalog={'models':{name:entry(name) for name in ('fake-a','fake-b')}}
            output=root/'results'
            class Worker:
                def __init__(self,cmd,**kwargs):
                    self.name=cmd[cmd.index('--worker')+1]
                    self.returncode=None
                    active.add(self.name)
                    def inference():
                        time.sleep(.1)
                        benchmark.append(output/'loads.jsonl',dict(model=self.name,repeat=1,kind='llm',load_s=.1))
                        time.sleep(1.2)
                        active.discard(self.name)
                        self.returncode=0
                    self.thread=threading.Thread(target=inference)
                    self.thread.start()
                def poll(self): return self.returncode
                def wait(self,timeout=None): self.thread.join(timeout); return self.returncode
                def kill(self): self.returncode=-9
                def terminate(self): self.returncode=-15
            args=argparse.Namespace(release='v5.5.0',resume=False,output=str(output),mode='all',models='fake-a,fake-b',local_model=None,download_cache=None,repeats=1,max_tokens=32,optimize_memory=False,native_timeout=300,stall_timeout=10,no_prefetch=False,limit=0,timeout=30)
            with patch.object(benchmark.fcntl,'flock'),patch('yaml.safe_load',return_value=catalog),patch.object(benchmark.subprocess,'Popen',Worker),patch.object(benchmark.shutil,'disk_usage',return_value=argparse.Namespace(free=20_000_000_000)):
                def transfer(cmd,**kwargs):
                    if cmd[0]=='curl':
                        downloads.append(cmd[cmd.index('--output')+1]); overlap.append('fake-a' in active)
                        Path(cmd[cmd.index('--output')+1]).write_bytes(source.read_bytes())
                        return subprocess.CompletedProcess(cmd,0)
                    return subprocess.CompletedProcess(cmd,1 if cmd[0]=='fuser' else 0,stdout='inactive' if cmd[0]=='systemctl' else 'test runtime',stderr='')
                with patch.object(benchmark.subprocess,'run',side_effect=transfer):
                    benchmark.main(args)
            events=[json.loads(line) for line in (output/'events.jsonl').read_text().splitlines()]
            self.assertEqual(len(downloads),2)
            self.assertEqual(overlap,[False,True])
            self.assertEqual(len([e for e in events if e['event']=='prefetch_started']),1)
            self.assertFalse(list((output/'downloads').iterdir()))

    def test_idle_guard_waits_for_resident_model_to_clear(self):
        busy=argparse.Namespace(ram_size_total=8_000_000,ram_size_used=6_000_000,nnc_utilization=0)
        idle=argparse.Namespace(ram_size_total=8_000_000,ram_size_used=250_000,nnc_utilization=0)
        with tempfile.TemporaryDirectory() as folder,patch('hailo_platform.Device') as device,patch.object(benchmark,'device_clients',return_value=([],[])),patch.object(benchmark.subprocess,'run',return_value=subprocess.CompletedProcess([],3,stdout='inactive',stderr='')),patch.object(benchmark.time,'sleep') as sleep:
            device.return_value.__enter__.return_value.control.query_performance_stats.side_effect=[busy,busy,idle]
            benchmark.wait_for_idle_device(Path(folder),'test',1)
            self.assertEqual(sleep.call_count,2)
            events=[json.loads(line) for line in (Path(folder)/'events.jsonl').read_text().splitlines()]
            self.assertEqual([e['event'] for e in events],['waiting_for_idle_device','device_idle_verified'])

    def test_monitor_is_not_treated_as_an_inference_client(self):
        result=subprocess.CompletedProcess([],0,stdout='123',stderr='')
        with patch.object(benchmark.subprocess,'run',return_value=result),patch.object(Path,'read_bytes',return_value=b'/usr/bin/hailortcli\0monitor\0'):
            self.assertEqual(benchmark.device_clients(),([],[123]))
        with patch.object(benchmark.subprocess,'run',return_value=result),patch.object(Path,'read_bytes',return_value=b'/usr/bin/python\0inference.py\0'):
            self.assertEqual(benchmark.device_clients(),([123],[]))

    def test_live_aggregation_includes_current_partial_repeat(self):
        rows=[dict(model='test',language='de',status='ok',ttft_s=value,total_s=value*2,tokens_per_s=4,decode_tokens_per_s=None) for value in (1,2,3)]
        loads=[dict(model='test',load_s=value) for value in (4,5,6)]
        values=benchmark.aggregate_summary(rows,loads,[],['test'])
        de=next(row for row in values if row['language']=='de')
        en=next(row for row in values if row['language']=='en')
        self.assertEqual(de['successful_answers'],3)
        self.assertEqual(de['successful_loads'],3)
        self.assertEqual(de['load_s_mean'],5)
        self.assertEqual(de['ttft_s_mean'],2)
        self.assertIsNone(de['decode_tokens_per_s_mean'])
        self.assertEqual(en['successful_answers'],0)
        self.assertIsNone(en['ttft_s_mean'])

    def test_memory_aggregation_preserves_missing_values_and_exact_size(self):
        from report import model_memory_rows
        metadata={'models':['loaded','failed']}
        loads=[{'model':'loaded','artifact_bytes':3*1024**3,'hailo_ram_loaded_bytes':1024**3,'host_rss_loaded_bytes':128*1024**2}, {'model':'loaded','hailo_ram_loaded_bytes':2*1024**3,'host_rss_loaded_bytes':256*1024**2}, {'model':'loaded'}]
        events=[{'model':'failed','event':'downloaded','bytes':5*1024**3}]
        loaded,failed=model_memory_rows(metadata,loads,events)
        self.assertEqual(loaded['artifact_bytes'],3*1024**3)
        self.assertEqual(loaded['hailo_ram_loaded_bytes_mean'],1.5*1024**3)
        self.assertEqual(loaded['hailo_ram_loaded_bytes_samples'],2)
        self.assertEqual(loaded['host_rss_loaded_bytes_mean'],192*1024**2)
        self.assertEqual(failed['artifact_bytes'],5*1024**3)
        self.assertIsNone(failed['hailo_ram_loaded_bytes_mean'])
        self.assertEqual(failed['hailo_ram_loaded_bytes_samples'],0)

    def test_selected_zoo_release_is_used_for_download(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); artifact=root/'versioned.hef'
            urls={'v5.4.0':'https://example.invalid/5.4/model.hef','v5.5.0':'https://example.invalid/5.5/model.hef'}
            entry=dict(kind='llm',minimum_bytes=1,maximum_bytes=100,releases=urls)
            def transfer(cmd,**kwargs):
                self.assertEqual(cmd[-1],urls['v5.4.0'])
                artifact.write_bytes(b'zoo54')
                return subprocess.CompletedProcess(cmd,0)
            with patch.object(benchmark.subprocess,'run',side_effect=transfer),patch.object(benchmark.shutil,'disk_usage',return_value=argparse.Namespace(free=20_000_000_000)):
                benchmark.prepare_artifact('model',entry,artifact,root,release='v5.4.0')
            receipt=json.loads((root/'versioned.hef.receipt.json').read_text())
            self.assertEqual(receipt['url'],urls['v5.4.0'])

    def test_cached_download_is_verified_without_redownload(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            artifact=root/'model.hef'
            artifact.write_bytes(b'known weights')
            import hashlib
            entry=dict(kind='llm',minimum_bytes=1,maximum_bytes=100,releases={'v5.5.0':'https://example.invalid/model.hef'})
            benchmark.write_json(root/'model.hef.receipt.json',dict(url=entry['releases']['v5.5.0'],bytes=artifact.stat().st_size,sha256=hashlib.sha256(artifact.read_bytes()).hexdigest()))
            with patch.object(benchmark.subprocess,'run') as network:
                benchmark.prepare_artifact('model',entry,artifact,root)
                network.assert_not_called()
            artifact.write_bytes(b'corrupted')
            with self.assertRaisesRegex(RuntimeError,'receipt mismatch'):
                benchmark.prepare_artifact('model',entry,artifact,root)

    def test_local_model_is_read_without_receipt_or_download(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            artifact=root/'service.hef'
            artifact.write_bytes(b'service weights')
            entry=dict(kind='llm',minimum_bytes=1,maximum_bytes=100,releases={'v5.5.0':'https://example.invalid/model.hef'})
            with patch.object(benchmark.subprocess,'run') as network:
                benchmark.prepare_artifact('service',entry,artifact,root,local=True)
                network.assert_not_called()
            self.assertEqual(artifact.read_bytes(),b'service weights')
            self.assertFalse((root/'service.hef.receipt.json').exists())

if __name__=='__main__': unittest.main()
