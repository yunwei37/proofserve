#!/usr/bin/env python3
"""Read the public CSV bundle without Workspace paths or third-party packages."""
import argparse
import csv
import json
import statistics
from pathlib import Path
HERE = Path(__file__).resolve().parent

def read(p):
    with p.open(newline="") as f:
        return list(csv.DictReader(f))

def summarize(directory):
    strata = read(directory/"strata.csv")
    sample = read(directory/"sample-costs.csv")
    cells, missing = [], []
    for h in strata:
        matches = [r for r in sample if r["stratum"] == h["stratum"]]
        if len(matches) != int(h["sample_size"]):
            raise ValueError("sample identity count does not match stratum " + h["stratum"])
        values = [float(r["cpu_s"]) for r in matches if r["status"] == "completed_cost"]
        if len(values) != len(matches):
            missing.append(h["stratum"])
            continue
        N, n = int(h["population_modules"]), len(values)
        cells.append(dict(stratum=h["stratum"], domain=h["regime_proxy"], population_modules=N,
            estimate_cpu_h=N*statistics.mean(values)/3600,
            variance_cpu_s2=N*N*(1-n/N)*statistics.variance(values)/n if n < N else 0))
    by_domain = {}
    for name in ["all", "ordinary_mathematics", "computation_certificate"]:
        members = [r for r in cells if name == "all" or r["domain"] == name]
        by_domain[name] = dict(covered_population_modules=sum(r["population_modules"] for r in members),
            covered_cell_build_CPU_h=sum(r["estimate_cpu_h"] for r in members),
            estimated_variance_CPU_s2=sum(r["variance_cpu_s2"] for r in members))
    return dict(schema="proofserve-openai-math-summary/v1",
        population_modules=sum(int(h["population_modules"]) for h in strata),
        original_draws=len(sample), completed_costs=sum(r["status"]=="completed_cost" for r in sample),
        missing_strata=missing, estimates=by_domain,
        sampling_intervals=read(directory/"sampling-intervals.csv"),
        scenario_ranges=read(directory/"scenario-ranges.csv"),
        limits=["Incomplete strata are excluded from covered-cell estimates, never imputed.",
                "Published nominal sampling intervals hold transfer factors fixed; scenarios are not confidence intervals.",
                "Checker CPU is a closure-factor transfer, not actual whole-library checking."])

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", type=Path, default=HERE)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    result = summarize(a.data)
    if a.json:
        print(json.dumps(result, indent=2))
    else:
        print(f'{result["completed_costs"]}/{result["original_draws"]} original completed costs; '
              f'{len(result["missing_strata"])} incomplete strata.')
        for domain, row in result["estimates"].items():
            print(f'{domain}: {row["covered_cell_build_CPU_h"]:.6f} CPU h '
                  f'over {row["covered_population_modules"]} covered modules.')
        print("Sampling intervals and transfer scenarios are separate CSVs; neither is a whole-library census.")
if __name__ == "__main__":
    main()
