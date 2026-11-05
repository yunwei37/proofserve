"""Fixed release evaluation. One blocking P-core lease per complete native cell.
CLI: python3 matrix.py CONFIG.json; raw files stay in the configured PVC directory.
No commits or publication from this program.
"""
import os,sys,json,time,fcntl,threading,signal,csv
from pathlib import Path
import guard

ROOTS={'math':'Mathlib.Data.Nat.Basic','grid':'OAI.Analysis.PlanarPacking.Grid','barrier':'OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41'}
def cells(cfg):
 """The immutable planned cells are also consumed by the reducer and estimator."""
 roots=cfg.get('roots',ROOTS);repeats=cfg.get('repeats',[1,2,3])
 for dataset in roots:
  for rep in repeats:
   ns=cfg.get('worker_points',{}).get(dataset,[1,2,4,8])
   for n in (list(reversed(ns))if rep==2 else ns):
    yield dict(key=f'{dataset}-P{n}-r{rep}',dataset=dataset,workers=n,repeat=rep,arm='native',flags=[])
  if dataset in ['math','grid']:
   for flag in ['--no-persistence','--no-split-fallback','--strict-theorem-bodies']:
    for rep in repeats:
     n=cfg.get('ablation_workers',8)
     yield dict(key=f'{dataset}-P{n}-{flag[2:]}-r{rep}',dataset=dataset,workers=n,repeat=rep,arm='native',flags=[flag])
 for dataset in roots:
  for mode in ['default','fresh']:
   for rep in repeats:
    yield dict(key=f'{dataset}-official-{mode}-r{rep}',dataset=dataset,workers=cfg.get('official_workers',8),repeat=rep,arm='official',flags=['--fresh']if mode=='fresh'else[])
 for mutation in ['bvar','unknown','sort']:
  yield dict(key='bad-real-prefix-'+mutation,dataset='math',workers=cfg.get('resume_workers',4),repeat=1,arm='bad-control',mutation=mutation)
 for suffix in ['interrupt','resume']:
  yield dict(key='math-'+suffix,dataset='math',workers=cfg.get('resume_workers',4),repeat=1,arm='native',flags=[],interrupt=suffix=='interrupt')
def dump(p,value):
 q=p.with_suffix(p.suffix+'.pending')
 with q.open('w')as f:json.dump(value,f,indent=2);f.flush();os.fsync(f.fileno())
 q.replace(p)
def main():
 cfg=json.loads(Path(sys.argv[1]).read_text());root=Path(cfg['raw']).resolve()
 root.mkdir(parents=True,exist_ok=True);guard.ROOT=root
 binary=Path(cfg['binary']);project=Path(cfg['project']);lease=Path(cfg['lease'])
 qualification=cfg.get('mode')=='qualification'
 initial_affinity=set(os.sched_getaffinity(0))
 start=time.monotonic()
 rows=json.loads((root/'completed.json').read_text())if(root/'completed.json').exists()else[]
 failures=json.loads((root/'failed-cells.json').read_text())if(root/'failed-cells.json').exists()else[]
 budget=cfg.get('matrix_limit_s',21600)-sum(r.get('wall_s',0)for r in rows+failures)
 dump(root/'planned-cells.json',list(cells(cfg)))
 refs={};cleanup=json.loads((root/'cleanup.json').read_text())if(root/'cleanup.json').exists()else[]
 def one(key,argv,dataset,workers,repeat,arm='native',state=None,interrupt=False,limit=1100):
  previous=next((r for r in rows if r['key']==key),None)
  if previous and previous['returncode']!=0 and arm!='bad-control' and not previous.get('manual_interruption') and cfg.get('retry_failed',False):
   archive=json.loads((root/'failed-cells.json').read_text())if(root/'failed-cells.json').exists()else[]
   archive.append(previous);dump(root/'failed-cells.json',archive)
   rows.remove(previous);previous=None
  if previous:
   result=json.loads((root/'runs'/previous.get('run_key',key)/'result.json').read_text())
   assert result['native_retired']and result['cgroup_retired']
   receipt=None
   if arm in ['native','full-math']and result['returncode']==0:
    receipt=json.loads((root/(key+'-receipt.json')).read_text())
    assert receipt['status']=='complete'
    if dataset in refs:assert refs[dataset]==receipt['accepted']
    else:refs[dataset]=receipt['accepted']
   elif arm=='native'and not previous['manual_interruption']:
    raise RuntimeError('old failed native cell requires explicit review')
   print('RETAIN_COMPLETED',key,flush=True)
   return result,receipt
  attempt=1
  run_key=key
  while(root/'runs'/run_key).exists():
   attempt+=1;run_key=key+'-attempt-'+str(attempt)
  if run_key!=key and state and key!='math-resume':
   new_state=root/run_key
   argv=[new_state if str(x)==str(state)else x for x in argv];state=new_state
  fs=os.statvfs(root);used=1-fs.f_bavail/fs.f_blocks
  if used>=.85:raise RuntimeError('disk85% boundary; preserve and stop')
  e=guard.environment();e['PATH']=str(guard.SDK/'bin')+':'+e['PATH']
  e['LEAN_PATH']=cfg.get('lean_path',cfg.get('overlay','')if dataset in ['grid','barrier']else'')
  e['LEAN_SYSROOT']=str(guard.SDK)

  if arm=='official'and dataset in ['grid','barrier'] and not qualification:
   rel=Path(str(argv[-1]).replace('.','/')+'.olean')
   real=(Path(cfg['overlay'])/rel).resolve(strict=True)
   canonical=real
   for _ in rel.parts:canonical=canonical.parent
   assert canonical/rel==real,'canonical module layout requires explicit qualification'
   # The original overlay stays first for lookup; this extra root lets the stock
   # CLI name the real file after moduleNameOfFileName resolves its symlink.
   e['LEAN_PATH']+=os.pathsep+str(canonical)
  e['LEAN_NUM_THREADS']=str(workers or 4)
  e['PROOFSERVE_BENCH_CLASSIFICATION']=cfg.get('evaluation_status','unclassified')
  os.chdir(project)
  print('WAIT',key,flush=True)
  import contextlib
  with (contextlib.nullcontext()if qualification else lease.open('a+'))as lock:
   if lock is not None:fcntl.flock(lock,fcntl.LOCK_EX);os.sched_setaffinity(0,set(range(8)))
   remaining=budget-(time.monotonic()-start)
   if remaining<=0:raise RuntimeError('matrix six-hour budget exhausted; no new cell launched')
   limit=min(limit,remaining)
   print('ACQUIRED',key,flush=True)
   stopped=threading.Event();proof=[]
   def interrupter():
    while not stopped.wait(.0005):
     if state and (state/'segment-0.json').exists()and guard.ACTIVE:
      cg,pid=guard.ACTIVE
      proof.append(dict(pid=pid,checkpoint=str(state/'segment-0.json'),reason='actual process interruption after first certified segment'))
      (cg/'cgroup.kill').write_text('1')
      dump(root/(key+'-interruption.json'),proof)
      break
   t=threading.Thread(target=interrupter,daemon=True)if interrupt else None
   if t:t.start()
   try:r=guard.run(run_key,argv,limit,not qualification,e,memory_gib=cfg.get('qualification_memory_gib',12)if qualification else None)
   finally:
    stopped.set()
    if t:t.join()
   os.sched_setaffinity(0,initial_affinity)
  receipt=None
  if arm in ['native','full-math']and r['returncode']==0:
   receipt=json.loads((root/'runs'/run_key/'stdout').read_text())
   assert receipt['status']=='complete'and receipt['execution_path']=='proofserve-parallel'
   assert len(receipt['accepted'])==len(set(receipt['accepted']))
   if dataset in refs:assert receipt['accepted']==refs[dataset]
   else:refs[dataset]=receipt['accepted']
   dump(root/(key+'-receipt.json'),receipt)
  row=dict(key=key,run_key=run_key,attempt=attempt,state_directory=str(state)if state else None,commit=cfg['commit'],dataset=dataset,workers=workers,repeat=repeat,arm=arm,
   returncode=r['returncode'],wall_s=r.get('wall_s'),cpu_s=r.get('user_s',0)+r.get('system_s',0),
   peak_rss_kib=r.get('peak_rss_kib'),rss_sample_bytes=r['sampled_tree_peak_bytes'],modules=len(receipt['accepted'])if receipt else None,
   segments=len(receipt['segments'])if receipt else None,manual_interruption=bool(proof))
  rows.append(row);dump(root/'completed.json',rows)
  if receipt:
   expected_policy='strict'if '-strict-theorem-bodies-'in key else'shared-checked'
   assert receipt['theorem_body_policy']==expected_policy
  if interrupt:assert proof and r['returncode']!=0
  elif r['returncode']!=0 and arm not in ['full-math','official','bad-control']:
   raise RuntimeError('native cell incomplete or failed; stop without imputing a result: '+key)
  if arm=='bad-control':
   text=(root/'runs'/run_key/'stdout').read_text()+(root/'runs'/run_key/'stderr').read_text()
   assert r['returncode']!=0 and ('kernel_reject:'in text or ('while replaying declaration'in text and '(kernel)'in text)) and cfg.get('roots',ROOTS)['math']in text
  assert r['native_retired']and r['cgroup_retired']
  print('RETURNED',json.dumps(row),flush=True)
  # Remove only reproducible successful output snapshots after preserving acceptance,
  # native logs,receipt and measurement. Input artifacts are never removed.
  if receipt and state and not interrupt:
   with(root/'README.md').open('a')as report:report.write(key+': completed; native logs and '+key+'-receipt.json retained; snapshots are regenerable.\n')
   for p in state.glob('ProofServeSegment*.olean'):
    assert p.resolve().is_relative_to(root)
    cleanup.append(dict(path=str(p),bytes=p.stat().st_size,evidence=key+'-receipt.json',reason='regenerable certified snapshot; completed native point retained'))
    p.unlink()
   dump(root/'cleanup.json',cleanup)
  return r,receipt
 roots=cfg.get('roots',ROOTS)
 for cell in cells(cfg):
  key=cell['key'];dataset=cell['dataset'];n=cell['workers'];rep=cell['repeat'];arm=cell['arm']
  state=None;interrupt=cell.get('interrupt',False)
  if arm=='official':
   argv=[guard.SDK/'bin/lake','env','leanchecker','-v',*cell['flags'],roots[dataset]]
  elif arm=='bad-control':
   os.environ['DECOUPLED_MUTATE_MODULE']=roots['math']
   argv=[guard.SDK/'bin/lake','env',binary,'--internal-segment','audit',cell['mutation'],roots['math']]
  else:
   os.environ.pop('DECOUPLED_MUTATE_MODULE',None)
   state=root/('math-interrupted-state'if key in ['math-interrupt','math-resume']else key)
   argv=[binary,project,'--root',roots[dataset],'--workers',str(n),'--checkpoint-dir',state,'--json',*cell['flags']]
   if key in ['math-interrupt','math-resume'] and qualification:argv+=['--segment-modules','1','--closure-roots','0']
  one(key,argv,dataset,n,rep,arm,state,interrupt,limit=cfg.get('cell_limit_s',1800))
 dump(root/'terminal.json',dict(complete=True,cells=len(rows),configuration=str(Path(sys.argv[1]).resolve()),meaning='all finite requested attempts returned; individual failures remain explicit',paper_eligible=not qualification))
 print('MATRIX_TERMINAL',flush=True)
if __name__=='__main__':main()
