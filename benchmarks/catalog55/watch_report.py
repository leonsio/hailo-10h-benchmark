"""Refresh the readable report while an already running benchmark completes."""
import json
from pathlib import Path
import sys
import time
from report import render

pid=int(sys.argv[1])
output=Path(sys.argv[2])
while True:
    try:
        render(output)
    except (FileNotFoundError,json.JSONDecodeError):
        pass
    try:
        state=Path(f'/proc/{pid}/stat').read_text().split()[2]
        running=state not in ('Z','X') and b'catalog55/run.py' in Path(f'/proc/{pid}/cmdline').read_bytes()
    except FileNotFoundError:
        running=False
    if not running:
        render(output)
        break
    time.sleep(5)
