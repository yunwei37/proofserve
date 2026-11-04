#!/usr/bin/env python3
"""Prepare only by default. Native census requires --execute; never auto-launched."""
import argparse,collections,fcntl,hashlib,json,os,signal,sys,time,subprocess
from pathlib import Path
import census_gate as native
from census import append,utc,records
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def corpus_artifact(rel):
    return rel.parts[0].split(".")[0] in {"OAI","ComparatorChallenges","HodgeConjecture"}

def inventory_imports(paths,deadline=None):
    """First-file-hit inventory; later module companions must not fill earlier holes."""
    expected={};owners={};visited_files=0
    for value in paths:
        base=Path(value)
        if not base.is_dir():continue
        # Follow directory aliases just as filesystem lookup does; reject cycles.
        def visit(directory,ancestors):
            stat=directory.stat();key=(stat.st_dev,stat.st_ino)
            if key in ancestors:raise ValueError("cyclic import directory: "+str(directory))
            for src in sorted(directory.iterdir()):
                if deadline is not None and time.monotonic()>=deadline:raise TimeoutError("subset validation six-hour limit during import inventory")
                rel=src.relative_to(base)
                if corpus_artifact(rel):continue
                if src.is_dir():yield from visit(src,ancestors|{key})
                elif src.is_file():yield rel,src
                elif src.is_symlink():raise ValueError("unresolved import symlink: "+str(src))
        for rel,src in visit(base,set()):
            visited_files+=1
            if rel not in expected:
                expected[rel]=src.resolve();owners[rel]=base
    # Lean finds IR/private/server data beside the selected olean, not through
    # a new independent search. Refuse partial shadowing rather than mix owners.
    anchors={rel.with_suffix(""):owners[rel] for rel in expected if rel.suffix==".olean"}
    for rel,src in expected.items():
        parts=rel.name.split(".");candidates=[rel.with_name(".".join(parts[:i]))for i in range(1,len(parts))]
        anchor=next((name for name in reversed(candidates)if name in anchors),None)
        if anchor is not None:
            original=anchors[anchor]/rel
            if not original.is_file()or original.resolve()!=src:
                raise ValueError("partial module-family shadowing: "+str(rel))
    return expected,visited_files

def materialize_import_view(view,expected,internal=None,deadline=None):
    internal=internal or {}
    for rel,src in expected.items():
        if deadline is not None and time.monotonic()>=deadline:raise TimeoutError("subset validation six-hour limit during view preparation")
        dst=view/rel
        if not dst.exists()and not dst.is_symlink():
            dst.parent.mkdir(parents=True,exist_ok=True);dst.symlink_to(src)
    return check_import_view(view,expected,internal)

def check_import_view(view,expected,internal=None):
    """Require the whole file manifest, not a suffix allowlist, before native launch."""
    required=dict(expected);required.update(internal or {})
    observed={}
    for root,dirs,files in os.walk(view,followlinks=False):
        root=Path(root)
        if any((root/name).is_symlink()for name in dirs):raise ValueError("unexpected directory alias in import view")
        for name in files:
            dst=root/name;observed[dst.relative_to(view)]=dst
    missing=sorted(str(x)for x in required.keys()-observed.keys())
    extra=sorted(str(x)for x in observed.keys()-required.keys())
    different=sorted(str(rel)for rel in required.keys()&observed.keys()
        if not observed[rel].is_file()or observed[rel].resolve()!=required[rel].resolve())
    return dict(checked_files=len(required),missing=missing,extra=extra,different=different,
        passed=not(missing or extra or different),native_started=False)

def module_products(obj):
    """All same-module siblings, including future artifact extensions."""
    return [p for p in sorted(obj.parent.iterdir())if p.is_file()and p.name.startswith(obj.stem+".")]

def write_view_inventory(path,expected):
    import csv,gzip
    with gzip.open(path,"wt",newline="")as f:
        writer=csv.writer(f);writer.writerow(["relative_path","resolved_original_path"])
        for rel,src in sorted(expected.items()):writer.writerow([str(rel),str(src)])

def run(a):
    m=json.loads(a.manifest.read_text())
    environment_ready=False;environment_reason=None
    if not a.functional:
        path=a.environment_export or Path(__file__).parent/"dependency-audit/lake-environment.json"
        if not path.is_file():environment_reason="actual Lake environment export missing"
        else:
            export=json.loads(path.read_text())
            if not export.get("context_export_verified")or not export.get("package_versions_verified"):environment_reason="Lake environment not verified"
            elif export.get("source_revision")!=m["source_revision"]or export.get("toolchain")!=m["lean"]:environment_reason="export pin/toolchain mismatch"
            elif Path(export["project"]).resolve()!=Path(m["source_project_root"]).resolve():environment_reason="export belongs to another project"
            elif Path(export["native_compiler"]).resolve()!=Path(m["lean_binary"]).resolve():environment_reason="export belongs to another compiler"
            else:
                m["env"]=dict(export["native_environment"]);environment_ready=True
                m["context_id"]="openai-math-4eaee875-root"
                if a.execute:
                    for pkg in export["packages"]:
                        checkout=Path(export["project"])/".lake/packages"/pkg["name"]
                        head=subprocess.check_output(["git","-C",str(checkout),"rev-parse","HEAD"],text=True).strip()
                        if head!=pkg["commit"]:raise ValueError("exported package pin changed: "+pkg["name"])
                    actual_manifest=json.loads(Path(export["manifest"]).read_text())
                    actual_pins={p["name"].strip("«»"):p["rev"]for p in actual_manifest["packages"]}
                    exported_pins={p["name"]:p["commit"]for p in export["packages"]}
                    if actual_pins!=exported_pins:raise ValueError("exported manifest package pins changed")
        if a.execute and not environment_ready:raise ValueError(environment_reason)
        if not environment_ready:m["env"]={}
    bounded=getattr(a,"validate_subset",False)
    if bounded and a.functional:raise ValueError("choose real-corpus subset or fixture, not both")
    deadline=time.monotonic()+21600 if bounded else None
    mods={r["module"]:r for r in m["modules"]}
    if bounded and not 1<=len(mods)<=2000:raise ValueError("subset validation requires 1..2000 source modules")
    if bounded and any(Path(r["source"]).name=="lakefile.lean"for r in mods.values()):raise ValueError("subset must contain source modules only")
    if bounded and any(set(r["deps"])-mods.keys()for r in mods.values()):raise ValueError("subset must contain its internal dependency closure")
    missing_external=[]
    if environment_ready:
        search=[Path(x)for x in m["env"]["LEAN_PATH"].split(":")if x]
        for name in sorted({n for r in mods.values()for n in r.get("external",[])}):
            if not any((base/Path(*name.split(".")).with_suffix(".olean")).is_file()for base in search):missing_external.append(name)
        if a.execute and missing_external:raise ValueError("actual context has unprepared external imports: "+str(missing_external))
    if a.functional and len(mods)>10:raise ValueError("functional control is limited to ten source units")
    pools={"P":list(range(8)),"E":list(range(10,24))}if a.pool=="22"else{"P":list(range(8)),"E":[]}
    if a.functional:pools={"P":[8],"E":[9]}
    if bounded:pools={"P":[],"E":list(range(10,17))}
    identity=dict(source_revision=m["source_revision"],mathlib=m["mathlib"],lean_binary=m["lean_binary"],pools=pools,
        threads=8,options=m["lean_options"],env=m["env"],lean_version=m["lean"],toolchain_stat=[Path(m["lean_binary"]).stat().st_size,Path(m["lean_binary"]).stat().st_mtime_ns],functional_only=a.functional,manifest_sha256=sha(a.manifest),workers={p:len(c)for p,c in pools.items()})
    if bounded:
        identity.update(bounded_validation=True,cost_measurement=False,validation_limits=dict(maximum_modules=2000,maximum_seconds=21600,native_charge_GiB=11,controller_charge_GiB=1,workers=1))
    if not a.functional:
        identity.update(measurement_commit=a.commit,controller_source_sha256=sha(__file__),
            adapter_source_sha256=sha(Path(native.__file__)),
            protocol_rules=dict(reserve_GiB=8,response_slack_GiB=1,sample_seconds=1,disk_stop_fraction=.85,native_retries=1,resource_retry="drain_to_exclusive_then_record_current_headroom_failure"))
    if not a.execute:print(json.dumps(dict(prepared=(a.functional or environment_ready),execute=False,modules=len(mods),dependency_inputs_ready=(environment_ready and not missing_external),environment_export_verified=environment_ready,environment_error=environment_reason,missing_external_artifacts=missing_external,protocol=identity)));return
    if not a.functional:
        version=subprocess.check_output([m["lean_binary"],"--version"],text=True).strip()
        if "version "+m["lean"]+","not in version:raise ValueError("toolchain version mismatch")
        identity["observed_toolchain"]=version
    contexts={r.get("context_id",m.get("context_id","unspecified"))for r in mods.values()}
    if len(contexts)!=1:raise ValueError("run distinct Lake contexts separately")
    out=a.out.resolve()
    if not out.is_relative_to(Path("/workspaces"))or not Path("/workspaces").is_mount():raise ValueError("existing PVC required")
    out.mkdir(parents=True,exist_ok=True)
    lock=open(out/"controller.lock","a");fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    config=out/"run-config.json"
    if config.exists()and json.loads(config.read_text())!=identity:raise ValueError("protocol changed; separate run required")
    config.write_text(json.dumps(identity,indent=2))
    pcore=None
    if not a.functional and not bounded:
        pcore=open("/workspaces/.agent-state/gpu-smt-captures/pcore.lock","a");fcntl.flock(pcore,fcntl.LOCK_EX)
    if not a.functional:os.sched_setaffinity(0,set(pools["E"]or pools["P"]))
    native.P=pools["P"];native.E=pools["E"]
    for ledger in (out/"records.jsonl",out/"lifecycle.jsonl"):
        if ledger.exists()and ledger.stat().st_size:
            with ledger.open("rb")as f:f.seek(-1,2);broken=f.read(1)!=b"\n"
            if broken:
                with ledger.open("ab")as f:f.write(b"\n");f.flush();os.fsync(f.fileno())
    previous=records(out/"records.jsonl");done={r["module"]for r in previous if r["status"]=="completed"}
    fails=collections.Counter(r["module"]for r in previous if r["status"]=="failure"and not r.get("interruption"))
    last={r["module"]:r for r in previous}
    for n in done:
        r=last[n]
        if sha(mods[n]["source"])!=r["source_sha256"]or not all(Path(v["path"]).is_file()for v in r["artifacts"].values()):raise ValueError("completed input/product changed: "+n)
    starts=out/"lifecycle.jsonl"
    returned={r["sequence"]for r in previous}
    if starts.exists():
        for line in starts.read_text().splitlines():
            try:r=json.loads(line)
            except ValueError:continue
            if r.get("event")!="native_start"or r["sequence"]in returned:continue
            stat=Path("/proc",str(r["pid"]),"stat")
            if stat.exists()and stat.read_text().rsplit(")",1)[1].split()[19]==r["birth"]:raise ValueError("previous native still alive")
            append(out/"interruptions.jsonl",dict(module=r["module"],sequence=r["sequence"],status="interrupted_unknown_cost",utc=utc()))
    scopefile=out/"active-scope.txt"
    if scopefile.exists():
        old=Path(scopefile.read_text())
        if old.exists():
            if not old.name.startswith("proofserve-W-census-gate-"):raise ValueError("unexpected scope")
            for child in old.iterdir():
                if child.is_dir():
                    if(child/"cgroup.procs").read_text().strip():raise ValueError("old scope populated")
                    child.rmdir()
            old.rmdir()
    view=out/"import-view";view.mkdir(exist_ok=True)
    expected,original_files=inventory_imports(m["env"]["LEAN_PATH"].split(":"),deadline)
    materialize_import_view(view,expected,deadline=deadline)
    internal_products={}
    def publish(n,row):
        obj=Path(row["artifacts"][".olean"]["path"]);rel=Path(*n.split(".")).with_suffix(".olean")
        for src in module_products(obj):
            relative=rel.parent/src.name;dest=view/relative;target=src.resolve()
            if not dest.exists()and not dest.is_symlink():
                dest.parent.mkdir(parents=True,exist_ok=True);dest.symlink_to(target)
            if not dest.is_file()or dest.resolve()!=target:raise ValueError("published module product collision: "+str(relative))
            internal_products[relative]=target
    for n in done:publish(n,last[n])
    preflight=check_import_view(view,expected,internal_products)
    preflight.update(original_files=original_files,resolved_external_files=len(expected),resumed_internal_files=len(internal_products),inventory="import-view-files.csv.gz")
    write_view_inventory(out/"import-view-files.csv.gz",expected)
    (out/"import-view-preflight.json").write_text(json.dumps(preflight,indent=2))
    if not preflight["passed"]:raise ValueError("import view differs from original path inventory; native launch refused")
    for n,r in mods.items():r["source_sha256"]=sha(r["source"])
    m["env"]=dict(m["env"],LEAN_PATH=str(view))
    c=dict(m,modules=mods,cwd=m.get("source_project_root",str(Path(next(iter(mods.values()))["root"]))),
        measurement_commit=a.commit,toolchain=dict(lean=m["lean"],binary=m["lean_binary"]),
        attempts=dict(collections.Counter(r["module"]for r in previous)),continue_native_failures=True,memory_preempt_requeue=True,functional_only=(a.functional or bounded),
        native_wall_s=30 if a.functional else None,maximum_charge_bytes=(11*2**30 if bounded else 8*2**30 if a.functional else None),validation_deadline=deadline)
    engine=native.Gate(c,out);scopefile.write_text(str(engine.cg))
    engine.seq=max([r["sequence"]for r in previous]+[int(p.name)for p in (out/"attempts").glob("*")if p.name.isdigit()]+[0])
    configuration={n for n,r in mods.items()if Path(r["source"]).name=="lakefile.lean"}
    pending=set(mods)-done-configuration;failed={n for n,k in fails.items()if k>=2};blocked={};resource_retries=collections.Counter(r["module"]for r in previous if r.get("interruption")=="memory_reserve")
    solo=set(resource_retries)
    if (out/"resource-failures.jsonl").exists():
        for line in (out/"resource-failures.jsonl").read_text().splitlines():failed.add(json.loads(line)["module"])
    lookup=[view]
    stop=None
    try:
        while pending or engine.live:
            for n in sorted(pending):
                ds=mods[n]["deps"]
                bad=sorted(set(ds)&(failed|set(blocked)))
                missing=[d for d in mods[n].get("external",[])if not any((p/Path(*d.split(".")).with_suffix(".olean")).exists()for p in lookup)]
                if n in failed:pending.remove(n);continue
                if bad or missing:
                    blocked[n]=dict(status="blocked",module=n,failed_dependencies=bad,missing_external=missing);pending.remove(n);continue
            if bounded and time.monotonic()>=deadline:engine.stop="subset_validation_six_hour_limit"
            if engine.stop:stop=engine.stop;break
            stat=os.statvfs(out)
            if 1-stat.f_bavail/stat.f_blocks>=.85:stop="disk_85_percent";break
            total,available=native.mem();charge=int((engine.cg/"memory.current").read_text())
            for pool in pools:
                cap=(1 if bounded and pools[pool] else len(pools[pool]))if not a.functional else 1
                while available>=9*2**30 and sum(j["meta"]["pool"]==pool for j in engine.live.values())<cap:
                    if solo and engine.live:break
                    running={j["meta"]["module"]for j in engine.live.values()}
                    ready=next((n for n in sorted(pending)if n not in running and (not solo or n in solo) and set(mods[n]["deps"])<=done),None)
                    if ready is None:break
                    exclusive=not engine.live
                    for previous_job in engine.live.values():previous_job["meta"]["exclusive_at_launch"]=False
                    pid=engine.launch(ready,pool,"subset_validation"if bounded else"functional"if a.functional else"census",0,"subset_validation"if bounded else"functional"if a.functional else"census",not(a.functional or bounded))
                    engine.live[pid]["meta"]["exclusive_at_launch"]=exclusive
                    if solo:break
                    _,available=native.mem()
            if not engine.live:
                if pending:stop="memory_admission"if available<9*2**30 else"dependency_cycle_or_unresolved_context"
                break
            before=len(engine.rows);engine.collect()
            for r in engine.rows[before:]:
                n=r["module"]
                if r["status"]=="completed":
                    done.add(n);pending.discard(n);solo.discard(n);publish(n,r)
                elif r.get("interruption")=="memory_reserve":
                    resource_retries[n]+=1
                    if r.get("exclusive_at_launch"):
                        failed.add(n);pending.discard(n);solo.discard(n)
                        append(out/"resource-failures.jsonl",dict(module=n,status="resource_failure_at_current_headroom",utc=utc()))
                    else:solo.add(n)
                else:
                    fails[n]+=1
                    if fails[n]>=2:failed.add(n);pending.discard(n)
        engine.drain()
        for n in pending:blocked[n]=dict(status="not_attempted",module=n,reason=stop)
        report=dict(functional_only=a.functional,full_census=not(a.functional or bounded),bounded_validation=bounded,cost_measurement=not(a.functional or bounded),
            successful=sorted(done),failed=sorted(failed),blocked=list(blocked.values()),stop=stop,
            configuration_units=sorted(configuration),total_source_units=len(mods),complete=len(done)+len(configuration)==len(mods))
        (out/"outcomes.json").write_text(json.dumps(report,indent=2))
        print(json.dumps(report))
    finally:
        for pid,j in list(engine.live.items()):
            j["killed"]="controller_interrupted"
            try:(j["cg"]/"cgroup.kill").write_text("1")
            except ProcessLookupError:pass
        engine.drain()
        engine.cg.rmdir()
def main():
    p=argparse.ArgumentParser();p.add_argument("--manifest",type=Path,required=True);p.add_argument("--out",type=Path,required=True)
    p.add_argument("--pool",choices=["22","P8"],default="22");p.add_argument("--execute",action="store_true")
    p.add_argument("--validate-subset",action="store_true",help="explicit non-measurement real-corpus closure: CPUs 10-16, one worker, <=2000 modules, <=6h; still requires --execute");
    p.add_argument("--environment-export",type=Path);p.add_argument("--functional",action="store_true");p.add_argument("--commit",required=True)
    run(p.parse_args())
if __name__=="__main__":main()
