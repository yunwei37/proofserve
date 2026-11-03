"""One-shot finite continuation: actual native exit, then offline decoding."""
import json,os,select,subprocess,sys,time
from pathlib import Path
P=Path(__file__).resolve().parent
assert str(P).startswith('/workspaces/.agent-state/gpu-smt-captures/')
assert set(os.sched_getaffinity(0))<=set(range(8,16))
launch=json.loads((P/'series-launch.json').read_text());pid=launch['pid']
if Path('/proc',str(pid)).exists():
 birth=Path('/proc',str(pid),'stat').read_text().split(') ',1)[1].split()[19]
 if birth!=launch['birth']:raise RuntimeError('PID birth mismatch; inspect')
 fd=os.pidfd_open(pid)
 try:
  poll=select.poll();poll.register(fd,select.POLLIN);poll.poll()
 finally:os.close(fd)
t=json.loads((P/'series-terminal.json').read_text())
if t['state']!='native_matrix_complete_requires_analysis':raise RuntimeError('incomplete native matrix; no automatic acceptance')
guard=(P/'native.py').read_text()
guard=guard.replace('14*1024**3','1*1024**3').replace('own_rss_sample_stop_gib=14','own_rss_sample_stop_gib=1').replace('cgroup_charged_memory_max_gib=14','cgroup_charged_memory_max_gib=1')
(P/'decode_guard.py').write_text(guard)
state='partial';done=[];error=None
try:
 for n in [4,8,1,2]:
  key='full-record-P'+str(n)+'-r1'
  z=subprocess.run(['python3','-u',str(P/'decode.py'),key])
  if z.returncode:raise RuntimeError('decode failed '+key+'; preserve')
  done.append(key)
 z=subprocess.run(['python3',str(P/'summarize.py'),str(P),str(P/'analysis')])
 if z.returncode:raise RuntimeError('summary failed')
 state='native_and_decode_complete_requires_scientific_review'
except BaseException as ex:error=repr(ex);raise
finally:
 (P/'analysis-terminal.json').write_text(json.dumps(dict(state=state,completed=done,error=error,utc=time.strftime('%FT%TZ',time.gmtime())),indent=2))
