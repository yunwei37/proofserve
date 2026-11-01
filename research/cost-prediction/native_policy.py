#!/usr/bin/env python3
"""One bounded native policy comparison; P-core shared lock required."""
import os,sys,json,time,signal,subprocess,resource,math
from pathlib import Path
ROOT=Path(__file__).parent
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
def main():
 global ACTIVE
 assert sorted(os.sched_getaffinity(0))==list(range(8))
 plan=json.loads((ROOT/'plan.json').read_text());B=float(plan['cpu_budget_s']);jobs=plan['candidates']
 env=os.environ.copy();env.update(PATH=str(SDK/'bin')+':'+env['PATH'],LEAN_SYSROOT=str(SDK),LEAN_NUM_THREADS='8',TMPDIR=str(ROOT/'tmp'))
 (ROOT/'tmp').mkdir(exist_ok=True)
 prep=json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/repair-v3/preparation.json').read_text())
 paths=[Path('/workspaces/.agent-state/gpu-smt-workloads/openai4341-oleans'),Path('/workspaces/.agent-state/gpu-smt-workloads/rellich4341-oleans')]
 paths += [Path(p)for p in prep['lean_path'].split(':')if'/repair-v3/oleans'not in p]
 env['LEAN_PATH']=':'.join(map(str,paths));env.pop('DECOUPLED_TIMING',None)
 allrows=[];summaries=[];setup_failure=None
 for policy in plan['policies']:
  order=jobs if policy=='fifo'else sorted(jobs,key=lambda r:r['point'])
  used=0.;completed=[];deferred=[];interrupts=0;parent0=resource.getrusage(resource.RUSAGE_SELF);begin=time.monotonic()
  for i,job in enumerate(order):
   parent=resource.getrusage(resource.RUSAGE_SELF);parentcpu=parent.ru_utime+parent.ru_stime-parent0.ru_utime-parent0.ru_stime
   remaining=B-used-parentcpu
   if remaining<1 or(policy=='upper_admission'and job['upper']>remaining):
    deferred.append(job['module']);continue
   directory=ROOT/policy/str(i).zfill(2);directory.mkdir(parents=True)
   source=Path(job['source']);source_root=source.parents[len(job['module'].split('.'))-1]
   file=directory/source.stem
   args=['timeout','--signal=TERM','--kill-after=5','300',str(SDK/'bin/lean'),'--root='+str(source_root),'-j8','-DautoImplicit=false',
    '-o',str(file)+'.olean','-i',str(file)+'.ilean','-c',str(file)+'.c',str(source)]
   current=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split('::',1)[1].lstrip('/')
   assert current.name.startswith('cri-containerd-')and'pod'in current.parent.name
   cg=current.parent/('proofserve-cost-'+str(os.getpid())+'-'+policy+'-'+str(i)+'.scope')
   cg.mkdir();(cg/'memory.max').write_text(str(12*1024**3-512*1024**2));(cg/'memory.oom.group').write_text('1')
   seconds=max(1,math.floor(remaining))
   def enter():
    (cg/'cgroup.procs').write_text('0')
    resource.setrlimit(resource.RLIMIT_CPU,(seconds,seconds+1))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
   (directory/'command.json').write_text(json.dumps(dict(module=job['module'],args=args,remaining_cpu_s=remaining,
    RLIMIT_CPU_soft_s=seconds,affinity=sorted(os.sched_getaffinity(0)),cgroup=str(cg),memory_max_bytes=12*1024**3-512*1024**2),indent=2))
   with(directory/'stdout').open('w')as fo,(directory/'stderr').open('w')as fe:
    start=time.monotonic();proc=subprocess.Popen(args,env=env,cwd=source_root,stdout=fo,stderr=fe,preexec_fn=enter,start_new_session=True)
    ACTIVE=(cg,proc.pid)
    _,status,usage=os.wait4(proc.pid,0);proc.returncode=os.waitstatus_to_exitcode(status);ACTIVE=None
   cpu=usage.ru_utime+usage.ru_stime;used+=cpu
   text=(directory/'stdout').read_text(errors='replace')+(directory/'stderr').read_text(errors='replace')
   accepted=proc.returncode==0 and"declaration uses 'sorry'"not in text
   me=(cg/'memory.events').read_text()
   interrupted=proc.returncode in[-24,152,-9,137,124,-15,143]or'oom_kill 1'in me
   row=dict(policy=policy,module=job['module'],returncode=proc.returncode,accepted=accepted,
    cpu_s=cpu,wall_s=time.monotonic()-start,peak_rss_kib=usage.ru_maxrss,resource_interruption=interrupted,
    predicted_cpu_s=job['point'],upper_cpu_s=job['upper'],definite_upper_miss=cpu>job['upper'],
    cgroup_memory_events=me,cgroup_peak_bytes=int((cg/'memory.peak').read_text()))
   (directory/'result.json').write_text(json.dumps(row,indent=2));allrows.append(row)
   try:cg.rmdir()
   except OSError:pass
   if accepted:completed.append(job['module'])
   if interrupted:interrupts+=1
   if'object file'in text and'does not exist'in text:
    setup_failure=job['module'];break
   with(ROOT/'native-results.jsonl').open('a')as out:out.write(json.dumps(row)+'\n');out.flush();os.fsync(out.fileno())
  parent=resource.getrusage(resource.RUSAGE_SELF);parentcpu=parent.ru_utime+parent.ru_stime-parent0.ru_utime-parent0.ru_stime
  summaries.append(dict(policy=policy,cpu_budget_s=B,child_cpu_s=used,parent_cpu_s=parentcpu,actual_total_cpu_s=used+parentcpu,
   budget_overshoot_s=max(0,used+parentcpu-B),wall_s=time.monotonic()-begin,completed=len(completed),completed_ids=completed,
   deferred=len(deferred),deferred_ids=deferred,resource_interruptions=interrupts,pass_at_1_subset=len(completed)/len(jobs),
   pass_at_k_gt_1='not identifiable: one reference proof per module',goodput_per_allocated_cpu_hour=len(completed)/B*3600,
   interval_definite_misses=sum(r['definite_upper_miss']for r in allrows if r['policy']==policy),
   scope='native fresh source compiles using precomputed heldout forecasts; not full online feature-extraction/production service'))
  (ROOT/'policy-summary.json').write_text(json.dumps(summaries,indent=2))
  if setup_failure:break
 (ROOT/'terminal.json').write_text(json.dumps(dict(status='setup_failure'if setup_failure else'complete',setup_failure=setup_failure,
  policies_completed=len(summaries),native_calls=len(allrows),scope='separate12GiB/j8/noM native point; CPU limits approximate to OS accounting quantum'),indent=2))
if __name__=='__main__':main()
