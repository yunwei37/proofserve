import os,json,sys,time
from pathlib import Path
from native import ROOT,SDK,run,environment
ASSETS=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-assets')
MODULE='OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41'
def runtime(workers,cpus):
 e=environment()
 prep=json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/repair-v3/preparation.json').read_text())
 e.update(LEAN_PATH=str(ROOT/'fixtures')+':'+str(ASSETS/'overlay-complete-v2')+':'+prep['lean_path'],
  LEAN_NUM_THREADS=str(workers),PARALLEL_WORKERS=str(workers),PARALLEL_ALLOWED_CPUS=json.dumps(cpus))
 for k in ['PARALLEL_CURVE_MODULES','PARALLEL_CHUNK_ASSETS','PARALLEL_CHUNK_ASSETS_CURVE','PARALLEL_DETERMINISM_CURVE','PARALLEL_CHECKED_OUTPUT','DECOUPLED_MEMORY_PROFILE']:
  e.pop(k,None)
 return e
def events(key):
 return [json.loads(s) for s in (ROOT/'runs'/key/'stdout').read_text().splitlines() if s.startswith('{')]
def compare_artifacts(folder):
 rows=[]
 for suffix in ['.olean','.olean.server','.olean.private']:
  files=sorted(folder.glob('*'+suffix))
  if not files:continue
  b=files[0].read_bytes()
  rows.append(dict(suffix=suffix,files=len(files),bytes=len(b),all_equal=all(f.read_bytes()==b for f in files)))
 if not rows or not all(x['files']==12 and x['all_equal'] for x in rows):raise RuntimeError('artifact byte difference')
 return rows
def main(phase):
 cells=[];begin=time.monotonic();state='failed';error=None
 try:
  if phase=='qualification':
   os.sched_setaffinity(0,set(range(8)))
   e=runtime(16,list(range(8)));e.update(PARALLEL_CURVE_MODULES='ComputeControl',PARALLEL_DETERMINISM_CURVE='1')
   output=ROOT/'control-output';output.mkdir()
   e['PARALLEL_CHECKED_OUTPUT']=str(output)
   r=run('control-extended',[ROOT/'parallel-stream','parallel','none','ComputeControl'],120,False,e);cells.append(r)
   ev=events(r['key'])
   if r['returncode'] or len([x for x in ev if x.get('event')=='unit_check'])!=1200:
    raise RuntimeError('extended native qualification failed')
   artifacts=compare_artifacts(output)
   for workers in [1,16,24]:
    e=runtime(workers,list(range(8)));e['DECOUPLED_MUTATE_MODULE']='ComputeControl';e['DECOUPLED_MUTATE_CONSTANT']='c0'
    r=run('control-corrupt-j'+str(workers),[ROOT/'parallel-stream','parallel','bvar','ComputeControl'],90,False,e);cells.append(r)
    if r['returncode']!=1 or not any(x.get('event')=='reject' for x in events(r['key'])):
     raise RuntimeError('bad proof not rejected')
   (ROOT/'extended-qualified.json').write_text(json.dumps(dict(native_controls=cells,artifacts=artifacts),indent=2))
  elif phase=='scaling':
   assert (ROOT/'extended-qualified.json').exists()
   ref=json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14/barrier-full-reference1-r1-summary.json').read_text())
   reference=set(ref['accepted'])
   for workers in [8,12,16,24]:
    cpus=list(range(workers));os.sched_setaffinity(0,set(cpus));e=runtime(workers,cpus)
    remaining=1690-(time.monotonic()-begin)
    if remaining<100:raise RuntimeError('finite window insufficient; retain completed cells')
    r=run('barrier-full-j'+str(workers),[ROOT/'parallel-stream','parallel','none',MODULE],min(500,int(remaining)),True,e);cells.append(r)
    ev=events(r['key']);accepted=[x['module'] for x in ev if x.get('event')=='accept']
    r['accepted_IDs']=accepted;r['accepted_set_equal_to_serial']=set(accepted)==reference
    r['complete_events']=[x for x in ev if x.get('event')=='complete']
    (ROOT/'scaling-results.json').write_text(json.dumps(cells,indent=2))
    if r['returncode'] or not r['complete_events'] or len(accepted)!=4449 or not r['accepted_set_equal_to_serial']:
     raise RuntimeError('scaling cell incomplete or verdict difference')
  elif phase=='determinism':
   assert (ROOT/'extended-qualified.json').exists()
   cpus=list(range(16));os.sched_setaffinity(0,set(cpus));e=runtime(16,cpus)
   e.update(PARALLEL_WORKERS='8',PARALLEL_CURVE_MODULES=MODULE,PARALLEL_DETERMINISM_CURVE='1')
   output=ROOT/'barrier-checked-output';output.mkdir();e['PARALLEL_CHECKED_OUTPUT']=str(output)
   r=run('barrier-determinism',[ROOT/'parallel-stream','parallel','none',MODULE],1680,True,e);cells.append(r)
   ev=events(r['key'])
   if r['returncode'] or len([x for x in ev if x.get('event')=='unit_check'])!=1200 or not any(x.get('event')=='complete' for x in ev):
    raise RuntimeError('determinism cell incomplete; retain raw')
   (ROOT/'determinism-artifacts.json').write_text(json.dumps(compare_artifacts(output),indent=2))
  else:raise ValueError(phase)
  state='complete'
 except BaseException as ex:
  error=repr(ex);raise
 finally:
  (ROOT/(phase+'-terminal.json')).write_text(json.dumps(dict(state=state,error=error,cells=cells,
   wall_s=time.monotonic()-begin,utc=time.strftime('%FT%TZ',time.gmtime())),indent=2))
if __name__=='__main__':main(sys.argv[1])
