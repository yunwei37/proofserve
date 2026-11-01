"""Prepared >=1s target matrix. Do not submit while another M capture exists.
P0-7 common lease required by caller. All outputs on PVC, no -M.
"""
from pathlib import Path
import os,json,time,re
from declaration_native import run,environment,SDK
ROOT=Path(__file__).resolve().parent
def env_for(out,k,negative=False):
 e=environment();e.update(LEAN_PATH=str(ROOT)+':'+str(ROOT/'overlay')+':'+str(out)+':'+e['LEAN_PATH'],
  CK_K=str(k),CK_OUT=str(out),LEAN_NUM_THREADS=str(max(1,k)))
 e.pop('CK_PREPARE',None)
 if negative:e['CK_NEGATIVE']='1'
 return e
def cell(key,k,negative=False):
 out=ROOT/'outputs'/key;out.mkdir(parents=True,exist_ok=False)
 env=env_for(out,k,negative)
 argv=[SDK/'bin/lean','--root='+str(ROOT),'-j'+str(max(1,k)),
   '--load-dynlib='+str(ROOT/'clock.so'),ROOT/'EnvelopeDriver.lean']
 begin=time.monotonic();phase_results=[]
 env['CK_PHASE']='produce'
 first=run(key+'-produce',argv,120,measured=True,env=env)
 phase_results.append(first)
 if first['returncode']==0 and k and not negative:
  assert first['native_retired'] and first['cgroup_retired']
  merge_env=dict(env,LEAN_NUM_THREADS='1')
  merge_argv=[SDK/'bin/lean','--root='+str(ROOT),'-j1','--load-dynlib='+str(ROOT/'clock.so'),ROOT/'EnvelopeMerger.lean']
  phase_results.append(run(key+'-merge',merge_argv,120,measured=True,env=merge_env))
 elapsed=time.monotonic()-begin
 aggregate=ROOT/'runs'/key;aggregate.mkdir(exist_ok=False)
 stdout=''.join((ROOT/'runs'/phase['key']/'stdout').read_text() for phase in phase_results)
 stderr=''.join((ROOT/'runs'/phase['key']/'stderr').read_text() for phase in phase_results)
 (aggregate/'stdout').write_text(stdout);(aggregate/'stderr').write_text(stderr)
 commands=[json.loads((ROOT/'runs'/phase['key']/'command.json').read_text()) for phase in phase_results]
 (aggregate/'command.json').write_text(json.dumps(dict(kind='sequential_native_phases',phase_commands=commands))+'\n')
 code=next((x['returncode'] for x in phase_results if x['returncode']),0)
 r=dict(kind='sequential_native_phases',key=key,returncode=code,wall_s=elapsed,
  user_s=sum(x['user_s'] for x in phase_results),system_s=sum(x['system_s'] for x in phase_results),
  peak_rss_kib=max(x['peak_rss_kib'] for x in phase_results),charged_peak_bytes=max(x['charged_peak_bytes'] for x in phase_results),
  native_retired=all(x['native_retired'] for x in phase_results),cgroup_retired=all(x['cgroup_retired'] for x in phase_results),
  stop_reasons=[v for x in phase_results for v in x['stop_reasons']],
  cpu_accounting_complete=all(x['returncode'] not in[-9,137] and not x['stop_reasons'] for x in phase_results),
  phase_keys=[x['key'] for x in phase_results],scope='producer fully retires before merge; all phase startup/import/export costs included')
 (aggregate/'result.json').write_text(json.dumps(r,indent=2)+'\n')
 text=stdout
 if negative:
  assert r['returncode'] not in [0,124,137,-9] and not r['stop_reasons'],'not a genuine finite negative control'
  assert 'original C++ kernel rejected declaration' in text+(ROOT/'runs'/key/'stderr').read_text(),'failure did not reach kernel'
 else:
  assert r['returncode']==0 and r['native_retired'] and r['cgroup_retired'] and not r['stop_reasons']
  assert 'CK_RESULT' in text
  if k:assert f'CK_VALID k={k} target_identical=true axioms=[propext] new_axioms=0 sorry=false children={k}' in text
  else:assert 'CK_ORIGINAL_AXIOMS [propext]' in text
 r.update(k=k,outputs=str(out),negative=negative)
 (ROOT/'runs'/key/'cell.json').write_text(json.dumps(r,indent=2)+'\n')
 return r
def main():
 assert sorted(os.sched_getaffinity(0))==list(range(8))
 start=time.monotonic();cells=[]
 # Explicit native target reject; do not reuse the previous small Grid control.
 cell('invalid-target',2,True)
 for rep in [1,2,3]:
  for k in ([8,4,2,1,0] if rep==2 else [0,1,2,4,8]):
   if time.monotonic()-start+260>1680:
    (ROOT/'terminal.json').write_text(json.dumps(dict(complete=False,planned=15,completed=len(cells),reason='finite active window'))+'\n')
    return
   key=f'envelope-k{k}-r{rep}'
   r=cell(key,k)
   cells.append(dict(k=k,rep=rep,raw=str(ROOT/'runs'/key),outputs=r['outputs']))
   (ROOT/'manifest.json').write_text(json.dumps(cells,indent=2)+'\n')
 (ROOT/'terminal.json').write_text(json.dumps(dict(complete=True,planned=15,completed=len(cells)))+'\n')
if __name__=='__main__':
 try:main()
 except BaseException as err:
  (ROOT/'failure.json').write_text(json.dumps(dict(error=repr(err)))+'\n')
  raise
