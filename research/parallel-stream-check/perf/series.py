# Finite declared matrix; one blocking lock/native cell at a time, no parallel decodes.
import json,os,subprocess,time,sys
from pathlib import Path
P=Path(__file__).resolve().parent
assert str(P).startswith('/workspaces/.agent-state/gpu-smt-captures/')
rows=[];state='partial';error=None
try:
 for n in [4,8,1,2]:
  for arm,rep in [('plain','r1-before'),('stat','r1'),('record','r1'),('plain','r1-after')]:
   key='full-'+arm+'-P'+str(n)+'-'+rep
   if (P/(key+'-terminal.json')).exists():raise RuntimeError('existing cell; inspect rather than overwrite')
   cmd=['flock','/workspaces/.agent-state/gpu-smt-captures/pcore.lock','timeout','--signal=TERM','--kill-after=5','1740','taskset','-c','0-7','python3','-u',str(P/'perf_run.py'),arm,str(n),rep]
   with (P/(key+'-controller.log')).open('w') as log:
    q=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT)
    birth=Path('/proc',str(q.pid),'stat').read_text().split(') ',1)[1].split()[19]
    (P/'series-active.json').write_text(json.dumps(dict(pid=q.pid,birth=birth,key=key,argv=cmd,utc=time.strftime('%FT%TZ',time.gmtime())),indent=2))
    print(json.dumps(dict(event='queued',key=key,pid=q.pid,birth=birth)),flush=True)
    rc=q.wait()
   terminal=P/(key+'-terminal.json')
   t=json.loads(terminal.read_text()) if terminal.exists() else {}
   rows.append(dict(key=key,wrapper_rc=rc,native_state=t.get('state'),cell=t.get('cell')))
   (P/'series-progress.json').write_text(json.dumps(rows,indent=2))
   print(json.dumps(dict(event='retired',key=key,returncode=rc,state=t.get('state'))),flush=True)
   if rc or t.get('state')!='complete':raise RuntimeError('incomplete cell; preserve and stop sequence')
 state='native_matrix_complete_requires_analysis'
except BaseException as ex:error=repr(ex);raise
finally:
 (P/'series-terminal.json').write_text(json.dumps(dict(state=state,error=error,rows=rows,utc=time.strftime('%FT%TZ',time.gmtime())),indent=2))
