#!/usr/bin/env python3
"""Prepare immutable conditional-panel plans; never launch Lean."""
import argparse,copy,csv,json,shutil
from pathlib import Path
from plan_build import load,closure
R=Path("/workspaces/repository")
B=Path("/workspaces/.agent-state/gpu-smt-captures/workloads")
A=Path("/workspaces/.agent-state/gpu-smt-workloads")

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    assert not a.out.exists()
    a.out.mkdir()
    panel=R/"workloads/openai-math/precision-noM-two-strata-20261103"
    rows=list(csv.DictReader((panel/"targets.csv").open()))
    profiles,modules,deps,external,reverse,order,depth=load(R/"workloads/openai-math/static-4eaee875")
    base=B/"openai4341-noM-final-AllocatedForecastPrimitiveCapBound-prepared-20261102"
    original=json.loads((base/"plan.json").read_text())
    template=original["cases"][-1]
    roots=json.loads((R/"workloads/openai-math/static-4eaee875/content/summary.json").read_text())["import_graph"]["source_roots"]
    snapshot=B/"precision-noM-two-strata-20261103/source-replay"
    helper=B/"openai4341-Eprep-AllocatedForecastPrimitiveCapBound-after-reboot-20261103T1507/prepare_dependencies.py"
    text=helper.read_text()
    # Keep the same implementation, add only the new leaf role to exclusion.
    text=text.replace('c["role"]=="original_probability_sample"',
                      'c["role"]in {"original_probability_sample","conditional_remainder_sample"}')
    assert text!=helper.read_text()
    (a.out/"prepare_dependencies.py").write_text(text)
    shutil.copyfile(base/"runner.py",a.out/"runner.py")
    controller=(base/"controller.py").read_text()
    controller=controller.replace('case["role"] == "original_probability_sample"',
                                  'case["role"] in {"original_probability_sample","conditional_remainder_sample"}')
    controller=controller.replace('result["probability_sample_target"] = case["role"] in {"original_probability_sample","conditional_remainder_sample"}',
        'result["probability_sample_target"] = True\n            result["sampling_design"] = case["role"]')
    (a.out/"controller.py").write_text(controller)
    # Qualified initial list is refreshed again after original42 completes.
    candidates=set(original["initial_ready"])
    for point in B.glob("openai4341-Eprep-*"):
        ledger=point/"preparation-results.jsonl"
        if not ledger.exists():continue
        for line in ledger.read_text().splitlines():
            x=json.loads(line)
            if x["status"]=="compile_ok" and x["native_retired"] and x["cgroup_retired"]:
                candidates.add(x["module"])
    candidates={m for m in candidates if (A/"openai4341-oleans").joinpath(*m.split(".")).with_suffix(".olean").exists()
        or (A/"rellich4341-oleans").joinpath(*m.split(".")).with_suffix(".olean").exists()}
    jobs=[]
    for row in rows:
        leaf=row["module"]
        needed=closure([leaf],deps)
        p=a.out/("panel-"+str(row["seed"])+"-"+row["position"])
        p.mkdir()
        cases=[]
        for m in order:
            if m not in needed:continue
            meta={"path":modules[m]}
            source=snapshot/meta["path"]
            pinned=A/"openai-math-4eaee875"/meta["path"]
            assert source.read_bytes()==pinned.read_bytes()
            root=max((x for x in roots if str(meta["path"]).startswith(x+"/")),key=len)
            c=copy.deepcopy(template)
            c.update(module=m,path=meta["path"],stratum=row["stratum"] if m==leaf else "dependency_not_population_sample",
                role="conditional_remainder_sample" if m==leaf else "dependency",
                pinned_source=str(pinned),cwd=str(snapshot),deps=sorted(deps[m]),self_wall_s=1200)
            c["args"]=[template["args"][0],"--root="+str(snapshot/root),"-j8","-DautoImplicit=false",
                "-o",str(p/"working"/str(len(cases))/(source.stem+".olean")),
                "-i",str(p/"working"/str(len(cases))/(source.stem+".ilean")),
                "-c",str(p/"working"/str(len(cases))/(source.stem+".c")),str(source)]
            assert not any(x.startswith("-M")for x in c["args"])
            cases.append(c)
        assert cases and cases[-1]["module"]==leaf
        (p/"plan.json").write_text(json.dumps(dict(cases=cases,initial_ready=sorted(candidates),
            original=leaf,scope="independent conditional remainder; no original42 weight; not launched"),indent=2)+"\n")
        for f in ["runner.py","controller.py","prepare_dependencies.py"]:
            shutil.copyfile(a.out/f,p/f)
        jobs.append(dict(module=leaf,stratum=row["stratum"],position=int(row["position"]),
            seed=int(row["seed"]),point=str(p),closure_modules=len(cases),
            missing_dependencies=sum(c["module"]not in candidates and c["module"]!=leaf for c in cases)))
    (a.out/"jobs.json").write_text(json.dumps(jobs,indent=2)+"\n")
    print(json.dumps(dict(prepared_jobs=len(jobs),native_started=0,points=[j["point"]for j in jobs])))
if __name__=="__main__":
    main()
