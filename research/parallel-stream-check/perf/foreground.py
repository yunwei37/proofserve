"""One finite foreground collection, immediate offline decode, native source unchanged."""
import json,os,select,signal,subprocess,time,sys
from pathlib import Path
P=Path(__file__).resolve().parent
assert str(P).startswith('/workspaces/.agent-state/gpu-smt-captures/')
assert set(os.sched_getaffinity(0))<=set(range(8,16))
series=json.loads((P/'series-launch.json').read_text())
def state(a):
 f=Path('/proc',str(a['pid']),'stat')
 if not f.exists():return None
 v=f.read_text().split(') ',1)[1].split()
 if v[19]!=a['birth']:raise RuntimeError('PID reused; preserve scene')
 return v[0]
def signal_series(sig):
 if state(series) is not None:os.kill(series['pid'],sig)
def wait_exit(a):
 if state(a) is None:return
 fd=os.pidfd_open(a['pid'])
 try:
  poll=select.poll();poll.register(fd,select.POLLIN);poll.poll()
 finally:os.close(fd)
def emit(x):print(json.dumps(x),flush=True)
completed=[];status='partial';error=None
try:
 assert state(series)=='T','only take over the deliberately paused waiting controller'
 for n in [4,8,1,2]:
  for arm,rep in [('plain','r1-before'),('stat','r1'),('record','r1'),('plain','r1-after')]:
   key='full-'+arm+'-P'+str(n)+'-'+rep
   terminal=P/(key+'-terminal.json')
   if terminal.exists():
    t=json.loads(terminal.read_text())
   else:
    a=json.loads((P/'series-active.json').read_text())
    if a['key']!=key:raise RuntimeError('unexpected active cell '+a['key']+' versus '+key)
    emit(dict(event='blocking_native_exit',key=key,pid=a['pid'],birth=a['birth']))
    wait_exit(a)
    t=json.loads(terminal.read_text())
   if t['state']!='complete':raise RuntimeError('incomplete native cell '+key)
   c=t['cell']
   emit(dict(event='collected',key=key,wall_s=c['wall_s'],user_s=c['user_s'],system_s=c['system_s'],
    accepted=c['accepted_count'],same_verdicts=c['accepted_set_equal_to_reference']))
   if arm=='record':
    d=P/('decode-'+key)
    if d.exists():raise RuntimeError('existing decode; inspect rather than overwrite')
    with (P/(key+'-decode-controller.log')).open('w') as log:
     z=subprocess.run(['python3','-u',str(P/'decode.py'),key],stdout=log,stderr=subprocess.STDOUT)
    if z.returncode:raise RuntimeError('decode failed '+key)
    emit(dict(event='decoded',key=key,terminal=json.loads((d/'decode-terminal.json').read_text())))
   z=subprocess.run(['python3',str(P/'summarize.py'),str(P),str(P/'analysis-progress')])
   if z.returncode:raise RuntimeError('summary failed '+key)
   completed.append(key)
   (P/'foreground-progress.json').write_text(json.dumps(dict(completed=completed,utc=time.strftime('%FT%TZ',time.gmtime())),indent=2))
   # Original controller retains frozen ordering/commands. Resume only after
   # collecting/decode; pause just the waiting parent once the next child exists.
   active=json.loads((P/'series-active.json').read_text())
   if active['key']==key:
    signal_series(signal.SIGCONT)
    while True:
     if state(series) is None or state(series)=='Z':break
     try:next_active=json.loads((P/'series-active.json').read_text())
     except json.JSONDecodeError:time.sleep(.05);continue
     if next_active['key']!=key:
      signal_series(signal.SIGSTOP)
      emit(dict(event='next_native_live_or_queued',**next_active))
      break
     time.sleep(.05)
 wait_exit(series)
 t=json.loads((P/'series-terminal.json').read_text())
 if t['state']!='native_matrix_complete_requires_analysis':raise RuntimeError('original matrix terminal incomplete')
 status='all16_native_and_four_decodes_complete_requires_scientific_review'
except BaseException as ex:error=repr(ex);raise
finally:
 # Never leave a healthy native matrix stranded behind an observer failure.
 signal_series(signal.SIGCONT)
 (P/'foreground-terminal.json').write_text(json.dumps(dict(state=status,error=error,completed=completed,
  utc=time.strftime('%FT%TZ',time.gmtime())),indent=2))
