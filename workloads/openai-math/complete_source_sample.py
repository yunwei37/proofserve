#!/usr/bin/env python3
"""Finite completion of the fixed remaining source sample; no AI/session scheduler."""
import argparse, copy, csv, datetime, json, os, select, shutil, subprocess, sys
from pathlib import Path
R=Path("/workspaces/repository")
B=Path("/workspaces/.agent-state/gpu-smt-captures/workloads")
F=R/"workloads/openai-math/final-seven-20261102"
CHILDREN={}
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(p,v): p.write_text(json.dumps(v,indent=2)+"\n")
def readcsv(p): return list(csv.DictReader(p.open()))
def birth(pid): return Path("/proc",str(pid),"stat").read_text().rsplit(")",1)[1].split()[19]
def mainbranch():
    assert subprocess.check_output(["git","symbolic-ref","--short","HEAD"],cwd=R,text=True).strip()=="main"
def disk_ok():
    s=os.statvfs("/workspaces");used=s.f_blocks-s.f_bfree
    assert used/(used+s.f_bavail)<.85,"user85percent storage threshold; no new compilation"
def event(v):
    v={"utc":utc(),**v}
    with(A.raw/"progress.jsonl").open("a")as f:f.write(json.dumps(v)+"\n");f.flush()
    print(json.dumps(v),flush=True)
def wait_owner(point,prep):
    launch=json.loads((point/("preparation-launch.json"if prep else"launch.json")).read_text())
    while True:
        stat=Path("/proc",str(launch["pid"]),"stat")
        s=stat.read_text().rsplit(")",1)[1].split()if stat.exists()else None
        if not s or s[19]!=launch["birth_ticks"]or s[0]=="Z":break
        try:fd=os.pidfd_open(launch["pid"])
        except ProcessLookupError:continue
        poll=select.poll();poll.register(fd,select.POLLIN);poll.poll(60000);os.close(fd)
    if launch["pid"]in CHILDREN:CHILDREN.pop(launch["pid"]).wait()
    path=point/("preparation-terminal.json"if prep else"terminal.json")
    assert path.exists(),"controller exited without terminal; retain raw and inspect"
    result=json.loads(path.read_text())
    if prep:assert result.get("preparation_final",True),"Econtroller ended between windows"
    return result
def launch(point,args,prep,module):
    name="preparation-launch.json"if prep else"launch.json"
    with(point/"controller.log").open("w")as f:
        child=subprocess.Popen(args,cwd=R,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT)
    CHILDREN[child.pid]=child
    item=dict(utc=utc(),pid=child.pid,birth_ticks=birth(child.pid),args=args,
              original_target=module,operation="untimed_E_preparation"if prep else"original_P_measurement")
    dump(point/name,item);dump(A.raw/"active-child.json",dict(point=str(point),**item))
    event(dict(event="child_launched",point=str(point),**item))
def refreshed_ready(plan):
    ready=set(plan["initial_ready"])
    for p in B.iterdir():
        files=[]
        if p.name.startswith("openai4341-Eprep-")and(p/"preparation-results.jsonl").exists():files.append(p/"preparation-results.jsonl")
        if(p.name.startswith("openai4341-noM-final-")or p.name.startswith("openai4341-noM-NativeCodeAssembly"))and(p/"results.jsonl").exists():files.append(p/"results.jsonl")
        for file in files:
            for line in file.read_text().splitlines():
                r=json.loads(line)
                if r["status"]!="compile_ok":continue
                assert r["native_retired"]and r["cgroup_retired"]
                parts=r.get("published",r.get("cache_published_after_native_retirement",[]))
                assert parts and all(Path(x).exists()for x in parts)
                ready.add(r["module"])
    return ready
def make_prep(seed,module):
    disk_ok();p=B/("openai4341-Eprep-"+module.rsplit(".",1)[-1]+"-"+A.raw.name)
    p.mkdir(exist_ok=False)
    plan=json.loads((seed/"plan.json").read_text());plan["initial_ready"]=sorted(refreshed_ready(plan))
    plan["scope"]="untimed prerequisites; current original role excluded"
    for c in plan["cases"]:c["self_wall_s"]=1200
    dump(p/"plan.json",plan)
    shutil.copyfile(A.attach_preparation/"prepare_dependencies.py",p/"prepare_dependencies.py")
    launch(p,[sys.executable,"-u",str(p/"prepare_dependencies.py"),"--point",str(p)],True,module)
    return p
def make_timed(prep,seed,module):
    disk_ok();p=B/("openai4341-noM-final-"+module.rsplit(".",1)[-1]+"-targetP-"+A.raw.name)
    p.mkdir(exist_ok=False)
    plan=json.loads((prep/"plan.json").read_text());ready=refreshed_ready(plan)
    c=copy.deepcopy(next(x for x in plan["cases"]if x["role"]=="original_probability_sample"))
    assert c["module"]==module and not(set(c["deps"])-ready)
    assert Path(c["args"][-1]).read_bytes()==Path(c["pinned_source"]).read_bytes()
    assert not any(x.startswith("-M")for x in c["args"])
    c["self_wall_s"]=1200
    for flag in ["-o","-i","-c"]:
        k=c["args"].index(flag)+1;c["args"][k]=str(p/"working/00"/Path(c["args"][k]).name)
    dump(p/"plan.json",dict(cases=[c],initial_ready=sorted(ready),scope="fresh originalP,noM,authoredHB,3facets; Eprerequisites unmeasured"))
    for f in ["controller.py","runner.py"]:shutil.copyfile(seed/f,p/f)
    launch(p,[sys.executable,"-u",str(p/"controller.py"),"--point",str(p)],False,module)
    return p

def baseline_records():
    rows=[]
    for r in readcsv(A.frame):
        if r["status"]=="completed_cost":
            row=json.loads(Path(r["source_file"]).read_text().splitlines()[int(r["source_line"])-1])
            assert row["module"]==r["module"]
            assert abs(row["user_cpu_s"]+row["system_cpu_s"]-float(r["cpu_s"]))<1e-8
            rows.append(row)
        elif r["status"]!="unmeasured":
            rows.append(dict(module=r["module"],status=r["status"],native_invoked=False,
                             derivation="baseline operational status; not a completed cost"))
    return rows
def analyze(records,module,point,status):
    ledger=A.raw/("selected-"+module.rsplit(".",1)[-1]+".jsonl")
    ledger.write_text("".join(json.dumps(x)+"\n"for x in records))
    count=sum(x.get("status")=="compile_ok"for x in records)
    out=F/("collection-"+A.raw.name)/("source"+str(count)+"-"+module.rsplit(".",1)[-1])
    out.mkdir(parents=True,exist_ok=False)
    env=os.environ.copy();env["PYTHONPATH"]=str(B/"statistics-python-deps")
    env["PYTHONDONTWRITEBYTECODE"]="1"
    commands=[
     ["estimate_native_build.py","--targets","workloads/openai-math/build-planning-4eaee875/phaseA-targets.csv",
      "--strata","workloads/openai-math/build-planning-4eaee875/strata.csv","--results",str(ledger),
      "--heartbeat-budget","authored_or_native_default","--memory-mib","0",
      "--outputs","olean_ilean_c","--locked-only","--out",str(out)],
     ["missing_draw_stress.py","--frame",str(out/"sample-costs.csv"),"--out",str(out/"missing-cost-scenarios")],
     ["cost_staircase.py","--frame",str(out/"sample-costs.csv"),"--latest-serial","--out",str(out/"latest-staircase")]]
    with(A.raw/("analysis-"+module.rsplit(".",1)[-1]+".log")).open("w")as log:
        for cmd in commands:
            subprocess.run([sys.executable,"workloads/openai-math/"+cmd[0],*cmd[1:]],cwd=R,env=env,
                           stdout=log,stderr=subprocess.STDOUT,check=True)
    old={r["module"]:r for r in readcsv(A.frame)}
    new=readcsv(out/"sample-costs.csv")
    for r in new:
        if old[r["module"]]["status"]=="completed_cost":
            assert r["status"]=="completed_cost"and abs(float(r["cpu_s"])-float(old[r["module"]]["cpu_s"]))<1e-8
    receipt=json.loads((out/"latest-staircase/receipt.json").read_text())
    envrows=readcsv(out/"latest-staircase/full-frame-scenario-envelope.csv")
    ranges={r["stage"]:[float(r["min_model_CPU_h"]),float(r["max_model_CPU_h"])]for r in envrows if r["domain"]=="all"}
    src=readcsv(out/"latest-staircase/full-frame-missing-staircase.csv")
    shares=[float(r["certificate_source_CPU_share"])for r in src if r["domain"]=="all"]
    observed=next(r for r in new if r["module"]==module)
    snapshot=dict(utc=utc(),completed_original_costs=receipt["original_costs"],
      complete_strata=receipt["complete_strata"],covered_modules=receipt["covered_modules"],
      uncovered_modules=receipt["missing_population_modules"],
      missing_domain_fraction=receipt["missing_population_modules"]/receipt["population_modules"],
      scenario_CPU_h=ranges,computation_share_scenario=[min(shares),max(shares)],
      new_original_module=module,new_original_status=status,new_original_CPU_s=observed["cpu_s"],
      raw_point=str(point),scenario_is_CI=False,actual_whole_library=False,
      audit="automatic provenance checks passed; thread scientific self-review remains separate")
    dump(out/"snapshot.json",snapshot)
    dump(out/"terminal.json",json.loads((point/("terminal.json"if(point/"terminal.json").exists()else"preparation-terminal.json")).read_text()))
    (out/"README.md").write_text(
      "# Fixed original sample update\n\n"+
      "This is an execution snapshot, with raw point and coverage in snapshot.json. "+
      "All completed baseline values are unchanged. No dependency receives a sample weight. "+
      "Source CPU is user+system; no -M; authored/native heartbeats; three output facets. "+
      "E-core prerequisite preparation is untimed and excluded.\n\n"+
      "The full-frame min/max envelope is a missing-cost/transfer scenario, not a confidence "+
      "interval or measured whole-library cost. Serial and parallel checker costs are closure-factor "+
      "transfers; parallel CPU can increase while elapsed falls. Static computation labels are proxies. "+
      "Non-completed attempts are not imputed, and operational failure does not prove a false goal.\n\n"+
      "Automated checks are not an independent review or paper acceptance. "+
      "This thread reviews native outcomes and final interpretation separately.\n")
    event(dict(event="original_recorded",output=str(out),**snapshot))
    return out

def publish(out,module):
    mainbranch()
    paths=[str(out.relative_to(R))]
    subprocess.run(["git","add","--",*paths],cwd=R,check=True)
    identity=subprocess.check_output(["git","show","-s","--format=%an%n%ae","7930025"],cwd=R,text=True).splitlines()
    subprocess.run(["git","-c","user.name="+identity[0],"-c","user.email="+identity[1],
                    "commit","--only","-m","workloads: record fixed original "+module.rsplit(".",1)[-1],*paths],
                   cwd=R,check=True)
    helper="!f() { echo username=x-access-token; echo password=$GH_TOKEN; }; f"
    git=["git","-c","credential.helper=","-c","credential.helper="+helper]
    # Never rebase other sessions' unpublished commits, stash their changes,
    # or force a push. An ordinary push may include their existing commits.
    fetch=subprocess.run([*git,"fetch","origin","main"],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if fetch.returncode:raise RuntimeError("fetch failed; local result preserved")
    ancestor=subprocess.run(["git","merge-base","--is-ancestor","origin/main","HEAD"],cwd=R)
    if ancestor.returncode:raise RuntimeError("origin advanced nonlinearly; do not rebase coauthor work")
    pull=subprocess.run([*git,"-c","rebase.autostash=false","pull","--rebase","origin","main"],
                        cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if (R/".git/rebase-merge").exists()or(R/".git/rebase-apply").exists():
        subprocess.run(["git","rebase","--abort"],cwd=R,check=True)
        raise RuntimeError("rebase conflict; aborted without rewriting coauthors")
    mainbranch()
    # Foreign dirty files may reject pull even when origin is already ancestor.
    if pull.returncode and subprocess.run(["git","merge-base","--is-ancestor","origin/main","HEAD"],cwd=R).returncode:
        raise RuntimeError("pull failed and upstream no longer ancestor")
    push=subprocess.run([*git,"push","origin","main"],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if push.returncode:raise RuntimeError("ordinary push failed; preserve local commit and inspect")
    event(dict(event="published",module=module,output=str(out),commit=subprocess.check_output(
        ["git","rev-parse","HEAD"],cwd=R,text=True).strip()))
def main():
    global A
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--frame",type=Path,required=True)
    ap.add_argument("--attach-preparation",type=Path,required=True)
    ap.add_argument("--raw",type=Path,required=True)
    A=ap.parse_args()
    assert A.raw.exists()and not(A.raw/"progress.jsonl").exists()
    os.sched_setaffinity(0,set(range(8,16)));mainbranch()
    records=baseline_records()
    frame=readcsv(A.frame)
    assert len(frame)==42 and 0<sum(r["status"]=="completed_cost"for r in frame)<42
    seeds=[s for s in readcsv(F/"six-prepared.csv") if next(r for r in frame if r["module"]==s["module"])["status"]!="completed_cost"]
    attachplan=json.loads((A.attach_preparation/"plan.json").read_text())
    attach=next(c["module"]for c in attachplan["cases"]if c["role"]=="original_probability_sample")
    seeds.sort(key=lambda r:r["module"]!=attach)  # Existing active preparation first.
    for s in seeds:
        module=s["module"]
        assert next(r for r in frame if r["module"]==module)["status"]!="completed_cost"
        seed=Path(s["point"])
        prep=A.attach_preparation if module==attach else make_prep(seed,module)
        terminal=wait_owner(prep,True)
        if not terminal["all_original_deps_ready"]:
            row=dict(module=module,status="dependency_preparation_blocked",native_invoked=False,
                     raw=str(prep),reason=terminal["stop"])
            point=prep
        else:
            point=make_timed(prep,seed,module);wait_owner(point,False)
            rows=[json.loads(x)for x in(point/"results.jsonl").read_text().splitlines()]
            assert len(rows)==1 and rows[0]["module"]==module
            row=rows[0]
            assert row["native_retired"]and row["cgroup_retired"]and row["source_exact"]
            assert row["threads"]==8 and row["pcore_lock"]and row["lean_memory_option_MiB"]==0
        records.append(row)
        out=analyze(records,module,point,row["status"])
        publish(out,module)
    dump(A.raw/"collection-terminal.json",dict(utc=utc(),all_planned_remaining_attempts_returned=True,planned_remaining_attempts=len(seeds),
        completed_originals=sum(x.get("status")=="compile_ok"for x in records),
        note="missing/dependency failures have no completed cost; thread must inspect final outcomes"))
    event(dict(event="collection_complete"))
if __name__=="__main__":
    main()
