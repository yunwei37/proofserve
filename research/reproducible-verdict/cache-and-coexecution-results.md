# Private runtime cache and mathematical coexecution
2026-11-01 UTC. Original Lean4.34.1, no -M, shared P0-7 lock, M16GiB.
All raw data remain under PVC reproducible-verdict-v8 and v5; failures preserved.

## Completed runtime cache experiment
512 observations / 256 paired candidate-mode-budget-repeat-thread comparisons:
0 verdict, diagnostic or axiom differences. All128 synchronous command heartbeat
vectors identical. Parent-only counters differ in42pairs; these do not measure
total asynchronous work.16retained real miniF2F sources; budgets1000/3000,
stock/sync, j1/j8, reversed order across two repeats.

The second mincore pass checked2,238,400private runtime pages:0resident in
each cold treatment, all resident in each warm treatment. Copied SDK/Mathlib
runtime files include .ir.sig. This evicts only owned private copies, not
system libc, loader or the whole machine. Native processes all retired,
return0, no memory stop; their cgroups retired. Qualification has six expected
accepted/rejected/incomplete rows. Cold process wall66.18–72.51s, warm8.83–15.04s:
page state changes elapsed cost substantially while tested verdicts remain stable.
These are diagnostic process times, not service-throughput or universal bounds.

## Completed mathematical batch subset, later kernel stage partial
256 real-source observations:16sources x2budgets x4workers x2repeats.
Independent candidate contexts actually coexecute on gated worker tasks.
Comparing j1againstj2/4/8 gives192pairs:0verdict differences but84command
allocation-heartbeat vectors differ. This is a different result from merely
changing available threads while submitting sources serially.
It does not show changed tactic branches, false goals, or changed pass sets.
Imported shared state, realization, task attribution and scheduling remain
possible causes; tiny parse/error controls are not tactic-dominated examples.

The old region task stopped on missing EnvelopePsiB.olean in its LEAN_PATH:
an infrastructure/input-path failure, not a kernel rejection. Eight mathematical
cells and four Grid cells completed first; no Envelope observation was returned.
The whole v5 point stays partial. Complete paired batches may be analyzed as
that subset, never represented as the planned whole computation-regime matrix.
New user-requested module samples still need matched original artifacts,
per-executing-thread counters and native kernel CPU.

## Claim boundary
The data support finite observational cache robustness, and allocation-accounting
variation during real coexecution. They do not yet prove the proposed division:
computational regimes naturally deterministic, mathematical regimes requiring
deterministic budgets. Native C++ kernel poll counters differ from allocation
heartbeats and are still unobserved.

## Subsequent completed computation census
The v5 partial stage is not repaired or relabeled. A new foreground v12 point
completed all2,524eligible computation helpers, at1/2/4/8workers x3repeats.
All30,288original-kernel observations accepted; every target's allocation
count was constant. See [census-results-v12/results.md](census-results-v12/results.md).
This strengthens the prepared-computation evidence; variable source elaboration
and stable prepared kernel rechecking are different phases. It does not prove
a subject-matter-only split or a universal deterministic-budget guarantee.
