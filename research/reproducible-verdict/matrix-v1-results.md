# First native thread/observer matrix

2026-11-01 UTC; self-review. Frozen e28ccc1 Probe; v1 raw capture retained.
This is a small diagnosis selected from a historical stratum, not an estimate of
population-wide inconsistency. It also exposed a measurement-adapter defect.

16 retained miniF2F sources: seven historical profiler flag changes plus three
from each retained class (no errors / ordinary error / diagnostic budget).
Lean4.34.1 with current matching Mathlib, budget3000, modes stock async and
synchronous frontend; observer off/native profiler/trace.profiler threshold0;
threads1/2/4/8, two repeats with observer order reversed. 768 completed rows.
Version4.9 historical outcomes are not mixed with these new outcomes.

| Comparison | Paired observations | Different verdict | Different acceptance | Different synchronous command counts |
|---|---:|---:|---:|---:|
| threads1 vs2/4/8, observer off |192|0|0|0|
| threads1 vs2/4/8, native profiler |192|0|0|0|
| threads1 vs2/4/8, trace profiler |192|0|0|0|
| off vs native profiler |256|0|0|4|
| off vs trace profiler |256|16|0|128|
| stock vs synchronous frontend |384|48|0|not comparable|
| repeat and reversed observer order |384|0|0|64|

A pair here is a source/configuration observation, not an independent source.
Raw labels: accepted480, lean_error224, budget_exhausted16, incomplete48.
No extras/new axioms or sorry-dependent theorem was counted as accepted.

The trace differences are ordinary-error vs budget-exhausted operational
classifications, not a new measured pass-set difference at budget3000.
All128 synchronous off/trace pairs change counted work. Four off/native
differences are ten raw heartbeats in the first opening command, not in the
theorem body. Reversed history changes64 trace command-count observations.
No observer-independent exact work count has been established.

## Measurement defect found, not hidden

48 stock/sync verdict differences are from two old-source syntax errors
(minif2f-6049 and6063). The legacy synchronous Frontend.processCommand calls
elabCommandTopLevel, which resets parser messages. v1 retained incomplete
(sorry-dependent) outcomes instead of stock lean_error. Acceptance is still
false in both, but diagnostic classification parity fails.

v2 therefore captures parser diagnostics before that reset and extends native
qualification with parse error and extra-axiom controls. It is a different
measurement source; v1 remains unmodified and is not pooled with v2. A small
new budget1000 arm is prepared to test near the observed heartbeat transitions.
Do not call the v1 synchronous frontend a transparent stock adapter.

## Task-local accounting control

Eight eager IO tasks each allocate a5000-element list. All checksums match.
The parent delta is130raw heartbeats, while child deltas sum to40110.
One child pays5026 and seven pay5012; at j4 the extra14 shifts from child0 to
child1 in both repeats. This is a measured per-task work attribution variation
despite invariant aggregate and output in this control, not evidence of a
shared global counter. It does not justify subtracting14 from arbitrary tactics.

All16 native cells completed, process/cgroup retired, no timeout/OOM/watchdog.
Matrix native process walls13.495–14.006s; task controls0.671–0.762s.
Maximum wait4 RSS8,848,472KiB, under M16GiB. Entire serial finite task
uses shared P0-7 lock; no Lean -M. No cross-machine or cold-cache result yet.

See results/matrix-rows.csv and matrix-summary.json; full stdout/errors and
memory/process evidence remain outside Git in reproducible-verdict-v1.
