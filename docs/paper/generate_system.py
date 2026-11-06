#!/usr/bin/env python3
"""Generate committed-release tables; preview measurements never become paper-ready."""
import argparse
import csv
import json
import math
import re
from pathlib import Path
import statistics
import subprocess


def truth(value):
    return str(value).lower() in {"true", "1", "yes"}


def numeric(row, field):
    value = row.get(field)
    if value in (None, "", "None", "null"):
        return None
    value = float(value)
    if not math.isfinite(value) or value < 0:
        raise ValueError("invalid " + field)
    return value


def read(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def emit(path, rows, fields=None):
    keys = fields or list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def tex(value):
    replacements = {"\\": r"\textbackslash{}", "_": r"\_", "%": r"\%", "&": r"\&",
                    "#": r"\#", "{": r"\{", "}": r"\}", "$": r"\$"}
    return "".join(replacements.get(char, char) for char in str(value))


def fmt(value):
    return "--" if value is None else f"{value:.2f}"


def stats(group, minimum=1):
    result = dict(observations=len(group),
                  successful=sum(row.get("returncode") == "0" for row in group))
    for metric in ("cpu_s", "wall_s"):
        values = [numeric(row, metric) for row in group if row.get("returncode") == "0"]
        known = [value for value in values if value is not None]
        # A partially known group is not a complete request-cost observation.
        result[metric + "_observed"] = len(known)
        for suffix, function in (("median", statistics.median), ("min", min), ("max", max)):
            result[metric + "_" + suffix] = (function(known) if known and len(known) == len(values)
                                             and (suffix != "median" or len(known) >= minimum) else None)
    return result


def policy(row, arm):
    if arm.startswith("official"):
        return arm
    value = row.get("theorem_body_policy") or row.get("policy", "")
    if value in {"strict", "default", "shared-checked"}:
        return "strict" if value == "strict" else "default"
    if value:
        raise ValueError("unknown theorem-body policy: " + str(value))
    flag = row.get("strict_theorem_bodies")
    if flag not in (None, ""):
        return "strict" if truth(flag) else "default"
    # Default is relative to the recorded executable, not a relabeling of old previews.
    strict = (re.search(r"(?:^|[-_])strict(?:[-_]|$)", row.get("key", "")) or
              row.get("arm") in {"strict", "native-strict", "proofserve-strict"})
    return "strict" if strict else "default"


def strict_costs(summary):
    points = {(row["dataset"], row["arm"], row["workers"], row["commit"], row["policy"]): row
              for row in summary}
    output = []
    for key, strict in sorted(points.items()):
        if key[-1] != "strict":
            continue
        default = points.get((*key[:-1], "default"))
        if default is None:
            continue
        row = dict(dataset=key[0], arm=key[1], workers=key[2], commit=key[3],
                   comparison="strict/default ratio of successful-point medians",
                   strict_successful=strict["successful"], default_successful=default["successful"])
        for metric in ("cpu_s", "wall_s"):
            numerator, denominator = strict[metric + "_median"], default[metric + "_median"]
            row[metric + "_ratio"] = (numerator / denominator if numerator is not None and
                                     denominator is not None and denominator > 0 else None)
        output.append(row)
    return output


def matrix_groups(rows, minimum=3):
    groups = {}
    for row in rows:
        if truth(row.get("manual_interruption")) or re.search(r"(?:resume|interrupt)", row["key"]):
            continue
        arm = "native" if row["arm"] in {"strict", "native-strict"} else row["arm"]
        if arm not in {"native", "no-persistence", "no-split-fallback", "official"}:
            continue
        if arm == "native":
            arm = next((name for name in ("no-persistence", "no-split-fallback")
                        if "-" + name + "-" in row["key"]), arm)
        if arm == "official":
            arm = next((name for name in ("official-default", "official-fresh")
                        if name in row["key"]), "official-unspecified")
        key = (row["dataset"], arm, row["workers"], row["commit"], policy(row, arm))
        groups.setdefault(key, []).append(row)
    output = []
    for (dataset, arm, workers, commit, mode), group in sorted(groups.items()):
        if len({row["repeat"] for row in group}) != len(group):
            raise ValueError("duplicate repeat in matrix point")
        output.append(dict(dataset=dataset, arm=arm, workers=workers, commit=commit, policy=mode,
                           modules=group[0].get("modules"), **stats(group, minimum=minimum)))
    return output


def external_groups(rows, acceptance=None):
    projects = (acceptance or {}).get("projects", [])
    if isinstance(projects, dict):
        projects = list(projects.values())
    scope = {p["project"]: p for p in projects}
    groups = {}
    for original in rows:
        row = dict(original)
        if row["arm"] not in {"proofserve", "proofserve-strict", "official-default", "official-fresh", "audit"}:
            continue
        row["bundle_commit"] = row.get("bundle_commit") or row.get("tool_commit", "")
        arm = "proofserve" if row["arm"] == "proofserve-strict" else row["arm"]
        metadata = scope.get(row["project"], {})
        row["theorem_body_policy"] = (row.get("theorem_body_policy") or
                                      row.get("native_theorem_body_policy") or
                                      metadata.get("theorem_body_policy", ""))
        workers = row.get("workers", "1")
        key = (*tuple(row.get(field, "") for field in
                      ("project", "upstream_commit", "bundle_commit", "checker_commit")),
               workers, arm, policy(row, arm))
        if not truth(row.get("cpu_accounting_valid", row.get("cpu_accounting_complete", "true"))):
            row["cpu_s"] = ""
        groups.setdefault(key, []).append(row)
    output = []
    for (project, source, bundle, checker, workers, arm, mode), group in sorted(groups.items()):
        if len({row["repeat"] for row in group}) != len(group):
            raise ValueError("duplicate repeat in external point")
        metadata = scope.get(project, {})
        closure = group[0].get("native_closure_modules") or metadata.get("native_closure_modules")
        roots = (group[0].get("official_default_modules") or group[0].get("local_roots") or
                 metadata.get("official_default_modules"))
        if arm == "proofserve" and group[0].get("scope") == "transitive_artifact_closure":
            closure = group[0]["checked_module_count"]
        if arm == "official-default" and group[0].get("scope") == "local_roots_with_trusted_imports":
            roots = group[0]["checked_module_count"]
        parity = [row.get("common_local_root_acceptance_equal",
                          row.get("local_root_acceptance_equal", "")) for row in group]
        output.append(dict(project=project, upstream_commit=source, bundle_commit=bundle,
                           checker_commit=checker, workers=workers, arm=arm, policy=mode,
                           native_closure_modules=closure, local_roots=roots,
                           common_root_parity="true" if all(truth(x) for x in parity) else "unestablished",
                           equal_proof_obligations=False,
                           **stats(group)))
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=Path("checker/results/fixed-cells.csv"))
    parser.add_argument("--external", type=Path, default=Path("data/external-projects/measurements.csv"))
    parser.add_argument("--acceptance", type=Path, help="M fixed-acceptance.json; default beside matrix")
    parser.add_argument("--external-status", type=Path, help="default timing-status.json beside external CSV")
    parser.add_argument("--resume", type=Path, help="M fixed-resume.json; default beside matrix")
    parser.add_argument("--failed-attempts", type=Path, help="default fixed-failed-attempts.csv beside matrix")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--matrix-only", action="store_true", help="publish the returned matrix while external timing is still pending")
    args = parser.parse_args()
    matrix, external = read(args.matrix), ([] if args.matrix_only else read(args.external))
    acceptance_path = args.acceptance or args.matrix.parent / "fixed-acceptance.json"
    external_status_path = args.external_status or args.external.parent / "timing-status.json"
    acceptance = json.loads(acceptance_path.read_text()) if acceptance_path.exists() else {}
    external_status = json.loads(external_status_path.read_text()) if external_status_path.exists() else {}
    native_summary, external_summary = matrix_groups(matrix, minimum=1 if args.preview else 3), external_groups(external, external_status)
    terminal_path = args.matrix.parent / "collection-terminal.json"
    terminal = json.loads(terminal_path.read_text()) if terminal_path.exists() else {}
    plan_path = args.matrix.parent / "planned-status.csv"
    plan = read(plan_path) if plan_path.exists() else []
    incomplete = [row for row in plan if row["status"] == "not_run"]

    if not args.preview:
        if str(acceptance.get("paper_eligible")).lower() == "false":
            raise ValueError("M acceptance sidecar explicitly designates nonfinal measurements")
        scoped_handoff = (terminal.get("handoff_ready") and
                          terminal.get("all_returned_native_and_cgroups_retired") and
                          terminal.get("status") == "collection_finished_with_incomplete_cells")
        if not truth(acceptance.get("paper_eligible")) and not scoped_handoff:
            raise ValueError("M data lack final designation or a verified retired scoped handoff")
        if args.matrix.name != "fixed-cells.csv":
            raise ValueError("use M's final fixed-cells.csv; preview/release single points are not final matrix data")
        if any(str(row.get("paper_eligible", "true")).lower() == "false" or
               "preview" in row.get("evaluation_status", "").lower() for row in matrix):
            raise ValueError("matrix is explicitly nonfinal")
        for key in ("within_dataset_module_sets_equal", "within_dataset_axiom_sets_equal",
                    "within_dataset_artifact_identities_equal", "actual_interruption_resume_equal"):
            if not acceptance.get(key):
                raise ValueError("missing completed M acceptance evidence: " + key)
        if scoped_handoff:
            if len(matrix) != terminal["returned_cells"] or len(plan) != terminal["original_planned_cells"]:
                raise ValueError("returned/plan inventories differ from the retired collection")
            if len(matrix) + len(incomplete) != len(plan) or {r["key"] for r in matrix} != {r["key"] for r in plan if r["status"] != "not_run"}:
                raise ValueError("returned and unattempted identities do not account for the plan")
            completed_native = sum(row["successful"] for row in native_summary
                                   if not row["arm"].startswith("official") and row["successful"] == 3)
            if completed_native != acceptance["complete_native_fixed_points"]:
                raise ValueError("completed repeated native scope differs from owner acceptance")
        if not native_summary:
            raise ValueError("empty final matrix")
        if not args.matrix_only and not external_status.get("final_system_timing_eligible") and not all(
                truth(row.get("final_system_timing_eligible")) for row in external):
            raise ValueError("external data are previews or lack a final timing designation")
        if any(not row["commit"] for row in native_summary):
            raise ValueError("matrix executable commit is missing")
        if any(not row["upstream_commit"] or not row["checker_commit"] or not row["bundle_commit"]
               for row in external_summary):
            raise ValueError("external tool/input commits are missing")
    args.out.mkdir(parents=True, exist_ok=True)
    prefix = "preview-" if args.preview else ""
    emit(args.out / (prefix + "system-summary.csv"), native_summary)
    policy_costs = strict_costs(native_summary)
    emit(args.out / (prefix + "strict-costs.csv"), policy_costs,
         ["dataset", "arm", "workers", "commit", "comparison", "strict_successful",
          "default_successful", "cpu_s_ratio", "wall_s_ratio"])
    if not args.matrix_only:
        emit(args.out / (prefix + "external-summary.csv"), external_summary)
    emit(args.out / (prefix + "unattempted-cells.csv"), incomplete, None if incomplete else ["key", "status", "reason"])
    failed = [dict(row, origin="matrix") for row in matrix if row.get("returncode") != "0"]
    failed += [dict(row, origin="external") for row in external if row.get("returncode") != "0"]
    failed_path = args.failed_attempts or args.matrix.parent / "fixed-failed-attempts.csv"
    archived_failures = read(failed_path) if failed_path.exists() else []
    seen_failures = {(r.get("key"), r.get("run_key", r.get("key")), r.get("attempt", "1"), r.get("returncode")) for r in failed}
    failed += [dict(row, origin="archived-matrix-attempt") for row in archived_failures
               if row.get("returncode") != "0" and
               (row.get("key"), row.get("run_key", row.get("key")), row.get("attempt", "1"), row.get("returncode")) not in seen_failures]
    emit(args.out / (prefix + "retained-nonzero-attempts.csv"), failed,
         None if failed else ["origin", "key", "project", "returncode", "cpu_s", "wall_s"])
    labels = {"math": "Nat.Basic", "grid": "Grid", "barrier": "Barrier"}
    native = [row for row in native_summary if row["arm"] == "native" and
              (args.preview or (row["successful"] == 3 and row["cpu_s_observed"] == 3 and row["wall_s_observed"] == 3))]
    workers = sorted({row["workers"] for row in native}, key=int)
    points = {}
    for row in native:
        points.setdefault((row["dataset"], row["policy"], row["commit"]), {})[row["workers"]] = row
    table = [r"\begin{tabular}{ll" + "r" * len(workers) + "}", r"\toprule",
             "Closure/mode & Clock & " + " & ".join(map(tex, workers)) + r"\\", r"\midrule"]
    for (dataset, mode, commit), group in sorted(points.items(), key=lambda x: ({"math": 0, "grid": 1, "barrier": 2}.get(x[0][0], 9), x[0][1], x[0][2])):
        name = labels.get(dataset, dataset) + (" S" if mode == "strict" else " D")
        if len({row["commit"] for row in native if row["dataset"] == dataset}) > 1:
            name += " " + commit[:7]
        for metric, clock in (("cpu_s", "CPU s"), ("wall_s", "Wall s")):
            cells = [fmt(group[worker][metric + "_median"]) if worker in group else "--"
                     for worker in workers]
            table.append((tex(name) if metric == "cpu_s" else "") + " & " + clock +
                         " & " + " & ".join(cells) + r"\\")
    table += [r"\bottomrule", r"\end{tabular}"]
    (args.out / (prefix + "system-table.tex")).write_text("\n".join(table) + "\n")
    if not args.matrix_only:
        table = [r"\begin{tabular}{lrrrrr}", r"\toprule",
                 r"& N/O & \multicolumn{2}{c}{ProofServe} & \multicolumn{2}{c}{Official}\\",
                 r"Project & modules & CPU & Wall & CPU & Wall\\", r"\midrule"]
        projects = sorted({row["project"] for row in external_summary if row["arm"] == "proofserve"},
                          key=lambda name: {"newspeak": 0, "solar": 1, "samuelburbulla-proofs": 2}.get(name, 9))
        for project in projects:
            native = [row for row in external_summary if row["project"] == project and row["arm"] == "proofserve" and row["policy"] == "default"]
            official = [row for row in external_summary if row["project"] == project and row["arm"] == "official-default"]
            if len(native) != 1 or len(official) != 1:
                raise ValueError("a project table row must identify one tool/input version per arm")
            n, o = native[0], official[0]
            name = ("AI proofs" if "samuelburbulla" in project else
                    "Newspeak" if "newspeak" in project.lower() else
                    "Solar" if "solar" in project.lower() else
                    "CrocSwap" if "croc" in project.lower() else project)
            table.append(tex(name) + " & " + tex(str(n["native_closure_modules"]) + "/" + str(o["local_roots"])) + " & " +
                         " & ".join(fmt(row[key]) for row, key in
                                    ((n, "cpu_s_median"), (n, "wall_s_median"),
                                     (o, "cpu_s_median"), (o, "wall_s_median"))) + r"\\")
        table += [r"\bottomrule", r"\end{tabular}"]
        (args.out / (prefix + "external-table.tex")).write_text("\n".join(table) + "\n")
    resume_path = args.resume or args.matrix.parent / "fixed-resume.json"
    resume = json.loads(resume_path.read_text()) if resume_path.exists() else None

    scaling = []
    ablations = []
    for row in native_summary:
        if row["policy"] != "default" or row["successful"] != 3:
            continue
        baseline = next((x for x in native_summary if x["dataset"] == row["dataset"] and
                         x["commit"] == row["commit"] and x["arm"] == "native" and
                         x["policy"] == "default" and x["workers"] == "1" and x["successful"] == 3), None)
        default8 = next((x for x in native_summary if x["dataset"] == row["dataset"] and
                         x["commit"] == row["commit"] and x["arm"] == "native" and
                         x["policy"] == "default" and x["workers"] == "8" and x["successful"] == 3), None)
        if row["arm"] == "native" and row["workers"] == "8" and baseline:
            scaling.append(dict(dataset=row["dataset"], commit=row["commit"],
                wall_speedup=baseline["wall_s_median"]/row["wall_s_median"],
                cpu_increase_fraction=row["cpu_s_median"]/baseline["cpu_s_median"]-1))
        if row["arm"] in {"no-persistence", "no-split-fallback"} and default8:
            ablations.append(dict(dataset=row["dataset"], arm=row["arm"], commit=row["commit"],
                wall_ratio=row["wall_s_median"]/default8["wall_s_median"],
                cpu_ratio=row["cpu_s_median"]/default8["cpu_s_median"]))
    emit(args.out / (prefix + "scaling.csv"), scaling,
         ["dataset", "commit", "wall_speedup", "cpu_increase_fraction"])
    emit(args.out / (prefix + "ablations.csv"), ablations,
         ["dataset", "arm", "commit", "wall_ratio", "cpu_ratio"])
    bounds = []
    for row in matrix:
        if policy(row, row["arm"]) != "strict" or row["returncode"] != "124":
            continue
        default = next((x for x in native_summary if x["dataset"] == row["dataset"] and
                        x["commit"] == row["commit"] and x["workers"] == row["workers"] and
                        x["arm"] == "native" and x["policy"] == "default" and x["successful"] == 3), None)
        if default:
            bounds.append(dict(key=row["key"], observed_timeout_wall_s=numeric(row,"wall_s"),
                default_wall_median_s=default["wall_s_median"],
                observed_censor_ratio=numeric(row,"wall_s")/default["wall_s_median"],
                interpretation="single censored strict attempt / default successful median; no strict median or completed cost"))
    emit(args.out / (prefix + "strict-bounds.csv"), bounds,
         ["key","observed_timeout_wall_s","default_wall_median_s","observed_censor_ratio","interpretation"])
    macros = []
    if not args.preview:
        ablation_text = []
        for arm, label in [("no-persistence", "Disabling persistence"), ("no-split-fallback", "Disabling split fallback")]:
            selected = sorted([x for x in ablations if x["arm"] == arm], key=lambda x: {"math":0,"grid":1}.get(x["dataset"],9))
            ablation_text.append(label + " changes Nat.Basic/Grid wall by " +
                "/".join(f'{100*(x["wall_ratio"]-1):+.1f}' for x in selected) +
                r"\% and CPU by " + "/".join(f'{100*(x["cpu_ratio"]-1):+.1f}' for x in selected) + r"\%.")
        macros.append(r"\def\AblationSummary{" + " ".join(ablation_text) + "}")

        order = {"math": 0, "grid": 1, "barrier": 2}
        chosen = sorted(scaling, key=lambda x:order.get(x["dataset"],9))
        macros.append(r"\def\ScalingSummary{Eight versus one worker gives " +
                      "/".join(fmt(x["wall_speedup"]) for x in chosen) +
                      r"$\times$ wall speedups for Nat.Basic/Grid/Barrier, with CPU increases of " +
                      "/".join(f'{100*x["cpu_increase_fraction"]:.1f}' for x in chosen) + r"\%, respectively.}")
        strict = next((x for x in policy_costs if x["dataset"] == "math" and x["wall_s_ratio"] is not None), None)
        if strict:
            macros.append(r"\def\StrictSummary{Nat.Basic strict mode costs " + fmt(strict["wall_s_ratio"]) +
                          r"$\times$ wall and " + fmt(strict["cpu_s_ratio"]) +
                          r"$\times$ CPU versus default at eight workers.}")
        if bounds:
            bound = bounds[0]
            macros.append(r"\def\StrictGridSummary{Grid strict mode timed out at 1,800 s (" +
                          r"at least $"+f'{math.floor(bound["observed_censor_ratio"]*10)/10:.1f}'+
                          r"\times$ default-eight median); this single censored attempt is not a strict median or full cost.}")
        if resume:
            macros.append(r"\def\ResumeSummary{One deliberate interruption and resume preserves the 1,330-module result and reuses one segment. Combined wall/CPU is "+
                          fmt(resume["wall_s"])+"/"+fmt(resume["cpu_s"])+
                          " s, "+f'{100*resume["wall_overhead_fraction"]:.2f}'+"/"+
                          f'{100*resume["cpu_overhead_fraction"]:.2f}'+r"\% above uninterrupted four-worker medians.}")
        macros.append(r"\def\MatrixScopeSummary{The 71-cell plan has 61 returned attempts and 10 unattempted cells.}")
        (args.out/"system-metrics.tex").write_text("\n".join(macros)+"\n")
    context_path = args.matrix.parent/"context.json"
    context = json.loads(context_path.read_text()) if context_path.exists() else {}
    try:
        publication = subprocess.run(["git","log","-1","--format=%H","--",str(args.matrix)],capture_output=True,text=True).stdout.strip() or None
    except OSError:
        publication = None
    external_publication = None
    if not args.matrix_only:
        try:
            external_publication = subprocess.run(
                ["git", "log", "-1", "--format=%H", "--", str(args.external)],
                capture_output=True, text=True).stdout.strip() or None
        except OSError:
            pass
    provenance = dict(publication_commit=publication, external_publication_commit=external_publication,
                      external_acceptance_evidence=None if args.matrix_only else external_status, matrix_context=context, preview=args.preview, matrix=str(args.matrix), external=None if args.matrix_only else str(args.external),
                      acceptance=str(acceptance_path), external_status=None if args.matrix_only else str(external_status_path),
                      matrix_commits=sorted({row["commit"] for row in native_summary}),
                      matrix_driver_commit=acceptance.get("driver_commit"),
                      archived_failed_attempts=str(failed_path) if failed_path.exists() else None,
                      full_ranges="system-summary.csv and external-summary.csv",
                      official_speedup="not computed: proof obligations differ",
                      failed_costs="retained individually, excluded from successful-point medians",
                      resumption_source=str(resume_path) if resume is not None else None,
                      resumption=resume,
                      acceptance_evidence=acceptance, collection_terminal=terminal, unattempted_cells=incomplete,
                      original_plan_complete=terminal.get("overall_original_matrix_complete"),
                      strict_cost_pairs=policy_costs,
                      policy_labels="default refers to the recorded tool default; strict is separate",
                      policy_cost_source="returned matrix only; old e155 isolation is not new strict timing")
    (args.out / (prefix + "system-provenance.json")).write_text(json.dumps(provenance, indent=2) + "\n")
    if not args.preview:
        (args.out / "matrix-ready.tex").write_text(r"\def\MatrixResultsReady{1}" + "\n")
        if not args.matrix_only:
            (args.out / "external-ready.tex").write_text(r"\def\ExternalResultsReady{1}" + "\n")
            (args.out / "system-ready.tex").write_text(r"\def\SystemResultsReady{1}" + "\n")
    print(json.dumps(dict(preview=args.preview, matrix_groups=len(native_summary),
                          external_groups=len(external_summary), nonzero_attempts=len(failed))))


if __name__ == "__main__":
    main()
