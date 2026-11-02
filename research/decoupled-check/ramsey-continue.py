#!/usr/bin/env python3
"""Wait for the submitted first source task, then continue this finite closure."""
import os,json,select,importlib.util
from pathlib import Path
os.sched_setaffinity(0,{8})
A=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/ramsey-20261102')
def main():
 v=json.loads((A/'first-target-submission.json').read_text());p=Path('/proc/'+str(v['pid']))
 if p.exists()and p.joinpath('stat').read_text().split(') ')[1].split()[19]==str(v['birth']):
  try:fd=os.pidfd_open(v['pid'])
  except ProcessLookupError:fd=None
  if fd is not None:
   try:select.select([fd],[],[])
   finally:os.close(fd)
 spec=importlib.util.spec_from_file_location('r',A/'ramsey-run-v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 m.reduce();m.publish()
 if m.state()['phase']not in ['complete','failure']:m.queue()
 m.atomic(A/'continuation-terminal.json',dict(state=m.state(),reduced=m.reduce()))
if __name__=='__main__':main()
