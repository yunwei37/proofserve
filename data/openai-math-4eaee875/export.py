#!/usr/bin/env python3
"""Export small, stable v1 tables from a completed/provisional original42 frame."""
import argparse
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COST_COLUMNS = ["module", "stratum", "population_modules", "sample_size",
    "inclusion_probability", "expansion_weight", "regime_proxy", "status",
    "user_cpu_s", "system_cpu_s", "cpu_s", "wall_s", "source_bytes",
    "memory_option_MiB", "threads", "pcore_lock", "source_exact",
    "native_retired", "cgroup_retired", "source_reference"]
STRATA_COLUMNS = ["stratum", "population_modules", "sample_size",
                  "inclusion_probability", "expansion_weight", "regime_proxy"]
def rows(p):
    with p.open(newline="") as f:
        return list(csv.DictReader(f))
def write(p, values, columns):
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        w.writeheader()
        w.writerows(values)
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--frame", type=Path, required=True)
    ap.add_argument("--staircase", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=HERE)
    a = ap.parse_args()
    strata = []
    for r in rows(ROOT / "workloads/openai-math/build-planning-4eaee875/strata.csv"):
        h = ";".join(r[k] for k in ["size_percentile_bin", "import_depth_bin", "has_decide_kernel"])
        N, n = int(r["population_modules"]), int(r["sample_modules"])
        strata.append(dict(stratum=h, population_modules=N, sample_size=n,
            inclusion_probability=n/N, expansion_weight=N/n,
            regime_proxy="computation_certificate" if h.endswith(";1") else "ordinary_mathematics"))
    mapping = {r["stratum"]: r for r in strata}
    frame = rows(a.frame)
    assert len(frame) == 42 and len({r["module"] for r in frame}) == 42
    output = []
    for r in frame:
        s = mapping[r["stratum"]]
        row = {k: s[k] for k in STRATA_COLUMNS}
        row.update(module=r["module"], status=r["status"])
        for k in COST_COLUMNS:
            row.setdefault(k, "")
        if r["status"] == "completed_cost":
            file = Path(r["source_file"])
            native = json.loads(file.read_text().splitlines()[int(r["source_line"])-1])
            assert native["module"] == r["module"]
            assert native["status"] == "compile_ok" and native["native_retired"] and native["cgroup_retired"]
            assert native["source_exact"] and native["pcore_lock"] and not native["profiled"]
            assert native["lean_memory_option_MiB"] == 0 and native["threads"] == 8
            assert native["heartbeat_budget"] == "authored_or_native_default"
            assert native["compilation_outputs"] == "olean_ilean_c"
            assert abs(float(r["cpu_s"])-native["user_cpu_s"]-native["system_cpu_s"]) < 1e-7
            for k in ["user_cpu_s", "system_cpu_s", "wall_s", "threads",
                      "pcore_lock", "source_exact", "native_retired", "cgroup_retired"]:
                row[k] = native[k]
            row["cpu_s"] = native["user_cpu_s"] + native["system_cpu_s"]
            row["memory_option_MiB"] = 0
            row["source_reference"] = native["raw"].split("/workloads/", 1)[-1]
            source = Path(native["args"][-1])
            row["source_bytes"] = source.stat().st_size if source.exists() else ""
        output.append(row)
    a.out.mkdir(parents=True, exist_ok=True)
    write(a.out / "sample-costs.csv", output, COST_COLUMNS)
    write(a.out / "strata.csv", strata, STRATA_COLUMNS)
    for src, dst in [("calibration.csv", "closure-ratios.csv"),
                     ("conditional-staircase.csv", "sampling-intervals.csv"),
                     ("full-frame-scenario-envelope.csv", "scenario-ranges.csv")]:
        raw = rows(a.staircase / src)
        # Native CPU is the primary estimand; no wall/CPU conversion.
        if src == "conditional-staircase.csv":
            raw = [r for r in raw if r["clock"] == "CPU_h"]
        write(a.out / dst, raw, list(raw[0]))
    metadata = dict(schema="proofserve-openai-math-costs/v1", upstream="https://github.com/openai/math",
        commit="4eaee87548250b2682affda7d05d947c05554bae", population_modules=163097,
        lean="4.34.1", mathlib="d13f23b723b8a846827a245b89c10fc7d3f11612",
        original_sample_size=42, completed_original_costs=sum(r["status"]=="completed_cost" for r in frame),
        missing_original_costs=sum(r["status"]!="completed_cost" for r in frame),
        sampling_seed=20261030, source_frame=a.frame.relative_to(ROOT).as_posix(),
        source_staircase=a.staircase.relative_to(ROOT).as_posix(),
        primary_clock="native user + system CPU seconds", memory_option_MiB=0,
        scope="per-module native compile incl imports and olean/ilean/C; not whole Lake build",
        checker_numbers="fixed selected-closure transfers, not actual whole-library verification",
        classifications="lexical any decide +kernel, not runtime cost ground truth",
        interval_scope="source sampling with fixed transfer factors; calibration/model uncertainty excluded",
        scenario_scope="missing-cost class min/max and selected closure factor sensitivity, not CI")
    (a.out/"metadata.json").write_text(json.dumps(metadata, indent=2)+"\n")
    print(json.dumps(metadata, indent=2))
if __name__ == "__main__":
    main()
