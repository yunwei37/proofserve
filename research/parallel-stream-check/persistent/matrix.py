import json,subprocess,time,os,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
assert str(P).startswith('/workspaces/.agent-state/gpu-smt-captures/')
assert json.loads((P/'qualification-terminal.json').read_text())['state']=='qualified'
schedule=[]
for rep in [1,2,3]:
 for n in ([8,4,2,1]if rep%2 else [1,2,4,8]):
  for mode in ([1,0]if rep%2 else [0,1]):schedule.append(('plain',mode,n,'r'+str(rep)))
for i,n in enumerate([1,8,2,4]):
 for mode in ([0,1]if i%2==0 else [1,0]):schedule.append(('stat',mode,n,'r1'))
assert len(schedule)==32
(P/'matrix-schedule.json').write_text(json.dumps(schedule))
rows=[];state='partial';error=None
try:
 for arm,mode,n,rep in schedule:
  usage=shutil.disk_usage('/workspaces')
  if usage.used/usage.total>=.85:raise RuntimeError('user disk85% ceiling reached; preserve results')
  key='full-'+arm+'-m'+str(mode)+'-P'+str(n)+'-'+rep
  if (P/(key+'-terminal.json')).exists():raise RuntimeError('existing point; inspect, never overwrite')
  argv=['flock','/workspaces/.agent-state/gpu-smt-captures/pcore.lock','timeout','--signal=TERM','--kill-after=5','1740','taskset','-c','0-7','python3','-u',str(P/'cell.py'),arm,str(mode),str(n),rep]
  with(P/(key+'-controller.log')).open('w')as log:
   q=subprocess.Popen(argv,stdout=log,stderr=subprocess.STDOUT)
   birth=Path('/proc',str(q.pid),'stat').read_text().split(') ',1)[1].split()[19]
   (P/'matrix-active.json').write_text(json.dumps(dict(key=key,pid=q.pid,birth=birth,argv=argv,utc=time.strftime('%FT%TZ',time.gmtime())),indent=2))
   print(json.dumps(dict(event='blocking_cell',key=key,pid=q.pid,birth=birth)),flush=True)
   rc=q.wait()
  file=P/(key+'-terminal.json')
  terminal=json.loads(file.read_text())if file.exists()else{}
  c=terminal.get('cell')or{}
  rows.append(dict(key=key,wrapper_rc=rc,state=terminal.get('state'),wall_s=c.get('wall_s'),
   CPU_s=c.get('user_s',0)+c.get('system_s',0),kernel_CPU_ns=c.get('kernel_CPU_ns'),
   checks=c.get('checks'),units=c.get('allocation_units'),accepted_equal=c.get('accepted_set_equal_to_reference'),
   sampled_peak=c.get('sampled_tree_peak_bytes'),mark=c.get('persistence')))
  (P/'matrix-progress.json').write_text(json.dumps(rows,indent=2))
  print(json.dumps(dict(event='cell_returned',completed=len(rows),**rows[-1])),flush=True)
  if rc or terminal.get('state')!='complete':raise RuntimeError('cell failed qualification; inspect retained actual result')
 state='all32_complete_requires_review'
except BaseException as ex:error=repr(ex);raise
finally:
 (P/'matrix-terminal.json').write_text(json.dumps(dict(state=state,error=error,rows=rows,
  utc=time.strftime('%FT%TZ',time.gmtime())),indent=2))
