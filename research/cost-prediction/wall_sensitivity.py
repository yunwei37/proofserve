#!/usr/bin/env python3
"""Wall-target sensitivity using the same fixed design; no tuning or Lean."""
import csv, math
import fit as model

def main():
    rows = [dict(r, _actual=r["compiler_wall_s"]) for r in csv.DictReader(
        (model.OUT / "features-and-costs.csv").open())
        if r["primary_completed"] == "True" and r["compiler_wall_s"]]
    ids = list(range(len(rows)))
    y = [math.log(float(r["_actual"])) for r in rows]
    summaries = []
    for name in ["constant", "bytes", "imports", "static", "regime"]:
        X = [model.feats(r, name) for r in rows]
        for scheme in ["loo_module", "5fold", "project_5fold"]:
            tests = [[i] for i in ids] if scheme == "loo_module" else model.folds(rows, scheme == "project_5fold")
            predictions = [None] * len(rows)
            for test in tests:
                excluded = set(test)
                b, _ = model.fit(X, y, [i for i in ids if i not in excluded])
                for i in test:
                    predictions[i] = model.safeexp(model.dot(X[i], b))
            vals = model.errors(rows, predictions)
            for domain in ["all", "ordinary_proxy", "certificate_proxy"]:
                subset = [v for v in vals if domain == "all" or
                          (v["regime"] == "1") == (domain == "certificate_proxy")]
                summaries.append(dict(cohort="primary31_wall", model=name,
                    validation=scheme, domain=domain, **model.metric(subset),
                    **model.bootstrap(subset, 500)))
    model.writecsv(model.OUT / "wall-errors.csv", summaries)

if __name__ == "__main__":
    main()
