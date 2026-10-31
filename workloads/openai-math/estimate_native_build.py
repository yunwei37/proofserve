#!/usr/bin/env python3
"""Conditional stratified native compilation CPU estimate, with explicit nonresponse."""
import argparse
import csv
import json
import math
import statistics
from collections import Counter
from pathlib import Path

STRATUM_FIELDS = ("size_percentile_bin", "import_depth_bin", "has_decide_kernel")


def stratum_estimate(population, planned_n, values):
    """Return HT total and finite-population variance only for a complete cell."""
    if not 0 < planned_n <= population:
        raise ValueError("invalid population/sample counts")
    if len(values) != planned_n:
        return None, None
    total = population * statistics.mean(values)
    if planned_n == population:
        return total, 0.0
    if planned_n < 2:
        return total, None
    variance = (population**2 * (1 - planned_n / population)
                * statistics.variance(values) / planned_n)
    return total, variance


def confidence_interval(cells, confidence=0.95):
    """Approximate stratified t interval; not a distribution-free tail bound."""
    if any(c["estimate"] is None or c["variance"] is None for c in cells):
        return None
    estimate = sum(c["estimate"] for c in cells)
    variance = sum(c["variance"] for c in cells)
    denominator = sum(c["variance"]**2 / (c["sample_n"] - 1)
                      for c in cells if c["variance"] > 0)
    dof = variance**2 / denominator if denominator else math.inf
    from scipy.stats import norm, t
    critical = (float(t.ppf((1 + confidence) / 2, dof))
                if math.isfinite(dof) else float(norm.ppf((1 + confidence) / 2)))
    margin = critical * math.sqrt(variance)
    return {"estimate_cpu_h": estimate / 3600,
            "lower_cpu_h": max(0, estimate - margin) / 3600,
            "upper_cpu_h": (estimate + margin) / 3600,
            "estimated_variance_cpu_s2": variance,
            "satterthwaite_dof": dof,
            "confidence": confidence}


def write_csv(path, rows):
    if not rows:
        return
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", type=Path, required=True)
    parser.add_argument("--strata", type=Path, required=True)
    parser.add_argument("--results", type=Path, nargs="+", required=True,
                        help="chronological files from the same pinned SDK/library")
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--heartbeat-budget", default="100000")
    parser.add_argument("--memory-mib", type=int, default=0,
                        help="current timing omits -M (0); nonzero is legacy methodology only")
    parser.add_argument("--outputs", default="olean_only",
                        help="output artifact mode; legacy W captures emit only .olean")
    parser.add_argument("--locked-only", action="store_true",
                        help="exclude observations before shared P-core serialization")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    targets = [r for r in csv.DictReader(args.targets.open())
               if r["role"] == "probability_sample"]
    if len({r["module"] for r in targets}) != len(targets):
        raise ValueError("duplicate probability target")
    strata = list(csv.DictReader(args.strata.open()))
    lookup = {r["module"]: r for r in targets}
    complete, attempts, excluded = {}, {}, Counter()
    for file in args.results:
        for number, line in enumerate(file.read_text().splitlines(), 1):
            row = json.loads(line)
            module = row.get("module")
            if module not in lookup:
                continue
            if row.get("native_invoked") is False:
                attempts[module] = row["status"]
                excluded["not_invoked"] += 1
                continue
            point = (row.get("threads") == args.threads
                     and str(row.get("heartbeat_budget")) == args.heartbeat_budget
                     and row.get("lean_memory_option_MiB") == args.memory_mib
                     and row.get("profiled") is False
                     and row.get("compilation_outputs", "olean_only") == args.outputs
                     and (not args.locked_only or row.get("pcore_lock") is True))
            if not point:
                excluded["other_or_unknown_resource_point"] += 1
                continue
            attempts[module] = row["status"]
            if (row["status"] == "compile_ok" and module not in complete
                    and "user_cpu_s" in row and "system_cpu_s" in row):
                complete[module] = dict(
                    cpu_s=row["user_cpu_s"] + row["system_cpu_s"],
                    file=str(file), line=number,
                    sorry_warning=row.get("sorry_warning", "unknown"),
                    pcore_lock=row.get("pcore_lock", False))
    cells, coverage = [], []
    for stratum in strata:
        key = ";".join(stratum[k] for k in STRATUM_FIELDS)
        selected = [r for r in targets if r["stratum"] == key]
        population = int(stratum["population_modules"])
        sample_n = int(stratum["sample_modules"])
        if len(selected) != sample_n:
            raise ValueError("stratum/sample frame disagreement: " + key)
        values = [complete[r["module"]]["cpu_s"] for r in selected
                  if r["module"] in complete]
        estimate, variance = stratum_estimate(population, sample_n, values)
        cells.append(dict(estimate=estimate, variance=variance, sample_n=sample_n))
        cell_interval = confidence_interval([cells[-1]])
        coverage.append(dict(
            stratum=key, population_modules=population,
            planned_sample=sample_n, completed_native_costs=len(values),
            measured_cpu_sum_s=sum(values),
            estimated_stratum_cpu_h="" if estimate is None else estimate / 3600,
            estimated_variance_cpu_s2="" if variance is None else variance,
            nominal_cell95_lower_cpu_h="" if cell_interval is None else cell_interval["lower_cpu_h"],
            nominal_cell95_upper_cpu_h="" if cell_interval is None else cell_interval["upper_cpu_h"],
            interval_scope="complete single stratum only; normal-cost model" if cell_interval else "unavailable: incomplete cell"))
    args.out.mkdir(parents=True, exist_ok=True)
    write_csv(args.out / "stratum-coverage.csv", coverage)
    sample_rows = []
    for row in targets:
        module = row["module"]
        chosen = complete.get(module, {})
        sample_rows.append(dict(
            module=module, stratum=row["stratum"],
            status="completed_cost" if chosen else attempts.get(module, "unmeasured"),
            cpu_s=chosen.get("cpu_s", ""), source_file=chosen.get("file", ""),
            source_line=chosen.get("line", ""), sorry_warning=chosen.get("sorry_warning", ""),
            pcore_lock=chosen.get("pcore_lock", "")))
    write_csv(args.out / "sample-costs.csv", sample_rows)
    interval = confidence_interval(cells) if args.memory_mib == 0 else None
    summary = dict(resource_convention="no_M_outer_cgroup" if args.memory_mib == 0 else "legacy_M_methodology_only",
        scope="conditional internal compiler CPU; output facets explicit; full Lake total unmeasured",
        compilation_outputs=args.outputs,
        population_modules=sum(int(s["population_modules"]) for s in strata),
        planned_probability_samples=len(targets), completed_costs=len(complete),
        complete_cells=sum(c["estimate"] is not None for c in cells),
        strata=len(strata), threads=args.threads, heartbeat_budget=args.heartbeat_budget,
        memory_mib=args.memory_mib,
        status="legacy_methodology_not_population_estimate" if args.memory_mib != 0 else "conditional_approximate_interval" if interval else "not_estimable_incomplete_or_failed_sample",
        estimate_cpu_h="", lower_cpu_h="", upper_cpu_h="",
        excluded_other_point_rows=excluded["other_or_unknown_resource_point"],
        noninvoked_target_records=excluded["not_invoked"],
        locked_only=args.locked_only,
        completed_locked_costs=sum(x["pcore_lock"] is True for x in complete.values()))
    if interval:
        summary.update(interval)
    write_csv(args.out / "summary.csv", [summary])
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
