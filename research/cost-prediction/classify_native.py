#!/usr/bin/env python3
"""Finite nine-cell checker-routing experiment, held shared P-core lock."""
import os,json,time,subprocess,resource,signal,threading,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ACTIVE=None
def abort(sig,frame):
 if ACTIVE:
  try:(ACTIVE/'cgroup.kill').write_text('1')
  except OSError:pass
 raise SystemExit(128+sig)
signal.signal(signal.SIGTERM,abort)
signal.signal(signal.SIGINT,abort)
def main():
 global ACTIVE
 assert sorted(os.sched_getaffinity(0))==list(range(8))
 plan=json.loads((ROOT/'plan.json').read_text())
 env=dict(os.environ,LEAN_PATH=plan['lean_path'],LEAN_SYSROOT=plan['sysroot'],LEAN_NUM_THREADS='8',TMPDIR=str(ROOT/'tmp'))
 (ROOT/'tmp').mkdir(exist_ok=True)
 for option in ['PARALLEL_CURVE_MODULES','PARALLEL_CHUNK_ASSETS','PARALLEL_CHUNK_ASSETS_CURVE','DECOUPLED_MEMORY_PROFILE','DECOUPLED_TIMING']:
  env.pop(option,None)
 summaries=[]
 for repeat in range(3):
  order=plan['jobs'][repeat:]+plan['jobs'][:repeat]
  policies=plan['policies'][repeat:]+plan['policies'][:repeat]
  for policy in policies:
   key=f'r{repeat}-{policy}';begin=time.monotonic()
   parent0=resource.getrusage(resource.RUSAGE_SELF)
   used=0.;wasted=0.;done=[];deferred=[];interrupted=[];calls=[];failure=None
   for job in order:
    ru=resource.getrusage(resource.RUSAGE_SELF)
    parent=ru.ru_utime+ru.ru_stime-parent0.ru_utime-parent0.ru_stime
    remaining=plan['budget_cpu_s']-used-parent
    route='serial' if policy=='fifo' or job['class']=='ordinary' else 'parallel4'
    upper=plan['type_upper_cpu_s'][job['class']]
    if remaining<1 or(policy=='upper_admission' and upper>remaining):
     deferred.append(job['id']);continue
    out=ROOT/key/job['id'];out.mkdir(parents=True)
    binary=ROOT/('stream-check' if route=='serial' else 'parallel-stream')
    mode='stream' if route=='serial' else 'parallel'
    argv=['timeout','--signal=TERM','--kill-after=5','180',str(binary),mode,'none',job['module']]
    current=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split('::',1)[1].lstrip('/')
    assert current.name.startswith('cri-containerd-') and 'pod' in current.parent.name
    cg=current.parent/('proofserve-o-class-'+str(os.getpid())+'-'+key+'-'+job['id']+'.scope')
    cg.mkdir();(cg/'memory.max').write_text(str(plan['child_memory_bytes']));(cg/'memory.oom.group').write_text('1')
    seconds=max(1,math.floor(remaining))
    def enter():
     (cg/'cgroup.procs').write_text('0')
     resource.setrlimit(resource.RLIMIT_CPU,(seconds,seconds+1))
     resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    e=dict(env,PARALLEL_WORKERS='4' if route=='parallel4' else '1')
    command=dict(argv=argv,remaining_cpu_s=remaining,RLIMIT_CPU=[seconds,seconds+1],
     route=route,module=job['module'],affinity=sorted(os.sched_getaffinity(0)),
     cgroup=str(cg),memory_max_bytes=plan['child_memory_bytes'])
    (out/'command.json').write_text(json.dumps(command,indent=2))
    stop=threading.Event();samples=[];rsspeak=[0];reasons=[]
    def sample():
     with (out/'memory.jsonl').open('w') as fo:
      while not stop.is_set():
       members=[]
       try:pids=(cg/'cgroup.procs').read_text().split()
       except OSError:pids=[]
       for pid in pids:
        try:
         st=Path('/proc',pid,'stat').read_text().split(') ',1)[1].split()
         members.append(dict(pid=int(pid),birth=st[19],rss=int(st[21])*os.sysconf('SC_PAGE_SIZE')))
        except (OSError,ValueError,IndexError):pass
       rss=sum(m['rss']for m in members);rsspeak[0]=max(rsspeak[0],rss)
       fo.write(json.dumps(dict(rss=rss,members=members))+'\n');fo.flush()
       if rss>plan['child_memory_bytes']:
        reasons.append('sampled_RSS_stop')
        try:(cg/'cgroup.kill').write_text('1')
        except OSError:pass
        break
       stop.wait(1)
    with (out/'stdout').open('w') as fo,(out/'stderr').open('w') as fe:
     start=time.monotonic();proc=subprocess.Popen(argv,env=e,stdout=fo,stderr=fe,
      preexec_fn=enter,start_new_session=True)
     ACTIVE=cg;command['pid']=proc.pid
     command['birth']=Path('/proc',str(proc.pid),'stat').read_text().split(') ',1)[1].split()[19]
     (out/'command.json').write_text(json.dumps(command,indent=2))
     thread=threading.Thread(target=sample,daemon=True);thread.start()
     _,status,usage=os.wait4(proc.pid,0)
     proc.returncode=os.waitstatus_to_exitcode(status)
     stop.set();thread.join(2);ACTIVE=None
    cpu=usage.ru_utime+usage.ru_stime;used+=cpu
    events=[]
    for line in (out/'stdout').read_text().splitlines():
     if line.startswith('{'):
      try:events.append(json.loads(line))
      except ValueError:pass
    completion=next((x for x in reversed(events)if x.get('event')=='complete'),None)
    accepted_ids=[x['module']for x in events if x.get('event')=='accept']
    accepted=proc.returncode==0 and completion is not None and job['module'] in accepted_ids
    mem=(cg/'memory.events').read_text()
    interrupt=proc.returncode in [-24,152,-9,137,124,-15,143] or bool(reasons) or 'oom_kill 1' in mem
    if accepted:
     assert len(accepted_ids)==job['modules'],(job['id'],len(accepted_ids))
     done.append(job['id'])
    elif interrupt:
     interrupted.append(job['id']);wasted+=cpu
    else:failure=job['id']
    result=dict(repeat=repeat,policy=policy,job=job['id'],module=job['module'],route=route,
     accepted=accepted,returncode=proc.returncode,cpu_s=cpu,wall_s=time.monotonic()-start,
     budget_interruption=interrupt,discarded_root_cpu_s=0 if accepted else cpu,
     accepted_dependency_count=len(accepted_ids),complete_event=completion,
     wait4_peak_rss_kib=usage.ru_maxrss,sampled_tree_peak_bytes=rsspeak[0],
     charged_peak_bytes=int((cg/'memory.peak').read_text()),memory_events=mem,stop_reasons=reasons,
     cpu_stat=(cg/'cpu.stat').read_text(),native_retired=not Path('/proc',str(proc.pid)).exists())
    (out/'result.json').write_text(json.dumps(result,indent=2))
    with (ROOT/'native-results.jsonl').open('a') as f:f.write(json.dumps(result)+'\n');f.flush();os.fsync(f.fileno())
    cg.rmdir();calls.append(result)
    if failure:break
   ru=resource.getrusage(resource.RUSAGE_SELF)
   parent=ru.ru_utime+ru.ru_stime-parent0.ru_utime-parent0.ru_stime
   summary=dict(repeat=repeat,policy=policy,arrival=[j['id']for j in order],
    budget_cpu_s=plan['budget_cpu_s'],child_cpu_s=used,parent_cpu_s=parent,
    total_cpu_s=used+parent,actual_budget_excess_cpu_s=max(0,used+parent-plan['budget_cpu_s']),
    wall_s=time.monotonic()-begin,completed=len(done),completed_ids=done,
    interruptions=len(interrupted),interrupted_ids=interrupted,deferred_ids=deferred,
    discarded_root_cpu_s=wasted,unused_budget_cpu_s=max(0,plan['budget_cpu_s']-used-parent),
    native_calls=len(calls),failure=failure,completion_fraction=len(done)/len(order),
    meaning='compiled full-closure roots; partial dependency accepts not completed root jobs')
   summaries.append(summary)
   (ROOT/'policy-summary.json').write_text(json.dumps(summaries,indent=2))
   print(json.dumps(summary),flush=True)
   if failure:raise RuntimeError('native semantic/setup failure retained: '+failure)
 (ROOT/'terminal.json').write_text(json.dumps(dict(status='complete',policy_cells=len(summaries),
  native_calls=sum(s['native_calls']for s in summaries),budget_s=plan['budget_cpu_s'],
  cpu_scope='wait4 child+parent charged; queue wait excluded; no-M; P0-7'),indent=2))
if __name__=='__main__':
 try:main()
 except BaseException as e:
  (ROOT/'terminal.json').write_text(json.dumps(dict(status='interrupted_or_failure',error=repr(e)),indent=2))
  raise
