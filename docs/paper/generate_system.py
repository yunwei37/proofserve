#!/usr/bin/env python3
"""Generate committed-release tables; preview measurements never become paper-ready."""
import argparse
import csv
import json
import math
import re
from pathlib import Path
import statistics


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


def stats(group):
    result = dict(observations=len(group),
                  successful=sum(row.get("returncode") == "0" for row in group))
    for metric in ("cpu_s", "wall_s"):
        values = [numeric(row, metric) for row in group if row.get("returncode") == "0"]
        known = [value for value in values if value is not None]
        # A partially known group is not a complete request-cost observation.
        result[metric + "_observed"] = len(known)
        for suffix, function in (("median", statistics.median), ("min", min), ("max", max)):
            result[metric + "_" + suffix] = function(known) if known and len(known) == len(values) else None
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


def matrix_groups(rows):
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
                           modules=group[0].get("modules"), **stats(group)))
    return output


def external_groups(rows):
    groups = {}
    for row in rows:
        # An interrupted preview resumed in another call is not a fresh full cost.
        if row["arm"] not in {"proofserve", "proofserve-strict", "official-default", "official-fresh", "audit"}:
            continue
        arm = "proofserve" if row["arm"] == "proofserve-strict" else row["arm"]
        key = (*tuple(row.get(field, "") for field in
                      ("project", "upstream_commit", "bundle_commit", "checker_commit")),
               arm, policy(row, arm))
        copied = dict(row)
        if not truth(row.get("cpu_accounting_valid", row.get("cpu_accounting_complete", "true"))):
            copied["cpu_s"] = ""
        groups.setdefault(key, []).append(copied)
    output = []
    for (project, source, bundle, checker, arm, mode), group in sorted(groups.items()):
        parity = [row.get("common_local_root_acceptance_equal",
                          row.get("local_root_acceptance_equal", "")) for row in group]
        output.append(dict(project=project, upstream_commit=source, bundle_commit=bundle,
                           checker_commit=checker, arm=arm, policy=mode,
                           native_closure_modules=group[0].get("native_closure_modules"),
                           local_roots=group[0].get("official_default_modules",
                                                   group[0].get("local_roots")),
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
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    matrix, external = read(args.matrix), read(args.external)
    acceptance_path = args.acceptance or args.matrix.parent / "fixed-acceptance.json"
    external_status_path = args.external_status or args.external.parent / "timing-status.json"
    acceptance = json.loads(acceptance_path.read_text()) if acceptance_path.exists() else {}
    external_status = json.loads(external_status_path.read_text()) if external_status_path.exists() else {}
    native_summary, external_summary = matrix_groups(matrix), external_groups(external)
    if not args.preview:
        if args.matrix.name != "fixed-cells.csv":
            raise ValueError("use M's final fixed-cells.csv; preview/release single points are not final matrix data")
        if any(str(row.get("paper_eligible", "true")).lower() == "false" or
               "preview" in row.get("evaluation_status", "").lower() for row in matrix):
            raise ValueError("matrix is explicitly nonfinal")
        for key in ("within_dataset_module_sets_equal", "within_dataset_axiom_sets_equal",
                    "within_dataset_artifact_identities_equal", "actual_interruption_resume_equal"):
            if not acceptance.get(key):
                raise ValueError("missing completed M acceptance evidence: " + key)
        for row in native_summary:
            if row["observations"] != 3:
                raise ValueError("final matrix point does not contain three repeat outcomes")
            if not row["arm"].startswith("official"):
                if row["successful"] != 3 or row["cpu_s_observed"] != 3 or row["wall_s_observed"] != 3:
                    raise ValueError("native/ablation point lacks three complete CPU/wall observations")
        if not native_summary:
            raise ValueError("empty final matrix")
        if not external_status.get("final_system_timing_eligible") and not all(
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
    emit(args.out / (prefix + "external-summary.csv"), external_summary)
    failed = [dict(row, origin="matrix") for row in matrix if row.get("returncode") != "0"]
    failed += [dict(row, origin="external") for row in external if row.get("returncode") != "0"]
    emit(args.out / (prefix + "retained-nonzero-attempts.csv"), failed,
         None if failed else ["origin", "key", "project", "returncode", "cpu_s", "wall_s"])
    labels = {"math": "Nat.Basic", "grid": "Grid", "barrier": "Barrier"}
    native = [row for row in native_summary if row["arm"] == "native"]
    workers = sorted({row["workers"] for row in native}, key=int)
    points = {}
    for row in native:
        points.setdefault((row["dataset"], row["policy"], row["commit"]), {})[row["workers"]] = row
    table = [r"\begin{tabular}{ll" + "r" * len(workers) + "}", r"\toprule",
             "Closure/mode & Clock & " + " & ".join(map(tex, workers)) + r"\\", r"\midrule"]
    for (dataset, mode, commit), group in sorted(points.items()):
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
    table = [r"\begin{tabular}{lrrrrr}", r"\toprule",
             r"& Closure & \multicolumn{2}{c}{ProofServe} & \multicolumn{2}{c}{Official}\\",
             r"Project & modules & CPU & Wall & CPU & Wall\\", r"\midrule"]
    projects = sorted({row["project"] for row in external_summary if row["arm"] == "proofserve"})
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
        table.append(tex(name) + " & " + tex(n["native_closure_modules"]) + " & " +
                     " & ".join(fmt(row[key]) for row, key in
                                ((n, "cpu_s_median"), (n, "wall_s_median"),
                                 (o, "cpu_s_median"), (o, "wall_s_median"))) + r"\\")
    table += [r"\bottomrule", r"\end{tabular}"]
    (args.out / (prefix + "external-table.tex")).write_text("\n".join(table) + "\n")
    resume_path = args.resume or args.matrix.parent / "fixed-resume.json"
    resume = json.loads(resume_path.read_text()) if resume_path.exists() else None
    provenance = dict(preview=args.preview, matrix=str(args.matrix), external=str(args.external),
                      acceptance=str(acceptance_path), external_status=str(external_status_path),
                      matrix_commits=sorted({row["commit"] for row in native_summary}),
                      full_ranges="system-summary.csv and external-summary.csv",
                      official_speedup="not computed: proof obligations differ",
                      failed_costs="retained individually, excluded from successful-point medians",
                      resumption_source=str(resume_path) if resume is not None else None,
                      resumption=resume,
                      acceptance_evidence=acceptance,
                      strict_cost_pairs=policy_costs,
                      policy_labels="default refers to the recorded tool default; strict is separate",
                      policy_cost_source="returned matrix only; old e155 isolation is not new strict timing")
    (args.out / (prefix + "system-provenance.json")).write_text(json.dumps(provenance, indent=2) + "\n")
    if not args.preview:
        (args.out / "system-ready.tex").write_text(r"\def\SystemResultsReady{1}" + "\n")
    print(json.dumps(dict(preview=args.preview, matrix_groups=len(native_summary),
                          external_groups=len(external_summary), nonzero_attempts=len(failed))))


if __name__ == "__main__":
    main()
