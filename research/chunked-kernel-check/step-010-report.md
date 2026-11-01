# Step010 — offline granularity analysis while the sole Envelope waiter is preserved

## EXPERIMENT_GATE
No additional native process or timing capture was started. On E8–15 analyzed
72completed Barrier wave observations from the existing15-cell matrix.
Dominant-frontier maximum worker-loop elapsed medians1/2/4/8:
43.543/22.284/12.141/6.328s. The loops include queue/map/audit overhead, not
pure C++ checking. At8workers slowest/fastest loop medians6.328/6.219s suggest
little elapsed imbalance. Complete heavy-stage wall is7.361s. The approximately
1.032s residual after subtracting maximum worker duration is only an upper
bound on time outside worker intervals, not an exact import attribution.
Whole pipeline still gives3.33x, not the loop's6.88x. See
parallel-worker-analysis.csv and parallel-granularity-analysis.md.

The pinned upstream LeanChecker.lean already dispatches independent modules
as tasks. A fixed serial-checker-work model on the unweighted retained31-module
panel has588.773s total and265.919s largest module Grid. An8processor
whole-module work bound is73.597s but the unbroken-module straggler bound is
265.919s. Even zero-cost Barrier leaves that bound unchanged. This is a model
ignoring memory, startup/import and contention, not observed wall or a
representative whole-library result. module-granularity-bound.json states
all assumptions; no14.127s wall is mixed into CPU weights.

Read-only source inspection identifies doKernel's explicit Elab.async=false
auxiliary-lemma addition in Lean/Elab/Tactic/Decide.lean116 and the generic
checked-environment task dependency in Lean/AddDecl.lean172. These identify
synchronous boundaries, not their measured compiler share. No async flag was
patched; source tactic backtracking semantics require separate care. The
source note scopes the positive compiled-replay result appropriately.

## WRITE_GATE
Added reproducible offline analysis and a primary-local-source interpretation
under M scope. No root paper edit and no new performance or novelty claim.

## REVIEW_GATE — 自审
Kept wall/CPU/worker maxima distinct, avoided interpreting an upper-bound
residual as an exact phase cost, retained existing module parallelism as a
necessary global baseline. No arbitrary source-compiler speedup is inferred
from independently timed replay. The actual Envelope waiter was already
verified by /proc/locks at the prior completed step and is not restarted here.

## Next
On actual Envelope completion collect its native result and all failures.
Until then preserve the single waiter and avoid another formal task.
