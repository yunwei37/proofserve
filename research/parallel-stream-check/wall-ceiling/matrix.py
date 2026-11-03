"""Finite per-cell blocking lease; no timing run overlaps another lane.
Raw captures are PVC-only; each native has a1100s and14GiB external budget.
"""
import os,json,time,fcntl,contextlib
from pathlib import Path
from native import ROOT,run,environment
CAP=Path('/workspaces/.agent-state/gpu-smt-captures')
OLD=CAP/'parallel-stream-persistence-20261103'
ASSETS=CAP/'parallel-stream-assets'
REFERENCE=CAP/'decoupled-check-20261031/stream-check'
PREP=json.loads((CAP/'profile-2026-10-31/startup-replay/repair-v3/preparation.json').read_text())
GRID=next(x['module'] for x in json.loads((ASSETS/'assets.json').read_text())['selected']if x['module'].endswith('.Grid'))
BARRIER='OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41'
def runtime(dataset,n,profile=False,trace=None):
 e=environment()
 for k in list(e):
  if k.startswith('PARALLEL_')or k.startswith('DECOUPLED_'):e.pop(k,None)
 overlay=str(CAP/'parallel-stream-check-v14/fixtures')+':'+str(CAP/'decoupled-check-20261031/constructed/lib') if dataset=='math' else str(CAP/'parallel-stream-check-v16/fixtures')+':'+str(ASSETS/'overlay-complete-v2')
 e.update(LEAN_PATH=overlay+':'+PREP['lean_path'],LEAN_NUM_THREADS=str(n),
   PARALLEL_WORKERS=str(n),PARALLEL_PROFILE='1'if profile else'0')
 if trace:e['PARALLEL_WALL_TRACE']=str(trace)
 return e
def events(key):
 return [json.loads(s)for s in(ROOT/'runs'/key/'stdout').read_text().splitlines()if s.startswith('{')]
def launch(key,argv,e,expected,mutation=False):
 print(json.dumps(dict(event='waiting',key=key,pid=os.getpid(),utc=time.strftime('%FT%TZ',time.gmtime()))),flush=True)
 with (CAP/'pcore.lock').open('a+')as lease:
  fcntl.flock(lease,fcntl.LOCK_EX)
  os.sched_setaffinity(0,set(range(8)))
  print(json.dumps(dict(event='acquired',key=key,pid=os.getpid())),flush=True)
  with(ROOT/'native.log').open('a')as log,contextlib.redirect_stdout(log):
   c=run(key,argv,1100,True,e)
  ev=events(key)
  c['accepted_IDs']=[x['module']for x in ev if x.get('event')=='accept']
  c['complete_events']=[x for x in ev if x.get('event')=='complete']
  c['reject_events']=[x for x in ev if x.get('event')=='reject']
  valid=c['native_retired']and c['cgroup_retired']and not c['stop_reasons']
  if mutation:valid=valid and c['returncode']==1 and bool(c['reject_events'])
  else:valid=valid and c['returncode']==0 and len(c['accepted_IDs'])==expected and bool(c['complete_events'])
  c['qualified']=bool(valid);(ROOT/(key+'-terminal.json')).write_text(json.dumps(c,indent=2))
  os.sched_setaffinity(0,set(range(8,16)))
 print(json.dumps(dict(event='returned',key=key,qualified=c['qualified'],wall_s=c['wall_s'],cpu_s=c['user_s']+c['system_s'],accepted=len(c['accepted_IDs']))),flush=True)
 if not valid:raise RuntimeError('native finite task failed; preserve raw '+key)
 return c
def main():
 # Same default/no override in positive and corrupted-proof controls.
 for n in[1,8]:
  e=runtime('math',n,True,ROOT/('control-v2-'+str(n)+'.jsonl'))
  launch('control-v2-P'+str(n),[ROOT/'parallel-stream','parallel','none','Waves'],e,2)
  e=runtime('math',n,True);e['DECOUPLED_MUTATE_MODULE']='Waves'
  launch('bad-v2-P'+str(n),[ROOT/'parallel-stream','parallel','bvar','Waves'],e,0,True)
 (ROOT/'qualified.json').write_text(json.dumps(dict(default_persistence=True,positive_and_bad_controls=True)))
 # One diagnostic and its same-executable, same-profile no-trace observer control.
 for label,trace in [('diagnostic',ROOT/'barrier-wave-trace.jsonl'),('observer-control',None)]:
  launch(label,[ROOT/'parallel-stream','parallel','none',BARRIER],runtime('barrier',8,True,trace),4449)
 # Historical scopes each get independent fresh processes, all three repeats.
 for dataset,target,count,ns in [('math','Mathlib.Data.Nat.Basic',1330,[1,8]),('grid',GRID,3793,[1,4,8])]:
  for rep in[1,2,3]:
   # Rotate reference to end on second repeat; preserve order as a caveat.
   arms=[('reference',REFERENCE,'stream',1)]+[('parallel'+str(n),ROOT/'parallel-stream','parallel',n)for n in ns]
   if rep==2:arms=arms[1:]+arms[:1]
   for arm,binary,mode,n in arms:
    c=launch(dataset+'-'+arm+'-r'+str(rep),[binary,mode,'none',target],runtime(dataset,n),count)
    reference=ROOT/(dataset+'-reference-r1-terminal.json')
    if reference.exists():
     ids=json.loads(reference.read_text())['accepted_IDs']
     if c['accepted_IDs']!=ids:raise RuntimeError('ordered acceptance differs')
 (ROOT/'matrix-terminal.json').write_text(json.dumps(dict(complete=True,utc=time.strftime('%FT%TZ',time.gmtime()))))
if __name__=='__main__':main()
