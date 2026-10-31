#!/usr/bin/env python3
"""Analyze complete matched memory-option cells; missing strata stay missing."""
import argparse
import csv
import filecmp
import json
from pathlib import Path
import statistics
import sys
sys.path.insert(0, "/workspaces/.agent-state/gpu-smt-captures/workloads/statistics-python-deps")
from scipy import stats


def write_csv(path, rows):
    if not rows:
        return
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--point", type=Path, required=True)
    ap.add_argument("--strata", type=Path, required=True)
    ap.add_argument("--end", type=int, default=26)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    plan = json.loads((args.point / "plan.json").read_text())
    rows = []
    controls = []
    for i, case in enumerate(plan["cases"][:args.end]):
        results = {}
        commands = {}
        for arm in ["M", "noM"]:
            d = args.point / "runs" / (str(i).zfill(2) + "-" + arm)
            results[arm] = json.loads((d / "result.json").read_text())
            commands[arm] = json.loads((d / "command.json").read_text())
            cleanup = json.loads((d / "cleanup.json").read_text())
            assert cleanup["cgroup_removed"] and cleanup["stop_reason"] is None
            assert results[arm]["native_retired"] and results[arm]["cgroup_retired"]
        a, b = results["M"], results["noM"]
        ca, cb = commands["M"], commands["noM"]
        same_args = [x for x in a["args"] if not x.startswith("-M")] == b["args"]
        native_equal = a["status"] == b["status"] and a["returncode"] == b["returncode"]
        da = args.point / "runs" / (str(i).zfill(2) + "-M")
        db = args.point / "runs" / (str(i).zfill(2) + "-noM")
        art_a = {p.name: p for p in (da / "artifacts").iterdir()}
        art_b = {p.name: p for p in (db / "artifacts").iterdir()}
        same_set = art_a.keys() == art_b.keys()
        artifacts_equal = same_set and all(filecmp.cmp(p, art_b[n], shallow=False) for n, p in art_a.items())
        diag_equal = (da / "native.log").read_bytes() == (db / "native.log").read_bytes()
        cpu_a, cpu_b = a["user_cpu_s"] + a["system_cpu_s"], b["user_cpu_s"] + b["system_cpu_s"]
        cost_valid = a["status"] == b["status"] == "compile_ok"
        row = dict(index=i, module=case["module"], stratum=case["stratum"], role=case["role"],
          M_status=a["status"], noM_status=b["status"], verdict_equal=native_equal,
          diagnostic_bytes_equal=diag_equal, artifact_bytes_equal=artifacts_equal,
          native_args_only_M_different=same_args, env_equal=ca["env"] == cb["env"],
          self_wall_equal=ca["self_wall_s"] == cb["self_wall_s"],
          M_self_wall_s=ca["self_wall_s"], noM_self_wall_s=cb["self_wall_s"],
          M_wall_s=a["wall_s"], noM_wall_s=b["wall_s"], M_CPU_s=cpu_a, noM_CPU_s=cpu_b,
          M_system_s=a["system_cpu_s"], noM_system_s=b["system_cpu_s"],
          M_over_noM_wall=a["wall_s"]/b["wall_s"] if cost_valid else None,
          M_over_noM_CPU=cpu_a/cpu_b if cost_valid else None,
          M_peak_rss_kib=a["peak_rss_kib"], noM_peak_rss_kib=b["peak_rss_kib"],
          M_cgroup_peak_bytes=a["cgroup_memory_peak_bytes"],
          noM_cgroup_peak_bytes=b["cgroup_memory_peak_bytes"],
          M_voluntary_switches=a["voluntary_switches"],
          noM_voluntary_switches=b["voluntary_switches"],
          complete_cost_pair=cost_valid)
        rows.append(row)
        controls.append(dict(index=i, module=case["module"], settings=ca["cgroup_settings"],
          M_events=a["cgroup_memory_events"], noM_events=b["cgroup_memory_events"]))
    populations = {";".join([x["size_percentile_bin"], x["import_depth_bin"], x["has_decide_kernel"]]):
                   int(x["population_modules"]) for x in csv.DictReader(args.strata.open())}
    strata = []
    for h in sorted({x["stratum"] for x in rows if x["role"] == "original_probability_sample"}):
        observed = [x for x in rows if x["stratum"] == h and x["complete_cost_pair"]]
        n, N = len(observed), populations[h]
        y = [x["M_CPU_s"] for x in observed]
        z = [x["noM_CPU_s"] for x in observed]
        delta = [a-b for a,b in zip(y,z)]
        complete = n == min(2, N)
        variance = N*N*(1-n/N)*statistics.variance(delta)/n if n > 1 else (0 if n == N else None)
        ci_half = float(stats.t.ppf(.975, n-1)) * variance**.5 / 3600 if complete and n > 1 else (0 if n == N else None)
        difference_h = N*statistics.mean(delta)/3600 if complete else None
        strata.append(dict(stratum=h, population_modules=N, paired_modules=n,
          original_two_draw_cell_complete=complete,
          mean_M_CPU_s=statistics.mean(y) if n else None,
          mean_noM_CPU_s=statistics.mean(z) if n else None,
          M_over_noM_CPU=sum(y)/sum(z) if n else None,
          estimated_cell_M_CPU_h=N*statistics.mean(y)/3600 if complete else None,
          estimated_cell_noM_CPU_h=N*statistics.mean(z)/3600 if complete else None,
          estimated_cell_CPU_difference_h=N*statistics.mean(delta)/3600 if complete else None,
          paired_difference_variance_s2=variance,
          nominal95_difference_low_h=difference_h-ci_half if ci_half is not None else None,
          nominal95_difference_high_h=difference_h+ci_half if ci_half is not None else None))
    valid = [x for x in rows if x["complete_cost_pair"] and x["role"] == "original_probability_sample"]
    complete = [x for x in strata if x["original_two_draw_cell_complete"]]
    v = sum(x["paired_difference_variance_s2"] for x in complete)
    terms = [x["paired_difference_variance_s2"]**2/(x["paired_modules"]-1) for x in complete if x["paired_modules"]>1]
    df = v*v/sum(terms) if sum(terms)>0 else None
    half = float(stats.t.ppf(.975, df))*v**.5/3600 if df is not None else 0
    diff = sum(x["estimated_cell_CPU_difference_h"] for x in complete)
    summary = dict(nominal95_complete_strata_difference_low_h=diff-half,
        nominal95_complete_strata_difference_high_h=diff+half,
        nominal95_df=df, interval_assumptions="conditional on completed strata; normal-cost/t approximation; two draws/cell; does not cover nonresponse or systematic runtime variation",
        planned_cases=args.end, actual_pairs=len(rows), completed_cost_pairs=len(valid),
        verdicts_all_equal=all(x["verdict_equal"] for x in rows),
        diagnostics_all_byte_equal=all(x["diagnostic_bytes_equal"] for x in rows),
        artifacts_all_byte_equal=all(x["artifact_bytes_equal"] for x in rows),
        native_args_only_M_different=all(x["native_args_only_M_different"] for x in rows),
        environments_all_equal=all(x["env_equal"] for x in rows),
        self_wall_all_equal=all(x["self_wall_equal"] for x in rows),
        observed_sample_M_CPU_s=sum(x["M_CPU_s"] for x in valid),
        observed_sample_noM_CPU_s=sum(x["noM_CPU_s"] for x in valid),
        observed_sample_M_wall_s=sum(x["M_wall_s"] for x in valid),
        observed_sample_noM_wall_s=sum(x["noM_wall_s"] for x in valid),
        completed_original_strata=len(complete), total_original_strata=len(populations),
        complete_strata_population=sum(x["population_modules"] for x in complete),
        complete_strata_M_CPU_h=sum(x["estimated_cell_M_CPU_h"] for x in complete),
        complete_strata_noM_CPU_h=sum(x["estimated_cell_noM_CPU_h"] for x in complete),
        complete_strata_CPU_difference_h=sum(x["estimated_cell_CPU_difference_h"] for x in complete),
        whole_library_cost=None, whole_library_correction=None,
        scope="fresh paired ready A26; hard original draws missing; purposeful heavy cases excluded from population weighting")
    args.out.mkdir(parents=True, exist_ok=True)
    write_csv(args.out / "paired-modules.csv", rows)
    write_csv(args.out / "paired-strata.csv", strata)
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    (args.out / "cgroup-controls.json").write_text(json.dumps(controls, indent=2)+"\n")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
