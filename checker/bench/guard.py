"""Owned finite native cells: external memory guard, sampled own RSS, no Lean -M."""
import os,json,signal,time,subprocess,threading
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sdk_path=os.environ.get('PROOFSERVE_BENCH_SDK')
if not sdk_path:raise RuntimeError('Set PROOFSERVE_BENCH_SDK to the frozen Lean SDK before starting the benchmark')
SDK=Path(sdk_path)
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
 e=dict(os.environ,TMPDIR=str(ROOT/'tmp'))
 (ROOT/'tmp').mkdir(exist_ok=True)
 return e

def run(key,argv,limit=600,measured=False,env=None,memory_gib=None):
 global ACTIVE
 assert not any(str(x).startswith('-M') for x in argv)
 if measured:
  requested=json.loads(env.get('PARALLEL_ALLOWED_CPUS',json.dumps(list(range(8))))) if env else list(range(8))
  assert requested and sorted(os.sched_getaffinity(0))==requested
  assert set(requested)<=set(range(24))
 out=ROOT/'runs'/key;out.mkdir(parents=True,exist_ok=False)
 current=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split('::',1)[1].lstrip('/')
 assert current.name.startswith('cri-containerd-') and 'pod' in current.parent.name
 cg=current.parent/('proofserve-m-decl-'+str(os.getpid())+'-'+key+'.scope')
 meminfo={k:int(v.split()[0])*1024 for k,v in (line.split(':',1)for line in Path('/proc/meminfo').read_text().splitlines())}
 reserve=8*1024**3
 if meminfo['MemAvailable']<=reserve+256*1024**2:raise RuntimeError('host reserve unavailable before native launch')
 budget=meminfo['MemAvailable']-reserve-256*1024**2
 if memory_gib is not None:budget=min(budget,int(memory_gib*1024**3))
 cg.mkdir();(cg/'memory.max').write_text(str(budget));(cg/'memory.oom.group').write_text('1')
 cmd=['timeout','--signal=TERM','--kill-after=5',str(limit)]+list(map(str,argv))
 record=dict(key=key,argv=cmd,affinity=sorted(os.sched_getaffinity(0)),measured=measured,
  wall_limit_s=limit,own_rss_sample_stop_gib=budget/1024**3,cgroup=str(cg),cgroup_charged_memory_max_gib=budget/1024**3,host_available_stop_gib=8,evaluation_status=(env or {}).get('PROOFSERVE_BENCH_CLASSIFICATION','unclassified'))
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
    fs=os.statvfs(ROOT)
    if 1-fs.f_bavail/fs.f_blocks>=.85:
     stops.append('disk85_budget')
     try:(cg/'cgroup.kill').write_text('1')
     except OSError:pass
     break
    available=int(next(l.split()[1]for l in Path('/proc/meminfo').read_text().splitlines()if l.startswith('MemAvailable:')))*1024
    if available<reserve:
     stops.append('host_available_below_8GiB')
     try:(cg/'cgroup.kill').write_text('1')
     except OSError:pass
     break
    if total>budget:
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
   try:
    _,status,ru=os.wait4(p.pid,0);reaped=True;p.returncode=os.waitstatus_to_exitcode(status)
    record.update(returncode=p.returncode,wall_s=time.monotonic()-begin,user_s=ru.ru_utime,
     system_s=ru.ru_stime,peak_rss_kib=ru.ru_maxrss,native_retired=not Path(f'/proc/{p.pid}').exists())
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
