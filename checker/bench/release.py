#!/usr/bin/env python3
"""Two explicit post-census phases. No automatic queue, commit or publication.

Matrix returns before O's external timing. Invoke corpus only after that handoff.
Qualification uses inherited CPU affinity, no lease, and no paper-eligible output.
"""
from __future__ import annotations
import argparse,contextlib,csv,fcntl,filecmp,json,os,shutil,subprocess,sys,time
from pathlib import Path

def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+".pending")
    with tmp.open("w") as f:
        json.dump(value,f,indent=2);f.write("\n");f.flush();os.fsync(f.fileno())
    tmp.replace(path)
def birth(pid):
    try:return Path("/proc",str(pid),"stat").read_text().rsplit(")",1)[1].split()[19]
    except (FileNotFoundError,ProcessLookupError):return None
def require_retired_census(cfg):
    terminal=json.loads(Path(cfg["census_terminal"]).read_text())
    if terminal.get("stop") is not None or not terminal.get("full_census",False):
        raise RuntimeError("W has not finished its complete census traversal")
    if not terminal.get("complete"):
        accounted=set(terminal.get("successful",[]))|set(terminal.get("failed",[]))|set(terminal.get("configuration_units",[]))
        blocked=terminal.get("blocked",[])
        if any(r.get("status")=="not_attempted"for r in blocked):
            raise RuntimeError("W still has unattempted modules; do not truncate the census")
        accounted|={r["module"]for r in blocked}
        if len(accounted)!=terminal.get("total_source_units"):
            raise RuntimeError("W census outcome frame is incomplete")
    launch=json.loads(Path(cfg["census_launch"]).read_text())
    expected=launch.get("birth_ticks",launch.get("birth"))
    if expected is None or birth(launch["pid"])==str(expected):
        raise RuntimeError("W census controller still live or missing birth identity")
    cg=Path(launch["cgroup"])
    if cg.exists() and any(p.read_text().strip()for p in cg.rglob("cgroup.procs")):
        raise RuntimeError("W census native cgroup still populated")
    return terminal

def frozen_binary(repo,raw,cfg):
    freeze_file=repo/"checker/results/theorem-body-policy/freeze.json"
    freeze=json.loads(freeze_file.read_text())
    commit=subprocess.check_output(["git","log","--diff-filter=A","-1","--format=%H","--",str(freeze_file.relative_to(repo))],cwd=repo,text=True).strip()
    for name,blob in freeze["native_source_blobs"].items():
        actual=subprocess.check_output(["git","hash-object",name],cwd=repo,text=True).strip()
        if actual!=blob:raise ValueError("frozen native input changed: "+name)
    binary=Path(freeze["binary"])
    saved=raw/"frozen";saved.mkdir(exist_ok=True)
    dest=saved/"proofserve-check"
    if dest.exists():
        if not filecmp.cmp(binary,dest,shallow=False):raise ValueError("frozen executable changed")
    else:shutil.copy2(binary,dest)
    driver_dirty=subprocess.run(["git","diff","--quiet","HEAD","--","checker/bench"],cwd=repo).returncode!=0
    driver_dirty=driver_dirty or bool(subprocess.check_output(["git","ls-files","--others","--exclude-standard","--","checker/bench"],cwd=repo,text=True).strip())
    if driver_dirty and cfg["mode"]!="qualification":raise ValueError("commit the evaluation driver before final execution")
    meta=dict(native_commit=commit,checker_binary_hash=freeze["checker_binary_hash"],
              native_source_blobs=freeze["native_source_blobs"],lean_version=freeze["lean_version"],
              driver_commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=repo,text=True).strip(),
              driver_dirty=driver_dirty,qualification=cfg["mode"]=="qualification")
    if (saved/"source.json").exists():
        old=json.loads((saved/"source.json").read_text())
        if any(old[k]!=meta[k]for k in ["native_commit","checker_binary_hash","native_source_blobs"]):
            raise ValueError("native freeze changed; use a new evaluation directory")
    write(saved/"source.json",meta)
    # Freeze driver source separately from the native executable provenance.
    for source in (repo/"checker/bench").glob("*.py"):
        target=saved/"bench"/source.name;target.parent.mkdir(exist_ok=True)
        if target.exists() and target.read_bytes()!=source.read_bytes():
            raise ValueError("evaluation driver changed; use a new raw directory")
        if not target.exists():shutil.copy2(source,target)
    return dest,meta

def bound_environment(cfg,manifest,project,sdk):
    env=dict(os.environ,PATH=str(sdk/"bin")+":"+os.environ["PATH"],LEAN_SYSROOT=str(sdk))
    if cfg.get("census_run_config"):
        native=json.loads(Path(cfg["census_run_config"]).read_text())["env"]
        env.update({k:v for k,v in native.items()if k in ["LEAN_PATH","LD_LIBRARY_PATH","LEAN_SYSROOT"]})
    else:env["LEAN_PATH"]=manifest.get("env",{}).get("LEAN_PATH","")
    overlay=Path(cfg["artifact_root"]).resolve()
    env["LEAN_PATH"]=str(overlay)+os.pathsep+env.get("LEAN_PATH","")
    selected=subprocess.check_output([sdk/"bin/lake","env","printenv","LEAN_PATH"],cwd=project,env=env,text=True).strip()
    env["LEAN_PATH"]=selected
    search=[Path(p)if Path(p).is_absolute()else project/p for p in selected.split(os.pathsep)if p]
    missing=[];wrong=[]
    for row in manifest["modules"]:
        name=row["module"];rel=Path(*name.split(".")).with_suffix(".olean")
        expected=overlay/rel
        if not expected.is_file():missing.append(name);continue
        chosen=next((p/rel for p in search if(p/rel).is_file()),None)
        if chosen is None or not os.path.samefile(chosen,expected):wrong.append(name)
    if wrong:raise ValueError("Lake selected different artifacts: "+str(wrong[:10]))
    return env,missing

def checkpoint_progress(state):
    """Trusted local progress only; normal resume revalidates these identities."""
    accepted=set();axioms=set()
    paths=list(state.glob("batch-*/certified.json"))
    if (state/"receipt.json").exists():paths.append(state/"receipt.json")
    for p in paths:
        j=json.loads(p.read_text());j=j.get("receipt",j)
        accepted.update(j.get("accepted",[]));axioms.update(j.get("axioms",[]))
    return accepted,axioms

def corpus_coverage(raw,names,pending,rows,revalidated=False):
    accepted,axioms=checkpoint_progress(raw/"whole-state")
    missing=set(names)-accepted
    result=dict(status="complete"if revalidated and not missing else"incomplete",expected_source_units=len(names),
                verified_source_units=len(set(names)&accepted)if revalidated else None,
                checkpoint_accepted_source_units=len(set(names)&accepted),accepted_closure_modules=len(accepted),
                missing_source_units=sorted(missing),pending_contexts=pending,axioms=sorted(axioms),
                evidence="trusted local native receipt/certified batches; checkpoint counts are provisional until current invocation validates inputs",
                inputs_revalidated_this_invocation=revalidated,
                native_subset_receipt=str(raw/"whole-state/receipt.json"))
    write(raw/"whole-coverage.json",result)
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("config",type=Path);ap.add_argument("--phase",choices=["matrix","corpus"],required=True)
    ap.add_argument("--retry-failed",action="store_true")
    a=ap.parse_args();cfg=json.loads(a.config.read_text())
    qualification=cfg["mode"]=="qualification"
    if cfg["mode"]not in ["final","qualification"]:raise ValueError("unknown mode")
    repo=Path(__file__).resolve().parents[2]
    if subprocess.check_output(["git","symbolic-ref","--short","HEAD"],cwd=repo,text=True).strip()!="main":
        raise ValueError("main branch required")
    census=None
    if not qualification:census=require_retired_census(cfg)
    raw=Path(cfg["raw"]).resolve()/a.phase
    parent=raw
    while not parent.exists():parent=parent.parent
    volume=Path("/workspaces").resolve()
    if not os.path.ismount(volume)or not raw.is_relative_to(volume)or parent.stat().st_dev!=volume.stat().st_dev:
        raise ValueError("outputs must be on the existing PVC")
    raw.mkdir(parents=True,exist_ok=True)
    lock=(raw/".driver.lock").open("a+");fcntl.flock(lock,fcntl.LOCK_EX)
    saved=raw/"workflow-config.json"
    if saved.exists()and json.loads(saved.read_text())!=cfg:raise ValueError("configuration changed; use a fresh directory")
    write(saved,cfg)
    if census is not None:write(raw/"census-retirement.json",dict(controller_retired=True,complete_traversal=True,
                                       all_sources_compiled=census.get("complete"),source_units=census.get("total_source_units")))
    binary,source=frozen_binary(repo,raw,cfg)
    sdk=Path(cfg["sdk"])
    version=subprocess.check_output([sdk/"bin/lean","--version"],text=True)
    if "version "+source["lean_version"]+","not in version:raise ValueError("frozen Lean SDK version differs")
    os.environ["PROOFSERVE_BENCH_SDK"]=str(sdk)
    sys.path.insert(0,str(raw/"frozen/bench"));import guard
    guard.ROOT=raw
    project=Path(cfg["project"]).resolve()
    manifest=json.loads(Path(cfg["manifest"]).read_text());names=[r["module"]for r in manifest["modules"]]
    if len(names)!=len(set(names)):raise ValueError("ambiguous module names")
    if not qualification and len(names)!=163097:raise ValueError("wrong full source frame")
    env,missing=bound_environment(cfg,manifest,project,sdk)
    write(raw/"artifact-binding.json",dict(requested=len(names),missing=missing,selected_existing_artifacts_match=True,
                                         source_revision=manifest.get("source_revision"),mathlib=manifest.get("mathlib"),
                                         evaluated_search_path=env["LEAN_PATH"],project=str(project)))
    env["TMPDIR"]=str(raw/"tmp");(raw/"tmp").mkdir(exist_ok=True)
    env["PROOFSERVE_BENCH_CLASSIFICATION"]="untimed E8-9 qualification"if qualification else"quiet final release evaluation"
    env["LEAN_NUM_THREADS"]="2"if qualification else"8"
    write(raw/"controller.json",dict(pid=os.getpid(),birth=birth(os.getpid()),phase=a.phase,**source))
    write(raw/"phase-terminal.json",dict(complete=False,phase=a.phase,status="running",native_commit=source["native_commit"]))
    export=repo/"checker/results"/("post-census-qualification"if qualification else"release-"+source["native_commit"][:12])/a.phase
    export.mkdir(parents=True,exist_ok=True)
    if a.phase=="matrix":
        mc=dict(raw=str(raw),binary=str(binary),project=str(project),lease=cfg.get("lease",""),
                commit=source["native_commit"],driver_commit=source["driver_commit"],overlay=cfg["artifact_root"],
                lean_path=env["LEAN_PATH"],mode=cfg["mode"],retry_failed=a.retry_failed,
                evaluation_status=env["PROOFSERVE_BENCH_CLASSIFICATION"],matrix_limit_s=21600,
                worker_points=cfg.get("worker_points",{}),cell_limit_s=cfg.get("cell_limit_s",1800))
        if qualification:
            mc.update(roots={d:cfg["qualification_root"]for d in ["math","grid","barrier"]},repeats=[1],
                      worker_points={d:[1,2]for d in ["math","grid","barrier"]},ablation_workers=2,
                      official_workers=2,resume_workers=2,qualification_memory_gib=12)
        write(raw/"config.json",mc)
        cmd=[sys.executable,str(raw/"frozen/bench/matrix.py"),str(raw/"config.json")]
        with (raw/"driver.stdout").open("a")as fo,(raw/"driver.stderr").open("a")as fe:
            result=subprocess.run(cmd,env=env,stdout=fo,stderr=fe)
        if result.returncode:
            completed=json.loads((raw/"completed.json").read_text())if(raw/"completed.json").exists()else[]
            if completed:
                for row in completed:
                    native=json.loads((raw/"runs"/row.get("run_key",row["key"])/"result.json").read_text())
                    row["cpu_s"]=native.get("cgroup_usage_s")
                with(export/"partial-cells.csv").open("w",newline="")as f:
                    w=csv.DictWriter(f,fieldnames=list(completed[0]));w.writeheader();w.writerows(completed)
            write(raw/"phase-terminal.json",dict(complete=False,phase="matrix",returncode=result.returncode))
            raise SystemExit(result.returncode)
        subprocess.run([sys.executable,str(raw/"frozen/bench/summarize.py"),str(raw),str(export)],env=env,check=True)
        terminal=dict(complete=True,phase="matrix",native_commit=source["native_commit"],paper_eligible=not qualification,
                      next="O external timings; corpus is a separate invocation, never automatic")
    else:
        env["LEAN_NUM_THREADS"]=str(cfg.get("corpus_workers",24)if not qualification else 2)
        if not qualification:
            matrix_terminal=json.loads((raw.parent/"matrix/phase-terminal.json").read_text())
            if not matrix_terminal["complete"]:raise RuntimeError("finish the final matrix before corpus checking")
        affinity=set(os.sched_getaffinity(0))
        rows=json.loads((raw/"workflow-results.json").read_text())if(raw/"workflow-results.json").exists()else[]
        # A signal may have retired the guarded child before stage() could append
        # its row. Recover the durable native result, preserving the old attempt.
        for file in sorted((raw/"runs").glob("*-attempt-*/result.json")):
            name,number=file.parent.name.rsplit("-attempt-",1)
            if any(r["phase"]==name and r["attempt"]==int(number)for r in rows):continue
            result=json.loads(file.read_text())
            if not result.get("native_retired")or not result.get("cgroup_retired"):
                raise RuntimeError("previous native attempt is not retired")
            rows.append(dict(phase=name,attempt=int(number),returncode=result["returncode"],wall_s=result.get("wall_s"),
                             cpu_s=result.get("cgroup_usage_s"),sampled_tree_peak_bytes=result["sampled_tree_peak_bytes"],
                             charged_peak_bytes=result["charged_peak_bytes"],native_commit=source["native_commit"]))
        rows.sort(key=lambda r:(r["phase"],r["attempt"]))
        write(raw/"workflow-results.json",rows)
        def stage(name,argv,limit):
            old=[r for r in rows if r["phase"]==name]
            if old and old[-1]["returncode"]!=0 and not a.retry_failed:
                raise RuntimeError(name+": retained failure; inspect it and use --retry-failed")
            attempt=max((r["attempt"]for r in old),default=0)+1;key=name+"-attempt-"+str(attempt)
            lease=contextlib.nullcontext()if qualification else Path(cfg["lease"]).open("a+")
            try:
                with lease as handle:
                    if handle is not None:
                        fcntl.flock(handle,fcntl.LOCK_EX);os.sched_setaffinity(0,set(range(os.cpu_count())))
                    before=Path.cwd();os.chdir(project)
                    try:r=guard.run(key,argv,limit,False,env,memory_gib=12 if qualification else None)
                    finally:os.chdir(before)
            finally:os.sched_setaffinity(0,affinity)
            row=dict(phase=name,attempt=attempt,returncode=r["returncode"],wall_s=r.get("wall_s"),
                     cpu_s=r.get("cgroup_usage_s"),sampled_tree_peak_bytes=r["sampled_tree_peak_bytes"],
                     charged_peak_bytes=r["charged_peak_bytes"],native_commit=source["native_commit"])
            rows.append(row);write(raw/"workflow-results.json",rows);return r
        pending=[dict(module=n,reason="W produced no source-qualified artifact",status="build_unavailable")for n in missing]
        exclusions=set(missing)
        revalidated=False
        try:
            for name in cfg.get("capacity_import_roots",["OAI"]):
                if name in exclusions:continue
                meta=stage("capacity-metadata-"+name,[binary,"--internal-module-meta",name],cfg.get("capacity_import_limit_s",1800))
                if meta["returncode"]!=0:raise RuntimeError("cannot establish umbrella metadata")
                out=raw/"runs"/("capacity-metadata-"+name+"-attempt-"+str(sum(r["phase"]=="capacity-metadata-"+name for r in rows)))/"stdout"
                info=json.loads(out.read_text())["module_metadata"][0]
                if not info["empty"]:raise RuntimeError("capacity exclusion is only valid for a compiled-empty module")
                context=stage("capacity-import-"+name,[binary,"--internal-empty-context",name],cfg.get("capacity_import_limit_s",1800))
                if context["returncode"]!=0:
                    exclusions.add(name);pending.append(dict(module=name,compiled_own_declarations=0,
                        context_status="not_completed",returncode=context["returncode"],
                        input_identity=info["inputs"],reason="bounded original combined-context check did not complete"))
            selected=[n for n in names if n not in exclusions]
            if not selected:raise RuntimeError("no artifact-backed roots remain")
            roots=raw/"whole-roots.txt";roots.write_text("\n".join(sorted(selected))+"\n")
            command=[binary,project,"--workers",str(cfg.get("corpus_workers",24)if not qualification else 2),
                     "--root-file",roots,"--closure-roots",str(cfg.get("closure_roots",500)),
                     "--checkpoint-dir",raw/"whole-state","--json"]
            result=stage("whole-library",command,cfg.get("whole_limit_s",259200))
            revalidated=result["returncode"]==0
        finally:
            coverage=corpus_coverage(raw,names,pending,rows,revalidated)
            write(raw/"phase-terminal.json",dict(complete=False,phase="corpus",status="stopped_or_returned",coverage=coverage))
            write(export/"whole-coverage.json",coverage)
            if rows:
                fields=list(rows[0])
                with (export/"workflow-cells.csv").open("w",newline="")as f:
                    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
        terminal=dict(complete=coverage["status"]=="complete",phase="corpus",native_commit=source["native_commit"],
                      coverage=coverage,paper_eligible=not qualification)
    write(raw/"phase-terminal.json",terminal);write(export/"phase-terminal.json",terminal)
    print(json.dumps(terminal),flush=True)
    if not terminal["complete"]:raise SystemExit(2)
if __name__=="__main__":main()
