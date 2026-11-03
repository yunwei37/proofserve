"""Common-optimization sensitivity: same executable,3 balanced repeats/arm."""
import os,json,time,fcntl,contextlib
from pathlib import Path
import parallel_matrix as m
from declaration_native import ROOT
CAP=Path('/workspaces/.agent-state/gpu-smt-captures')
def one(key,k,mark,bad=False):
 os.environ['PS_MARK_SERIAL']=str(mark)
 (ROOT/(key+'-environment.json')).write_text(json.dumps(dict(PS_MARK_SERIAL=mark,LEAN_NUM_THREADS=max(1,k))))
 with(CAP/'pcore.lock').open('a+')as lease:
  print('WAIT',key,flush=True);fcntl.flock(lease,fcntl.LOCK_EX);os.sched_setaffinity(0,set(range(8)))
  with(ROOT/'native.log').open('a')as log,contextlib.redirect_stdout(log):
   c=m.cell(key,json.loads((ROOT/'input.json').read_text())['olean'],k,'bvar'if bad else'none',True,300)
  os.sched_setaffinity(0,set(range(8,16)))
 c['serial_mark']=mark;c['arm']='wave8'if k else'serial'+str(mark)
 assert c['all_native_retired']
 if bad:
  assert not c['accepted']
  assert any('loose bound variables'in(ROOT/'runs'/stage/'stderr').read_text()for stage in c['stage_keys'])
 else:assert c['accepted']and c['acceptance']['count']==3425
 print(json.dumps(dict(key=key,arm=c['arm'],accepted=c['accepted'],wall=c['whole_pipeline_wall_s'],cpu=c['native_user_s']+c['native_system_s'])),flush=True)
 return c
def main():
 one('bad-serial-persistent',0,1,True)
 arms=[(0,0),(0,1),(8,0)];rows=[];names=None
 for rep in[1,2,3]:
  order=arms[rep-1:]+arms[:rep-1]
  for k,mark in order:
   c=one('r'+str(rep)+'-'+('wave8'if k else'serial'+str(mark)),k,mark)
   c['repeat']=rep
   if names is None:names=c['acceptance']['names']
   assert c['acceptance']['names']==names
   rows.append(c);(ROOT/'completed.json').write_text(json.dumps(rows,indent=2))
 (ROOT/'terminal.json').write_text(json.dumps(dict(complete=True,cells=9)))
if __name__=='__main__':main()
