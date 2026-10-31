# W handoff: minimal paired panel for the cost of native `-M`

Design only, M self-review, 2026-10-31. **No new capture is launched by M.**
This measures a benchmark-policy effect; it is not a Lean optimization or a
whole-library result inferred from the three purposively chosen modules.

## Fixed panel and cost

Use the **26 original probability-sample modules** already returned in
`workloads/openai-math/standard-artifact-native-a/modules.csv`, linked to their
unchanged original 42-draw frame and inclusion probabilities. The exact panel is
in [w-paired-targets.csv](w-paired-targets.csv). Do not select only high-system-time
modules. Grid is a separate purposive sentinel and carries **no population weight**.

Each target needs **one new unprofiled no-M run**. Reuse a baseline only if it has
the same pinned source, SDK, dependencies, source path, standard artifact outputs,
j8, authored heartbeats, P-core lock, outer memory protection and matched runtime
conditions. Otherwise run one adjacent fresh baseline as well. The old 26-module
capture is useful for planning, but its non-locked observations are not a
contemporaneous matched baseline. UMoments9 and EnvelopePsiB already have complete
matched three-repeat measurements in this matrix; retain these, do not rerun
them merely to fill the panel. Thus at most **24 new two-arm pairs (48 native
runs)** are needed for this initial ready panel.

Old 26-target wall sum is 471.72 s; twice this is about 15.7 minutes of native
work as a conservative planning reference for all 26 two-arm pairs, excluding
preparation/queue wait and any interference. This is an estimate, not a deadline
or a promise of the new machine clock. Keep W's approved per-child limits and
resource allocation; acquire the common P-core lock for each native run.
One repeat per arm is a first population-oriented screen, not a variance estimate
of runtime noise. The existing three-repeat sentinel range shows why a close
ratio needs repetition before interpretation.

## Matched arms

- Fixed original source (no instrumentation), Lean4.34.1/5045d005,
  OpenAI/math4eaee875, Mathlibd13f, same cached dependency build and search path.
- Both arms j8 on CPU0–7, standard `.olean/.ilean/.c`, same authored/default
  heartbeats, same environment and same temporary **outer** memory protection.
- Baseline retains original `-M9216`; treatment removes **only** that option.
  Neither arm changes the outer physical memory limit. Native `-M` and outer
  cgroup memory accounting enforce different policies; this tests policy
  replacement, not identical interruption semantics for arbitrary failures.
- Balance baseline-first and no-M-first by the existing draw order, e.g. alternate
  pair order; keep pairs adjacent. Do not pool perf runs or dependency setup.
- Record native wall/user/system, wait4 peak RSS, own-tree sampled peak, faults,
  context switches, decision, diagnostic bytes and all output bytes.
  Keep controller time/queue time separately. Compare entire `.olean` bytes;
  also report `.ilean/.c` differences rather than silently accepting them.
- A changed outcome, budget exit or timeout stays in the table. No censored arm
  becomes a zero-cost successful run. Show paired complete costs and outcome
  changes separately. Do not infer a faster full build from failed comparisons.

## Estimands and honest reach

First report the **observed-panel** sums and paired deltas:
`delta_i = (user+system)_M - (user+system)_noM`, and analogously native wall.
Keep negative deltas. Give both excess-over-noM `sum(delta)/sum(noM)` and the
fraction of baseline removed `sum(delta)/sum(M)`; they are different denominators.
Also tabulate by historical system-share band as descriptive heterogeneity,
without changing original sampling weights.

For a complete original stratum h (both original draws observed in both arms),
estimate CPU-cost difference as
`Delta_h = N_h * mean(delta_i)`, with paired design variance
`N_h^2*(1-n_h/N_h)*s_delta,h^2/n_h`.
Estimate both arm totals using the same original inclusion weights, then form
the ratio; use paired resampling/design covariance, not independent intervals
for two unrelated means. n=2 per stratum makes heavy-tail intervals fragile.
Single repeats do not quantify within-module runtime noise.

The initial 26 returned targets cover **11 complete strata / 93,998 modules**
of the original **21-stratum / 163,097-module** frame; 16 original draws were
not returned in that capture. Later W completions can extend the SAME frame,
with their paired arms and completeness recorded. Report totals only for
complete strata, and keep the rest unknown. The initial panel alone does **not**
identify the full-library inflation factor. Nonresponse is not random and
must not be reweighted away. Complete all original strata or publish a
conditional estimate with an explicit unmeasured remainder.

CPU cost estimates sum module work, not a parallel full-build makespan. A
whole-build claim additionally needs the build DAG, concurrency and resource
model or a full native build. Dependencies, failed builds, output mode and
runtime options must retain their existing scopes. Do not pool historical
`.olean`-only or pre-lock points with the standard-artifact pair.
