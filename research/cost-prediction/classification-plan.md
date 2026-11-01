# Binary regime classification and budgeted method selection

2026-11-01UTC, O line. Self-review; no regression is fitted or retuned.
Supporting characterization for the current two-regime RQ: can cheap source
labels identify independently measured computation-bearing checking, and does
that justify choosing a checker/admission route under CPU constraints?

## Classifier and independent evaluation
Use the existing fixed explicit-marker-density>0 rule, no training. Its agreement
with W is scanner/rule consistency, not accuracy against independent truth.
Evaluate against M's completed no-M per-declaration original-kernel trace:
computation-dominant when decision-helper CPU / all kernel-call CPU >=0.5.
That outcome is dynamic within its own checker invocation, not source compiler
phase share or a whole-library label. Original29 matched probability draws
are primary;2purposeful hot modules are separate. Missing13 original dynamic
labels remain unknown. Report confusion and CPU-weighted mistakes, and sensitivity
at independent share thresholds0.25/0.75, with project-block resampling.
Do not redefine truth from the static source marker. A code-shape correctness
check does not make this a classifier of propositions' validity.

## Method evaluation: preserve task/CPU boundaries
Current measured complete-closure pairs cover only three complete inputs:
Mathlib.Data.Nat.Basic1330, Barrier4449, Grid3793. They are purposefully selected
diagnostics, not31 randomly selected module requests. The ordinary route uses
O's original serial stock-kernel stream. The computation route uses M's qualified
v14 uniform4 original-kernel declaration-wave rechecking, no chunk rewrite or
new trusted solver. Reuse actual full-process wall/CPU measurements; do not
assign the Grid speedup to unmeasured modules.

A counterfactual CPU-budget matrix runs all six arrival permutations at fixed
budgets120/600/900/1200CPU seconds. Mathlib's3 existing v14 repetitions remain
distinct; the single Grid/Barrier pair is not bootstrapped into native repeats.
FIFO uses serial stream for every root. Type-route preserves FIFO order but
selects serial/math versus parallel4/computation. Upper-admission adds a type
envelope (maximum existing whole-process CPU in that type/selected route) and
defers roots exceeding remaining CPU. This is historical-workload calibration,
not out-of-project or per-instance statistical coverage. It does not reuse
the prior compiler regression or confuse compiler costs with checker costs.
Expose the cost of extra parallel CPU and report CPU consumed by interrupted
root jobs as discarded-root work, not mathematical rejection or necessarily
reclaimable dependency work.

Run a separate bounded native matrix: three cyclic arrivals of the same three
roots, crossed with all three policies,120CPU seconds per policy. Rotate policy
execution order across repetitions. One whole finite matrix takes the existing
P-core lock after current holders/waiters, <=1740s active wall. P0–7, no-M,
11.5GiB child cgroup plus512MiB controller reserve, each child has a wall bound
and remaining-CPU RLIMIT. All payload/command/stdout/CPU/memory/partial accepts
are written to PVC. Each policy's driver and child CPU are charged, completed
whole roots and exact IDs reported. No generation/source compilation is timed.
The120s point intentionally permits the ordinary closure but cannot complete
either computational closure even in the historical parallel route; it tests
availability by deferring unsuitable jobs, not a broad throughput claim.
Queue wait is outside active budget. Partial dependent accepts are not completed
root requests. Three repeats permit observed ranges, not a precise population
CI; paired bootstrap is descriptive only. Different proof modules cannot give
pass@32; only completion fraction of these three known reference roots.

## Interpretation and prior art
A positive classification and negative method-selection result are compatible:
a computation label does not prove parallelism reduces CPU or the declaration
graph is wide. Reject any inference of a bounded runtime, failure verdict, or
general service throughput. SATzilla2012 already performs cost-sensitive
classification without predicting runtime; the label-versus-regression
distinction is not a novelty defense. Our possible increment is Lean-specific
independent regime validation and measured wall/CPU/admission tradeoffs.

Falconer stays unchanged and active; it releases the lock at its finite window
boundary. No new controller for Falconer, no source edits in other lanes.
Raw: /workspaces/.agent-state/gpu-smt-captures/cost-classification-20261101.
