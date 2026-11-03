#!/usr/bin/env python3
"""Export only the frozen twelve observed responses, without imputing failures."""
import argparse
import csv
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
COLUMNS = ["module", "stratum", "seed", "position", "status", "completed_cost",
           "user_cpu_s", "system_cpu_s", "cpu_s", "wall_s", "source_reference"]

def read(p):
    with p.open(newline="") as f:
        return list(csv.DictReader(f))
def eligible(r):
    return (r.get("status")=="compile_ok" and r.get("threads")==8 and
        r.get("lean_memory_option_MiB")==0 and r.get("profiled") is False and
        r.get("pcore_lock") is True and r.get("source_exact") is True and
        r.get("native_retired") is True and r.get("cgroup_retired") is True and
        r.get("heartbeat_budget")=="authored_or_native_default" and
        r.get("compilation_outputs")=="olean_ilean_c")
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--results", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=HERE)
    a = ap.parse_args()
    design = read(HERE/"precision-design.csv")
    inputs = [json.loads(x) for x in a.results.read_text().splitlines()]
    expected = {r["module"] for r in design}
    assert len(expected)==12 and {r["module"] for r in inputs} <= expected
    output = []
    for draw in design:
        attempts = [r for r in inputs if r["module"]==draw["module"]]
        r = next((r for r in attempts if eligible(r)), attempts[-1] if attempts else {})
        good = eligible(r)
        user, system = r.get("user_cpu_s"), r.get("system_cpu_s")
        output.append(dict(module=draw["module"], stratum=draw["stratum"],
            seed=draw["seed"], position=draw["position"], status=r.get("status", "unmeasured"),
            completed_cost=good, user_cpu_s=user if user is not None else "",
            system_cpu_s=system if system is not None else "",
            cpu_s=user+system if user is not None and system is not None else "",
            wall_s=r.get("wall_s", ""), source_reference=str(r.get("raw", "")).split("/workloads/",1)[-1]))
    a.out.mkdir(parents=True, exist_ok=True)
    with (a.out/"precision-costs.csv").open("w",newline="") as f:
        w = csv.DictWriter(f,fieldnames=COLUMNS,lineterminator="\n")
        w.writeheader();w.writerows(output)
    print("completed costs", sum(r["completed_cost"] for r in output), "/12;",
          "other clocks, if present, describe incomplete/failed attempts and are excluded from estimates")
if __name__=="__main__":
    main()
