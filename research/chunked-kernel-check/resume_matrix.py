"""Resume only missing frozen-v3 native cells in one bounded common-lock window."""
import os,pathlib,json,subprocess,fcntl,datetime,sys
BASE=pathlib.Path(__file__).resolve().parent
RAW=BASE.parent
LOCK=pathlib.Path('/workspaces/.agent-state/gpu-smt-captures/pcore.lock')
os.sched_setaffinity(0,set(range(8,16)))
def alive(identity):
 p=pathlib.Path(f"/proc/{identity['pid']}/stat")
 try:
  fields=p.read_text().split(') ',1)[1].split()
  return fields[19]==str(identity['birth']) and fields[0]!='Z'
 except FileNotFoundError:return False
def main():
 old=json.loads((RAW/'frozen-grid-v3/launch.json').read_text())
 assert not alive(old),'original finite controller still alive'
 for p in (RAW/'runs').glob('grid-v3-*/identity.json'):
  assert not alive(json.loads(p.read_text())),str(p)
 lockfd=int(os.environ['CK_PCORE_LOCK_FD'])
 assert (os.fstat(lockfd).st_dev,os.fstat(lockfd).st_ino)==(LOCK.stat().st_dev,LOCK.stat().st_ino)
 # flock from the outer shell and this fd are the same open file description.
 fcntl.flock(lockfd,fcntl.LOCK_EX)
 cells=[]
 try:
  for rep in [1,2,3]:
   for k in ([8,4,2,1,0] if rep==2 else [0,1,2,4,8]):
    original=RAW/'runs'/f'grid-v3-k{k}-r{rep}'
    if (original/'result.json').exists():
     r=json.loads((original/'result.json').read_text())
     assert r['returncode']==0 and r['retired'] and not r['stop_reasons']
     path=original
    else:
     label=f'grid-v3-resume1-k{k}-r{rep}'
     cp=subprocess.run([sys.executable,'-u',str(BASE/'run.py'),label,str(k)],
       env=os.environ,pass_fds=(lockfd,),check=True)
     path=RAW/'runs'/label
     r=json.loads((path/'result.json').read_text())
     assert r['returncode']==0 and r['retired'] and not r['stop_reasons']
    cells.append(dict(k=k,rep=rep,raw=str(path),reused_original=path==original))
    (BASE/'progress.json').write_text(json.dumps(dict(planned=15,completed=len(cells),last=cells[-1]),indent=2)+'\n')
  (BASE/'manifest.json').write_text(json.dumps(cells,indent=2)+'\n')
  (BASE/'terminal.json').write_text(json.dumps(dict(complete=True,completed=15,planned=15,
    original_source=str(RAW/'frozen-grid-v3'),continuation_source=str(BASE),
    hardware_unchanged=True,clock_boundary='native cells only; queue/controller durations not combined into service throughput'),indent=2)+'\n')
 except BaseException as e:
  (BASE/'terminal.json').write_text(json.dumps(dict(complete=False,completed=len(cells),error=repr(e)),indent=2)+'\n')
  raise
if __name__=='__main__':main()
