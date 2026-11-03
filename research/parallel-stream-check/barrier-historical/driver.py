"""Exact historical stock/export/import workflow,3repeats; per-cell blocking lease."""
import fcntl,os,json,time,contextlib
from pathlib import Path
import parallel_matrix as m
from declaration_native import ROOT
CAP=Path('/workspaces/.agent-state/gpu-smt-captures')
def main():
 target=json.loads((ROOT/'input.json').read_text())['olean'];ref=None;rows=[]
 # Corrupt the same real module before any whole-pipeline timing sample.
 for k in[0,8]:
  key='bad-k'+str(k)
  with(CAP/'pcore.lock').open('a+')as lease:
   print('WAIT',key,flush=True);fcntl.flock(lease,fcntl.LOCK_EX);os.sched_setaffinity(0,set(range(8)))
   with(ROOT/'native.log').open('a')as log,contextlib.redirect_stdout(log):
    c=m.cell(key,target,k,'bvar',True,300)
   os.sched_setaffinity(0,set(range(8,16)))
  assert not c['accepted']and c['all_native_retired'];print('BAD_REJECTED',key,flush=True)
 for rep in[1,2,3]:
  for k in[0,1,2,4,8]:
   key='r'+str(rep)+'-k'+str(k)
   with(CAP/'pcore.lock').open('a+')as lease:
    print('WAIT',key,flush=True);fcntl.flock(lease,fcntl.LOCK_EX);os.sched_setaffinity(0,set(range(8)))
    with(ROOT/'native.log').open('a')as log,contextlib.redirect_stdout(log):
     c=m.cell(key,target,k,'none',True,300)
    os.sched_setaffinity(0,set(range(8,16)))
   assert c['accepted']and c['all_native_retired']
   names=c['acceptance']['names']
   if ref is None:ref=names
   assert names==ref and len(names)==3425
   rows.append(c);(ROOT/'completed.json').write_text(json.dumps(rows,indent=2))
   print(json.dumps(dict(key=key,wall=c['whole_pipeline_wall_s'],cpu=c['native_user_s']+c['native_system_s'],typed=3425)),flush=True)
 (ROOT/'terminal.json').write_text(json.dumps(dict(complete=True,completed=len(rows))))
if __name__=='__main__':main()
