#!/usr/bin/env python3
"""Describe actual published source CPU; do not infer checker cost or regimes."""
from pathlib import Path
import csv, io, json, os, subprocess, datetime

D = Path(__file__).resolve().parent
R = D.parent.parent
def main():
    os.sched_setaffinity(0, {8})
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=R, text=True).strip()
    def read(name):
        text = subprocess.check_output(["git", "show", head + ":research/decoupled-check/" + name], cwd=R, text=True)
        return list(csv.DictReader(io.StringIO(text)))
    census = {v["module"]: v for v in read("ramsey-target-census.csv")}
    costs = read("ramsey-source-costs.csv")
    target_total = sum(float(v["source_cpu_s"]) for v in costs if v["target"] == "True")
    groups = {g: dict(group=g, source_modules=0, source_cpu_s=0.0, source_wall_sum_s=0.0,
                      target_cpu_share=None, kernel_cpu_s=None)
              for g in ["dependency", "kernel-marked", "unmarked-certificate-family",
                        "other-unmarked-plain-decide", "other-unmarked"]}
    for v in costs:
        label = census[v["module"]]["descriptive_group"] if v["target"] == "True" else "dependency"
        g = groups[label]
        g["source_modules"] += 1
        g["source_cpu_s"] += float(v["source_cpu_s"])
        g["source_wall_sum_s"] += float(v["source_wall_s"])
    for label, g in groups.items():
        if label != "dependency" and target_total:
            g["target_cpu_share"] = g["source_cpu_s"] / target_total
    with (D / "ramsey-source-groups.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=next(iter(groups.values())), lineterminator=chr(10))
        w.writeheader(); w.writerows(groups.values())
    n = sum(g["source_modules"] for k, g in groups.items() if k != "dependency")
    provenance = dict(input_commit=head, measured_targets=n, target_population=444,
        complete_source_coverage=n == 444, target_source_cpu_s=target_total,
        dependency_ordered_prefix=True, kernel_cpu_inferred=False,
        created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    (D / "ramsey-source-groups-provenance.json").write_text(json.dumps(provenance, indent=2)+chr(10))
    assert sum(g["source_modules"] for g in groups.values()) == len(costs)
    assert abs(sum(g["source_cpu_s"] for g in groups.values()) - sum(float(v["source_cpu_s"]) for v in costs)) < 0.0001
    print(json.dumps(provenance))
    for g in groups.values(): print(g)
if __name__ == "__main__": main()
