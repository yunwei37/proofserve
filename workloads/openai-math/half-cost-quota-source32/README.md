# Per-stratum half-cost quotas: source32 snapshot

This is a conditional plug-in, not a whole-library census. The frozen original42
draws have32 completed costs and15 complete cells representing104,632 of163,097
source modules. Ten draws in six cells remain missing; no cost is imputed here.

For a complete stratum with population N and two CPU costs a <= b, the empirical
distribution assigns N/2 modules to each cost. Its fractional number needed for
half that stratum's CPU is N(a+b)/(4b). Round each cell upward, then sum: **33,971**
model-equivalent modules (fractional sum33,964.11), or32.47% of the covered domain.
This is a quota in every stratum; it differs from selecting the globally hottest
modules until half the total CPU is reached (the previous conditional16,376).
These are model-equivalent counts, not known actual module identities.

## What interval is supportable?

Enumerating all16,384 collapsed ordinary bootstrap outcomes resamples two draws
within each of14 noncensus cells; the true N=2 census is fixed. R7 reference
percentiles are **34,483.15–51,806.85** integer modules. They exclude33,971:
each n=2 resample either retains the distinct pair, or becomes an equal-cost pair
whose estimated half quota is N/2. Thus bootstrap shifts this nonlinear estimate
upward. This reference range is **not a valid population95% confidence interval**,
nor evidence of precision. Exact enumeration removes Monte Carlo noise, not n=2
identifiability or nonresponse bias. No population CI is claimed.

For finite nonnegative costs, universal nonsharp sums of integer per-cell half
quotas range15–52,319 for the covered15 cells, and21–81,553 for all21 cells.
These are algebraic ranges, not realistic predictions or statistical confidence.
Unobserved within-cell tails can change the conclusion; observed sample pairs
alone do not identify them. Full-library actual half-quota count remains unknown.

## Censoring audit

[completed-source-audit.csv](completed-source-audit.csv) dereferences all32
original raw rows: each is compile_ok, source-exact, no-M, P-core locked, native
and cgroup retired. Total observedCPU817.179526s. None is a timeout substitution.
Missing10 original costs are excluded, not assigned zero or an upper bound.
Successful-return selection still biases these conditional distributions.

The TableDensity dependency's earlier32.6025s group-remainder interruption was
later recovered at114.0233s. IntegralPairings remains right-censored on its two
approximately600s attempts (second observedCPU634.316372s). Neither dependency is
one of these32 original draw costs. A wall timeout is not an upper bound on
completion CPU, and operational interruption is not a mathematical rejection.
Hodge's440 successful dependency prefix ended on its finite group allowance;
the unstarted original endpoint is not a censored measured source cost.

## Reconcile O clocks before transferring ratios

Latest complete segmented closures give CPU check/build:
Falconer2038.443942/32292.603807 = **6.3124%**;
Mathlib91.145172/1018.219383 = **8.9514%**.
O's9.2563%/14.6662% figures use elapsed time and are not contradictory CPU ratios.
Falconer includes2461 internal AI and10744 external modules; not all163097.
W rechecked each Falconer source raw cost and the committed complete checker
reduction; acceptance/graph parity is O's evidence, not a fresh W replay.

[per-stratum-check-transfer.csv](per-stratum-check-transfer.csv) is explicitly a
sensitivity model: ordinary cells transfer one of the two latest complete
segmented anchors; marker-positive cells retain the older unsegmented Grid CPU
factor8.4671%, since no matched new computational checkpoint factor was supplied.
The covered15 modeled sums12.2394–15.3193CPUh versus174.2512constructionCPUh are
**mixed-protocol transfers, not measurements of these32 checks or full-library
verification**. They do not replace the earlier frozen models.

O's whole-library finite window ended incomplete:2488 sourceIDs accepted,
160609 missing,0.694505CPUh observed prefix. Its9124 source errors/censors and
151485 blocked sources are operational statuses, not false-proof counts. Do not
divide this partial cost by any whole-library projection.

Reproduce: python3 workloads/openai-math/half_cost_quota.py. It runs analysis on
E8–15, reads frozen32 draw raw records and O's complete reduction, and never runs
Lean. Self-review (自审): CPU/elapsed denominators, ceil-per-cell vs global count,
census handling, bootstrap degeneracy, censor omission and missing domains checked.
