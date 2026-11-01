"""Finite exit-event handoff between two already requested experiments.

No agent, duty, periodic polling or standing scheduler. At most one timed task
is submitted by this process, only after the previous exact owner retires.
"""
from pathlib import Path
import json,os,select,subprocess,time
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
NEXT=BASE/'reproducible-verdict-v5'
def alive(pid,birth):
 try:return Path(f'/proc/{pid}/stat').read_text().split(') ',1)[1].split()[19]==str(birth)
 except OSError:return False
def main():
 launch=json.loads((ROOT/'private-launch.json').read_text())
 record=dict(owner=launch,started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
   next_point=str(NEXT),policy='one finite exit-event handoff; no recurring runner')
 try:
  if alive(launch['pid'],launch['birth']):
   fd=os.pidfd_open(launch['pid'])
   try:
    # The PID identity has been checked and pidfd follows this exact process.
    if alive(launch['pid'],launch['birth']):select.select([fd],[],[])
   finally:os.close(fd)
  terminal=json.loads((ROOT/'private-terminal.json').read_text())
  for cell in terminal['cells']:
   if 'pid' not in cell:continue
   if alive(cell['pid'],cell['birth']):raise RuntimeError('old native still live')
   if not cell.get('native_retired')or not cell.get('cgroup_retired'):
    raise RuntimeError('old native/cgroup retirement incomplete')
  record.update(previous_state=terminal['state'],retirement_confirmed=True,
    submit_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
  (ROOT/'handoff-state.json').write_text(json.dumps(record,indent=2))
  if (NEXT/'region-launch.json').exists()or(NEXT/'runs').exists():
   raise RuntimeError('next task already submitted/started; never duplicate')
  cmd=['flock',str(BASE/'pcore.lock'),'timeout','--signal=TERM','--kill-after=5','1740',
    'taskset','-c','0-7','python3','-u',str(NEXT/'run_regions.py')]
  with(NEXT/'region-controller.log').open('x')as f:
   child=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT)
  birth=Path(f'/proc/{child.pid}/stat').read_text().split(') ',1)[1].split()[19]
  (NEXT/'region-launch.json').write_text(json.dumps(dict(pid=child.pid,birth=birth,argv=cmd,
    prior_point=str(ROOT),utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())),indent=2))
  record.update(next_pid=child.pid,next_birth=birth)
  (ROOT/'handoff-state.json').write_text(json.dumps(record,indent=2))
  record['next_exit']=child.wait()
  record['next_terminal_exists']=(NEXT/'region-terminal.json').exists()
  record['state']='finite_handoff_finished'
 except BaseException as error:
  record.update(state='handoff_stopped_preserve',error=repr(error))
 (ROOT/'handoff-terminal.json').write_text(json.dumps(record,indent=2))
 return 0 if record['state']=='finite_handoff_finished'else 1
if __name__=='__main__':raise SystemExit(main())
