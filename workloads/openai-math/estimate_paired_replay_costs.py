#!/usr/bin/env python3
"""Paired native source/replay costs on the original finite-population frame."""
import argparse
import collections
import csv
import json
import math
from pathlib import Path
import statistics
import sys

sys.path.insert(0, "/workspaces/.agent-state/gpu-smt-captures/workloads/statistics-python-deps")
from scipy.stats import norm, t


def band(parts):
    """Nominal t interval for a nonnegative total; not a heavy-tail guarantee."""
    total = sum(x[0] for x in parts)
    var = sum(x[1] for x in parts)
    den = sum(x[1] ** 2 / (x[2] - 1) for x in parts if x[1] > 0)
    df = var * var / den if den else math.inf
    critical = float(t.ppf(.975, df)) if math.isfinite(df) else float(norm.ppf(.975))
    margin = critical * math.sqrt(max(0., var))
    return dict(estimate=total, low=max(0., total-margin), high=total+margin,
                variance=var, df=df)


def total_part(N, values):
    n = len(values)
    if n < 2 or n > N:
        raise ValueError("variance requires at least two original draws")
    return (N*statistics.mean(values),
            N*N*(1-n/N)*statistics.variance(values)/n, n)


def paired_band(cells):
    """Paired delta ratio includes the covariance through q-r*b residuals."""
    B = band([total_part(N, [b for b, q in pairs]) for N, pairs in cells])
    Q = band([total_part(N, [q for b, q in pairs]) for N, pairs in cells])
    if B["estimate"] <= 0:
        raise ValueError("positive observed source cost required")
    ratio = Q["estimate"]/B["estimate"]
    residuals = [total_part(N, [q-ratio*b for b, q in pairs]) for N, pairs in cells]
    centered = band([(0., v/B["estimate"]**2, n) for _, v, n in residuals])
    margin = centered["high"]
    return B, Q, dict(estimate=ratio, low=max(0., ratio-margin),
                     high=ratio+margin, variance=centered["variance"],
                     df=centered["df"])


def write_csv(path, rows):
    if not rows:
        return
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--targets", type=Path, required=True)
    p.add_argument("--strata", type=Path, required=True)
    p.add_argument("--source-costs", type=Path, required=True)
    p.add_argument("--replay-results", type=Path, nargs="+", required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    frame = [x for x in csv.DictReader(a.targets.open()) if x["role"]=="probability_sample"]
    assert len(frame)==42 and len({x["module"] for x in frame})==42
    lookup = {x["module"]:x for x in frame}
    strata = {";".join(x[k] for k in ["size_percentile_bin","import_depth_bin","has_decide_kernel"]):x
              for x in csv.DictReader(a.strata.open())}
    source = {}
    for row in csv.DictReader(a.source_costs.open()):
        if row["status"]!="completed_cost":
            continue
        f = Path(row["source_file"])
        x = json.loads(f.read_text().splitlines()[int(row["source_line"])-1])
        assert x["module"] in lookup and x["status"]=="compile_ok"
        assert x["source_exact"] and x["lean_memory_option_MiB"]==0
        assert x["pcore_lock"] and x["threads"]==8 and not x["profiled"]
        assert x["compilation_outputs"]=="olean_ilean_c"
        assert x["heartbeat_budget"]=="authored_or_native_default"
        source[x["module"]] = x
    replay = {}
    attempts = {}
    outcomes = collections.Counter()
    mismatched = []
    for f in a.replay_results:
        for number, line in enumerate(f.read_text().splitlines(),1):
            x = json.loads(line); m = x["module"]
            outcomes[x["status"]]+=1
            attempts[m] = x["status"]
            if m not in lookup or m not in source or x["status"]!="accepted":
                continue
            assert x["operation"]=="kernel_target_replay"
            assert x["compilation_outputs"]=="none_kernel_replay"
            assert x["native_retired"] and x["cgroup_retired"]
            assert x["lean_memory_option_MiB"]==0 and x["source_exact"]
            assert x["pcore_lock"] and x["threads"]==8 and not x["profiled"]
            expected = Path(source[m]["raw"])/"artifacts"
            refs = x.get("matched_artifact_parts",[])
            if not refs or any(Path(z["producer_copy"]).parent!=expected for z in refs):
                mismatched.append(dict(module=m,file=str(f),line=number))
                continue
            if m not in replay:
                replay[m] = dict(x, ledger=str(f), line=number)
    paired = source.keys() & replay.keys()
    members = {h:[x["module"] for x in frame if x["stratum"]==h] for h in strata}
    assert all(len(members[h])==int(strata[h]["sample_modules"]) for h in strata)
    source_h = [h for h in strata if all(m in source for m in members[h])]
    pair_h = [h for h in strata if all(m in paired for m in members[h])]
    observations = []
    for row in frame:
        m = row["module"]; b = source.get(m); q = replay.get(m)
        observations.append(dict(module=m,stratum=row["stratum"],source_CPU_s=b["user_cpu_s"]+b["system_cpu_s"] if b else "",
            replay_CPU_s=q["user_cpu_s"]+q["system_cpu_s"] if q else "",
            source_wall_s=b["wall_s"] if b else "",replay_wall_s=q["wall_s"] if q else "",
            replay_over_source_CPU=(q["user_cpu_s"]+q["system_cpu_s"])/(b["user_cpu_s"]+b["system_cpu_s"]) if b and q else "",
            replay_over_source_wall=q["wall_s"]/b["wall_s"] if b and q else "",
            paired=m in paired,population_weight=1/float(row["inclusion_probability"]) if m in paired else "",
            replay_status=q["status"] if q else attempts.get(m, "unmeasured")))
    summaries = []
    for domain, required in [("all",list(strata)),("certificate_proxy",[h for h in strata if h.endswith(";1")]),
                             ("ordinary_proxy",[h for h in strata if h.endswith(";0")])]:
        complete = [h for h in required if h in pair_h]
        build_complete = [h for h in required if h in source_h]
        cells = [(int(strata[h]["population_modules"]),[(source[m]["user_cpu_s"]+source[m]["system_cpu_s"],
                  replay[m]["user_cpu_s"]+replay[m]["system_cpu_s"]) for m in members[h]]) for h in complete]
        B,Q,R = paired_band(cells) if cells else ({},{},{})
        global_B = band([total_part(int(strata[h]["population_modules"]),
                        [source[m]["user_cpu_s"]+source[m]["system_cpu_s"] for m in members[h]])
                         for h in required]) if len(build_complete)==len(required) else {}
        done = len(complete)==len(required)
        summaries.append(dict(domain=domain,required_strata=len(required),source_complete_strata=len(build_complete),
            paired_complete_strata=len(complete),paired_population_modules=sum(int(strata[h]["population_modules"]) for h in complete),
            missing_source_population_modules=sum(int(strata[h]["population_modules"]) for h in required if h not in source_h),
            missing_paired_population_modules=sum(int(strata[h]["population_modules"]) for h in required if h not in pair_h),
            conditional_source_CPU_h=B.get("estimate",0)/3600 if B else "",
            conditional_replay_CPU_h=Q.get("estimate",0)/3600 if Q else "",
            conditional_replay_over_source_CPU=R.get("estimate",""),
            conditional_ratio95_low=R.get("low",""),conditional_ratio95_high=R.get("high",""),
            global_source_CPU_h=global_B.get("estimate",0)/3600 if global_B else "",
            global_source_CI95_low_h=global_B.get("low",0)/3600 if global_B else "",
            global_source_CI95_high_h=global_B.get("high",0)/3600 if global_B else "",
            global_target_replay_CPU_h=Q["estimate"]/3600 if done else "",
            global_target_replay_CI95_low_h=Q["low"]/3600 if done else "",
            global_target_replay_CI95_high_h=Q["high"]/3600 if done else "",
            global_replay_over_source_CPU=R["estimate"] if done else "",
            global_ratio95_low=R["low"] if done else "",global_ratio95_high=R["high"] if done else "",
            cost_scope="fresh target-only replay; imported environment trusted; not empty-environment streaming verification",
            interval_scope="nominal t/delta model,2draws/cell; no censoring,nonresponse,context or label correction"))
    ratios=[x for x in observations if x["paired"]]
    sb=sum(x["source_CPU_s"] for x in ratios);sq=sum(x["replay_CPU_s"] for x in ratios)
    wb=sum(x["source_wall_s"] for x in ratios);wq=sum(x["replay_wall_s"] for x in ratios)
    observed=dict(pairs=len(ratios),source_CPU_s=sb,replay_CPU_s=sq,replay_over_source_CPU=sq/sb if sb else "",
        source_wall_s=wb,replay_wall_s=wq,replay_over_source_wall=wq/wb if wb else "",
        median_module_CPU_ratio=statistics.median(x["replay_over_source_CPU"] for x in ratios) if ratios else "",
        median_module_wall_ratio=statistics.median(x["replay_over_source_wall"] for x in ratios) if ratios else "",
        scope="unweighted observed pairs,not population cost or parallel makespan")
    a.out.mkdir(parents=True,exist_ok=False)
    write_csv(a.out/"paired-modules.csv",observations)
    write_csv(a.out/"domain-costs.csv",summaries)
    write_csv(a.out/"observed-pairs.csv",[observed])
    (a.out/"receipt.json").write_text(json.dumps(dict(source_costs=len(source),accepted_replays=len(replay),
        paired_costs=len(paired),planned_costs=42,complete_paired_cells=len(pair_h),population_cells=21,
        statuses=dict(outcomes),mismatched_producer_references=mismatched,
        all_strata_cost_covered=len(pair_h)==21,is_full_library_acceptance=False,review="self-review; actual ledger only"),indent=2)+"\n")
    print(json.dumps(observed))
    print(json.dumps(summaries))


if __name__=="__main__":
    main()
