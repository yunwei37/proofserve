# OpenAI math: native build-cost sample (v1)

A small, citable data package for **openai/math at
4eaee87548250b2682affda7d05d947c05554bae**: 163,097 source modules, 21 strata,
42 original probability draws (two per stratum, seed 20261030).

**Current snapshot: 41 completed costs / 42 original draws.** The last draw
is still being prepared. Blank costs are missing, never zero or imputed.
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

The strata combine fixed source-size percentile boundaries, source import
depth bins, and any explicit comment/string-masked decide +kernel occurrence.
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
