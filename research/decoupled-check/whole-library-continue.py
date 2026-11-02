#!/usr/bin/env python3
"""Exit-driven finite experiment continuation, not a schedule or service."""
import importlib.util,json,os,select
from pathlib import Path
os.sched_setaffinity(0,{8})
O=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/whole-library-20261102')
def main():
 first=json.loads((O/'first-window-retry-submission.json').read_text())
 p=Path('/proc/'+str(first['pid']))
 if p.exists()and p.joinpath('stat').read_text().split(') ')[1].split()[19]==str(first['birth']):
  try:fd=os.pidfd_open(first['pid'])
  except ProcessLookupError:fd=None
  if fd is not None:
   try:select.select([fd],[],[])
   finally:os.close(fd)
 spec=importlib.util.spec_from_file_location('whole',O/'whole-library-run.py')
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 m.reduce();m.publish()
 if not m.state('all')['terminal']:m.queue('all',1000)
 s=m.state('all')
 # Checkpointing does not shrink a growing environment. A stopped native
 # episode gets explicitly separate fresh directory contexts; work is charged.
 if s.get('status')=='native_incomplete_partition_or_repair_required':
  for cohort in m.GROUPS+['remainder']:
   if not m.state(cohort)['terminal']:m.queue(cohort,1000)
 m.reduce();m.publish()
 m.atomic(O/'continuation-terminal.json',dict(all_state=m.state('all'),
   directory_states={c:m.state(c)for c in m.GROUPS+['remainder']if(O/(c+'-state.json')).exists()},
   complete=json.loads((O/'reduced.json').read_text())['complete']))
if __name__=='__main__':main()
