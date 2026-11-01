# Library-cost estimation: bounded prior-art check (2026-11-01 UTC)

This W-line report addresses whether cost measurement or weighting itself is
new. It does not revise the root paper, its RQs or another lane's results.
Search and source checks completed in this session, well within half a day.
Queries and inclusion decisions are in queries.csv; verified primary sources
and measurement distinctions are in sources.csv.

## Judgment

**Stratification and Horvitz–Thompson totals are standard survey methods, not
a contribution.** The original method estimates finite-population totals using
known inclusion probabilities. Our two draws per source-size/import-depth/
explicit-computation stratum are an application. The nominal variance/t
intervals do not fix nonresponse, censoring or proxy misclassification.
[Horvitz and Thompson, 1952](https://www.stat.cmu.edu/~brian/905-2008/papers/Horvitz-Thompson-1952-jasa.pdf).

**Measuring library performance, CPU work or per-file cost is also established.**
Mathlib's current build benchmark measures the complete build and module data,
including wall/task clocks, instructions, RSS and profiles. Its 2025 maintenance
paper describes performance tracking and component-level optimization.
We must not claim that earlier work only reports wall time.
[Mathlib benchmark](https://raw.githubusercontent.com/leanprover-community/mathlib4/master/scripts/bench/build/README.md),
[Growing Mathlib, section 5](https://arxiv.org/html/2508.21593v1#S5).

Isabelle build monitoring archives session-level performance records; an
actual AFP CI report contains elapsed, CPU and GC times. The community
benchmark studies hardware/thread/memory effects on HOL-Analysis and reports
both CPU and wall time. This is a direct precedent for native cost and
parallelism studies, rather than a probability sample of all AFP modules.
[Build-status author report](https://mailmanbroy.in.tum.de/pipermail/isabelle-dev/2017-May/007393.html),
[AFP CI log](https://mailman46.in.tum.de/pipermail/isabelle-dev/2019-November/017047.html),
[Huch and Bode, 2022](https://arxiv.org/pdf/2209.13894).

Rocq already provides per-file user/system/real times, peak memory and
per-command timing. Its CI bench script compares package versions and records
user time/instruction counters; a public PR shows an actual result table.
Neither native CPU accounting nor a timing table is new here.
[Rocq manual](https://rocq-prover.org/doc/v9.1/refman/practical-tools/utilities.html#timing-targets-and-performance-testing),
[CI script](https://raw.githubusercontent.com/rocq-prover/rocq/master/dev/bench/bench.sh),
[actual CI result](https://github.com/rocq-prover/rocq/pull/22136).

Independent whole-Mathlib checking is not new either: Lean Kernel Arena
publishes checker comparisons over a complete export. Checker, export format,
Lean version and trust boundary differ from stock-kernel olean replay; those
differences need matching evidence, not an assertion that checking was unstudied.
[Kernel Arena](https://arena.lean-lang.org/round/2026-09/test/mathlib/).

The bounded search did not identify an inspected source estimating *AI-generated
library build versus independent native verification*, split by the two
source-defined domains, using this design. This is not proof of priority.
The possible contribution is an empirical distribution and explanation at that
workload/trust boundary, if the missing native costs support it. Metric names,
sampling weights and CIs alone supply no novelty.

## What RQ1 still needs

Current no-M source-compiler frame has31/42 original costs and14/21 complete
strata. Its163,097-module population is all discovered source modules at
4eaee875, not the smaller default Lake target. Incomplete strata contain59,629
modules. Missing, failed or budget-exceeded draws cannot become zero cost.
No old -M denominator or purposeful example fills them.

The current covered-stratum certificate/ordinary CPU estimates24.146735h/
116.704826h do not describe the entire library. Their conditional primary
share is17.1434%, nominal delta95%[0,43.6646%], conservative joint bounds[0,100%].
No complete global CPU total, two-domain verification total or global CI exists.

Our measured build variable is one native source compiler process per module:
imports, elaboration/tactics, kernel work, and standard olean/ilean/C emission.
It excludes setup, Lake orchestration, linking and unmeasured external-library
construction. It is not a complete executable/project clean-build bill.

Independent verification must consume the exact measured typed artifacts,
check the intended dependency/axiom boundary, account for skipped unsafe/partial
entries, and measure checker CPU directly. A producer C++ stack fraction is
neither an independent-check CPU measurement nor a multiplier for the full
library. O's complete closures demonstrate concrete check/build comparisons,
but their purposeful closure ratios cannot weight our random sample.

For a per-module verifier, use the same original draws and inclusion weights.
For a shared streaming verifier, startup/shared dependencies are not additive:
per-module replay CPU plus shared read/setup terms require explicit accounting,
and closure time cannot be assigned repeatedly to each source module. The
two estimands must be reported separately, with a matched covariance when
forming a build/check ratio. Domain proxy thresholds and misclassification
sensitivity remain explicit. Native wall cannot be divided by eight to create
CPU, nor CPU by eight to predict a parallel whole-library makespan.

metric-scope.csv records these distinctions and deliberately leaves unavailable
global values blank. Resource cleanup is complete (W064); the unchanged next36
hard-draw jobs are live, with one shared-lock request per task. Subsequent
missing original draws retain their memberships and probabilities.
