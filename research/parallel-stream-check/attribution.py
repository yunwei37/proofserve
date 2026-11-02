import os,json,time,sys,collections
from pathlib import Path
from native import ROOT,SDK,run,environment
ASSETS=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-assets')
MODULE='OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41'
def runtime(workers,allowed,pins,coor=0,profile=True):
 e=environment()
 prep=json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/repair-v3/preparation.json').read_text())
 e.update(LEAN_PATH='/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v16/fixtures:'+str(ASSETS/'overlay-complete-v2')+':'+prep['lean_path'],
  LEAN_NUM_THREADS=str(workers),PARALLEL_WORKERS=str(workers),PARALLEL_ALLOWED_CPUS=json.dumps(allowed),
  PARALLEL_PIN_CPUS=','.join(map(str,pins)),PARALLEL_COORDINATOR_CPU=str(coor),PARALLEL_PROFILE='1' if profile else '0')
 for key in ['PARALLEL_CURVE_MODULES','PARALLEL_CHUNK_ASSETS','PARALLEL_CHUNK_ASSETS_CURVE','PARALLEL_DETERMINISM_CURVE','PARALLEL_CHECKED_OUTPUT','PARALLEL_HARDWARE_CURVE','PARALLEL_SAMPLE_COUNT']:
  e.pop(key,None)
 return e
def events(key):
 return [json.loads(s) for s in (ROOT/'runs'/key/'stdout').read_text().splitlines() if s.startswith('{')]
def file_results(folder,expected=9):
 out=[]
 for suffix in ['.olean','.olean.server','.olean.private']:
  files=sorted(folder.glob('*'+suffix))
  if files:
   b=files[0].read_bytes();out.append(dict(suffix=suffix,files=len(files),bytes=len(b),all_equal=all(f.read_bytes()==b for f in files)))
 if not out or any(x['files']!=expected for x in out):raise RuntimeError('missing artifact')
 return out
def main(phase):
 begin=time.monotonic();cells=[];state='partial';error=None
 try:
  if phase=='qualify':
   allowed=list(range(24));os.sched_setaffinity(0,set(allowed));e=runtime(24,allowed,list(range(8)),0,True)
   output=ROOT/'qualifier-output';output.mkdir()
   e.update(PARALLEL_WORKERS='8',PARALLEL_CURVE_MODULES='ComputeControl',PARALLEL_DETERMINISM_CURVE='1',
    PARALLEL_SAMPLE_COUNT='50',PARALLEL_HARDWARE_CURVE='1',PARALLEL_CHECKED_OUTPUT=str(output))
   r=run('attribution-control',[ROOT/'parallel-stream','parallel','none','ComputeControl'],240,True,e);cells.append(r)
   ev=events(r['key']);current=None;seen=collections.defaultdict(list)
   for x in ev:
    if x.get('event')=='curve_begin':current=(x['kind'],x['repeat'])
    if x.get('event')=='unit_check':assert current is not None;seen[current].append(x)
   if r['returncode'] or sum(map(len,seen.values()))!=450 or len(seen)!=9:raise RuntimeError('native attribution control incomplete')
   for (kind,rep),rows in seen.items():
    assert len(rows)==50
    allowed_workers={0} if kind=='p1' else {8} if kind=='e1' else set(range(24))
    if not all(x['cpu'] in allowed_workers for x in rows):raise RuntimeError('worker placement differs from requested map')
   if not all(x['all_equal'] for x in file_results(output)):raise RuntimeError('control snapshot mismatch')
   for x in ev:
    if x.get('event')=='profile_module':
     m=x['metrics'];assert m['kernel_union_ns']<=m['batch_wall_ns']
     assert all(w['within_check_migrations']==0 for w in m['workers'])
   os.sched_setaffinity(0,set(range(8)))
   two=runtime(2,list(range(8)),[0,1],0,True)
   r2=run('attribution-two-core-control',[ROOT/'parallel-stream','parallel','none','ComputeControl'],180,True,two);cells.append(r2)
   ev2=events(r2['key'])
   core_checks=collections.Counter()
   for item in ev2:
    if item.get('event')=='profile_module':
     for worker in item['metrics']['workers']:core_checks[worker['cpu']]+=worker['checks']
   if r2['returncode'] or set(core_checks)!={0,1} or not all(core_checks.values()):raise RuntimeError('two actual CPU control incomplete')
   os.sched_setaffinity(0,set(range(24)))
   ee=runtime(24,list(range(24)),list(range(24)),0,True)
   ee['DECOUPLED_MUTATE_MODULE']='ComputeControl';ee['DECOUPLED_MUTATE_CONSTANT']='c0'
   bad=run('attribution-bad-control',[ROOT/'parallel-stream','parallel','bvar','ComputeControl'],180,True,ee);cells.append(bad)
   if bad['returncode']!=1 or not any(x.get('event')=='reject' for x in events(bad['key'])):raise RuntimeError('bad original proof not rejected')
   (ROOT/'qualified.json').write_text(json.dumps(dict(cells=cells,samples=450,pin_maps_verified=True,artifacts=file_results(output)),indent=2))
  elif phase in ['p12','p48','types','observer','placement']:
   assert (ROOT/'qualified.json').exists()
   specs={'p12':[('P1',1,list(range(8)),[0],0,True),('P2',2,list(range(8)),[0,1],0,True)],
    'p48':[('P4',4,list(range(8)),list(range(4)),0,True),('P8',8,list(range(8)),list(range(8)),0,True)],
    'types':[('E16',16,list(range(8,24)),list(range(8,24)),8,True),('M24',24,list(range(24)),list(range(24)),0,True)],
    'observer':[('P8-noProfile',8,list(range(8)),list(range(8)),0,False),('M24-noProfile',24,list(range(24)),list(range(24)),0,False)],
    'placement':[('P8-unpinned',8,list(range(8)),[],0,False),('M24-unpinned',24,list(range(24)),[],0,False)]}[phase]
   reference=set(json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14/barrier-full-reference1-r1-summary.json').read_text())['accepted'])
   for name,workers,allowed,pins,coor,profile in specs:
    os.sched_setaffinity(0,set(allowed));e=runtime(workers,allowed,pins,coor,profile)
    remaining=1690-(time.monotonic()-begin)
    if remaining<120:raise RuntimeError('finite window ended; retain completed cells')
    r=run('full-'+name,[ROOT/'parallel-stream','parallel','none',MODULE],min(750,int(remaining)),True,e);cells.append(r)
    ev=events(r['key']);ids=[x['module'] for x in ev if x.get('event')=='accept']
    r.update(accepted_IDs=ids,accepted_set_equal_to_serial=set(ids)==reference,profile_enabled=profile,
     worker_pins=pins,coordinator_cpu=coor,complete_events=[x for x in ev if x.get('event')=='complete'])
    (ROOT/(phase+'-results.json')).write_text(json.dumps(cells,indent=2))
    if r['returncode'] or len(ids)!=4449 or not r['complete_events'] or not r['accepted_set_equal_to_serial']:raise RuntimeError('incomplete or differing full-closure verdict')
  elif phase=='det24':
   assert (ROOT/'qualified.json').exists()
   allowed=list(range(24));os.sched_setaffinity(0,set(allowed));e=runtime(24,allowed,list(range(8)),0,True)
   output=ROOT/'hardware-leaf-output';output.mkdir()
   e.update(PARALLEL_WORKERS='8',PARALLEL_CURVE_MODULES=MODULE,PARALLEL_DETERMINISM_CURVE='1',
    PARALLEL_SAMPLE_COUNT='50',PARALLEL_HARDWARE_CURVE='1',PARALLEL_CHECKED_OUTPUT=str(output))
   r=run('hardware-leaf',[ROOT/'parallel-stream','parallel','none',MODULE],1680,True,e);cells.append(r)
   ev=events(r['key'])
   if r['returncode'] or len([x for x in ev if x.get('event')=='unit_check'])!=450 or not any(x.get('event')=='complete' for x in ev):raise RuntimeError('hardware leaf incomplete')
   (ROOT/'hardware-artifacts.json').write_text(json.dumps(file_results(output),indent=2))
  else:raise ValueError(phase)
  state='complete'
 except BaseException as ex:error=repr(ex);raise
 finally:
  (ROOT/(phase+'-terminal.json')).write_text(json.dumps(dict(state=state,error=error,cells=cells,
   wall_s=time.monotonic()-begin,utc=time.strftime('%FT%TZ',time.gmtime())),indent=2))
if __name__=='__main__':main(sys.argv[1])
