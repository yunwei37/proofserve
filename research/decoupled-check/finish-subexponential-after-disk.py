#!/usr/bin/env python3
"""Finish only missing references and negative controls; no periodic Git commits."""
from pathlib import Path
import os,json,time,subprocess,importlib.util,shutil,signal,sys
R=Path('/workspaces/repository');D=R/'research/decoupled-check'
A=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/subexponential-20261103')
LOCK=A.parent.parent/'pcore.lock'
def main():
 os.sched_setaffinity(0,{8})
 spec=importlib.util.spec_from_file_location('s',A/'subexponential-run-resume-v2.py')
 s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
 expected={v['module']for v in json.loads((A/'frame.json').read_text())}
 resume=sys.argv[1:]==['--resume']
 assert not sys.argv[1:] or resume,'only --resume is supported'
 current=s.state()
 assert len(expected)==14721 and set(current['built'])==set(current['stream_ids'])==expected
 backup=A/'pre-final-reference-state.json'
 if resume:
  original=json.loads(backup.read_text())
  prior=json.loads((A/'finish-after-disk-failure.json').read_text())
  assert prior['error']=="RuntimeError('finite final-reference window exhausted')"
  assert current['phase']=='oracle'
  claim=A/'reference-resume-claim.json'
  with claim.open('x')as f:
   json.dump(dict(pid=os.getpid(),remaining=len(expected-set(current['oracle_ids'])),prior_stop=prior),f)
  windows=json.loads((A/'final-reference-progress.json').read_text())['windows']
 else:
  original=current
  assert original['phase']=='failure'and original['failure']['operation']=='disk_ceiling'
  assert not backup.exists(),'already launched; inspect terminal and PID before another attempt'
  s.atomic(backup,original)
  state=dict(original);state['historical_failures']=state.get('historical_failures',[])+[state.pop('failure')]
  state['phase']='oracle';s.atomic(A/'state.json',state)
  windows=0
 # The finite input set and strict cursor advancement bound this invocation.
 # Queue waits are not a scientific failure or an additional overall deadline.
 remaining_at_start=len(expected-set(s.state()['oracle_ids']))
 allowed_windows=(remaining_at_start+15)//16
 calls=0
 begin=time.monotonic()
 def call(args,label,limit):
  nonlocal windows
  assert shutil.disk_usage('/workspaces').used/shutil.disk_usage('/workspaces').total<.85
  cmd=['flock',str(LOCK),'taskset','-c','0-7','timeout','--signal=TERM','--kill-after=10',str(limit),'python3','-u']+args
  log=A/('final-'+label+'-'+str(time.monotonic_ns())+'.log')
  with log.open('x')as f:
   p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
   peak=0;failure=None
   while p.poll()is None:
    table={}
    for entry in Path('/proc').iterdir():
     if not entry.name.isdigit():continue
     try:
      fields=(entry/'stat').read_text().split(') ')[1].split()
      table[int(entry.name)]=(int(fields[1]),int(fields[21])*os.sysconf('SC_PAGE_SIZE'),fields[19])
     except (OSError,ValueError,IndexError):pass
    owned={os.getpid(),p.pid};changed=True
    while changed:
     added={pid for pid,(ppid,rss,birth)in table.items()if ppid in owned}
     changed=not added<=owned;owned|=added
    rss=sum(table[pid][1]for pid in owned if pid in table)
    peak=max(peak,rss)
    if rss>12*1024**3:
     failure='aggregate O RSS budget'
     for pid in owned-{os.getpid()}:
      try:
       if Path('/proc',str(pid),'stat').read_text().split(') ')[1].split()[19]==table[pid][2]:os.kill(pid,signal.SIGKILL)
      except (OSError,KeyError):pass
     p.wait();break
    time.sleep(1)
   rc=p.wait()
  windows+=1
  s.atomic(A/'final-reference-progress.json',dict(windows=windows,phase=s.state()['phase'],oracle_qualified=len(s.state()['oracle_ids']),expected=len(expected),latest_log=str(log),returncode=rc,observed_tree_peak_rss=peak,failure=failure,elapsed_wall_s=time.monotonic()-begin,elapsed_clock_scope='this controller invocation; historical stop retained',resumed=resume))
  if rc or failure:raise RuntimeError((label,rc,failure))
 while True:
  action=s.next_action()
  if action is None:break
  assert action[0]=='oracle','never rebuild or recheck accepted stream'
  assert calls<allowed_windows,'finite reference frame exhausted without completion'
  before=set(s.state()['oracle_ids'])
  requested=set(action[1:])
  assert requested and not requested&before,'never repeat a qualified reference'
  call([str(A/'subexponential-run-resume-v2.py'),'worker']+action,'oracle',1740)
  assert set(s.state()['oracle_ids'])==before|requested,'require exact cursor advancement'
  calls+=1
  s.reduce() # persistent local CSV/state only; never publish each window
 assert s.state()['phase']=='complete'and set(s.state()['oracle_ids'])==expected
 s.reduce()
 call([str(D/'subexponential-negative-controls.py')],'negative-controls',900)
 subprocess.run(['taskset','-c','8','python3',str(D/'analyze-subexponential-complete.py')],check=True)
 controls=json.loads((A/'negative-controls-terminal.json').read_text())
 (D/'subexponential-negative-controls.json').write_text(json.dumps(controls,indent=2)+'\n')
 s.atomic(A/'finish-after-disk-terminal.json',dict(complete=True,reference_count=len(s.state()['oracle_ids']),bad_proofs_rejected=controls['rejected'],native_rejection_processes=controls['native_rejection_processes'],historical_failure=original['failure'],elapsed_wall_s=time.monotonic()-begin,elapsed_clock_scope='this controller invocation; historical stop retained',resumed=resume))
if __name__=='__main__':
 try:main()
 except BaseException as e:
  (A/('finish-after-disk-resume-failure.json'if sys.argv[1:]==['--resume']else'finish-after-disk-failure.json')).write_text(json.dumps(dict(error=repr(e)),indent=2));raise
