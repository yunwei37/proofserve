# Census qualification data, 2026-11-04

Result: **failed instruction-invariance gate; no full census started**.
Measurement commit: 2c901ec4f0bbf73b75b534bbc255fcc973aebe6f.
See ../../census-plan.md for the complete result, metric sensitivity and choices.

This is 20 purposeful original-sample modules × four conditions × three
repetitions (240 foreground calls), 240 enabled/disabled-counter controls,
and 1,413 completed background compiler calls. It is not a probability sample,
a full-library measurement, a proof checker receipt, or a speedup claim.

- census-gate-attempts.csv.gz: all 1,893 returned native attempts; role,
  condition, repetition, affinity, source hash, compiler commit/version,
  native CPU, wall, max RSS, actual cgroup peak, instruction modes/coverage.
  Disabled counters are empty, not zero instructions. Background cost is
  explicitly separate from the foreground and overhead controls.
- census-gate-modules.csv: per-module medians in all four conditions,
  user/kernel/total instruction spreads and loaded/quiet CPU ratios.
- census-gate-overhead.csv: median of three paired enabled/disabled differences
  per module/pool; not a uniform 1% guarantee.
- census-gate-artifact-parity.csv: hash provenance, distinct hashes and retained
  historical availability. census-gate-direct-byte-comparison.csv additionally
  records actual streaming byte comparisons of all three compiler products.
- protocol.json: frozen exact inputs/settings, including machine-specific
  paths. terminal.json: completed controller result. environment.json labels
  post-run observations. self-review.json: cardinality/options/quantile checks.
- counter-control.c and counter-control.json: tiny pthread hardware/ABI setup
  control. Its unlocked pre-gate P-core portion is disclosed in census-plan.md
  and excluded from Lean timing and gate statistics.
- source-acquisition.json: full pinned source acquisition completed before
  the gate. It postdates the separate initial readiness CSV, which is retained
  as its original snapshot rather than rewritten.

Recalculate the gate statistics directly from the small module table:

    import csv, statistics
    rows = list(csv.DictReader(open("census-gate-modules.csv")))
    v = sorted(float(r["cross_condition_spread"]) for r in rows)
    print(statistics.median(v), v[18] * .95 + v[19] * .05)

These are fractions: 0.01331198 and 0.03149811 (1.3312% and 3.1498%).
Each spread is max/min minus one across four condition medians. P95 uses
linear interpolation at (n-1)*.95. Relative-to-P-quiet pooled deviations use
another statistic and are retained separately; they do not replace the failed
cross-condition comparison.

To regenerate all summaries from retained raw JSONL:

    python data/openai-math-4eaee875/analyze_census_gate.py RAW_POINT OUTPUT_DIR

The analyzer exports a plain attempt CSV; this package compresses that file.
Raw native logs and products remain outside Git on the existing PVC at
/workspaces/.agent-state/gpu-smt-captures/workloads/census-gate-20261104/run-1.
The gate runner takes --config and --out, requires Linux x86-64, the documented
hybrid PMUs and core masks, a mounted /workspaces PVC and already-built pinned
dependencies. Porting its machine-specific protocol is a different experiment.
It never launches a census. Do not run it as a portable ProofServe product
benchmark. Production check/audit acceptance is a separate M/O deliverable.

Hashes are provenance; direct byte equality is checked separately. Compiler
success and byte equality do not prove absence of axioms or independent kernel
acceptance. Current bytes agree for all 20 modules. Retained historical
olean/ilean/C sets exist for only 17; the other three are explicitly unknown.
CPU and wall stay separate, P/E CPU is never converted, and failed or missing
attempt costs are never imputed. This analysis is self-review (自审).
