#!/usr/bin/env python3
"""Independent remainder panels; original HT and conditional components stay separate."""
import argparse
import csv
import json
import math
import statistics
from pathlib import Path
from estimate_native_build import stratum_estimate, confidence_interval

HERE = Path(__file__).resolve().parent

def read_csv(p):
    return list(csv.DictReader(p.open()))

def write_csv(p, rows):
    if not rows:
        return
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

def conditional_cell(population, known, fresh):
    """Known members have weight one; SRSWOR fresh draws represent only the remainder."""
    remainder = population - len(known)
    n = len(fresh)
    if not 0 < n <= remainder:
        raise ValueError("invalid remainder draw count")
    total = sum(known) + remainder * statistics.mean(fresh)
    if n == remainder:
        variance = 0.
    elif n < 2:
        raise ValueError("one draw cannot estimate non-census variance")
    else:
        variance = remainder**2 * (1-n/remainder) * statistics.variance(fresh) / n
    return dict(estimate=total, variance=variance, sample_n=n)

def eligible(row):
    return (row.get("status") == "compile_ok" and row.get("threads") == 8
        and row.get("lean_memory_option_MiB") == 0
        and row.get("heartbeat_budget") == "authored_or_native_default"
        and row.get("compilation_outputs") == "olean_ilean_c"
        and row.get("profiled") is False and row.get("pcore_lock") is True
        and row.get("source_exact") is True and row.get("native_retired") is True
        and row.get("cgroup_retired") is True
        and all(isinstance(row.get(k), (int,float)) and math.isfinite(row[k])
                and row[k] >= 0 for k in ["user_cpu_s","system_cpu_s"]))

def collect_results(files, targets):
    accepted, attempts = {}, {m: [] for m in targets}
    known_cpu, unknown_cpu = 0., 0
    for file in files:
        for number, line in enumerate(file.read_text().splitlines(), 1):
            row = json.loads(line)
            if row.get("module") not in targets:
                continue
            m = row["module"]
            usage = [row.get(k) for k in ["user_cpu_s","system_cpu_s"]]
            recorded_cpu = sum(usage) if all(isinstance(x,(int,float)) and math.isfinite(x) and x>=0 for x in usage) else None
            if row.get("pcore_lock") is True:
                if recorded_cpu is None:
                    unknown_cpu += 1
                else:
                    known_cpu += recorded_cpu
            attempts[m].append(dict(status=row.get("status","unknown"), file=str(file),
                line=number, matched_success=eligible(row), recorded_CPU_s=recorded_cpu))
            if eligible(row) and m not in accepted:
                accepted[m] = dict(cpu_s=recorded_cpu, file=str(file), line=number,
                                  wall_s=row.get("wall_s",""))
    return accepted, attempts, known_cpu, unknown_cpu

def interval_rows(cells, scope):
    rows = []
    for domain, subset in [
        ("all", list(cells)),
        ("ordinary_proxy", [h for h in cells if h.endswith(";0")]),
        ("certificate_proxy", [h for h in cells if h.endswith(";1")])]:
        interval = confidence_interval([cells[h] for h in subset])
        rows.append(dict(scope=scope, domain=domain, **interval,
            high_over_low=interval["upper_cpu_h"]/interval["lower_cpu_h"] if interval["lower_cpu_h"]>0 else "inf",
            interpretation="nominal model interval; no global conditional/adaptive-stopping coverage guarantee",
            calibration_uncertainty_included=False, actual_whole_library=False))
    return rows

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--frame", type=Path, required=True)
    ap.add_argument("--targets", type=Path, required=True)
    ap.add_argument("--results", type=Path, nargs="*", default=[])
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    frame, design = read_csv(a.frame), read_csv(a.targets)
    if len(frame)!=42 or any(r["status"]!="completed_cost" for r in frame):
        receipt = dict(status="pending_original42", completed=sum(r["status"]=="completed_cost" for r in frame),
            full_interval_emitted=False, input_frame=str(a.frame))
        (a.out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
        print(json.dumps(receipt))
        return 2
    assert len({r["module"] for r in frame})==42
    strata = {}
    for r in read_csv(HERE/"build-planning-4eaee875/strata.csv"):
        h = ";".join(r[k] for k in ["size_percentile_bin","import_depth_bin","has_decide_kernel"])
        strata[h] = int(r["population_modules"])
    members = {h:[r for r in frame if r["stratum"]==h] for h in strata}
    groups = {h:[r for r in design if r["stratum"]==h] for h in {r["stratum"]for r in design}}
    assert len(groups)==2 and all(len(g)==6 for g in groups.values())
    targets = {r["module"]:r for r in design}
    assert len(targets)==12 and not(set(targets)&{r["module"]for r in frame})
    for h, group in groups.items():
        assert all(int(r["remainder_population"])+len(members[h])==strata[h] for r in group)
    selected, attempts, spent, unknown = collect_results(a.results, targets)
    cells, original, known_by_cell = {}, {}, {}
    for h,N in strata.items():
        y = [float(r["cpu_s"]) for r in members[h]]
        assert len(y)==2
        T,V = stratum_estimate(N,2,y)
        original[h] = dict(estimate=T,variance=V,sample_n=2)
        cells[h] = dict(original[h])
        known_by_cell[h] = y
    expanded = []
    table = []
    for h, group in groups.items():
        z = [selected[r["module"]]["cpu_s"] for r in group if r["module"] in selected]
        if len(z)==len(group):
            cells[h] = conditional_cell(strata[h],known_by_cell[h],z)
            expanded.append(h)
    for h,N in strata.items():
        table.append(dict(stratum=h,population_modules=N,
            method="known_members_plus_independent_remainder" if h in expanded else "original42_HT",
            original_members=len(members[h]), planned_new_members=len(groups.get(h,[])),
            completed_new_members=sum(r["module"]in selected for r in groups.get(h,[])),
            estimate_CPU_h=cells[h]["estimate"]/3600,variance_CPU_s2=cells[h]["variance"],
            variance_df=cells[h]["sample_n"]-1,
            note="unexpanded/incomplete panels retain baseline; no partial-response substitution"))
    write_csv(a.out/"cell-estimates.csv",table)
    intervals = interval_rows(original,"original42_HT_unchanged")+interval_rows(cells,"conditional_panels_working_model")
    write_csv(a.out/"intervals.csv",intervals)
    response_rows = []
    for row in design:
        m = row["module"]
        hit = selected.get(m,{})
        response_rows.append(dict(module=m,stratum=row["stratum"],position=row["position"],
            completed_cost=m in selected,cpu_s=hit.get("cpu_s",""),
            source_file=hit.get("file",""),source_line=hit.get("line",""),
            attempts=len(attempts[m]),statuses=";".join(x["status"] for x in attempts[m])))
    write_csv(a.out/"responses.csv",response_rows)
    # Prospective independent NEXT stage, conditional on all measured members.
    # This is a plug-in power/budget calculation, never an observed interval.
    forecast = []
    for count in [2,3,4,6,8,12,16,24,32,64]:
        projected = {h:dict(original[h]) for h in original}
        expected_cpu = 0.
        for h, group in groups.items():
            fresh = [selected[r["module"]]["cpu_s"] for r in group if r["module"] in selected]
            complete = len(fresh)==len(group)
            known = known_by_cell[h] + (fresh if complete else [])
            proxy = fresh if complete else known_by_cell[h]
            remainder = strata[h]-len(known)
            n = min(count,remainder)
            projected[h] = dict(estimate=sum(known)+remainder*statistics.mean(proxy),
                variance=remainder**2*(1-n/remainder)*statistics.variance(proxy)/n,
                sample_n=n)
            expected_cpu += n*statistics.mean(proxy)
        ci = confidence_interval(list(projected.values()))
        forecast.append(dict(new_independent_draws_per_selected_cell=count,
            total_new_draws=2*count,expected_leaf_CPU_h=expected_cpu/3600,
            **ci, high_over_low=ci["upper_cpu_h"]/ci["lower_cpu_h"] if ci["lower_cpu_h"]>0 else "inf",
            exceeds_target=ci["lower_cpu_h"]>0 and ci["upper_cpu_h"]/ci["lower_cpu_h"]<=3,
            note="pilot plug-in forecast, not guaranteed; dependency preparation and calibration uncertainty excluded"))
    write_csv(a.out/"next-stage-planning.csv",forecast)
    whole = next(x for x in intervals if x["scope"]=="conditional_panels_working_model" and x["domain"]=="all")
    all_complete = len(selected)==len(targets)
    meets = all_complete and whole["lower_cpu_h"]>0 and whole["high_over_low"]<=3
    first_plan = next((x for x in forecast if x["exceeds_target"]),None)
    receipt = dict(status="all_planned_panels_complete" if all_complete else "panels_incomplete",
        original_completed=42,planned_new_draws=12,completed_new_draws=len(selected),
        expanded_cells=expanded,goal_nominal_ratio_below_three=meets,
        recorded_target_attempt_CPU_h_lower_bound=spent/3600,
        target_attempts_missing_CPU=unknown,
        projected_additional_draws=0 if meets else first_plan["total_new_draws"] if first_plan else None,
        projected_additional_leaf_CPU_h=0 if meets else first_plan["expected_leaf_CPU_h"] if first_plan else None,
        dependency_preparation_CPU_h="unmeasured; excluded, not zero",
        limitations=[
            "Original42 HT stays unchanged; expanded cells use weight-one known members plus SRS remainder.",
            "Whole-frame hybrid interval is nominal: adaptive cell choice and repeated looks lack global coverage guarantee.",
            "All six fresh responses are required before a cell replaces its original HT component.",
            "Sparse cells/heavy tails can invalidate t approximation; missingness is not imputed.",
            "Future sample count/CPU is a plug-in forecast, excluding dependency preparation and calibration uncertainty.",
            "Neither whole-library census nor actual whole-library checker measurement."])
    (a.out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
