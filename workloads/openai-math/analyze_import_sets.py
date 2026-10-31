#!/usr/bin/env python3
"""Exact import-name sets and graph closure classes, not native environment keys."""
import argparse
from collections import Counter
import csv
import gzip
import json
import os
from pathlib import Path
import resource
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plan_build import load


def csv_rows(path, rows, fields):
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "wt", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--inventory", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    os.sched_setaffinity(0, set(range(8, 16)))
    args.out.mkdir(parents=True, exist_ok=False)
    profiles, modules, deps, external, reverse, order, depth = load(args.inventory)
    del profiles, reverse, depth
    external_names = sorted(set().union(*external.values()))
    labels = external_names + sorted(modules)
    ids = {name: i for i, name in enumerate(labels)}
    direct, closure, ordered = {}, {}, {}
    per_module = {}
    sequences = {m: [] for m in modules}
    with gzip.open(args.inventory / "content/imports.csv.gz", "rt") as f:
        for row in csv.DictReader(f):
            sequences[row["module"]].append(row["imports"])

    def intern(groups, key, module):
        record = groups.get(key)
        if record is None:
            record = dict(group_id=len(groups)+1, module_count=0,
                          representative_module=module, key=key)
            groups[key] = record
        record["module_count"] += 1
        return record

    for m in order:
        names = tuple(sorted(deps[m] | external[m]))
        dg = intern(direct, names, m)
        og = intern(ordered, tuple(sequences[m]), m)
        bits = 0
        for name in external[m]:
            bits |= 1 << ids[name]
        for d in deps[m]:
            bits |= per_module[d]["closure"]["key"] | (1 << ids[d])
        cg = intern(closure, bits, m)
        per_module[m] = dict(direct=dg, closure=cg, ordered=og)

    scope_summary, top_rows, hist_rows = [], [], []
    for kind, groups in [("direct_import_set", direct),
                         ("internal_transitive_closure_plus_external_frontier", closure),
                         ("ordered_direct_import_names", ordered)]:
        ranked = sorted(groups.values(), key=lambda x: (-x["module_count"], x["group_id"]))
        cumulative = 0
        for rank, rec in enumerate(ranked, 1):
            count = rec["module_count"]
            cardinality = rec["key"].bit_count() if kind.startswith("internal") else len(rec["key"])
            common = dict(kind=kind, rank=rank, group_id=rec["group_id"],
                          module_count=count, import_name_count=cardinality,
                          representative_module=rec["representative_module"])
            cumulative += count
            if rank <= 100:
                top_rows.append(dict(**common, cumulative_modules=cumulative,
                                     cumulative_fraction=cumulative/len(modules)))
        all_rows = []
        for rec in groups.values():
            all_rows.append(dict(group_id=rec["group_id"], module_count=rec["module_count"],
                import_name_count=rec["key"].bit_count() if kind.startswith("internal") else len(rec["key"]),
                representative_module=rec["representative_module"]))
        csv_rows(args.out / (kind+"-all-classes.csv.gz"), all_rows, list(all_rows[0]))
        hist = Counter(x["module_count"] for x in groups.values())
        hist_rows.extend(dict(kind=kind, class_module_count=n, classes=number,
                             covered_modules=n*number) for n, number in sorted(hist.items()))
        empty = groups.get(0 if kind.startswith("internal") else ())
        top100 = sum(x["module_count"] for x in ranked[:100])
        scope_summary.append(dict(kind=kind, modules=len(modules), distinct_classes=len(groups),
            top1_modules=ranked[0]["module_count"],
            top100_modules=top100, top100_fraction=top100/len(modules),
            empty_import_class_modules=empty["module_count"] if empty else 0,
            singleton_classes=hist.get(1,0),
            ideal_one_process_per_class_loads=len(groups),
            ideal_same_class_reuse_fraction=1-len(groups)/len(modules),
            scope="names in pinned source graph; not elaborated state/options/import modifiers or external-library closure"))

    mapping = [dict(module=m, path=modules[m],
                    direct_group_id=x["direct"]["group_id"],
                    closure_group_id=x["closure"]["group_id"],
                    ordered_group_id=x["ordered"]["group_id"]) for m,x in per_module.items()]
    csv_rows(args.out/"module-groups.csv.gz", mapping, list(mapping[0]))
    csv_rows(args.out/"top100-classes.csv", top_rows, list(top_rows[0]))
    csv_rows(args.out/"class-size-histogram.csv", hist_rows, list(hist_rows[0]))
    csv_rows(args.out/"summary.csv", scope_summary, list(scope_summary[0]))
    receipt = dict(source_revision="4eaee87548250b2682affda7d05d947c05554bae",
        modules=len(modules), external_frontier_names=len(external_names),
        topological_modules=len(order), exact_integer_bitsets=True,
        no_hash_collision_or_approximation=True, native_runs=0,
        affinity=sorted(os.sched_getaffinity(0)),
        analysis_leader_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        findings=scope_summary)
    (args.out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt),flush=True)


if __name__ == "__main__":
    main()
