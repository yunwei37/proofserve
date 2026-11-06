from pathlib import Path
import json,os,time,fcntl,signal,subprocess,datetime
raw=Path(__file__).resolve().parent
pid=3019309;birth='23727126'
def born(p):
 try:return Path('/proc',str(p),'stat').read_text().rsplit(')',1)[1].split()[19]
 except FileNotFoundError:return None
assert born(pid)==birth
lease=Path('/workspaces/.agent-state/gpu-smt-captures/pcore.lock').open('a+')
(raw/'boundary-handoff-wait.json').write_text(json.dumps(dict(pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),old_pid=pid,old_birth=birth,reason='finish current cell, then collect originally planned controls before remaining official repetitions'),indent=2)+'\n')
fcntl.flock(lease,fcntl.LOCK_EX)
assert born(pid)==birth
for _ in range(300):
 unfinished=[p.name for p in(raw/'runs').iterdir()if(p/'command.json').exists()and not(p/'result.json').exists()]
 wchan=Path('/proc',str(pid),'wchan').read_text().strip()
 if not unfinished and 'lock'in wchan:
  break
 time.sleep(.05)
else:raise RuntimeError('no safe between-cell collector boundary observed; do not signal')
proof=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),old_pid=pid,old_birth=birth,old_wchan=wchan,
 no_active_native=True,completed_keys=[r['key']for r in json.loads((raw/'completed.json').read_text())])
os.kill(pid,signal.SIGTERM)
for _ in range(200):
 stat=Path('/proc',str(pid),'stat')
 if not stat.exists()or stat.read_text().rsplit(')',1)[1].split()[0]=='Z':break
 time.sleep(.05)
else:raise RuntimeError('old finite collector did not retire')
old_end=raw/'collection-terminal.json'
if old_end.exists():(raw/'continuation-1-end.json').write_text(old_end.read_text())
fcntl.flock(lease,fcntl.LOCK_UN);lease.close()
cfg=json.loads((raw/'config.json').read_text());wf=json.loads((raw/'workflow-config.json').read_text())
env=dict(os.environ);sdk=Path(wf['sdk'])
old=json.loads(Path(wf['census_run_config']).read_text())['env']
env.update({k:v for k,v in old.items()if k in ['LD_LIBRARY_PATH','LEAN_SYSROOT']})
env.update(PROOFSERVE_BENCH_SDK=str(sdk),LEAN_SYSROOT=str(sdk),LEAN_PATH=cfg['lean_path'],PATH=str(sdk/'bin')+':'+env['PATH'],LEAN_NUM_THREADS='8')
with(raw/'continuation-2.stdout').open('a')as out,(raw/'continuation-2.stderr').open('a')as err:
 p=subprocess.Popen(['python3','-u',str(raw/'continue-prioritized-controls.py')],env=env,cwd='/workspaces/repository',stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True)
proof['new_pid']=p.pid
(raw/'between-cell-handoff.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(proof),flush=True)
