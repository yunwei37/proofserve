"""Finite exit-driven continuation of one fixed 5085-module experiment."""
import os,sys,time,json,subprocess,shutil,select
from pathlib import Path
os.sched_setaffinity(0,set(range(8,16)))
R=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
REPO=Path('/workspaces/repository')
start=time.monotonic()
# Initial descriptor is opened while the owning first-window PID is still live.
fd=os.pidfd_open(137341);select.select([fd],[],[],28800);os.close(fd)
if not(R/'window-001-terminal.json').exists():raise SystemExit('first window has no actual terminal')
for source,dest in [('window-next.py','window.py'),('native-next.py','native.py')]:shutil.copy2(R/source,R/dest)
def publish():
 subprocess.run(['python3',str(R/'reduce.py')],check=True)
 os.chdir(REPO)
 assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],text=True).strip()=='main'
 files=['research/decoupled-check/'+p.name for p in(REPO/'research/decoupled-check').glob('*.csv')]+['research/decoupled-check/results.md']
 subprocess.run(['git','add','--']+files,check=True)
 changed=subprocess.run(['git','diff','--cached','--quiet','--']+files).returncode
 if not changed:return
 subprocess.run(['git','-c','user.name=Yunwei 123','-c','user.email=yunwei356@gmail.com','commit','--only','-m','research: retain measured decoupled-check closure window','--']+files,check=True)
 subprocess.run(['git','pull','--rebase','--no-autostash','origin','main'])
 helper="!python3 -c 'import os; print(\"username=x-access-token\"); print(\"password=\"+os.environ[\"ENVBUILDER_GIT_PASSWORD\"])'"
 subprocess.run(['git','-c','credential.helper='+helper,'fetch','origin','main'],check=True)
 subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],check=True)
 subprocess.run(['git','-c','credential.helper='+helper,'push','origin','main'],check=True)
 (R/'last-published.txt').write_text(subprocess.check_output(['git','rev-parse','HEAD'],text=True))
while True:
 publish()
 state=json.loads((R/'progress.json').read_text())
 if any(state.get(k)for k in ['build_failure','stream_failure','matched_failure','oracle_failure']):
  raise SystemExit('real cell failure; retain and review, no automatic weakening or retry')
 if len(state.get('constructed_oracle_done',[]))==4:
  (R/'all-complete.json').write_text(json.dumps(dict(status='complete',windows=state['windows'])))
  break
 if time.monotonic()-start>28800:
  (R/'coordinator-limit.json').write_text(json.dumps(dict(status='eight-hour finite continuation bound; partials retained')))
  break
 # Do not restart after an old native group remains populated.
 current=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split('::',1)[1].lstrip('/')
 for cg in current.parent.glob('proofserve-decoupled-*.scope'):
  if(cg/'cgroup.procs').read_text().strip():raise SystemExit('previous own native scope still populated')
 number=state['windows']+1
 before=Path('/proc/locks').read_text()
 (R/f'window-{number:03d}-locks-before.txt').write_text(before)
 snapshot=R/f'source-window-{number:03d}';snapshot.mkdir()
 for f in ['StreamCheck.lean','native.py','window.py']:shutil.copy2(R/f,snapshot/f)
 args=['flock','/workspaces/.agent-state/gpu-smt-captures/pcore.lock','taskset','-c','0-7',
       'timeout','--signal=TERM','--kill-after=10','1740','python3','-u',str(R/'window.py')]
 with(R/f'window-{number:03d}.log').open('w')as f:
  p=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
  (R/f'window-{number:03d}-submit.json').write_text(json.dumps(dict(pid=p.pid,args=args,locks_before=before),indent=2))
  rc=p.wait()
 if not(R/f'window-{number:03d}-terminal.json').exists():raise SystemExit(f'window exited {rc} without terminal')
