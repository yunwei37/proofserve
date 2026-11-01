"""Owned finite native cells: external memory guard, sampled own RSS, no Lean -M."""
import os,json,signal,time,subprocess,threading
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SDK=Path('/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux')
ACTIVE=None
def abort(signum,frame):
 if ACTIVE:
  cg,pid=ACTIVE
  try:(cg/'cgroup.kill').write_text('1')
  except OSError:
   try:os.killpg(pid,signal.SIGKILL)
   except ProcessLookupError:pass
 raise SystemExit(128+signum)
signal.signal(signal.SIGTERM,abort);signal.signal(signal.SIGINT,abort)
def environment():
 old=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime/inputs.json')
 e=dict(os.environ,LEAN_PATH=json.loads(old.read_text())['LEAN_PATH'],LEAN_SYSROOT=str(SDK),LEAN_NUM_THREADS='8',TMPDIR=str(ROOT/'tmp'))
 (ROOT/'tmp').mkdir(exist_ok=True)
 return e
def run(key,argv,limit=600,measured=False,env=None):
 global ACTIVE
 assert not any(str(x).startswith('-M') for x in argv)
 if measured:assert sorted(os.sched_getaffinity(0))==list(range(8))
 out=ROOT/'runs'/key;out.mkdir(parents=True,exist_ok=False)
 current=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split('::',1)[1].lstrip('/')
 assert current.name.startswith('cri-containerd-') and 'pod' in current.parent.name
 cg=current.parent/('proofserve-m-decl-'+str(os.getpid())+'-'+key+'.scope')
 cg.mkdir();(cg/'memory.max').write_text(str(14*1024**3));(cg/'memory.oom.group').write_text('1')
 cmd=['timeout','--signal=TERM','--kill-after=5',str(limit)]+list(map(str,argv))
 record=dict(key=key,argv=cmd,affinity=sorted(os.sched_getaffinity(0)),measured=measured,
  wall_limit_s=limit,own_rss_sample_stop_gib=14,cgroup=str(cg),cgroup_charged_memory_max_gib=14)
 (out/'command.json').write_text(json.dumps(record,indent=2)+'\n')
 done=threading.Event();stops=[];peak=[0];p=None;reaped=False
 def enter():(cg/'cgroup.procs').write_text('0')
 def sample():
  with (out/'memory.jsonl').open('w') as f:
   while not done.is_set():
    members=[]
    try:ids=(cg/'cgroup.procs').read_text().split()
    except OSError:ids=[]
    for pid in ids:
     try:
      fields=Path('/proc',pid,'stat').read_text().split(') ',1)[1].split()
      members.append(dict(pid=int(pid),birth=fields[19],rss=int(fields[21])*os.sysconf('SC_PAGE_SIZE')))
     except (OSError,ValueError,IndexError):pass
    total=sum(x['rss'] for x in members);peak[0]=max(peak[0],total)
    f.write(json.dumps(dict(rss_bytes=total,processes=members))+'\n');f.flush()
    if total>14*1024**3:
     stops.append('sampled_own_RSS_budget')
     try:(cg/'cgroup.kill').write_text('1')
     except OSError:pass
     break
    done.wait(1)
 thread=None
 try:
  with (out/'stdout').open('w') as fo,(out/'stderr').open('w') as fe:
   begin=time.monotonic()
   p=subprocess.Popen(cmd,env=environment() if env is None else env,stdout=fo,stderr=fe,preexec_fn=enter,start_new_session=True)
   ACTIVE=(cg,p.pid)
   fields=Path(f'/proc/{p.pid}/stat').read_text().split(') ',1)[1].split()
   record.update(pid=p.pid,birth=fields[19])
   thread=threading.Thread(target=sample,daemon=True);thread.start()
   _,status,ru=os.wait4(p.pid,0);reaped=True;p.returncode=os.waitstatus_to_exitcode(status)
   record.update(returncode=p.returncode,wall_s=time.monotonic()-begin,user_s=ru.ru_utime,
    system_s=ru.ru_stime,peak_rss_kib=ru.ru_maxrss,native_retired=not Path(f'/proc/{p.pid}').exists())
 finally:
  if p is not None and not reaped:
   try:(cg/'cgroup.kill').write_text('1')
   except OSError:pass
   try:os.wait4(p.pid,0)
   except ChildProcessError:pass
  done.set()
  if thread:thread.join(2)
  ACTIVE=None
  record.update(sampled_tree_peak_bytes=peak[0],stop_reasons=stops,
   memory_events=(cg/'memory.events').read_text(),charged_peak_bytes=int((cg/'memory.peak').read_text()))
  cpu_text=(cg/'cpu.stat').read_text()
  record['cgroup_cpu_stat']=cpu_text
  cpu_values={k:int(v) for k,v in (line.split()for line in cpu_text.splitlines())}
  for label in ['usage','user','system']:
   if label+'_usec'in cpu_values:record['cgroup_'+label+'_s']=cpu_values[label+'_usec']/1e6
  record['wait4_usage_complete']=reaped and not stops and record.get('returncode',-1)>=0
  for attempt in range(6):
   try:cg.rmdir();record['cgroup_retired']=True;break
   except OSError as err:
    if attempt==5:record['cgroup_cleanup_pending']=str(err)
    else:time.sleep(0.05)
  (out/'result.json').write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps(record),flush=True)
 return record
