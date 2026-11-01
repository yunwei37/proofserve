#!/usr/bin/env python3
"""Finite, exit-driven extension of the current native experiment; no service/schedule."""
import os,sys,time,json,select,subprocess,shutil
from pathlib import Path
os.sched_setaffinity(0,{8})
BASE=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
ROOT=BASE/'scale-study/falconer-project-20261101'
SOURCES=Path(__file__).parent
ROOT.mkdir(exist_ok=True)
REPO=Path('/workspaces/repository')
def terminal(status,**fields):
 (ROOT/'coordinator-terminal.json').write_text(json.dumps(dict(status=status,**fields),indent=2))
def wait_owner(pid,birth):
 try:
  actual=Path('/proc/'+str(pid)+'/stat').read_text().split(') ')[1].split()[19]
 except FileNotFoundError:return
 if actual!=str(birth):return
 fd=os.pidfd_open(pid)
 try:
  ready=select.select([fd],[],[],43200)[0]
  if not ready:raise RuntimeError('finite dependency wait expired; raw data retained')
 finally:os.close(fd)
def publish():
 subprocess.run(['python3',str(SOURCES/'reduce-falconer.py')],check=True)
 names=['falconer-result.md','falconer-source-costs.csv','falconer-memory-curve.csv','falconer-memory-fit.csv','falconer-whole-library-memory-scenarios.csv']
 files=['research/decoupled-check/'+n for n in names if(REPO/'research/decoupled-check'/n).exists()]
 if not files:return
 assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=REPO,text=True).strip()=='main'
 subprocess.run(['git','add','--']+files,cwd=REPO,check=True)
 if not subprocess.run(['git','diff','--cached','--quiet','--']+files,cwd=REPO).returncode:return
 subprocess.run(['git','-c','user.name=Yunwei 123','-c','user.email=yunwei356@gmail.com','commit','--only','-m','research: retain full Falconer native closure checkpoint','--']+files,cwd=REPO,check=True)
 subprocess.run(['git','pull','--rebase','--no-autostash','origin','main'],cwd=REPO)
 helper="!python3 -c 'import os; print(\"username=x-access-token\"); print(\"password=\"+os.environ[\"ENVBUILDER_GIT_PASSWORD\"])'"
 subprocess.run(['git','-c','credential.helper='+helper,'fetch','origin','main'],cwd=REPO,check=True)
 subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],cwd=REPO,check=True)
 subprocess.run(['git','-c','credential.helper='+helper,'push','origin','main'],cwd=REPO,check=True)
def main():
 launch=json.loads((SOURCES/'extension-submission.json').read_text())
 wait_owner(launch['parent_pid'],launch['parent_birth'])
 if not(BASE/'all-complete.json').exists():
  terminal('parent incomplete; preserve primary collection and do not replace it');return
 b=BASE/'scale-study/boundary-v4'
 sub=json.loads((b/'submission.json').read_text());wait_owner(sub['pid'],sub['birth'])
 if not(b/'qualified.json').exists()or not(ROOT.parent/'measurement-v1/measurement-qualified.json').exists()or not(ROOT/'cohort-plan.json').exists():
  terminal('native context qualification or external graph incomplete');return
 plan=json.loads((ROOT/'cohort-plan.json').read_text())
 if plan['status']!='prepared':terminal('complete source graph unavailable');return
 (ROOT/'source-reference.json').write_text(json.dumps(dict(qualification=str(b),sources=str(SOURCES),
  common_artifact_root=str(BASE/'constructed/lib'),accounting='exact immutable common nodes from same finite experiment'),indent=2))
 start=time.monotonic()
 while time.monotonic()-start<43200:
  state=json.loads((ROOT/'progress.json').read_text())if(ROOT/'progress.json').exists()else{}
  if state.get('failure')or state.get('complete'):
   publish();terminal('complete'if state.get('complete')else'actual cell failure',state=state);return
  number=state.get('windows',0)+1
  before=Path('/proc/locks').read_text()
  args=['flock','/workspaces/.agent-state/gpu-smt-captures/pcore.lock','taskset','-c','0-7','timeout','--signal=TERM','--kill-after=10','1740','python3','-u',str(ROOT/'falconer-window.py')]
  with(ROOT/f'window-{number:03d}.log').open('w')as f:
   proc=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
   (ROOT/f'window-{number:03d}-submit.json').write_text(json.dumps(dict(pid=proc.pid,args=args,locks_before=before),indent=2))
   rc=proc.wait()
  if not(ROOT/f'window-{number:03d}-terminal.json').exists():
   terminal('window exit without terminal',returncode=rc);publish();return
  publish()
 terminal('finite twelve-hour continuation bound; partial observations preserved')
if __name__=='__main__':
 try:main()
 except BaseException as err:
  terminal('controller exception',error=repr(err));raise
