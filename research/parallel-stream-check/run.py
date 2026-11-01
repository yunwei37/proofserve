"""Native controls, then one finite Mathlib closure matrix."""
import os,json,time,sys,subprocess
from pathlib import Path
from native import run,SDK,ROOT,environment
R=Path('/workspaces/repository/research/parallel-stream-check')
ORAW=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
def env():
 e=environment()
 p=json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/repair-v3/preparation.json').read_text())
 e['LEAN_PATH']=str(ROOT/'fixtures')+':'+str(ORAW/'constructed/lib')+':'+p['lean_path']
 return e
def events(key):
 return [json.loads(x) for x in (ROOT/'runs'/key/'stdout').read_text().splitlines() if x.startswith('{')]
def controls():
 os.sched_setaffinity(0,set(range(8,16)))
 d=ROOT/'fixtures';d.mkdir(exist_ok=True);e=env()
 cases={
 'DupA':'namespace Shared\ntheorem t : True := True.intro\nend Shared\n',
 'DupB':'namespace Shared\ntheorem t : True := True.intro\nend Shared\n',
 'ExtraA':'namespace Shared\ntheorem externalProof : True := True.intro\nend Shared\n',
 'ExtraB':'namespace LocalB\ntheorem result : True := True.intro\nend LocalB\n',
 'DefA':'namespace Shared\ndef f : Nat := 0\nend Shared\n',
 'DefB':'namespace Shared\ndef f : Nat := 1\nend Shared\n',
 'PrivateA':'private theorem helper : True := True.intro\ntheorem privateA : True := helper\n',
 'PrivateB':'private theorem helper : True := True.intro\ntheorem privateB : True := helper\n',
 'Waves':'def a : Nat := 7\ndef b : Nat := 8\ntheorem aa : Eq a a := Eq.refl a\ntheorem bb : Eq b b := Eq.refl b\ntheorem cc : Eq a a := aa\n'}
 for mod,text in cases.items():
  p=d/(mod+'.lean');p.write_text('prelude\nimport Init.Prelude\n'+text)
  r=run('fixture-'+mod,[SDK/'bin/lean','--root='+str(d),'-o',d/(mod+'.olean'),p],60,False,e)
  if r['returncode']:raise RuntimeError('compile fixture')
 controls=[
 ('ordinary','none',None,['DupA','DupB'],True,None),
 ('corrupt','bvar','DupB',['DupA','DupB'],False,None),
 ('sibling','sibling','ExtraB',['ExtraA','ExtraB'],False,None),
 ('definitions','none',None,['DefA','DefB'],True,None),
 ('private','none',None,['PrivateA','PrivateB'],True,None),
 ('waves','none',None,['Waves'],True,None),
 ('duplicate-token','none',None,['Waves'],False,'duplicate'),
 ('stale-token','none',None,['Waves'],False,'stale')]
 rows=[]
 for name,mutation,target,roots,expected,fault in controls:
  for workers in [1,8]:
   ee=e.copy();ee['PARALLEL_WORKERS']=str(workers)
   if target:ee['DECOUPLED_MUTATE_MODULE']=target
   if fault:ee['PARALLEL_FAULT']=fault
   key=name+'-'+str(workers)
   rr=run(key,[ROOT/'parallel-stream','parallel',mutation]+roots,180,False,ee)
   ev=events(key);reject=any(x.get('event')=='reject' for x in ev)
   ok=rr['returncode']==0 if expected else rr['returncode']==1 and reject
   rows.append(dict(key=key,expected_accept=expected,returncode=rr['returncode'],explicit_reject=reject,qualified=ok))
   (ROOT/'controls.json').write_text(json.dumps(rows,indent=2))
   if not ok:raise RuntimeError('control failed '+key)
 (ROOT/'controls-qualified.json').write_text(json.dumps(dict(cases=len(rows),utc=time.strftime('%FT%TZ',time.gmtime()))))
def matrix():
 assert (ROOT/'controls-qualified.json').exists()
 os.sched_setaffinity(0,set(range(8)))
 e=env();records=[];deadline=time.monotonic()+1670
 modes=[('reference',ORAW/'stream-check','stream',1),('audited',ROOT/'parallel-stream','audit',1)]+[('parallel'+str(w),ROOT/'parallel-stream','parallel',w)for w in [1,2,4,8]]
 for repeat in range(3):
  for name,binary,mode,w in modes:
   if time.monotonic()>deadline-180:raise RuntimeError('finite-window-incomplete; retain cells')
   ee=e.copy();ee['PARALLEL_WORKERS']=str(w)
   key='math-'+name+'-'+str(repeat)
   rr=run(key,[binary,mode,'none','Mathlib.Data.Nat.Basic'],180,True,ee)
   ev=events(key);accepted=[x['module'] for x in ev if x.get('event')=='accept']
   rr['accepted']=accepted;rr['complete']=[x for x in ev if x.get('event')=='complete']
   records.append(rr);(ROOT/'matrix-results.json').write_text(json.dumps(records,indent=2))
   if rr['returncode'] or len(accepted)!=1330:raise RuntimeError('matrix incomplete '+key)
   if set(accepted)!=set(records[0]['accepted']):raise RuntimeError('accepted-set difference '+key)
 (ROOT/'matrix-complete.json').write_text(json.dumps(dict(cells=len(records),utc=time.strftime('%FT%TZ',time.gmtime()))))
if __name__=='__main__':
 try:
  if sys.argv[1]=='controls':controls()
  elif sys.argv[1]=='matrix':matrix()
 finally:
  (ROOT/(sys.argv[1]+'-terminal.json')).write_text(json.dumps(dict(utc=time.strftime('%FT%TZ',time.gmtime()))))
