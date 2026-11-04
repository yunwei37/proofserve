#!/usr/bin/env python3
"""Prepare only by default. Native census requires --execute; never auto-launched."""
import argparse,collections,fcntl,hashlib,json,os,signal,sys,time,subprocess
from pathlib import Path
import census_gate as native
from census import append,utc,records
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
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
    mods={r["module"]:r for r in m["modules"]}
    missing_external=[]
    if environment_ready:
        search=[Path(x)for x in m["env"]["LEAN_PATH"].split(":")if x]
        for name in sorted({n for r in mods.values()for n in r.get("external",[])}):
            if not any((base/Path(*name.split(".")).with_suffix(".olean")).is_file()for base in search):missing_external.append(name)
        if a.execute and missing_external:raise ValueError("actual context has unprepared external imports: "+str(missing_external))
    if a.functional and len(mods)>10:raise ValueError("functional control is limited to ten source units")
    pools={"P":list(range(8)),"E":list(range(10,24))}if a.pool=="22"else{"P":list(range(8)),"E":[]}
    if a.functional:pools={"P":[8],"E":[9]}
    identity=dict(source_revision=m["source_revision"],mathlib=m["mathlib"],lean_binary=m["lean_binary"],pools=pools,
        threads=8,options=m["lean_options"],env=m["env"],lean_version=m["lean"],toolchain_stat=[Path(m["lean_binary"]).stat().st_size,Path(m["lean_binary"]).stat().st_mtime_ns],functional_only=a.functional,manifest_sha256=sha(a.manifest),workers={p:len(c)for p,c in pools.items()})
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
    if not a.functional:
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
    for path in m["env"]["LEAN_PATH"].split(":"):
        base=Path(path)
        if not base.is_dir():continue
        for src in base.rglob("*.olean*"):
            rel=src.relative_to(base)
            if rel.parts[0].split(".")[0]in {"OAI","ComparatorChallenges","HodgeConjecture"}:continue
            dst=view/rel
            if not dst.exists():dst.parent.mkdir(parents=True,exist_ok=True);dst.symlink_to(src.resolve())
    def publish(n,row):
        obj=Path(row["artifacts"][".olean"]["path"]);rel=Path(*n.split(".")).with_suffix(".olean")
        for src in obj.parent.glob(obj.name+"*"):
            dest=view/rel.parent/src.name;dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists():dest.symlink_to(src.resolve())
    for n in done:publish(n,last[n])
    for n,r in mods.items():r["source_sha256"]=sha(r["source"])
    m["env"]=dict(m["env"],LEAN_PATH=str(view))
    c=dict(m,modules=mods,cwd=m.get("source_project_root",str(Path(next(iter(mods.values()))["root"]))),
        measurement_commit=a.commit,toolchain=dict(lean=m["lean"],binary=m["lean_binary"]),
        attempts=dict(collections.Counter(r["module"]for r in previous)),continue_native_failures=True,memory_preempt_requeue=True,functional_only=a.functional,
        native_wall_s=30 if a.functional else None,maximum_charge_bytes=8*2**30 if a.functional else None)
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
            if engine.stop:stop=engine.stop;break
            stat=os.statvfs(out)
            if 1-stat.f_bavail/stat.f_blocks>=.85:stop="disk_85_percent";break
            total,available=native.mem();charge=int((engine.cg/"memory.current").read_text())
            for pool in pools:
                cap=len(pools[pool])if not a.functional else 1
                while available>=9*2**30 and sum(j["meta"]["pool"]==pool for j in engine.live.values())<cap:
                    if solo and engine.live:break
                    running={j["meta"]["module"]for j in engine.live.values()}
                    ready=next((n for n in sorted(pending)if n not in running and (not solo or n in solo) and set(mods[n]["deps"])<=done),None)
                    if ready is None:break
                    exclusive=not engine.live
                    for previous_job in engine.live.values():previous_job["meta"]["exclusive_at_launch"]=False
                    pid=engine.launch(ready,pool,"functional"if a.functional else"census",0,"functional"if a.functional else"census",not a.functional)
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
        report=dict(functional_only=a.functional,full_census=False if a.functional else True,
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
    p.add_argument("--environment-export",type=Path);p.add_argument("--functional",action="store_true");p.add_argument("--commit",required=True)
    run(p.parse_args())
if __name__=="__main__":main()
