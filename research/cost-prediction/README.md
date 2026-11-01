# Cost predictability: declared protocol and novelty judgment

2026-11-01UTC, O line; self-review. Results belong only to this directory.
The current finite Falconer source window is allowed to retire; its owning
controller is SIGSTOP-paused so no further window starts until this task ends.
The full source/failed/native records remain. Cleanup is already recorded in
../decoupled-check/cleanup-20261101.md: O freed12.32GiB; live free space is now
about38GB, so the reported7.9GiB is stale. No additional useful typed inputs or
unpublished current artifacts are deleted.

## Judgment before fitting

A static-feature log-runtime regression and predicted-size scheduling are not
new methods. Empirical hardness/runtime models are established in SAT/SMT.
More directly, an independent openai/math study already fits checking time
from closure source size, decide+kernel count and certificate-module count,
and discusses computational outliers. The candidate novelty is at most a
controlled, leakage-conscious empirical explanation of when the two Lean
source-defined regimes improve prediction/calibration and when they do not.
A deterministic per-instance error bound is not supplied by regression or a
sample confidence interval. We do not assume the desired result.

## Input and target definitions

Freeze available observations before fitting. Primary: unchanged original
42-target probability frame, completed no-M, P0–7,j8, unprofiled exact-source
three-output compiler costs. Keep unavailable/operational/censored targets
explicit; never substitute zeros or old-M results.
Auxiliary: every eligible measured module available from current W no-M
captures and the source-produced O closure, deduplicated by module/protocol.
SDK/Mathlib auxiliary modules are not representative AI candidates.

Targets remain separate: native compiler CPU(user+system), native compiler
wall, and O's existing per-module kernel-replay wall component. Compiler
costs include imports, elaboration/search/checking/output; they are not pure
kernel verification. Kernel-component observations do not include imports,
have many tiny/empty modules and only a few AI roots. We will not bridge these
variables with a guessed fraction.

Features never run Lean. Use source bytes, dependency-file count, direct and
transitive source import counts/depth/closure bytes, lexical declarations,
decide+kernel density/markers, numeral size/range-call risk and lexical
statement-shape fractions. Actual goal states, elaborated declarations,
proof-term nodes, measured RSS/time and post-execution artifact sizes are
forbidden as predictors. Source-shape and large-evaluation flags are proxies,
not semantic claims; imported definitions/macros can hide computation.
Unresolved source imports/cycles/missing source are reported.

## Fixed model/validation choices

No feature tuning from held-out costs. Models: training log-mean baseline;
log-bytes ridge; source/import ridge; source/import plus source-defined regime,
declaration/numeral/shape features and regime interactions. Ridge penalty1,
intercept unpenalized, fixed log1p feature transforms, no full-data scaling.
Leave-one-module-out uses exact ridge PRESS with this fixed design. Report
five-fold, project-group five-fold and project holdout sensitivity.
The two domains are explicit-marker density>0 versus absent, fixed before cost;
these are not measured kernel-dominance labels.

Report median/P90 absolute relative error, multiplicative error and log error,
both pooled and per domain. Bootstrap confidence intervals resample project
blocks; they are descriptive for the observed subset, not whole-corpus
coverage under incomplete stratified sampling.

One-sided upper intervals use a separate calibration part within outer
training folds, never outer-test residuals. A finite-sample quantile with
rank beyond calibration size yields infinity. Exchangeability, grouping,
small samples and censoring prevent a per-request bound or general corpus
coverage guarantee. Interval and point policies use the same calibrated
point model in the scheduling comparison.

## Scheduling evaluation

First replay actual observed CPU service work at fixed budgets, comparing FIFO,
predicted cost ordering and predicted-upper admission, plus an oracle reference.
Use fixed budget fractions and reproducible arrival permutations. Upper
admission defers jobs; it does not call them false. Report budget exhaustion,
completed jobs, deferred jobs, interval misses and work consumed.

The42 library modules are distinct results, not alternative proof candidates.
On a success-only completed subset, pass@1 degenerates to completion fraction;
pass@k for k>1 is not identified. Do not group different lemmas by directory
and pretend they are alternative proofs. Existing miniF2Fsource-cost ranking
already had a negative heldout result and is not silently redone or mixed with
this hardware/Lean/compiler target.

If the model and input coverage justify it, a small matched native policy
prototype will use a fixed CPU-work budget, P-core lock, no-M and outer12GiB
protection. It will record deferrals/interruptions and exact accepted IDs.
This is separate from an offline simulation, not a production-engine claim.
No performance or bounded-error result is prefilled.

## Completed evidence

See [analysis.md](analysis.md) for the negative bounded-error/novelty finding,
all validation splits, native policy results and limitations. Raw snapshots are
on the existing PVC; v1 extraction and corrected v2 are both retained.

## Binary classification follow-up

[classification-analysis.md](classification-analysis.md) tests the fixed source
label against independent original-kernel CPU traces and completes9native
budgeted policy batches. Classification accuracy does not imply a cost bound
or successful CPU-budgeted route selection. This follow-up fits no regression.

## Mixed-request mechanism feasibility

[mechanism-analysis.md](mechanism-analysis.md) compares full construction,
streaming, class-selected checking and class-selected admission across mixed
requests, per-request/total budgets and injected10/20%classification errors.
This is actual-cost-driven replay, not new native throughput. Streaming wins or
ties class-selected modes under the measured CPU costs.
