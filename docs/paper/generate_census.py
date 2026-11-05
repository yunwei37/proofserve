#!/usr/bin/env python3
"""Render W's published per-module census without pooling P/E CPU seconds."""
import argparse
import ast
import csv
import gzip
import json
import math
import os
from pathlib import Path
import shutil
import statistics
import subprocess


def rows(path):
    if path.suffix == ".json":
        value = json.loads(path.read_text())
        return value if isinstance(value, list) else value["attempts"]
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", newline="") as handle:
        return list(csv.DictReader(handle))


def number(value):
    if value is None or str(value).strip().lower() in {"", "null", "none"}:
        return None
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise ValueError("invalid nonnegative observation: " + str(value))
    return result


def first(row, *names):
    return next((row[name] for name in names if row.get(name) not in (None, "")), None)


def counter(row, pool):
    value = first(row, "user_instructions", "instructions_user",
                  ("cpu_core" if pool == "P" else "cpu_atom") + "_user_instructions")
    coverage = first(row, "user_instruction_coverage", "instructions_user_coverage", "user_coverage")
    if value is None and row.get("counters"):
        counters = row["counters"]
        if isinstance(counters, str):
            try:
                counters = json.loads(counters)
            except json.JSONDecodeError:
                counters = ast.literal_eval(counters)
        event = counters.get(("cpu_core" if pool == "P" else "cpu_atom") + "_user", {})
        value, coverage = event.get("instructions"), event.get("coverage")
    count = None if number(value) is None else int(value)
    if count is not None and count < 0:
        raise ValueError("negative retired instruction count")
    return count, number(coverage)


def normalize(row):
    pool = first(row, "pool", "cpu_class")
    if pool not in {"P", "E"}:
        raise ValueError("explicit P/E pool required for " + row.get("module", "?"))
    user = number(first(row, "user_cpu_s", "user_s"))
    system = number(first(row, "system_cpu_s", "system_s"))
    instructions, coverage = counter(row, pool)
    return dict(module=row["module"], pool=pool, status=row["status"],
                returncode=first(row, "returncode", "exit"),
                attempt=first(row, "attempt", "sequence"),
                cpu_s=None if user is None or system is None else user + system,
                user_cpu_s=user, system_cpu_s=system,
                wall_s=number(row.get("wall_s")),
                user_instructions=instructions, instruction_coverage=coverage,
                source_revision=row.get("source_revision", ""),
                measurement_commit=row.get("measurement_commit", ""),
                kernel_marked=first(row, "kernel_marked", "marker"),
                default_covered=row.get("default_covered"))


def quantile(values, p, presorted=False):
    ordered = values if presorted else sorted(values)
    x = (len(ordered) - 1) * p
    i = int(x)
    return ordered[i] + (ordered[min(i + 1, len(ordered) - 1)] - ordered[i]) * (x - i)


def emit(path, records):
    keys = list(dict.fromkeys(key for row in records for key in row))
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def tex_number(value, digits=2):
    return "--" if value is None else f"{value:,.{digits}f}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data/openai-math-4eaee875/census"))
    parser.add_argument("--csv", type=Path, help="explicit per-module CSV or CSV.gz")
    parser.add_argument("--preview-json", type=Path, help="W's functional attempts.json; requires --preview")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--tectonic", default=os.environ.get("TECTONIC"),
                        help="optional Tectonic executable; compiles the generated scientific figure")
    args = parser.parse_args()
    if args.preview_json and not args.preview:
        parser.error("functional JSON is preview evidence, not census data")
    source = args.csv or args.preview_json
    if source is None:
        candidates = [args.data / name for name in
                      ("module-costs.csv.gz", "module-costs.csv", "modules.csv.gz", "modules.csv")]
        present = [path for path in candidates if path.is_file()]
        if len(present) != 1:
            parser.error("select one published module CSV with --csv; census publication may still be pending")
        source = present[0]
    observations = [normalize(row) for row in rows(source)]
    completed = {}
    for row in observations:
        if row["status"] == "completed":
            if row["returncode"] is not None and int(row["returncode"]) != 0:
                raise ValueError("completed row has a nonzero native return code")
            if row["module"] in completed:
                raise ValueError("duplicate successful module; select a single census rather than pool repeats")
            completed[row["module"]] = row
    values = list(completed.values())
    outcome_file = args.data / "outcomes.json"
    outcome = json.loads(outcome_file.read_text()) if outcome_file.exists() else {}
    failed_rows = [dict(module=item, status="failed") if isinstance(item, str) else item
                   for item in outcome.get("failed", [])]
    blocked_rows = [dict(module=item, status="blocked") if isinstance(item, str) else item
                    for item in outcome.get("blocked", [])]
    configuration = outcome.get("configuration_units", [])
    classifications = ([dict(module=name, status="completed") for name in completed] +
                       [dict(module=name, status="configuration") for name in configuration] +
                       failed_rows + blocked_rows)
    if not args.preview:
        if not outcome.get("full_census") or not outcome.get("cost_measurement"):
            raise ValueError("publication needs W's full-census cost-measurement terminal; use --preview for validation")
        if outcome.get("stop") is not None:
            raise ValueError("the campaign stopped before natural completion; wait for its final terminal")
        if set(outcome["successful"]) != set(completed):
            raise ValueError("CSV successes differ from W's terminal")
        names = [item["module"] for item in classifications]
        if len(names) != len(set(names)):
            raise ValueError("terminal outcome categories overlap or contain duplicate modules")
        if len(names) != int(outcome["total_source_units"]):
            raise ValueError("terminal categories do not account for the full source frame")
        if any(item.get("status") not in {"completed", "configuration", "failed", "blocked"}
               for item in classifications):
            raise ValueError("unattempted/unresolved inputs are not a completed campaign")
        if bool(outcome.get("complete")) != (len(completed) + len(configuration) == len(names)):
            raise ValueError("all-success flag disagrees with the terminal classifications")
        if any(row["cpu_s"] is None or row["wall_s"] is None or
               row["user_instructions"] is None for row in values):
            raise ValueError("successful final rows contain unobserved costs/instructions; never fill them with zero")
    total_units = outcome.get("total_source_units")
    configuration_units = len(configuration)
    args.out.mkdir(parents=True, exist_ok=True)
    prefix = "preview-" if args.preview else ""
    emit(args.out / (prefix + "census-modules.csv"), observations)
    if classifications:
        emit(args.out / (prefix + "census-outcomes.csv"), classifications)
    summaries = []
    for pool in ("P", "E"):
        group = [row for row in values if row["pool"] == pool]
        cpu = [row["cpu_s"] for row in group if row["cpu_s"] is not None]
        wall = [row["wall_s"] for row in group if row["wall_s"] is not None]
        inst = [row["user_instructions"] for row in group if row["user_instructions"] is not None]
        summaries.append(dict(pool=pool, completed_modules=len(group),
            cpu_observed_modules=len(cpu), cpu_s=math.fsum(cpu) if cpu else None,
            cpu_hours=math.fsum(cpu) / 3600 if cpu else None,
            native_wall_observed_modules=len(wall), summed_native_wall_s=math.fsum(wall) if wall else None,
            user_instruction_observed_modules=len(inst),
            user_instructions=sum(inst) if inst else None,
            user_instructions_median=statistics.median(inst) if inst else None,
            user_instructions_p95=quantile(inst, .95) if inst else None,
            failed_or_interrupted_attempts=sum(row["pool"] == pool and row["status"] != "completed"
                                              for row in observations)))
    emit(args.out / (prefix + "census-summary.csv"), summaries)
    groups = []
    for field in ("kernel_marked", "default_covered"):
        for label in sorted({str(row[field]) for row in values if row[field] is not None}):
            for pool in ("P", "E"):
                selected = [row for row in values if str(row[field]) == label and row["pool"] == pool]
                known = [row["cpu_s"] for row in selected if row["cpu_s"] is not None]
                groups.append(dict(field=field, label=label, pool=pool, modules=len(selected),
                                   cpu_observed_modules=len(known),
                                   cpu_hours=math.fsum(known) / 3600 if known else None))
    if groups:
        emit(args.out / (prefix + "census-groups.csv"), groups)
    curves = []
    for metric, label in (("user_instructions", "All-user-instructions"), ("cpu_s", "P"), ("cpu_s", "E")):
        xs = [row[metric] for row in values if row[metric] is not None and row[metric] > 0
              and (label == "All-user-instructions" or row["pool"] == label)]
        if xs:
            xs.sort()
            for i in range(1001):
                curves.append(dict(metric=metric, pool=label, quantile=i / 1000,
                                   value=quantile(xs, i / 1000, presorted=True)))
    emit(args.out / (prefix + "census-quantiles.csv"), curves)
    # Separate PGFPlots input files keep the figure dependency-free at generation time.
    for label in ("All-user-instructions", "P", "E"):
        emit(args.out / (prefix + "curve-" + label + ".csv"),
             [row for row in curves if row["pool"] == label] or
             [dict(metric="", pool=label, quantile="", value="")])
    table = [r"\begin{tabular}{lrrr}", r"\toprule",
             r"Pool & Native modules & Observed CPUh & CPU observations\\", r"\midrule"]
    for row in summaries:
        table.append(f'{row["pool"]} & {row["completed_modules"]:,} & '
                     f'{tex_number(row["cpu_hours"])} & {row["cpu_observed_modules"]:,}'+r"\\")
    table += [r"\bottomrule", r"\end{tabular}"]
    (args.out / (prefix + "census-table.tex")).write_text("\n".join(table) + "\n")
    axes = []
    for metric, title in (("user_instructions", "User-mode instructions"),
                          ("cpu_s", "Native CPU seconds")):
        plots = []
        labels = ["All-user-instructions"] if metric == "user_instructions" else ["P", "E"]
        for label in labels:
            if any(row["pool"] == label for row in curves):
                plots += [r"\addplot table[x=value,y=quantile,col sep=comma] {" +
                          prefix + "curve-" + label + r".csv};",
                          r"\addlegendentry{" + label.replace("All-user-instructions", "Modules") + "}"]
        if not plots:
            plots = [r"\node at (rel axis cs:0.5,0.5) {No measured costs supplied};"]
        axes += [r"\nextgroupplot[xmode=log,xlabel={" + title +
                 r"},ylabel={Empirical quantile},ymin=0,ymax=1]", *plots]
    figure = (r"\documentclass[tikz,border=2pt]{standalone}" + "\n" +
              r"\usepackage{pgfplots}\usepgfplotslibrary{groupplots}\pgfplotsset{compat=1.18}" + "\n" +
              r"\begin{document}\begin{tikzpicture}\begin{groupplot}[group style={group size=1 by 2,vertical sep=1.1cm},width=8cm,height=4.2cm,legend pos=south east]" +
              "\n" + "\n".join(axes) +
              "\n" + r"\end{groupplot}\end{tikzpicture}\end{document}" + "\n")
    figure_path = args.out / (prefix + "census-distribution.tex")
    figure_path.write_text(figure)
    manifest = dict(preview=args.preview, input=str(source), outcomes=str(outcome_file),
                    completed_modules=len(values), terminal_complete=outcome.get("complete"),
                    result_scope="preview" if args.preview else "completed campaign; success and genuine failure/blocked outcomes separated",
                    total_source_units=total_units, configuration_units=configuration_units,
                    failed_modules=len(failed_rows), blocked_modules=len(blocked_rows),
                    all_native_successful=outcome.get("complete"),
                    cpu_totals_scope="successful observed native modules only; unsuccessful attempts retained separately",
                    snapshot_utc=outcome.get("snapshot_utc", outcome.get("finished_utc")),
                    source_revisions=sorted({row["source_revision"] for row in values}),
                    measurement_commits=sorted({row["measurement_commit"] for row in values}),
                    pool_cpu_combination="none; no P-to-E conversion or pooled CPU total",
                    summed_native_wall_is_makespan=False,
                    instruction_criterion="user-mode instructions, selected after the failed total-instruction gate",
                    missing_values="blank, never zero-filled",
                    instruction_coverage_values={pool: sorted({row["instruction_coverage"] for row in values if row["pool"] == pool and row["instruction_coverage"] is not None}) for pool in ("P", "E")},
                    plot="1001 interpolated empirical quantiles per curve",
                    machine_wall_s=outcome.get("machine_wall_s"))
    (args.out / (prefix + "census-provenance.json")).write_text(json.dumps(manifest, indent=2) + "\n")
    if not args.preview:
        macros = [r"\def\CensusNativeModules{" + f"{len(values):,}" + "}",
                  r"\def\CensusSourceUnits{" + f'{outcome["total_source_units"]:,}' + "}",
                  r"\def\CensusConfigurationUnits{" + str(configuration_units) + "}",
                  r"\def\CensusFailedModules{" + str(len(failed_rows)) + "}",
                  r"\def\CensusBlockedModules{" + str(len(blocked_rows)) + "}",
                  r"\def\CensusScopeSummary{The completed campaign accounts for "
                  r"\CensusSourceUnits{} source units: \CensusNativeModules{} successfully costed native modules, "
                  r"\CensusConfigurationUnits{} configuration units, \CensusFailedModules{} genuinely failed modules "
                  r"and \CensusBlockedModules{} blocked modules.}"]
        for row in summaries:
            macros.append(r"\def\Census" + row["pool"] + "CPUHours{" + tex_number(row["cpu_hours"]) + "}")

    if args.tectonic:
        executable = shutil.which(args.tectonic) or args.tectonic
        subprocess.run([executable, figure_path.name], cwd=args.out, check=True)
        if not args.preview:
            (args.out / "census-ready.tex").write_text("\n".join(macros) + "\n")
    print(json.dumps(manifest))


if __name__ == "__main__":
    main()
