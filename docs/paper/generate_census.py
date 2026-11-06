#!/usr/bin/env python3
"""Generate observed-subset census artifacts; never extrapolate missing work."""
import argparse
import ast
import csv
from datetime import datetime
import gzip
import json
import math
import os
from pathlib import Path
import shutil
import statistics
import subprocess
import sys


def rows(path):
    if path.suffix == ".json":
        value = json.loads(path.read_text())
        return value if isinstance(value, list) else value["attempts"]
    # Real unfinished dependency lists exceed csv's default 128-KiB field limit.
    csv.field_size_limit(sys.maxsize)
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", newline="") as handle:
        return list(csv.DictReader(handle))


def first(row, *names):
    return next((row[name] for name in names if row.get(name) not in (None, "")), None)


def number(value):
    if value is None or str(value).strip().lower() in {"", "null", "none"}:
        return None
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise ValueError("invalid nonnegative observation: " + str(value))
    return result


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
    return None if number(value) is None else int(value), number(coverage)


def normalize(row):
    pool = first(row, "pool", "cpu_class")
    if row["status"] == "completed" and pool not in {"P", "E"}:
        raise ValueError("successful module needs an explicit P/E pool")
    user, system = number(first(row, "user_cpu_s", "user_s")), number(first(row, "system_cpu_s", "system_s"))
    instructions, coverage = counter(row, pool) if pool in {"P", "E"} else (None, None)
    result = dict(row)
    result.update(pool=pool, cpu_s=None if user is None or system is None else user + system,
                  user_cpu_s=user, system_cpu_s=system, wall_s=number(row.get("wall_s")),
                  user_instructions=instructions, instruction_coverage=coverage,
                  kernel_marked=first(row, "kernel_marked", "marker", "marked"),
                  default_covered=first(row, "default_covered", "default_graph"),
                  family_prefix=first(row, "family_prefix", "deferred_family_prefix"),
                  trigger_module=first(row, "trigger_module", "deferred_trigger_module"),
                  source_revision=row.get("source_revision", ""),
                  measurement_commit=row.get("measurement_commit", ""))
    return result


def emit(path, records):
    keys = list(dict.fromkeys(key for row in records for key in row)) or ["module", "status"]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def quantile(values, p):
    x = (len(values) - 1) * p
    i = int(x)
    return values[i] + (values[min(i + 1, len(values) - 1)] - values[i]) * (x - i)


def tex_number(value, digits=2):
    return "--" if value is None else f"{value:,.{digits}f}"



def utc_time(value):
    result = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("segment and record times need an explicit timezone")
    return result



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data/openai-math-4eaee875/census"))
    parser.add_argument("--csv", type=Path)
    parser.add_argument("--preview-json", type=Path, help="functional attempts.json, requires --preview")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--stopped", action="store_true", help="explicit user-stopped observed-subset publication")
    parser.add_argument("--retired", action="store_true", help="publish the retired campaign after runnable non-deferred work is exhausted")
    parser.add_argument("--failed-attempts", type=Path)
    parser.add_argument("--tectonic", default=os.environ.get("TECTONIC"))
    args = parser.parse_args()
    if args.preview_json and not args.preview:
        parser.error("functional JSON cannot populate the paper")
    if args.stopped and args.retired:
        parser.error("select either a historical stopped snapshot or the retired campaign")
    if not args.preview and not (args.stopped or args.retired):
        parser.error("select --stopped for segment 1 or --retired for the completed campaign")
    source = args.csv or args.preview_json
    if source is None:
        present = [args.data / name for name in
                   ("module-costs.csv.gz", "module-costs.csv", "modules.csv.gz", "modules.csv")
                   if (args.data / name).is_file()]
        if len(present) != 1:
            parser.error("select exactly one published module inventory with --csv")
        source = present[0]
    observations = [normalize(row) for row in rows(source)]
    names = [row["module"] for row in observations]
    if len(names) != len(set(names)):
        raise ValueError("module inventory contains repeated identities; do not pool repeats")
    values = [row for row in observations if row["status"] == "completed"]
    if any(first(row, "returncode", "exit") is not None and
           int(first(row, "returncode", "exit")) != 0 for row in values):
        raise ValueError("completed module has a nonzero return code")

    summary_path = args.data / "summary.json"
    published = json.loads(summary_path.read_text()) if summary_path.exists() else {}
    segment_path = args.data / "segment-totals.csv"
    segments = rows(segment_path) if segment_path.exists() else []
    configuration = [row for row in observations if row["status"] == "configuration"]
    unfinished = [row for row in observations if row["status"] not in {"completed", "configuration"}]
    failures = [row for row in unfinished if row["status"] in {"failed", "failure"}]
    blocked = [row for row in unfinished if row["status"] == "blocked"]
    source_modules = published.get("source_modules")
    if not args.preview:
        expected_segments = published.get("segment_count") if args.retired else 1
        if not isinstance(expected_segments, int) or expected_segments < (2 if args.retired else 1):
            raise ValueError("retired campaign needs its complete executed-interval ledger")
        if args.stopped and published.get("stop_reason") != "user_requested_stop":
            raise ValueError("historical stopped publication needs its explicit user-stop terminal")
        if published.get("segment_count") != expected_segments or len(segments) != expected_segments:
            raise ValueError("published segment count differs from executed wall ledger")
        if bool(published.get("segment2_launched")) != args.retired:
            raise ValueError("do not relabel a one-segment snapshot as the final continued campaign")
        if {str(item.get("segment")) for item in segments} != {str(i) for i in range(1, expected_segments + 1)}:
            raise ValueError("executed segment identities are missing or duplicated")
        if any(number(item.get("wall_s")) is None or not item.get("start_utc") or not item.get("end_utc")
               for item in segments):
            raise ValueError("each segment needs an actual retired wall interval")
        if len(observations) != int(published["source_units"]):
            raise ValueError("inventory must retain all source identities, including deferred and unmeasured")
        if source_modules != len(observations) - len(configuration):
            raise ValueError("source denominator differs from the inventory/configuration split")
        if published.get("completed_source_modules") != len(values) or published.get("unfinished_source_modules") != len(unfinished):
            raise ValueError("published retirement counts differ from the module ledger")
        if published.get("known_final_native_failures") != len(failures):
            raise ValueError("failed attempts must not become final failed modules")
        known = {"completed", "configuration", "failure", "failed", "blocked", "not_attempted", "deferred_by_user"}
        if any(row["status"] not in known for row in observations):
            raise ValueError("unresolved module status in the published inventory")
        if any(row["cpu_s"] is None or row["wall_s"] is None or row["user_instructions"] is None for row in values):
            raise ValueError("observed successful cost is absent; never zero-fill it")
        ids = {str(item["segment"]) for item in segments}
        if any(str(row.get("segment")) not in ids for row in values):
            raise ValueError("successful record belongs to an unreported segment")
        if args.retired and any(row["status"] == "not_attempted" for row in observations):
            raise ValueError("runnable work remains unattempted; this is not an exhausted campaign")

    segment_reporting = []
    segments.sort(key=lambda row: int(row["segment"]))
    for item in segments:
        original = number(item.get("wall_s"))
        start = utc_time(item["start_utc"]) if item.get("start_utc") else None
        end = utc_time(item["end_utc"]) if item.get("end_utc") else None
        if start and end and end < start:
            raise ValueError("reversed segment wall interval")
        reporting = original
        segment_reporting.append(dict(item, operational_wall_s=original, reporting_wall_s=reporting,
            later_drain_wall_s=None if original is None or reporting is None else max(0.0, original - reporting),
            wall_scope="complete retired segment interval including actual drain"))
    wall_s = (math.fsum(row["reporting_wall_s"] for row in segment_reporting)
              if segment_reporting and all(row["reporting_wall_s"] is not None for row in segment_reporting) else None)
    transition_gap_s = 0.0
    for earlier, later in zip(segment_reporting, segment_reporting[1:]):
        gap = (utc_time(later["start_utc"]) - utc_time(earlier["end_utc"])).total_seconds()
        if gap < 0:
            raise ValueError("overlapping segment wall intervals")
        transition_gap_s += gap

    failed_source = args.failed_attempts or next(
        (args.data / name for name in ("failed-attempts.csv.gz", "failed-attempts.csv")
         if (args.data / name).exists()), None)
    unsuccessful = rows(failed_source) if failed_source else []
    if any(row["status"] == "completed" for row in unsuccessful):
        raise ValueError("unsuccessful-attempt ledger contains a successful record")
    args.out.mkdir(parents=True, exist_ok=True)
    prefix = "preview-" if args.preview else ""
    if not args.preview:
        (args.out / "census-ready.tex").unlink(missing_ok=True)
    # Retain original unfinished reasons/identities and unsuccessful observations.
    emit(args.out / (prefix + "census-modules.csv"), observations)
    emit(args.out / (prefix + "census-outcomes.csv"),
         [{key: row.get(key) for key in ("module", "status", "segment", "family",
                                        "reason", "blocked_reason", "deferred_reason", "family_prefix",
                                        "trigger_module", "deferred_dependency", "utc", "deferred_utc",
                                        "failed_dependencies", "uncompleted_dependencies",
                                        "interruption")} for row in observations])
    deferred = [row for row in unfinished if row["status"] == "deferred_by_user"]
    emit(args.out / (prefix + "census-deferred-by-user.csv"), deferred)
    emit(args.out / (prefix + "census-outcome-summary.csv"),
         [dict(status=status, modules=sum(row["status"] == status for row in observations))
          for status in sorted({row["status"] for row in observations})])
    emit(args.out / (prefix + "census-unmeasured.csv"), unfinished)
    emit(args.out / (prefix + "census-failed-attempts.csv"), unsuccessful)
    emit(args.out / (prefix + "census-segments.csv"), segment_reporting)

    summaries = []
    for pool in ("P", "E"):
        group = [row for row in values if row["pool"] == pool]
        cpu = [row["cpu_s"] for row in group if row["cpu_s"] is not None]
        wall = [row["wall_s"] for row in group if row["wall_s"] is not None]
        inst = sorted(row["user_instructions"] for row in group if row["user_instructions"] is not None)
        summaries.append(dict(pool=pool, completed_modules=len(group),
            cpu_observed_modules=len(cpu), cpu_s=math.fsum(cpu) if cpu else None,
            cpu_hours=math.fsum(cpu) / 3600 if cpu else None,
            native_wall_observed_modules=len(wall), summed_native_wall_s=math.fsum(wall) if wall else None,
            user_instruction_observed_modules=len(inst), user_instructions=sum(inst) if inst else None,
            user_instructions_median=statistics.median(inst) if inst else None,
            user_instructions_p95=quantile(inst, .95) if inst else None,
            failed_or_interrupted_attempts=sum(row.get("pool") == pool for row in unsuccessful),
            scope="observed successful modules only; lower bound, not full-library estimate"))
    emit(args.out / (prefix + "census-summary.csv"), summaries)

    segment_costs = []
    for item in segment_reporting:
        for pool in ("P", "E"):
            group = [row for row in values if str(row.get("segment")) == str(item["segment"]) and row["pool"] == pool]
            cpu = [row["cpu_s"] for row in group if row["cpu_s"] is not None]
            segment_costs.append(dict(segment=item["segment"], pool=pool, completed_modules=len(group),
                                      cpu_observed_modules=len(cpu), cpu_hours=math.fsum(cpu) / 3600 if len(cpu) == len(group) else None,
                                      scope="all observed successful completions in this retired segment"))
    emit(args.out / (prefix + "census-segment-costs.csv"), segment_costs)

    coverage, groups = [], []
    for field in ("kernel_marked", "default_covered"):
        labels = sorted({str(row[field]) for row in observations
                         if row["status"] != "configuration" and row[field] is not None})
        for label in labels:
            frame = [row for row in observations if row["status"] != "configuration" and str(row[field]) == label]
            seen = [row for row in values if str(row[field]) == label]
            coverage.append(dict(field=field, label=label, frame_modules=len(frame),
                                 observed_modules=len(seen), unmeasured_modules=len(frame) - len(seen),
                                 scope="source-label coverage; costs apply only to observed modules"))
            for pool in ("P", "E"):
                selected = [row for row in seen if row["pool"] == pool]
                cpu = [row["cpu_s"] for row in selected if row["cpu_s"] is not None]
                inst = [row["user_instructions"] for row in selected if row["user_instructions"] is not None]
                denominator = next(row["cpu_s"] for row in summaries if row["pool"] == pool)
                groups.append(dict(field=field, label=label, pool=pool, observed_modules=len(selected),
                                   cpu_observed_modules=len(cpu), cpu_hours=math.fsum(cpu) / 3600 if cpu else None,
                                   share_of_observed_pool_cpu=None if not cpu or not denominator else math.fsum(cpu) / denominator,
                                   user_instructions=sum(inst) if inst else None,
                                   scope="dependency-ordered observed subset; no extrapolation"))
    emit(args.out / (prefix + "census-coverage.csv"), coverage)
    emit(args.out / (prefix + "census-groups.csv"), groups)

    curves = []
    for metric, label in [("user_instructions", "All-user-instructions"), ("cpu_s", "P"), ("cpu_s", "E")]:
        xs = sorted(row[metric] for row in values if row[metric] is not None and row[metric] > 0
                    and (label == "All-user-instructions" or row["pool"] == label))
        if xs:
            curves.extend(dict(metric=metric, pool=label, quantile=i / 1000, value=quantile(xs, i / 1000))
                          for i in range(1001))
    emit(args.out / (prefix + "census-quantiles.csv"), curves)
    for label in ("All-user-instructions", "P", "E"):
        emit(args.out / (prefix + "curve-" + label + ".csv"),
             [row for row in curves if row["pool"] == label] or
             [dict(metric="", pool=label, quantile="", value="")])
    table = [r"\begin{tabular}{lrrr}", r"\toprule",
             r"Pool & Observed modules & CPUh lower bound & CPU observations\\", r"\midrule"]
    for row in summaries:
        table.append(f'{row["pool"]} & {row["completed_modules"]:,} & '
                     f'{tex_number(row["cpu_hours"])} & {row["cpu_observed_modules"]:,}'+r"\\")
    table += [r"\bottomrule", r"\end{tabular}"]
    (args.out / (prefix + "census-table.tex")).write_text("\n".join(table) + "\n")
    axes = []
    for metric, title in (("user_instructions", "User instructions"),
                          ("cpu_s", "CPU seconds")):
        plots = []
        for label in (["All-user-instructions"] if metric == "user_instructions" else ["P", "E"]):
            if any(row["pool"] == label for row in curves):
                plots += [r"\addplot table[x=value,y=quantile,col sep=comma] {" +
                          prefix + "curve-" + label + r".csv};",
                          r"\addlegendentry{" + label.replace("All-user-instructions", "Observed") + "}"]
        if not plots:
            plots = [r"\node at (rel axis cs:0.5,0.5) {No measured costs supplied};"]
        axes += [r"\nextgroupplot[xmode=log,xlabel={" + title +
                 r"},ylabel={" + ("Quantile" if metric == "user_instructions" else "") + r"},ymin=0,ymax=1]", *plots]
    figure = (r"\documentclass[tikz,border=2pt]{standalone}" + "\n" +
              r"\usepackage{pgfplots}\usepgfplotslibrary{groupplots}\pgfplotsset{compat=1.18}" + "\n" +
              r"\begin{document}\begin{tikzpicture}\begin{groupplot}[group style={group size=2 by 1,horizontal sep=0.9cm},width=4.2cm,height=4.5cm,tick label style={font=\scriptsize},label style={font=\small},legend style={font=\scriptsize},legend pos=south east]" +
              "\n" + "\n".join(axes) +
              "\n" + r"\end{groupplot}\end{tikzpicture}\end{document}" + "\n")
    figure_path = args.out / (prefix + "census-distribution.tex")
    figure_path.write_text(figure)

    try:
        revision = subprocess.run(["git", "log", "-1", "--format=%H", "--", str(source)],
                                  capture_output=True, text=True, check=False)
        publication_commit = revision.stdout.strip() or None
    except OSError:
        publication_commit = None
    manifest = dict(published_data_commit=publication_commit,
        preview=args.preview, explicitly_stopped_subset=args.stopped,
        retired_final=args.retired and not args.preview,
        native_completed_at_retirement=published.get("completed_source_modules"),
        native_unfinished_at_retirement=published.get("unfinished_source_modules"),
        segment_reporting=segment_reporting,
        transition_gap_s=transition_gap_s,
        input=str(source), published_summary=str(summary_path), segment_ledger=str(segment_path),
        completed_modules=len(values), source_modules=source_modules,
        unfinished_source_modules=len(unfinished), configuration_units=len(configuration),
        final_failed_modules=len(failures), genuinely_blocked_modules=len(blocked),
        deferred_by_user_modules=len(deferred),
        deferral_scope="unfinished memory-intensive families and transitive dependents; earlier completed modules retained",
        selection_bias="dependency order plus explicit memory-family deferral favors less-memory-intensive remaining work",
        completed_fraction=None if not source_modules else len(values) / source_modules,
        unsuccessful_attempts=len(unsuccessful), unsuccessful_attempt_source=str(failed_source),
        source_revisions=sorted({row["source_revision"] for row in values}),
        measurement_commits=sorted({row["measurement_commit"] for row in values}),
        machine_wall_s=wall_s, segment2_launched=published.get("segment2_launched"),
        source_scope="dependency-ordered and selectively deferred observed subset; not random",
        inference="separate P/E observed-work lower bounds only; no full-library cost, original42 or model completion",
        cost_groups="observed modules only; frame-label coverage retained separately",
        pool_cpu_combination="none; no P/E conversion or pooled CPU total",
        summed_native_wall_is_makespan=False,
        wall_scope="sum of segment reporting intervals; complete operational intervals including drain; transition gap and unsuccessful CPU separate",
        instruction_criterion="user-mode instructions selected after the failed total-instruction gate",
        missing_values="blank, never zero-filled",
        active_instruction_coverage={pool: sorted({row["instruction_coverage"] for row in values
            if row["pool"] == pool and row["instruction_coverage"] is not None}) for pool in ("P", "E")})
    (args.out / (prefix + "census-provenance.json")).write_text(json.dumps(manifest, indent=2) + "\n")
    macros = []
    if not args.preview:
        fraction = 100 * len(values) / source_modules
        by_pool = {row["pool"]: row for row in summaries}
        macros = [
            r"\def\CensusFinal{" + ("1" if args.retired else "0") + "}",
            r"\def\CensusScopeLabel{" + ("Retired campaign" if args.retired else "First-segment snapshot") + "}",
            r"\def\CensusNativeModules{" + f"{len(values):,}" + "}",
            r"\def\CensusExecutableModules{" + f"{source_modules:,}" + "}",
            r"\def\CensusUnmeasuredModules{" + f"{len(unfinished):,}" + "}",
            r"\def\CensusDeferredModules{" + f"{len(deferred):,}" + "}",
            r"\def\CensusObservedPercent{" + tex_number(fraction, 2) + "}",
            r"\def\CensusPCPUHours{" + tex_number(by_pool["P"]["cpu_hours"], 3) + "}",
            r"\def\CensusECPUHours{" + tex_number(by_pool["E"]["cpu_hours"], 3) + "}",
            r"\def\CensusWallHours{" + tex_number(wall_s / 3600, 3) + "}",
            r"\def\CensusScopeSummary{\CensusNativeModules{} of \CensusExecutableModules{} modules completed "
            r"(\CensusObservedPercent{}\%); \CensusDeferredModules{} were deferred.}",
            r"\def\CensusObservedSummary{Successful work is \CensusPCPUHours{} P / "
            r"\CensusECPUHours{} E CPU-hours. "
            r"Retired intervals total \CensusWallHours{} wall-hours, including drain.}"]
        parts = []
        for item in segment_reporting:
            costs = {row["pool"]: row for row in segment_costs if row["segment"] == item["segment"]}
            parts.append("Interval " + str(item["segment"]) + " (" + f'{int(item["completed_modules"]):,}' + " modules): " +
                         tex_number(costs["P"]["cpu_hours"], 3) + " P / " +
                         tex_number(costs["E"]["cpu_hours"], 3) + " E CPUh, " +
                         tex_number(item["reporting_wall_s"] / 3600, 3) + " wallh.")
        macros.append(r"\def\CensusSegmentSummary{" + " ".join(parts) + "}")
        macros.append(r"\def\CensusDeferredSummary{\CensusDeferredModules{} modules are deferred by user, "
                      r"separately from native failure and failed-dependency blocking.}")


        all_instructions = sorted(row["user_instructions"] for row in values)
        def scientific(value):
            exponent = math.floor(math.log10(value))
            return "$" + f"{value / 10**exponent:.3f}" + r"\times10^{" + str(exponent) + "}$"
        instruction_total = sum(all_instructions)
        macros.append(r"\def\CensusInstructionSummary{User-mode instructions total " +
                      scientific(instruction_total) + "; the per-module median and 95th percentile are " +
                      scientific(statistics.median(all_instructions)) + " and " +
                      scientific(quantile(all_instructions, .95)) + ", respectively.}")
        calendar_s = (utc_time(segment_reporting[-1]["end_utc"]) -
                      utc_time(segment_reporting[0]["start_utc"])).total_seconds()
        macros.append(r"\def\CensusClockSummary{The calendar span is " + tex_number(calendar_s / 3600, 3) +
                      " hours, including " + tex_number(transition_gap_s / 3600, 3) +
                      " hours of gaps. Final native failures / dependency blocks: " +
                      str(len(failures)) + "/" + str(len(blocked)) + "; " + str(len(unsuccessful)) +
                      " unsuccessful attempts are excluded from successful CPU.}")
        label_groups = {(row["field"], row["label"], row["pool"]): row for row in groups}
        group_text = []
        for field, labels, description in [
                ("kernel_marked", ("1", "0"), "Marked/unmarked"),
                ("default_covered", ("0", "1"), "Outside/inside the default graph")]:
            inventories = [next((r for r in coverage if r["field"] == field and r["label"] == label), None)
                           for label in labels]
            if all(inventories):
                text = description + ": " + "/".join(f'{r["observed_modules"]:,}' for r in inventories) + " completed modules; "
                for pool in ("P", "E"):
                    pair = [label_groups[(field, label, pool)] for label in labels]
                    text += "/".join(tex_number(r["cpu_hours"], 3) for r in pair) + " " + pool + " CPUh" + (", " if pool == "P" else ".")
                group_text.append(text)
        macros.append(r"\def\CensusGroupSummary{" + " ".join(group_text) + "}")

    if args.tectonic:
        subprocess.run([shutil.which(args.tectonic) or args.tectonic, figure_path.name], cwd=args.out, check=True)
        if not args.preview:
            (args.out / "census-ready.tex").write_text("\n".join(macros) + "\n")
    print(json.dumps(manifest))


if __name__ == "__main__":
    main()
