#!/usr/bin/env python3
"""Frozen public-checker evaluation workflow; no automatic publication.

Run only after W's build census has finished. Qualification mode uses E8-9,
one small project, no P-core lease, and never creates final paper tables.
A failed attempt is retained. Reinvoke with --retry-failed to retry explicitly.
"""
from __future__ import annotations
import argparse,contextlib,csv,fcntl,json,os,shutil,signal,subprocess,sys,time
from pathlib import Path

def write(path,value):
    tmp=path.with_suffix(path.suffix+".pending")
    tmp.write_text(json.dumps(value,indent=2)+"\n");tmp.replace(path)
def birth(pid):
    try:return Path("/proc",str(pid),"stat").read_text().rsplit(")",1)[1].split()[19]
    except FileNotFoundError:return None
def require_retired_census(cfg):
    terminal=json.loads(Path(cfg["census_terminal"]).read_text())
    if terminal.get("complete")is not True:
        raise RuntimeError("W census is not complete; no P-core work started")
    launch=json.loads(Path(cfg["census_launch"]).read_text())
    pid=launch["pid"];expected=launch.get("birth_ticks",launch.get("birth"))
    if expected is None:raise RuntimeError("W census launch has no process birth identity")
    if birth(pid)==str(expected):
        raise RuntimeError("W census controller is still live; no P-core work started")
    cg=Path(launch["cgroup"])
    if cg.exists():
        for procs in cg.rglob("cgroup.procs"):
            if procs.read_text().strip():raise RuntimeError("W census native cgroup is still populated")
    return dict(complete=True,controller_retired=True,terminal=str(cfg["census_terminal"]))

def main():
    ap=argparse.ArgumentParser();ap.add_argument("config",type=Path);ap.add_argument("--retry-failed",action="store_true");ap.add_argument("--freeze-only",action="store_true")
    a=ap.parse_args();cfg=json.loads(a.config.read_text())
    qualification=cfg["mode"]=="qualification"
    if cfg["mode"]not in("final","qualification"):raise ValueError("unknown workflow mode")
    repo=Path(__file__).resolve().parents[2];package=repo/"checker"
    preparation_affinity=set(os.sched_getaffinity(0))
    census_status=None
    if not qualification:census_status=require_retired_census(cfg)
    raw=Path(cfg["raw"]).resolve()
    volume=Path("/workspaces").resolve()
    parent=raw
    while not parent.exists():parent=parent.parent
    if not os.path.ismount(volume) or not raw.is_relative_to(volume) or parent.stat().st_dev!=volume.stat().st_dev:
        raise ValueError("workflow outputs must be on the existing /workspaces PVC")
    raw.mkdir(parents=True,exist_ok=True)
    lock=(raw/".driver.lock").open("a+");fcntl.flock(lock,fcntl.LOCK_EX)
    (raw/"runs").mkdir(exist_ok=True)
    config_file=raw/"workflow-config.json"
    if config_file.exists() and json.loads(config_file.read_text())!=cfg:
        raise ValueError("workflow configuration changed; use a new raw directory")
    write(config_file,cfg)
    if census_status is not None:write(raw/"census-retirement.json",census_status)
    sdk=Path(cfg["sdk"]).resolve();os.environ["PROOFSERVE_BENCH_SDK"]=str(sdk)
    sys.path.insert(0,str(package/"bench"));import guard
    guard.ROOT=raw
    env=guard.environment();env["PATH"]=str(sdk/"bin")+":"+env["PATH"]
    env["LEAN_NUM_THREADS"]="2" if qualification else "8"
    env["PROOFSERVE_BENCH_CLASSIFICATION"]="untimed workflow qualification"if qualification else"final release evaluation"
    def git(*args):return subprocess.check_output(["git",*args],cwd=repo,text=True).strip()
    if git("symbolic-ref","--short","HEAD")!="main":raise ValueError("main branch required")
    saved_source=raw/"frozen/source.json"
    saved_commit=json.loads(saved_source.read_text())["commit"]if saved_source.exists()else None
    commit=cfg.get("commit")or saved_commit or git("rev-parse","HEAD")
    source_paths=["checker/Main.lean","checker/ProofServe","checker/c","checker/bench","checker/lakefile.lean","checker/lean-toolchain"]
    dirty=subprocess.run(["git","diff","--quiet",commit,"--",*source_paths],cwd=repo).returncode!=0
    dirty=dirty or bool(subprocess.check_output(["git","ls-files","--others","--exclude-standard","--",*source_paths],cwd=repo,text=True).strip())
    if dirty and not qualification:raise ValueError("commit the checker before final binary freeze")
    write(raw/"controller.json",dict(pid=os.getpid(),birth=birth(os.getpid()),mode=cfg["mode"],commit=commit))
    rows=json.loads((raw/"workflow-results.json").read_text())if(raw/"workflow-results.json").exists()else[]
    def save_rows():
        write(raw/"workflow-results.json",rows)
        fields=["phase","attempt","commit","mode","outcome","returncode","wall_s","cpu_s","sampled_tree_peak_bytes","charged_peak_bytes","receipt"]
        with(raw/"workflow-cells.csv").open("w",newline="")as f:
            w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(rows)
    def stage(name,argv,cwd,environment,native_json=False,timed=True,limit=1100):
        old=[r for r in rows if r["phase"]==name]
        if old and old[-1]["outcome"]=="complete":return old[-1]
        if old and not a.retry_failed:raise RuntimeError(name+": previous failure retained; use --retry-failed after review")
        attempt=len(old)+1;key=name+"-attempt-"+str(attempt)
        previous=Path.cwd();os.chdir(cwd)
        try:
            lease=contextlib.nullcontext()
            if timed and not qualification:
                lease=Path(cfg["lease"]).open("a+")
            with lease as handle:
                if handle is not None:fcntl.flock(handle,fcntl.LOCK_EX);os.sched_setaffinity(0,set(range(8)))
                result=guard.run(key,argv,limit,measured=timed and not qualification,env=environment,
                                 memory_gib=cfg.get("qualification_memory_gib",16) if qualification else None)
            os.sched_setaffinity(0,preparation_affinity)
        finally:os.chdir(previous)
        receipt=None;outcome="complete"if result["returncode"]==0 else"failed"
        if native_json and result["returncode"]==0:
            receipt=json.loads((raw/"runs"/key/"stdout").read_text())
            if receipt.get("status")!="complete"or receipt.get("execution_path")!="proofserve-parallel":
                outcome="incomplete"
            write(raw/(name+"-receipt.json"),receipt)
        row=dict(phase=name,attempt=attempt,commit=commit,mode=cfg["mode"],outcome=outcome,
                 returncode=result["returncode"],wall_s=result.get("wall_s"),cpu_s=result.get("cgroup_usage_s"),
                 sampled_tree_peak_bytes=result["sampled_tree_peak_bytes"],charged_peak_bytes=result["charged_peak_bytes"],
                 receipt=str(raw/(name+"-receipt.json"))if receipt else None)
        rows.append(row);save_rows()
        if outcome!="complete":
            write(raw/"workflow-terminal.json",dict(complete=False,failed_phase=name,attempt=attempt,mode=cfg["mode"]))
            raise RuntimeError(name+": did not complete; original attempt retained")
        return row
    frozen=raw/"frozen";frozen.mkdir(exist_ok=True)
    frozen_binary=frozen/"proofserve-check"
    if not frozen_binary.exists():
        stage("freeze-build",[sdk/"bin/lake","build"],package,env,False,False,600)
        shutil.copy2(package/".lake/build/bin/proofserve-check",frozen_binary)
        bench=frozen/"bench";bench.mkdir(exist_ok=True)
        for source in(package/"bench").glob("*.py"):shutil.copy2(source,bench/source.name)
        (frozen/"source.patch").write_text(subprocess.check_output(["git","diff",commit,"--","checker"],cwd=repo,text=True))
        sources=[package/"Main.lean",package/"lakefile.lean",package/"lean-toolchain"]
        sources+=list((package/"ProofServe").glob("*.lean"))+list((package/"c").glob("*.c"))+list((package/"bench").glob("*.py"))
        for source in sources:
            dest=frozen/"source-tree"/source.relative_to(package)
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
        write(frozen/"source.json",dict(commit=commit,checker_git_tree=git("rev-parse",commit+":checker"),worktree_dirty=dirty,mode=cfg["mode"],
                                       lean_version=subprocess.check_output([sdk/"bin/lean","--version"],text=True).strip()))
    frozen_source=json.loads((frozen/"source.json").read_text())
    if frozen_source["commit"]!=commit or frozen_source["mode"]!=cfg["mode"]:raise ValueError("frozen binary source differs")
    if a.freeze_only:
        print(json.dumps(dict(frozen=True,workflow_complete=False,binary=str(frozen_binary),source=frozen_source)),flush=True)
        return
    manifest_path=Path(cfg["manifest"]);manifest=json.loads(manifest_path.read_text());modules=manifest["modules"]
    names=[r["module"]for r in modules]
    if len(names)!=len(set(names)):raise ValueError("split ambiguous module names into distinct execution contexts")
    if not qualification and len(names)!=163097:raise ValueError("full pinned manifest must have 163097 source units")
    project=Path(cfg["project"]).resolve();artifact_root=Path(cfg["artifact_root"]).resolve()
    absent=[name for name in names if not(artifact_root/Path(*name.split(".")).with_suffix(".olean")).is_file()]
    if absent:
        write(raw/"missing-source-artifacts.json",dict(count=len(absent),modules=absent,mode=cfg["mode"]))
        write(raw/"workflow-terminal.json",dict(complete=False,mode=cfg["mode"],reason="source artifacts missing",missing=len(absent)))
        raise RuntimeError(f"{len(absent)} requested source artifacts missing; no whole check started")
    base=dict(env)
    base["LEAN_PATH"]=str(artifact_root)+os.pathsep+manifest.get("env",{}).get("LEAN_PATH","")
    evaluated=subprocess.check_output([sdk/"bin/lake","env","printenv","LEAN_PATH"],cwd=project,env=base,text=True).strip()
    search=[Path(p)if Path(p).is_absolute()else project/p for p in evaluated.split(":")]
    mismatched=[]
    for name in names:
        rel=Path(*name.split(".")).with_suffix(".olean")
        chosen=next((p/rel for p in search if(p/rel).is_file()),None)
        expected=artifact_root/rel
        if chosen is None or not os.path.samefile(chosen,expected):mismatched.append(name)
    if mismatched:
        write(raw/"artifact-binding-failure.json",dict(modules=mismatched,count=len(mismatched),search_path=evaluated))
        raise RuntimeError("Lake selects artifacts other than the recorded census outputs; no whole check started")
    write(raw/"artifact-binding.json",dict(source_modules=len(names),all_selected_artifacts_match=True,search_path=evaluated))
    # Capacity-only importer preflight for compiled-empty umbrella contexts.
    # It accepts no imported proof bodies. A failure stops before expensive
    # whole-library replay; prior small closures do not establish this bound.
    context_env=dict(base,LEAN_PATH=evaluated)
    for index,context_root in enumerate(cfg.get("capacity_import_roots",[])):
        row=stage("capacity-import-"+str(index),[frozen_binary,"--internal-empty-context",context_root],
              project,context_env,False,False,cfg.get("capacity_import_limit_s",1800))
        output=raw/"runs"/("capacity-import-"+str(index)+"-attempt-"+str(row["attempt"]))/"stdout"
        checked=json.loads(output.read_text())
        if checked.get("empty_context_checked")is not True or checked.get("module")!=context_root:
            raise ValueError("capacity importer did not validate the configured empty context")
    roots=raw/"whole-roots.txt";roots.write_text("\n".join(sorted(names))+"\n")
    whole_command=[frozen_binary,project,"--workers","1"if qualification else"4",
          "--root-file",roots,"--closure-roots",str(cfg.get("closure_roots",500)),"--checkpoint-dir",raw/"whole-state","--json"]
    already_complete=any(r["phase"]=="whole-library"and r["outcome"]=="complete"for r in rows)
    stage("whole-library",whole_command,project,base,True,True,cfg.get("whole_limit_s",259200))
    if already_complete:
        # Native resume revalidates all local certificate input hashes. A
        # controller restart must not trust a successful historical row alone.
        number=sum(r["phase"].startswith("whole-input-validation-")for r in rows)+1
        stage("whole-input-validation-"+str(number),whole_command,project,base,True,True,cfg.get("whole_limit_s",259200))
    whole=json.loads((raw/"whole-library-receipt.json").read_text())
    if not set(names)<=set(whole["accepted"]):raise ValueError("source-unit coverage missing from complete receipt")
    contexts={}
    for r in modules:contexts[r["root"]]=contexts.get(r["root"],0)+1
    write(raw/"whole-coverage.json",dict(commit=commit,source_revision=manifest.get("source_revision"),mathlib_pin=manifest.get("mathlib"),project=str(project),source_project_root=cfg.get("source_project_root"),source_units=len(names),accepted_closure=len(whole["accepted"]),
          source_compile_roots=contexts,execution_contexts=1,all_requested_sources_accepted=True,
          axiom_free=not whole["axioms"],mode=cfg["mode"]))
    if qualification:
        root=cfg["qualification_root"]
        stage("matrix-native",[frozen_binary,project,"--root",root,"--workers","1","--closure-roots","0",
              "--checkpoint-dir",raw/"matrix-small-state","--json"],project,base,True)
        for mode in("default","fresh"):
            flags=["--fresh"]if mode=="fresh"else[]
            stage("matrix-official-"+mode,[sdk/"bin/lake","env","leanchecker","-v",*flags,root],project,base)
    else:
        mc=dict(raw=str(raw/"matrix"),binary=str(frozen_binary),project=str(project),lease=cfg["lease"],
                commit=commit,overlay=str(artifact_root),retry_failed=a.retry_failed,evaluation_status="final release evaluation")
        write(raw/"matrix-config.json",mc)
        # The fixed matrix owns a lease per native cell and its own native guards.
        # Do not place its coordinator in another native cgroup or hold its lease.
        cmd=[sys.executable,str(frozen/"bench/matrix.py"),str(raw/"matrix-config.json")]
        record=raw/"matrix/workflow-finished.json"
        if not record.exists():
            with(raw/"matrix-driver.stdout").open("a")as fo,(raw/"matrix-driver.stderr").open("a")as fe:
                process=subprocess.Popen(cmd,env=base,stdout=fo,stderr=fe,start_new_session=True)
                write(raw/"matrix-driver.json",dict(pid=process.pid,birth=birth(process.pid),commit=commit))
                code=process.wait()
            if code:raise RuntimeError("fixed matrix stopped; inspect retained native result before resuming")
            write(record,dict(complete=True,commit=commit))
        subprocess.run([sys.executable,str(frozen/"bench/summarize.py"),str(raw/"matrix"),str(raw/"summary/matrix")],check=True,env=base)
        root="OAI.Analysis.PlanarPacking.Main"
    for workers in("default","8"if not qualification else"2"):
        flag=[]if workers=="default"else["--workers",workers]
        if qualification:flag=["--workers","1"if workers=="default"else workers]
        stage("planar-"+workers,[frozen_binary,project,"--root",root,*flag,
              "--checkpoint-dir",raw/("planar-state-"+workers),"--json"],project,base,True,
              limit=600 if qualification else cfg.get("planar_limit_s",129600))
    if not qualification:
        for mode in("default","fresh"):
            flags=["--fresh"]if mode=="fresh"else[]
            stage("planar-official-"+mode,[sdk/"bin/lake","env","leanchecker","-v",*flags,root],
                  project,base,limit=cfg.get("planar_limit_s",129600))
    expected=set(json.loads((raw/"planar-default-receipt.json").read_text())["accepted"])
    actual=set(json.loads((raw/("planar-"+("2"if qualification else"8")+"-receipt.json")).read_text())["accepted"])
    if actual!=expected:raise ValueError("Planar worker acceptance sets differ")
    export=repo/"checker/results"/("workflow-qualification"if qualification else"release-"+commit[:12])
    export.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(raw/"workflow-cells.csv",export/"workflow-cells.csv")
    shutil.copyfile(raw/"whole-coverage.json",export/"whole-coverage.json")
    if not qualification:
        for f in(raw/"summary/matrix").glob("*"):shutil.copyfile(f,export/f.name)
    terminal=dict(complete=True,mode=cfg["mode"],commit=commit,raw=str(raw),output=str(export),
                  frozen_source=frozen_source,performance_eligible=not qualification,qualification_root=cfg.get("qualification_root")if qualification else None,planar_acceptance_equal=True)
    write(raw/"workflow-terminal.json",terminal);write(export/"workflow-terminal.json",terminal)
    print(json.dumps(terminal),flush=True)
if __name__=="__main__":main()
