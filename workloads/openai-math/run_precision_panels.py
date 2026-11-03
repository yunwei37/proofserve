#!/usr/bin/env python3
"""Finite execution of the two fixed independent six-draw panels."""
import argparse,csv,json,os,shutil,subprocess,sys
from pathlib import Path
from types import SimpleNamespace
import complete_source_sample as core

R=core.R
B=core.B
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--frame",type=Path,required=True)
    ap.add_argument("--prepared",type=Path,required=True)
    ap.add_argument("--raw",type=Path,required=True)
    a=ap.parse_args()
    frame=core.readcsv(a.frame)
    assert len(frame)==42 and all(x["status"]=="completed_cost"for x in frame)
    assert a.raw.exists()and not(a.raw/"progress.jsonl").exists()
    jobs=json.loads((a.prepared/"jobs.json").read_text())
    assert len(jobs)==12 and len({j["module"]for j in jobs})==12
    targets=R/"workloads/openai-math/precision-noM-two-strata-20261103/targets.csv"
    design=core.readcsv(targets)
    assert {j["module"]for j in jobs}=={j["module"]for j in design}
    os.sched_setaffinity(0,set(range(8,16)))
    core.A=SimpleNamespace(raw=a.raw,attach_preparation=a.prepared,frame=a.frame)
    records=[]
    for i,j in enumerate(jobs):
        module=j["module"]; seed=Path(j["point"])
        prep=core.make_prep(seed,module)
        terminal=core.wait_owner(prep,True)
        if not terminal["all_original_deps_ready"]:
            row=dict(module=module,stratum=j["stratum"],status="dependency_preparation_blocked",
                native_invoked=False,raw=str(prep),reason=terminal["stop"],
                sampling_design="conditional_remainder_sample")
            point=prep
        else:
            point=core.make_timed(prep,seed,module)
            core.wait_owner(point,False)
            rows=[json.loads(x)for x in(point/"results.jsonl").read_text().splitlines()]
            assert len(rows)==1 and rows[0]["module"]==module
            row=rows[0]
            assert row["native_retired"]and row["cgroup_retired"]and row["source_exact"]
        records.append(row)
        ledger=a.raw/"panel-results.jsonl"
        ledger.write_text("".join(json.dumps(x)+"\n"for x in records))
        out=R/"workloads/openai-math/precision-noM-two-strata-20261103"/a.raw.name/(
            str(i+1).zfill(2)+"-"+module.rsplit(".",1)[-1])
        out.mkdir(parents=True)
        env=os.environ.copy()
        env["PYTHONPATH"]=str(B/"statistics-python-deps")
        env["PYTHONDONTWRITEBYTECODE"]="1"
        with(a.raw/(str(i+1).zfill(2)+"-analysis.log")).open("w")as f:
            subprocess.run([sys.executable,str(R/"workloads/openai-math/analyze_precision.py"),
                "--frame",str(a.frame),"--targets",str(targets),"--results",str(ledger),
                "--out",str(out)],cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
        core.dump(out/"new-return.json",row)
        core.dump(out/"native-terminal.json",terminal if point==prep else
            json.loads((point/"terminal.json").read_text()))
        (out/"README.md").write_text(
            "# Fixed conditional-panel return\n\n"
            "Pinned independent remainder draw; no original42 HT weight is changed. "
            "Partial panels retain their original cell estimate until all six costs return. "
            "See receipt.json for native response coverage and nominal-interval limitations. "
            "Ordinary failures, censors and dependency blockers are retained without imputation. "
            "Source CPU excludes E-core preparation and queue/setup/cleanup.\n")
        core.event(dict(event="conditional_recorded",output=str(out),module=module,status=row["status"]))
        core.publish(out,module,"workloads: record conditional draw "+module.rsplit(".",1)[-1])
    core.dump(a.raw/"collection-terminal.json",dict(utc=core.utc(),
        planned_attempts=12,returned_attempts=len(records),
        completed_costs=sum(x["status"]=="compile_ok"for x in records),
        scope="two fixed six-draw independent conditional remainder panels",
        all_planned_attempts_returned=True))
if __name__=="__main__":
    main()
