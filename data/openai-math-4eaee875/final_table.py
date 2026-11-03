#!/usr/bin/env python3
"""Final original42/conditional-panel CPU tables; SciPy only for t quantiles."""
import argparse
import csv
import math
import statistics
from pathlib import Path
HERE = Path(__file__).resolve().parent

def read(p):
    with p.open(newline="") as f:
        return list(csv.DictReader(f))
def write(p, values):
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(values[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(values)
def interval(cells):
    from scipy.stats import norm, t
    estimate = sum(c["estimate"] for c in cells)
    variance = sum(c["variance"] for c in cells)
    denominator = sum(c["variance"]**2/(c["n"]-1) for c in cells if c["variance"])
    df = variance*variance/denominator if denominator else math.inf
    critical = float(t.ppf(.975, df)) if math.isfinite(df) else float(norm.ppf(.975))
    margin = critical*math.sqrt(variance)
    return estimate/3600, max(0, estimate-margin)/3600, (estimate+margin)/3600, df

def tables(data, precision=None):
    strata, original = read(data/"strata.csv"), read(data/"sample-costs.csv")
    if len(original) != 42 or any(r["status"] != "completed_cost" for r in original):
        raise ValueError("original42 costs incomplete; do not emit a final full-frame table")
    cells = {}
    for h in strata:
        values = [float(r["cpu_s"]) for r in original if r["stratum"] == h["stratum"]]
        N, n = int(h["population_modules"]), int(h["sample_size"])
        assert len(values) == n == 2
        cells[h["stratum"]] = dict(estimate=N*statistics.mean(values),
            variance=N*N*(1-n/N)*statistics.variance(values)/n, n=n,
            domain=h["regime_proxy"], known=values, population=N)
    models = {"original42_HT_unchanged": cells}
    applied = 0
    qualified = 0
    if precision is not None:
        design = read(data/"precision-design.csv")
        responses = {r["module"]: r for r in read(precision)}
        if len(responses) != 12 or set(responses) != {r["module"] for r in design}:
            raise ValueError("precision responses do not match the fixed twelve identities")
        if set(responses) & {r["module"] for r in original}:
            raise ValueError("original/precision membership overlap")
        expanded = {h: dict(c) for h, c in cells.items()}
        for h in {r["stratum"] for r in design}:
            draws = [responses[r["module"]] for r in design if r["stratum"] == h]
            assert len(draws) == 6
            good = [r for r in draws if r["completed_cost"] == "True"]
            qualified += len(good)
            if len(good) != 6:
                continue
            c = expanded[h]
            z = [float(r["cpu_s"]) for r in good]
            R = c["population"] - len(c["known"])
            c.update(estimate=sum(c["known"])+R*statistics.mean(z),
                variance=R*R*(1-6/R)*statistics.variance(z)/6, n=6)
            applied += 1
        models["conditional_panels_working_model"] = expanded
    factors = {r["calibration"]: float(r["CPU_factor"]) for r in read(data/"closure-ratios.csv")}
    scenarios = {
        "Mathlib_segmented_Grid_unsegmented": (factors["latest_segmented_Mathlib"], factors["compute-grid"]),
        "Falconer_segmented_Amplitudes_unsegmented": (factors["latest_segmented_Falconer"], factors["compute-amplitudes"])}
    output = []
    for estimator, source in models.items():
        source_total = sum(c["estimate"] for c in source.values())
        for scenario, (ordinary, compute) in scenarios.items():
            for stage in ("build", "serial_stream", "parallel_stream"):
                of = 1 if stage == "build" else ordinary
                cf = 1 if stage == "build" else compute
                if stage == "parallel_stream":
                    of *= factors["math_parallel8"]
                    cf *= factors["grid_parallel4"]
                for domain in ("all", "ordinary_mathematics", "computation_certificate"):
                    selected = [c for c in source.values() if domain == "all" or c["domain"] == domain]
                    weighted = []
                    for c in selected:
                        f = of if c["domain"] == "ordinary_mathematics" else cf
                        weighted.append(dict(estimate=c["estimate"]*f, variance=c["variance"]*f*f, n=c["n"]))
                    point, low, high, df = interval(weighted)
                    output.append(dict(estimator=estimator, transfer_scenario=scenario, domain=domain,
                        stage=stage, estimate_CPU_h=point, nominal95_low_CPU_h=low,
                        nominal95_high_CPU_h=high, satterthwaite_df=df,
                        ordinary_CPU_factor=of, computation_CPU_factor=cf,
                        source_CPU_share=sum(c["estimate"] for c in selected)/source_total,
                        qualified_precision_costs=qualified, applied_conditional_cells=applied,
                        interval_scope="source sampling only; fixed transfers; hybrid is nominal, not global adaptive coverage",
                        whole_library_measurement=False))
    sensitivity = []
    for estimator in models:
        for domain in ("all", "ordinary_mathematics", "computation_certificate"):
            for stage in ("build", "serial_stream", "parallel_stream"):
                values = [r["estimate_CPU_h"] for r in output if
                    (r["estimator"], r["domain"], r["stage"]) == (estimator, domain, stage)]
                sensitivity.append(dict(estimator=estimator, domain=domain, stage=stage,
                    min_transfer_estimate_CPU_h=min(values), max_transfer_estimate_CPU_h=max(values),
                    scope="selected closure-factor sensitivity, not CI or a population bound"))
    return output, sensitivity

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", type=Path, default=HERE)
    ap.add_argument("--precision-costs", type=Path)
    ap.add_argument("--out", type=Path, default=HERE)
    a = ap.parse_args()
    try:
        values, sensitivity = tables(a.data, a.precision_costs)
    except ValueError as e:
        ap.exit(2, str(e)+"\n")
    a.out.mkdir(parents=True, exist_ok=True)
    write(a.out/"final-estimates.csv", values)
    write(a.out/"transfer-scenarios.csv", sensitivity)
    print("Wrote final CPU estimates and separate transfer scenarios; no native measurement.")
if __name__ == "__main__":
    main()
