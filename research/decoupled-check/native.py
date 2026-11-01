"""Bounded experiment-native subprocesses; cgroups are children of this Workspace Pod."""
import json,os,subprocess,signal
from pathlib import Path
ROOT=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031')
SDK=Path('/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux')
def environment():
    old=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/repair-v3/preparation.json')
    e=os.environ.copy();e.update(PATH=str(SDK/'bin')+':'+e['PATH'],LEAN_SYSROOT=str(SDK),
        LEAN_PATH=json.loads(old.read_text())['lean_path'],LEAN_NUM_THREADS='8',TMPDIR=str(ROOT/'tmp'))
    (ROOT/'tmp').mkdir(exist_ok=True)
    e.pop('DECOUPLED_TIMING',None)
    return e
def run(key,command,limit=120,measured=False,env=None,cwd=None):
    affinity=sorted(os.sched_getaffinity(0))
    if measured:assert affinity==list(range(8)),'timed runs require P cores and outer shared flock'
    current=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split('::',1)[1].lstrip('/')
    assert current.name.startswith('cri-containerd-')and'pod'in current.parent.name
    cg=current.parent/('proofserve-decoupled-'+str(os.getpid())+'-'+key+'.scope')
    cg.mkdir();(cg/'memory.max').write_text(str(12*1024**3-128*1024**2));(cg/'memory.oom.group').write_text('1')
    args=['timeout','--signal=TERM','--kill-after=5',str(limit)]+list(map(str,command))
    record=dict(key=key,args=args,affinity=affinity,cgroup=str(cg),memory_max_bytes=int((cg/'memory.max').read_text()),measured=measured,limit_s=limit)
    (ROOT/(key+'.command.json')).write_text(json.dumps(record,indent=2))
    def enter():(cg/'cgroup.procs').write_text('0')
    chosen=environment()if env is None else env
    if measured:chosen=dict(chosen,DECOUPLED_TIMING='1')
    import time
    with(ROOT/(key+'.stdout')).open('w')as fo,(ROOT/(key+'.stderr')).open('w')as fe:
        begin=time.monotonic()if measured else None
        p=subprocess.Popen(args,cwd=cwd or ROOT,env=chosen,stdout=fo,stderr=fe,preexec_fn=enter,start_new_session=True)
        if measured:
            _,status,usage=os.wait4(p.pid,0);p.returncode=os.waitstatus_to_exitcode(status)
            record.update(wall_s=time.monotonic()-begin,user_s=usage.ru_utime,system_s=usage.ru_stime,peak_rss_kib=usage.ru_maxrss,minor_faults=usage.ru_minflt,major_faults=usage.ru_majflt)
        else:p.wait()
    record.update(returncode=p.returncode,cgroup_peak_bytes=int((cg/'memory.peak').read_text()),memory_events=(cg/'memory.events').read_text())
    (ROOT/(key+'.result.json')).write_text(json.dumps(record,indent=2))
    try:cg.rmdir()
    except OSError as err:record['cleanup_pending']=str(err);(ROOT/(key+'.result.json')).write_text(json.dumps(record,indent=2))
    print(json.dumps(record),flush=True)
    return record
