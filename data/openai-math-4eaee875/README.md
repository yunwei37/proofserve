# OpenAI math: native build-cost sample (v1)

A small, citable data package for **openai/math at
4eaee87548250b2682affda7d05d947c05554bae**: 163,097 source modules, 21 strata,
42 original probability draws (two per stratum, seed 20261030).

**Current snapshot: 41 completed costs / 42 original draws.** The last draw
is still being prepared. Blank costs are missing, never zero or imputed. A completed_cost means a
native compiler return under the frozen flags, not an axiom-free proof or
independent-checker certificate; upstream admits/axioms are not removed.
The frozen 12 independent precision draws are not pooled into the original42.
This directory is the stable small-table interface; research raw logs remain
in their original retained locations. Column names below form the v1 contract.

## Files and units

| File | Contents |
|---|---|
| sample-costs.csv | 42 original identities, statuses, native CPU/wall, weights and proxy classes |
| strata.csv | 21 populations, sample sizes, inclusion probabilities, N_h/2 weights |
| closure-ratios.csv | Selected closure measurements used for checker transfer factors, CPU and wall kept separate |
| sampling-intervals.csv | Covered-cell nominal source-sampling intervals and fixed-factor transfers, by regime |
| scenario-ranges.csv | Full-frame missing-cost / closure-factor sensitivity ranges, **not confidence intervals** |
| metadata.json | Pins, snapshot coverage and measurement scope |
| precision-design.csv | Exactly 12 fixed independent remainder draws, kept separate from original42 |
| summarize.py | Recompute covered-cell CPU/variance from this small bundle only |
| export.py | Rebuild tables from preserved original-frame evidence; no native measurement |

sample-costs.csv columns are fixed:
module, stratum, population_modules, sample_size, inclusion_probability,
expansion_weight, regime_proxy, status, user_cpu_s, system_cpu_s, cpu_s,
wall_s, source_bytes, memory_option_MiB, threads, pcore_lock, source_exact,
native_retired, cgroup_retired, source_reference.

CPU seconds are native **user + system**, not elapsed times divided by eight.
Native compile includes per-module imports and .olean/.ilean/C emission.
It excludes prerequisite preparation, queueing, process setup/cleanup,
separate C compilation/linking, cache acquisition and whole-Lake driver costs.
Therefore the weighted sum is a **native per-module build estimate**, not
a measured end-to-end full-Lake build. Source wall seconds are a separate
per-module observation, not a parallel campaign makespan.

## Reproducibility and classification

Lean **4.34.1**, Mathlib **d13f23b723b8a846827a245b89c10fc7d3f11612**.
No -M; authored/native-default heartbeats; eight threads; P cores 0–7 on
i9-14900K; one timed request under the recorded shared P-core lock.
External cgroup memory protection, up to 16 GiB W-owned RSS response.
Sampled RSS and cgroup-charged memory are different quantities; neither a
sampled threshold nor an observed peak is a kernel hard RSS quota.
Host-restart interruptions are excluded, not relabeled as native censors.

The strata combine fixed source-size percentile boundaries (4,400 / 15,057 /
80,757 bytes for the frozen 50th/90th/99th-percentile cuts), source import
depth bins (1–10 / 11–100 / 101+), and any explicit comment/string-masked
decide +kernel occurrence. Depth is the longest unit-weight source-import
chain inside the pinned universe, excluding external dependency depth. Source
module identity uses the longest matching of lean/ and the nested
lean/ComparatorChallenges/HodgeConjectureCMAbelianVarieties/ source roots.
regime_proxy is computation_certificate for that occurrence, otherwise
ordinary_mathematics. This matches the W probability design; it is **not**
an elaborated cost classifier and can miss macro-generated or other expensive
closed computation. Prerequisite builds receive no sampling weight.

Original inference uses sum_h N_h * mean(y_h) with finite-population variance
sum_h N_h^2 * (1 - n_h/N_h) * s_h^2/n_h. Nominal 95% t intervals use
Satterthwaite degrees of freedom; n_h=2 and heavy tails make them fragile.
Incomplete strata are not silently promoted to complete cells. Scenario
ranges substitute observed class extremes for missing original costs, and
vary selected closure transfer ratios. They are neither finite population
bounds nor statistical confidence intervals.

Checker CPU is **transferred**, not an actual whole-library checker census.
Ordinary closures use Falconer segmented 6.3124% and matched Mathlib segmented
8.9514% source-to-check CPU ratios. Computational settings use the separately
reported Grid/Amplitudes closure measurements. Parallel factors must use CPU
ratios; elapsed speedups are not CPU savings. Calibration and model uncertainty
are excluded from the nominal source-sampling intervals. See each ratio's
scope/evidence fields; no population-wide universal ratio is asserted.

From a repository checkout with retained research inputs:

```sh
python3 data/openai-math-4eaee875/export.py \
  --frame workloads/openai-math/final-seven-20261102/collection-remaining-four-hostrecovery-20261103T1512/source41-GroundMainFinalStructuralRefinementOutputs/sample-costs.csv \
  --staircase workloads/openai-math/final-seven-20261102/collection-remaining-four-hostrecovery-20261103T1512/source41-GroundMainFinalStructuralRefinementOutputs/latest-staircase
```

This exports evidence; it does not download upstream source or reproduce a
measurement on a different machine. The published CSVs can be read without
those raw files or a Workspace. source_reference is provenance, not a public
download URL or a required runtime path.

Upstream source is Apache-2.0; dependencies retain their own licenses.
Measurement tables and tooling are distributed under this repository's license.
Cite the upstream immutable commit, this package path and the repository
revision of the snapshot used. No claim of final paper acceptance is implied.


## Read the published package alone

No Lean toolchain, raw captures or Workspace path is needed:

```sh
python3 data/openai-math-4eaee875/summarize.py
python3 data/openai-math-4eaee875/summarize.py --json
```

The summarizer recomputes covered-cell totals and finite-population variance
from the small original tables, and carries the published sampling intervals
and scenario ranges as separate fields. It never fills incomplete strata.

The frozen additional12 design is independent SRS of each of two remainders.
Each selected cell conditions on its two already observed original members:
T = sum(known2) + (N - 2) * mean(fresh6).
The known members carry weight one in that conditional component. The original
42 HT estimate remains separately available; do not pool old2+new6 as eight
exchangeable draws. Adaptive cell selection and heavy tails limit interpretation
of the whole-frame hybrid nominal interval. All six costs must return before
a cell is substituted. No further draws, precision target or stopping threshold
is planned after these12, regardless of the eventual interval width.


## Final table derivation (after the authorized returns)

```sh
# Optional statistical analysis dependency; audit/summarize use stdlib only.
python3 -m pip install scipy
python3 data/openai-math-4eaee875/final_table.py
# After the fixed12 ledger has returned:
python3 data/openai-math-4eaee875/export_precision.py --results /path/to/panel-results.jsonl
python3 data/openai-math-4eaee875/final_table.py --precision-costs data/openai-math-4eaee875/precision-costs.csv
```

final_table.py refuses to emit a full-frame table while original42 costs are
incomplete. It preserves original42 HT separately from the conditional-panel
working model, with build / serial stream / parallel stream CPU by each regime
and total. Nominal source-sampling intervals hold selected transfer factors
fixed; transfer-scenarios.csv is a separate selected-factor sensitivity table.
Partial panels retain the original cell, with failed/censored attempts visible
in precision-costs.csv. Non-completed attempt CPU is not a successful sample cost.
These scripts do not start Lean or request more samples. The current provisional
snapshot has no final-estimates.csv yet; the actual41 input was correctly refused.
A numeric check on the actual20 complete cells exactly reproduced the published
278.091768 estimate and 94.148040–462.035496 nominal interval; this is not a
pretend observation for the missing original or additional12.
