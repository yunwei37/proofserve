#!/usr/bin/env python3
"""Append-only native Lean compilation census. Linux, Python standard library."""
import argparse
import collections
import csv
import ctypes
import fcntl
import datetime
import gzip
import heapq
import json
import os
from pathlib import Path
import resource
import selectors
import shutil
import signal
import sys
import time

PIN = "4eaee87548250b2682affda7d05d947c05554bae"
MATHLIB = "d13f23b723b8a846827a245b89c10fc7d3f11612"
COLUMNS = ["module", "attempt", "status", "returncode", "user_cpu_s",
           "system_cpu_s", "wall_s", "peak_rss_kib", "cpu_class", "affinity",
           "lean_threads", "source_bytes", "artifact_bytes", "launch_wall_s",
           "source_revision", "run", "log"]

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def append(path, row):
    data = (json.dumps(row, separators=(",", ":"))+"\n").encode()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        view = memoryview(data)
        while view:
            n = os.write(fd, view)
            view = view[n:]
        os.fsync(fd)
    finally:
        os.close(fd)

def records(path):
    """Keep damaged bytes; only complete valid result lines may resume work."""
    if not path.exists():
        return []
    out = []
    with path.open("rb") as f:
        for line in f:
            if not line.endswith(b"\n"):
                continue
            try:
                r = json.loads(line)
            except (ValueError, UnicodeDecodeError):
                continue
            if r.get("record") == "result":
                out.append(r)
    return out

def prepare(a):
    base = a.inventory
    with gzip.open(base/"content/file-metrics.csv.gz", "rt") as f:
        profiles = list(csv.DictReader(f))
    roots = json.loads((base/"content/summary.json").read_text())["import_graph"]["source_roots"]
    modules = {}
    old_names = {}
    for p in profiles:
        rel = p["path"]
        root = max((r for r in roots if rel.startswith(r+"/")), key=len)
        name = Path(rel).relative_to(root).with_suffix("").as_posix().replace("/", ".")
        old_name = name
        # The pinned Lake custom facet reroots only HodgeConjecture.*.
        # CM, Challenge and Solution keep their ComparatorChallenges names.
        nested = "lean/ComparatorChallenges/HodgeConjectureCMAbelianVarieties"
        if root == nested and not name.startswith("HodgeConjecture."):
            root = "lean"
            name = Path(rel).relative_to(root).with_suffix("").as_posix().replace("/", ".")
        old_names[old_name] = name
        modules[name] = dict(module=name, source=str((a.source/rel).resolve()),
                             root=str((a.source/root).resolve()), bytes=int(p["bytes"]), deps=[])
    external = collections.defaultdict(set)
    with gzip.open(base/"content/imports.csv.gz", "rt") as f:
        for edge in csv.DictReader(f):
            owner = old_names[edge["module"]]
            if edge["imports"] in modules:
                modules[owner]["deps"].append(edge["imports"])
            else:
                external[owner].add(edge["imports"])
    for name, row in modules.items():
        row["deps"] = sorted(set(row["deps"]))
        row["external"] = sorted(external[name])
    assert len(modules) == 163097, "pinned universe differs; do not silently narrow it"
    template = json.loads(a.template.read_text())["cases"][0]
    env = dict(template["env"])
    env.pop("LEAN_NUM_THREADS", None)
    value = dict(source_revision=PIN, mathlib=MATHLIB, lean="4.34.1",
                 lean_binary=template["args"][0], env=env,
                 lean_options=["-DautoImplicit=false"],
                 root_policy="pinned Lake comparatorSourceModules: only HodgeConjecture.* is rerooted; other nested files retain ComparatorChallenges namespace",
                 modules=list(modules.values()))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(value, separators=(",", ":"))+"\n")
    print(json.dumps(dict(modules=len(modules), external_names=len(set().union(*external.values())),
                          source_files_present=sum(Path(x["source"]).is_file() for x in modules.values()),
                          manifest=str(a.out), native_started=False)))

def export(out):
    rows = records(out/"records.jsonl")
    with gzip.open(out/"module-costs.csv.gz", "wt", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return rows

def run(a):
    call_started=time.monotonic()
    call_usage=resource.getrusage(resource.RUSAGE_SELF)
    manifest = json.loads(a.manifest.read_text())
    if manifest["source_revision"] != PIN or manifest["mathlib"] != MATHLIB or manifest["lean"] != "4.34.1":
        raise ValueError("this census protocol is for the documented pinned corpus")
    cpus = {int(x) for x in a.cpus.split(",")}
    if not cpus or not cpus <= os.sched_getaffinity(0):
        raise ValueError("CPU affinity is unavailable")
    if a.workers < 1 or a.threads < 1:
        raise ValueError("positive explicit worker/thread counts required")
    if cpus <= set(range(8,24)):
        cpu_class = "E"
    elif cpus <= set(range(8)):
        cpu_class = "P"
        raise ValueError("the currently authorized census pilot is E-only; P work uses the existing protocol")
    else:
        raise ValueError("do not mix P/E CPU clocks")
    out = a.out.resolve()
    workspaces = Path("/workspaces")
    if not workspaces.is_mount() or not out.is_relative_to(workspaces):
        raise ValueError("census output must be on the existing /workspaces PVC")
    out.mkdir(parents=True, exist_ok=True)
    if out.stat().st_dev != workspaces.stat().st_dev:
        raise ValueError("census output is on a nested different device")
    os.sched_setaffinity(0, cpus)
    all_modules = {r["module"]:r for r in manifest["modules"]}
    selected = set(a.targets.read_text().split()) if a.targets else set(all_modules)
    if not selected or not selected <= set(all_modules):
        raise ValueError("target list is empty or contains unknown modules")
    identity = dict(source_revision=PIN, mathlib=MATHLIB, lean=manifest["lean"],
                    lean_binary=manifest["lean_binary"], cpus=sorted(cpus),
                    workers=a.workers, threads=a.threads, target_modules=sorted(selected),
                    memory_gib=a.memory_gib, wall_limit_s=a.wall_limit_s,
                    external_lean_path=manifest["env"]["LEAN_PATH"], no_M=True,
                    compiler_options=manifest["lean_options"], account_roots=a.account_root)
    owner_lock = (out/"controller.lock").open("a")
    fcntl.flock(owner_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    config = out/"run-config.json"
    if config.exists() and json.loads(config.read_text()) != identity:
        raise ValueError("resume configuration changed; use a separate run directory")
    config.write_text(json.dumps(identity, indent=2)+"\n")
    ledger = out/"records.jsonl"
    if ledger.exists() and ledger.stat().st_size:
        with ledger.open("rb") as f:
            f.seek(-1, os.SEEK_END)
            broken = f.read(1) != b"\n"
        if broken:
            with ledger.open("ab") as f:
                f.write(b"\n");f.flush();os.fsync(f.fileno())
            append(out/"lifecycle.jsonl", dict(utc=utc(), event="partial_tail_preserved"))
    # Lean resolves a namespace at the first search directory containing it,
    # rather than falling back per missing leaf. A target-only pilot therefore
    # needs read-only prerequisite links within its output namespace. The full
    # census has no such seeds: each internal predecessor must be built here.
    if a.targets:
        closure=set(selected)
        todo=list(selected)
        while todo:
            name=todo.pop()
            for dep in all_modules[name]["deps"]:
                if dep not in closure:
                    closure.add(dep);todo.append(dep)
        search=[Path(p) for p in manifest["env"]["LEAN_PATH"].split(":") if p]
        linked=0
        for name in sorted(closure-selected):
            relative=Path(*name.split(".")).with_suffix(".olean")
            base=next((p/relative for p in search if (p/relative).is_file()),None)
            if base is None:
                raise ValueError("pilot prerequisite cache missing: "+name)
            target=out/"artifacts"/relative
            target.parent.mkdir(parents=True,exist_ok=True)
            for source in base.parent.glob(base.name+"*"):
                dest=target.parent/source.name
                if not dest.exists():
                    dest.symlink_to(source.resolve());linked+=1
        (out/"seeded-prerequisites.json").write_text(json.dumps(dict(
            modules=len(closure-selected),linked_files=linked,
            scope="pilot-only read-only prerequisite links, never selected output files"))+"\n")
    past = records(ledger)
    lifecycle = out/"lifecycle.jsonl"
    starts = []
    if lifecycle.exists():
        for line in lifecycle.read_text().splitlines():
            try:
                item = json.loads(line)
            except ValueError:
                continue
            if item.get("event") == "native_started":
                starts.append(item)
    returned = {(r["module"],r["attempt"]) for r in past}
    for item in starts:
        if (item["module"],item["attempt"]) in returned:
            continue
        stat = Path("/proc",str(item["pid"]),"stat")
        st = stat.read_text().rsplit(")",1)[1].split() if stat.exists() else None
        if st and st[0] != "Z" and st[19] == item["birth_ticks"]:
            raise ValueError("previous native process still alive; do not duplicate it")
        row = dict(record="result",utc=utc(),module=item["module"],attempt=item["attempt"],
                   status="interrupted_unknown_cost",returncode=None,user_cpu_s="",system_cpu_s="",
                   wall_s="",peak_rss_kib="",cpu_class=cpu_class,affinity=a.cpus,
                   lean_threads=a.threads,source_bytes=all_modules[item["module"]]["bytes"],
                   artifact_bytes="",launch_wall_s="",source_revision=PIN,run=out.name,log="",
                   products=[],source_stat=[],native_retired=True)
        append(ledger,row);past.append(row)
    last = {r["module"]:r for r in past}
    completed = set()
    for name, r in last.items():
        if r["status"] == "completed" and all((out/p).is_file() for p in r["products"]):
            row = all_modules[name]
            st = Path(row["source"]).stat()
            if [st.st_size, st.st_mtime_ns] != r["source_stat"]:
                raise ValueError("previously completed source changed: "+name)
            completed.add(name)
    attempted = {name for name,r in last.items() if r["status"] != "interrupted_unknown_cost"}
    for name,r in last.items():
        if r["status"] == "completed" and name not in completed:
            raise ValueError("completed products missing: "+name)
    pending = selected-completed-attempted
    failed = attempted-completed
    reverse = collections.defaultdict(list)
    remaining = {}
    for name in pending:
        ds = set(all_modules[name]["deps"]) & selected
        remaining[name] = len(ds-completed)
        for dep in ds:
            reverse[dep].append(name)
    ready = [name for name,n in remaining.items() if not n]
    heapq.heapify(ready)
    current = Path("/sys/fs/cgroup")/Path("/proc/self/cgroup").read_text().strip().split("::",1)[1].lstrip("/")
    previous_path=out/"cgroup-path.txt"
    if previous_path.exists():
        old=Path(previous_path.read_text().strip())
        if old.exists():
            if old.parent != current.parent or not old.name.startswith("proofserve-W-census-"):
                raise ValueError("unexpected recorded cgroup path")
            for child in old.iterdir():
                if child.is_dir():
                    if (child/"cgroup.procs").read_text().strip():
                        raise ValueError("previous cgroup still populated")
                    child.rmdir()
            if (old/"cgroup.procs").read_text().strip():
                raise ValueError("previous cgroup still populated")
            old.rmdir()
    group = current.parent/("proofserve-W-census-"+str(os.getpid())+".scope")
    group.mkdir()
    (out/"cgroup-path.txt").write_text(str(group)+"\n")
    (group/"memory.max").write_text(str(int((a.memory_gib-1)*1024**3)))
    (group/"cgroup.subtree_control").write_text("+memory")
    sel = selectors.DefaultSelector()
    live = {}
    attempts = collections.Counter()
    for r in past:attempts[r["module"]]=max(attempts[r["module"]],r["attempt"])
    start = time.monotonic()
    driver_before = resource.getrusage(resource.RUSAGE_SELF)
    stop = None
    peak_owned_rss = 0
    next_sample = 0.
    def additional_owned_rss():
        roots=set()
        for identity in a.account_root:
            pid,birth=identity.split(":",1)
            p=Path("/proc",pid,"stat")
            if p.exists() and p.read_text().rsplit(")",1)[1].split()[19]==birth:
                roots.add(int(pid))
        parents={}
        if roots:
            for p in Path("/proc").iterdir():
                if p.name.isdigit():
                    try:parents[int(p.name)]=int((p/"stat").read_text().rsplit(")",1)[1].split()[1])
                    except (FileNotFoundError,ProcessLookupError):pass
            while True:
                expanded=roots|{pid for pid,pp in parents.items() if pp in roots}
                if expanded==roots:break
                roots=expanded
        total=0
        native=[]
        for pid in roots-set(live):
            try:
                proc=Path("/proc",str(pid))
                total+=int((proc/"statm").read_text().split()[1])*os.sysconf("SC_PAGE_SIZE")
                argv=(proc/"cmdline").read_bytes().split(b"\0")
                if argv and Path(os.fsdecode(argv[0])).name=="lean":native.append(pid)
            except (FileNotFoundError,ProcessLookupError):pass
        return total,native
    def launch(name):
        row = all_modules[name]
        source = Path(row["source"])
        st = source.stat()
        if st.st_size != row["bytes"]:
            raise ValueError("source size differs from pinned inventory: "+name)
        if set(row["deps"]) & selected - completed:
            raise ValueError("internal dependency scheduled before a durable completion")
        attempt = attempts[name]+1
        attempts[name] = attempt
        number = len(past)+len(live)+1
        job = out/"attempts"/(str(number).zfill(7)+"-"+str(attempt))
        while job.exists():
            number += 1
            job = out/"attempts"/(str(number).zfill(7)+"-"+str(attempt))
        job.mkdir(parents=True)
        rel = Path(*name.split("."))
        obj = out/"artifacts"/rel.with_suffix(".olean")
        ilean = out/"artifacts"/rel.with_suffix(".ilean")
        cfile = out/"ir"/rel.with_suffix(".c")
        obj.parent.mkdir(parents=True, exist_ok=True)
        cfile.parent.mkdir(parents=True, exist_ok=True)
        previous=list(obj.parent.glob(obj.name+"*"))+[ilean,cfile]
        for product in previous:
            if product.exists():
                prior=job/"prior-products";prior.mkdir(exist_ok=True)
                product.rename(prior/product.name)
        args = [manifest["lean_binary"], "--root="+row["root"], "-j"+str(a.threads),
                *manifest["lean_options"], "-o",str(obj),"-i",str(ilean),"-c",str(cfile),str(source)]
        env = dict(os.environ)
        for k in ["GLIBC_TUNABLES","LD_PRELOAD","LEAN_NUM_THREADS"]:
            env.pop(k,None)
        env.update(manifest["env"])
        env.update(LEAN_NUM_THREADS=str(a.threads),TMPDIR=str(out/"tmp"),
                   LEAN_PATH=str(out/"artifacts")+":"+manifest["env"]["LEAN_PATH"])
        (out/"tmp").mkdir(exist_ok=True)
        childgroup = group/str(number)
        childgroup.mkdir()
        begin = time.monotonic()
        readfd, writefd = os.pipe()
        log = job/"native.log"
        parent_pid = os.getpid()
        pid = os.fork()
        if pid == 0:
            try:
                if os.getppid() != parent_pid:
                    os._exit(125)
                if ctypes.CDLL(None).prctl(1,signal.SIGKILL,0,0,0) != 0:
                    raise OSError("cannot attach parent-death signal")
                if os.getppid() != parent_pid:
                    os._exit(125)
                os.close(readfd)
                os.sched_setaffinity(0,cpus)
                (childgroup/"cgroup.procs").write_text(str(os.getpid()))
                fd = os.open(log,os.O_WRONLY|os.O_CREAT,0o644)
                os.dup2(fd,1);os.dup2(fd,2);os.close(fd)
                if a.wall_limit_s:
                    signal.setitimer(signal.ITIMER_REAL,a.wall_limit_s)
                os.write(writefd,str(time.monotonic()).encode())
                os.close(writefd)
                os.execvpe(args[0],args,env)
            except BaseException as error:
                print(repr(error),file=sys.stderr,flush=True)
                os._exit(127)
        os.close(writefd)
        ready_clock = os.read(readfd,128)
        os.close(readfd)
        handle = os.pidfd_open(pid)
        sel.register(handle,selectors.EVENT_READ,pid)
        live[pid] = dict(module=name,attempt=attempt,pid=pid,handle=handle,group=childgroup,
                         begin=begin,job=job,source_stat=[st.st_size,st.st_mtime_ns],
                         launch_wall_s=float(ready_clock)-begin if ready_clock else "",
                         resource_killed=False)
        (job/"command.json").write_text(json.dumps(dict(args=args,env=env,
            source_revision=PIN,affinity=sorted(cpus)),indent=2)+"\n")
        append(out/"lifecycle.jsonl",dict(utc=utc(),event="native_started",pid=pid,
            birth_ticks=Path("/proc",str(pid),"stat").read_text().rsplit(")",1)[1].split()[19],
            module=name,attempt=attempt))
    try:
        while ready or live:
            _,other_native=additional_owned_rss()
            while ready and len(live)<a.workers and not stop and not other_native:
                usage=shutil.disk_usage(out)
                if usage.used/usage.total>=.85:
                    stop="disk_85_percent";break
                name=heapq.heappop(ready)
                launch(name)
            now=time.monotonic()
            if now>=next_sample:
                own=int(Path("/proc/self/statm").read_text().split()[1])*os.sysconf("SC_PAGE_SIZE")
                rss={}
                for pid,job in live.items():
                    rss[pid]=0
                    for member in (job["group"]/"cgroup.procs").read_text().split():
                        try:rss[pid]+=int(Path("/proc",member,"statm").read_text().split()[1])*os.sysconf("SC_PAGE_SIZE")
                        except FileNotFoundError:pass
                additional,_=additional_owned_rss()
                total=own+sum(rss.values())+additional
                peak_owned_rss=max(peak_owned_rss,total)
                if total>a.memory_gib*1024**3 and rss:
                    victim=max(rss,key=rss.get)
                    live[victim]["resource_killed"]=True
                    (live[victim]["group"]/"cgroup.kill").write_text("1")
                append(out/"memory.jsonl",dict(utc=utc(),rss=rss,parent_RSS=own,
                    total_RSS=total,additional_owned_RSS=additional,charged_memory=int((group/"memory.current").read_text())))
                next_sample=now+1
            if not live:
                if ready and other_native and not stop:
                    # Preserve the already-running precision collection; do not
                    # start another job while one of its Lean leaves is active.
                    try:
                        handle=os.pidfd_open(other_native[0])
                    except ProcessLookupError:
                        continue
                    wait=selectors.DefaultSelector()
                    wait.register(handle,selectors.EVENT_READ)
                    wait.select(1)
                    wait.close();os.close(handle)
                    continue
                break
            for key,_ in sel.select(max(0,min(1,next_sample-time.monotonic()))):
                pid=key.data
                r=live.pop(pid)
                _,status,usage=os.wait4(pid,0)
                ended=time.monotonic()
                sel.unregister(r["handle"]);os.close(r["handle"])
                rc=os.waitstatus_to_exitcode(status)
                events=dict(x.split() for x in(r["group"]/"memory.events").read_text().splitlines())
                charged=int((r["group"]/"memory.peak").read_text())
                leftover=bool((r["group"]/"cgroup.procs").read_text().strip())
                if leftover:
                    (r["group"]/"cgroup.kill").write_text("1")
                    deadline=time.monotonic()+5
                    while (r["group"]/"cgroup.procs").read_text().strip():
                        if time.monotonic()>deadline:
                            raise RuntimeError("own descendants failed to retire; retain the cgroup evidence")
                        time.sleep(.01)
                r["group"].rmdir()
                products=list((out/"artifacts").joinpath(*r["module"].split(".")).parent.glob(
                    r["module"].split(".")[-1]+".olean*"))
                stem=out/"artifacts"/Path(*r["module"].split("."))
                ilean=stem.with_suffix(".ilean")
                cfile=out/"ir"/Path(*r["module"].split(".")).with_suffix(".c")
                ok=rc==0 and not leftover and bool(products) and ilean.is_file() and cfile.is_file()
                if ok:products += [ilean,cfile]
                result=dict(record="result",utc=utc(),module=r["module"],attempt=r["attempt"],
                    status="completed" if ok else "resource_failure" if r["resource_killed"] or int(events["oom_kill"])
                        else "descendants_not_retired" if leftover
                        else "wall_budget_censor" if rc==-signal.SIGALRM else "native_failure",
                    returncode=rc,user_cpu_s=usage.ru_utime,system_cpu_s=usage.ru_stime,
                    wall_s=ended-r["begin"],peak_rss_kib=usage.ru_maxrss,cpu_class=cpu_class,
                    affinity=",".join(map(str,sorted(cpus))),lean_threads=a.threads,
                    source_bytes=all_modules[r["module"]]["bytes"],
                    artifact_bytes=sum(p.stat().st_size for p in products),
                    launch_wall_s=r["launch_wall_s"],source_revision=PIN,
                    run=out.name,log=str((r["job"]/"native.log").relative_to(out)),
                    products=[str(p.relative_to(out)) for p in products],
                    source_stat=r["source_stat"],cgroup_memory_events=events,
                    cleanup_killed_leftover_descendants=leftover,
                    cgroup_charged_peak_bytes=charged,native_retired=True,cgroup_retired=True)
                append(ledger,result);past.append(result)
                # Direct lean does not create Lake setup lists. Remove only our own
                # finished job's transient setup lists, never another job's inputs.
                for p in r["job"].glob("*.setup.json"):
                    p.unlink()
                if ok:
                    completed.add(r["module"])
                    for child in reverse[r["module"]]:
                        remaining[child]-=1
                        if remaining[child]==0:heapq.heappush(ready,child)
                else:
                    failed.add(r["module"])
            if stop and not live:
                break
    finally:
        for pid,r in live.items():
            (r["group"]/"cgroup.kill").write_text("1")
            os.wait4(pid,0)
            if r["group"].exists():r["group"].rmdir()
        sel.close()
        group.rmdir()
        export(out)
    driver_after=resource.getrusage(resource.RUSAGE_SELF)
    terminal=dict(utc=utc(),selected_modules=len(selected),completed=len(completed),
        failed=len(failed),unreached=len(selected-completed-failed),stop=stop,
        all_selected_returned=len(completed|failed)==len(selected),
        elapsed_s=time.monotonic()-start,setup_wall_s=start-call_started,
        invocation_wall_s=time.monotonic()-call_started,
        driver_total_user_cpu_s=driver_after.ru_utime-call_usage.ru_utime,
        driver_total_system_cpu_s=driver_after.ru_stime-call_usage.ru_stime,
        driver_user_cpu_s=driver_after.ru_utime-driver_before.ru_utime,
        driver_system_cpu_s=driver_after.ru_stime-driver_before.ru_stime,
        peak_owned_sampled_RSS_bytes=peak_owned_rss,no_M=True,full_census=not bool(a.targets),
        scope="direct Lean compilation with olean/ilean/C emission; not C linking or independent replay")
    (out/"terminal.json").write_text(json.dumps(terminal,indent=2)+"\n")
    print(json.dumps(terminal),flush=True)
    return 0 if len(completed)==len(selected) else 2

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    subs=ap.add_subparsers(dest="command",required=True)
    p=subs.add_parser("prepare")
    for name in ["inventory","source","template","out"]:p.add_argument("--"+name,type=Path,required=True)
    p=subs.add_parser("run")
    for name in ["manifest","out"]:p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--targets",type=Path)
    p.add_argument("--cpus",required=True)
    p.add_argument("--workers",type=int,default=1)
    p.add_argument("--threads",type=int,default=1)
    p.add_argument("--memory-gib",type=float,default=16)
    p.add_argument("--wall-limit-s",type=float)
    p.add_argument("--account-root",action="append",default=[],metavar="PID:BIRTH",
                   help="also count this existing owned tree; only this new run may be killed")
    a=ap.parse_args()
    if a.command=="prepare":prepare(a);return 0
    if not(1<a.memory_gib<=16):ap.error("W aggregate budget must be at most16GiB")
    return run(a)
if __name__=="__main__":
    raise SystemExit(main())
