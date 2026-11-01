"""Read-only native type census for W's completed no-M panel, in small E-core batches."""
import os,pathlib,json,re,subprocess,signal,csv
HERE=pathlib.Path(__file__).resolve().parent
RAW=pathlib.Path('/workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check')
W=pathlib.Path('/workspaces/.agent-state/gpu-smt-captures/workloads/openai4341-noM-standard-a-20261031')
def main():
 os.sched_setaffinity(0,set(range(8,16)))
 rows=[json.loads(l) for l in (W/'results.jsonl').read_text().splitlines() if json.loads(l)['arm']=='noM']
 assert len(rows)==31 and all(r['returncode']==0 and r['native_retired'] for r in rows)
 out=RAW/'native-panel';out.mkdir(exist_ok=True)
 cache=out/'module-path';cache.mkdir(exist_ok=True)
 old=json.loads(pathlib.Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime/inputs.json').read_text())
 env=dict(os.environ,LEAN_PATH=old['LEAN_PATH'])
 cache_global=pathlib.Path('/workspaces/.agent-state/gpu-smt-workloads/openai4341-oleans')
 (out/'all31-costs.json').write_text(json.dumps(rows,indent=2)+'\n')
 rows=[r for r in rows if (cache_global/pathlib.Path(*r['module'].split('.')).with_suffix('.olean')).exists()]
 source=(HERE/'NativeCensus.lean').read_text()
 body=source[source.index('import Lean'):]
 begin=body.index('  let mods := [');end=body.index('  let mut counts',begin)
 results=[]
 for index in range(0,len(rows),4):
  batch=rows[index:index+4];mods=[r['module'] for r in batch]
  src='\n'.join('import '+m for m in mods)+'\n'+body[:begin]+\
      '  let mods := ['+', '.join(chr(96)+m for m in mods)+']\n'+body[end:]
  path=out/f'batch-{index}.lean'
  log=out/f'batch-{index}.log'
  if log.exists() and 'CK_NATIVE_COUNT' in log.read_text():
   for module,shape,n in re.findall(r'^CK_NATIVE_COUNT (\S+) (\S+) (\d+)$',log.read_text(),re.M):
    results.append(dict(module=module,shape=shape,n=int(n)))
   print('retained native metadata',index+len(batch),flush=True)
   continue
  if log.exists():log.rename(log.with_suffix('.bounded-attempt1.log'))
  if path.exists():path.rename(path.with_suffix('.bounded-attempt1.lean'))
  path.write_text(src)
  with log.open('w') as f:
   ret=subprocess.run(['/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux/bin/lean',
     '-j1','-DmaxHeartbeats=1000000',str(path)],env=env,stdout=f,stderr=subprocess.STDOUT,
     timeout=95,preexec_fn=lambda:signal.alarm(90))
  if ret.returncode:raise RuntimeError(f'native metadata batch failure {index}; preserved raw')
  for module,shape,n in re.findall(r'^CK_NATIVE_COUNT (\S+) (\S+) (\d+)$',log.read_text(),re.M):
   results.append(dict(module=module,shape=shape,n=int(n)))
  print('native metadata returned',index+len(batch),'of',len(rows),flush=True)
 with (HERE/'native-panel-shapes.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
 (out/'costs.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':main()
