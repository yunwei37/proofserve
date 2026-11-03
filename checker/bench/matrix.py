"""Fixed release evaluation. One blocking P-core lease per complete native cell.
CLI: python3 matrix.py CONFIG.json; raw files stay in the configured PVC directory.
No commits or publication from this program.
"""
import os,sys,json,time,fcntl,threading,signal,csv
from pathlib import Path
import guard
def dump(p,value):
 q=p.with_suffix(p.suffix+'.pending')
 with q.open('w')as f:json.dump(value,f,indent=2);f.flush();os.fsync(f.fileno())
 q.replace(p)
def main():
 cfg=json.loads(Path(sys.argv[1]).read_text());root=Path(cfg['raw']).resolve()
 root.mkdir(parents=True,exist_ok=True);guard.ROOT=root
 binary=Path(cfg['binary']);project=Path(cfg['project']);lease=Path(cfg['lease'])
 rows=[];refs={};cleanup=[]
 def one(key,argv,dataset,workers,repeat,arm='native',state=None,interrupt=False,limit=1100):
  fs=os.statvfs(root);used=1-fs.f_bavail/fs.f_blocks
  if used>=.85:raise RuntimeError('disk85% boundary; preserve and stop')
  e=guard.environment();e['PATH']=str(guard.SDK/'bin')+':'+e['PATH'];e['LEAN_PATH']=cfg.get('overlay','')if dataset in['grid','barrier']else''
  e['LEAN_NUM_THREADS']=str(workers or 4)
  os.chdir(project)
  print('WAIT',key,flush=True)
  with lease.open('a+')as lock:
   fcntl.flock(lock,fcntl.LOCK_EX);os.sched_setaffinity(0,set(range(8)))
   print('ACQUIRED',key,flush=True)
   stopped=threading.Event();proof=[]
   def interrupter():
    while not stopped.wait(.01):
     if state and (state/'segment-0.json').exists()and guard.ACTIVE:
      cg,pid=guard.ACTIVE
      proof.append(dict(pid=pid,checkpoint=str(state/'segment-0.json'),reason='actual process interruption after first certified segment'))
      (cg/'cgroup.kill').write_text('1')
      dump(root/(key+'-interruption.json'),proof)
      break
   t=threading.Thread(target=interrupter,daemon=True)if interrupt else None
   if t:t.start()
   try:r=guard.run(key,argv,limit,True,e)
   finally:
    stopped.set()
    if t:t.join()
   os.sched_setaffinity(0,set(range(8,16)))
  receipt=None
  if arm in ['native','full-math']and r['returncode']==0:
   receipt=json.loads((root/'runs'/key/'stdout').read_text())
   assert receipt['status']=='complete'and receipt['execution_path']=='proofserve-parallel'
   assert len(receipt['accepted'])==len(set(receipt['accepted']))
   if dataset in refs:assert receipt['accepted']==refs[dataset]
   else:refs[dataset]=receipt['accepted']
   dump(root/(key+'-receipt.json'),receipt)
  row=dict(key=key,commit=cfg['commit'],dataset=dataset,workers=workers,repeat=repeat,arm=arm,
   returncode=r['returncode'],wall_s=r.get('wall_s'),cpu_s=r.get('user_s',0)+r.get('system_s',0),
   peak_rss_kib=r.get('peak_rss_kib'),rss_sample_bytes=r['sampled_tree_peak_bytes'],modules=len(receipt['accepted'])if receipt else None,
   segments=len(receipt['segments'])if receipt else None,manual_interruption=bool(proof))
  rows.append(row);dump(root/'completed.json',rows)
  if interrupt:assert proof and r['returncode']!=0
  elif r['returncode']!=0 and arm not in ['full-math','official','bad-control']:
   raise RuntimeError('native cell incomplete or failed; stop without imputing a result: '+key)
  if arm=='bad-control':
   text=(root/'runs'/key/'stdout').read_text()+(root/'runs'/key/'stderr').read_text()
   assert r['returncode']!=0 and ('kernel_reject:'in text or ('while replaying declaration'in text and '(kernel)'in text)) and 'Mathlib.Data.Nat.Basic'in text
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
 roots={'math':'Mathlib.Data.Nat.Basic','grid':'OAI.Analysis.PlanarPacking.Grid','barrier':'OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41'}
 for dataset in ['math','grid','barrier']:
  for rep in [1,2,3]:
   ns=[1,2,4,8]if rep!=2 else[8,4,2,1]
   for n in ns:
    key=dataset+'-P'+str(n)+'-r'+str(rep);state=root/key
    one(key,[binary,project,'--root',roots[dataset],'--workers',str(n),'--checkpoint-dir',state,'--json'],dataset,n,rep,state=state)
  if dataset in ['math','grid']:
   for flag in ['--no-persistence','--no-split-fallback']:
    for rep in[1,2,3]:
     key=dataset+'-P8-'+flag[2:]+'-r'+str(rep);state=root/key
     one(key,[binary,project,'--root',roots[dataset],'--workers','8','--checkpoint-dir',state,'--json',flag],dataset,8,rep,state=state)
 # Official CLI controls have different proof ledgers. Preserve separate rows,no imputed speedup.
 for dataset in roots:
  for mode in ['default','fresh']:
   for rep in[1,2,3]:
    flags=['--fresh']if mode=='fresh'else[]
    one(dataset+'-official-'+mode+'-r'+str(rep),[guard.SDK/'bin/lake','env','leanchecker','-v',*flags,roots[dataset]],dataset,8,rep,'official')
 # Original-kernel bad proof after a real Mathlib prefix.
 for mutation in ['bvar','unknown','sort']:
  os.environ['DECOUPLED_MUTATE_MODULE']=roots['math']
  one('bad-real-prefix-'+mutation,[binary,'--internal-segment','audit',mutation,roots['math']],'math',4,1,'bad-control')
 os.environ.pop('DECOUPLED_MUTATE_MODULE',None)
 # Actual abrupt kill,then resume the same successful-prefix directory.
 state=root/'math-interrupted-state'
 one('math-interrupt',[binary,project,'--root',roots['math'],'--workers','4','--checkpoint-dir',state,'--json'],'math',4,1,state=state,interrupt=True)
 one('math-resume',[binary,project,'--root',roots['math'],'--workers','4','--checkpoint-dir',state,'--json'],'math',4,1,state=state)
 # All source modules at the fixed version,not the Nat.Basic closure.
 modules=cfg['full_math_modules']
 for quota in[500,100]:
  state=root/('full-math-quota'+str(quota))
  args=[binary,project,'--checkpoint-dir',state,'--segment-modules',str(quota),'--json']
  for mod in modules:args+=['--root',mod]
  r,j=one('full-math-quota'+str(quota),args,'full-math',0,1,'full-math',state=state,limit=1700)
  if r['returncode']==0:
   assert j and set(modules)<=set(j['accepted'])
   break
  events={k:int(v)for k,v in(line.split()for line in r['memory_events'].splitlines())}
  memory=events.get('oom_kill',0)>0 or bool(r['stop_reasons'])
  if not memory:break
 dump(root/'terminal.json',dict(complete=True,cells=len(rows),meaning='all finite requested attempts returned; individual failures remain explicit'))
 print('MATRIX_TERMINAL',flush=True)
if __name__=='__main__':main()
