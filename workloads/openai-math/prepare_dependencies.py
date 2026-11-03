#!/usr/bin/env python3
"""Untimed E-core dependency preparation; original targets are never compiled here."""
import argparse
import datetime
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import threading
import time

def dump(p, x):
    p.write_text(json.dumps(x, indent=2)+"\n")

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--point",type=Path,required=True)
    a=ap.parse_args()
    os.sched_setaffinity(0,set(range(8,16)))
    p=a.point
    plan=json.loads((p/"plan.json").read_text())
    ready=set(plan.get("initial_ready",[]))
    ledger=p/"preparation-results.jsonl"
    if ledger.exists():
        for line in ledger.read_text().splitlines():
            r=json.loads(line)
            if r["status"]=="compile_ok":
                assert all(Path(q).exists() for q in r["published"])
                ready.add(r["module"])
    started=time.monotonic()
    rows=[]
    stop=None
    for index,c in enumerate(plan["cases"]):
        if c["role"]=="original_probability_sample" or c["module"] in ready:
            continue
        remaining=1700-(time.monotonic()-started)
        if remaining<15:
            stop="finite preparation window exhausted; unstarted jobs retained"
            break
        blockers=sorted(set(c.get("deps",[]))-ready)
        if blockers:
            rows.append(dict(module=c["module"],status="dependency_not_ready",blockers=blockers))
            continue
        # No native elapsed/CPU measurement: only bounded execution and resource accounting.
        nominal=float(c["self_wall_s"])
        allowance=min(nominal,remaining-10)
        attemptroot=p/"preparation-attempts"
        attemptroot.mkdir(exist_ok=True)
        attempt=len(list(attemptroot.iterdir()))
        out=attemptroot/(str(attempt).zfill(5)+"-"+str(index))
        out.mkdir()
        source=Path(c["args"][-1])
        assert source.read_bytes()==Path(c["pinned_source"]).read_bytes()
        args=list(c["args"])
        assert not any(t.startswith("-M")for t in args)
        for flag in ["-o","-i","-c"]:
            if flag in args:
                k=args.index(flag)
                del args[k:k+2]
        objectfile=out/(source.stem+".olean")
        args[-1:-1]=["-o",str(objectfile)]
        current=Path("/sys/fs/cgroup")/Path("/proc/self/cgroup").read_text().strip().split("::",1)[1].lstrip("/")
        assert current.name.startswith("cri-containerd-") and "pod" in current.parent.name
        cg=current.parent/("proofserve-W-Eprep-"+str(os.getpid())+".scope")
        cg.mkdir()
        (cg/"memory.max").write_text(str(15*1024**3))
        env=os.environ.copy()
        for k in ["GLIBC_TUNABLES","LD_PRELOAD","LEAN_NUM_THREADS"]:
            env.pop(k,None)
        env.update(c["env"])
        done=threading.Event()
        samples=[]
        child=None
        def before_exec():
            (cg/"cgroup.procs").write_text(str(os.getpid()))
            signal.signal(signal.SIGALRM,signal.SIG_DFL)
            signal.setitimer(signal.ITIMER_REAL,allowance)
        def sample():
            with(out/"resources.jsonl").open("w")as f:
                while not done.is_set():
                    owned=[]
                    for pid in (cg/"cgroup.procs").read_text().split():
                        try:
                            rss=int(Path("/proc",pid,"statm").read_text().split()[1])*os.sysconf("SC_PAGE_SIZE")
                            owned.append(dict(pid=int(pid),rss_bytes=rss))
                        except FileNotFoundError:
                            pass
                    parent=int(Path("/proc/self/statm").read_text().split()[1])*os.sysconf("SC_PAGE_SIZE")
                    row=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),native=owned,parent_RSS=parent)
                    row["sampled_RSS_sum"]=parent+sum(x["rss_bytes"]for x in owned)
                    if row["sampled_RSS_sum"]>16*1024**3:
                        row["resource_kill"]=True
                        (cg/"cgroup.kill").write_text("1")
                    samples.append(row)
                    f.write(json.dumps(row)+"\n")
                    f.flush()
                    done.wait(1)
        dump(out/"command.json",dict(module=c["module"],args=args,env=c["env"],
             source=str(source),pinned_source=c["pinned_source"],source_exact=True,
             affinity=sorted(os.sched_getaffinity(0)),pcore_lock=False,
             operation="untimed_dependency_preparation",nominal_wall_budget_s=nominal,
             actual_wall_budget_s=allowance,cgroup=str(cg)))
        thread=threading.Thread(target=sample)
        try:
            with(out/"native.log").open("w")as f:
                child=subprocess.Popen(args,cwd=c["cwd"],env=env,stdout=f,
                    stderr=subprocess.STDOUT,preexec_fn=before_exec)
                birth=Path("/proc",str(child.pid),"stat").read_text().rsplit(")",1)[1].split()[19]
                dump(out/"native-identity.json",dict(pid=child.pid,birth_ticks=birth))
                thread.start()
                rc=child.wait()
            done.set()
            thread.join()
            text=(out/"native.log").read_text(errors="replace")
            events=dict(x.split()for x in(cg/"memory.events").read_text().splitlines())
            status=("resource_failure"if any(x.get("resource_kill")for x in samples)
                or int(events["oom_kill"]) else
                "group_remainder_censor"if rc==-signal.SIGALRM and allowance<nominal else
                "full_wall_budget_censor"if rc==-signal.SIGALRM else
                "native_process_failure"if rc<0 or "INTERNAL PANIC"in text else
                "resource_failure"if any(x in text.lower()for x in
                    ["memory_exception","excessive memory","bad_alloc","out of memory"])else
                "compile_with_sorry"if rc==0 and "declaration uses 'sorry'"in text else
                "compile_ok"if rc==0 and objectfile.exists() else
                "missing_artifact"if rc==0 else
                "native_budget_diagnostic"if any(x in text.lower()for x in
                    ["heartbeats","deterministic timeout","maximum recursion depth"])else"lean_or_setup_error")
            published=[]
            if status=="compile_ok":
                dest=Path(c["publish_cache"]).joinpath(*c["module"].split(".")).with_suffix(".olean")
                dest.parent.mkdir(parents=True,exist_ok=True)
                for obj in sorted(out.glob(source.stem+".olean*")):
                    tail=obj.name[len(source.stem+".olean"):]
                    target=Path(str(dest)+tail)
                    temporary=Path(str(target)+".W-Eprep")
                    shutil.copyfile(obj,temporary)
                    os.replace(temporary,target)
                    published.append(str(target))
                ready.add(c["module"])
            assert not(cg/"cgroup.procs").read_text().strip()
            r=dict(module=c["module"],status=status,operation="untimed_dependency_preparation",
                 original_probability_target=False,affinity=sorted(os.sched_getaffinity(0)),
                 pcore_lock=False,nominal_wall_budget_s=nominal,actual_wall_budget_s=allowance,
                 source_exact=True,native_pid=child.pid,native_birth_ticks=birth,
                 cgroup_memory_events=events,charged_memory_peak_bytes=int((cg/"memory.peak").read_text()),
                 resource_watchdog_fired=any(x.get("resource_kill")for x in samples),
                 native_retired=not Path("/proc",str(child.pid)).exists(),
                 sampled_RSS_peak_bytes=max((x["sampled_RSS_sum"]for x in samples),default=0),
                 published=published,raw=str(out),returncode=rc)
        finally:
            done.set()
            if thread.is_alive():
                thread.join()
            if(cg/"cgroup.procs").read_text().strip():
                (cg/"cgroup.kill").write_text("1")
                if child and child.poll()is None:
                    child.wait()
            assert not(cg/"cgroup.procs").read_text().strip()
            cg.rmdir()
        r["cgroup_retired"]=not cg.exists()
        dump(out/"result.json",r)
        with ledger.open("a")as f:
            f.write(json.dumps(r)+"\n")
        rows.append(r)
        if status!="compile_ok":
            stop="unfinished dependency; retain diagnostics and review allowance before continuing"
            break
    original=[c for c in plan["cases"]if c["role"]=="original_probability_sample"]
    missing={c["module"]:sorted(set(c.get("deps",[]))-ready)for c in original}
    result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        operation="untimed_dependency_preparation",new_rows=len(rows),stop=stop,
        original_dependency_blockers=missing,all_original_deps_ready=all(not ds for ds in missing.values()),
        no_population_cost_measurements=True,affinity=sorted(os.sched_getaffinity(0)))
    dump(p/"preparation-terminal.json",result)
    print(json.dumps(result),flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
