# Step 007 — qualify actual worker startup before final curves

## EXPERIMENT
Used exact Lean runtime source plus one bounded P-lock native control to resolve
the requested-eight/achieved-four ambiguity. Pool growth hides private queues:
first ordinary8 has three idle task closures, gated8 distributes all 64 jobs.
This control is a dependency of the real workload measurement, not a new claim.
Implemented shared start gate, release-on-error and join-before-error. Preserved
all mathematical checking and checked-token commit obligations. Also preserved
import traversal while changing membership lookup from list to set.

## WRITE
worker-start.md documents the observed race, exact raw, correction, potential
per-wave cost and extra sleeping runtime threads. correctness.md documents
coordinator, C ABI and certificate-selector trust boundaries. Copied frozen v14
native results; no independent closure or speed claim inferred from controls.

## REVIEW — 自审
Native compile, 20 positive/negative/fault controls, five mock curve paths and
three actual-certificate scenarios passed. All ten source ConstantInfo values
matched selector references; 80 chunks and ten merges checked, only propext.
Bad source and bad certificate reached explicit original-kernel rejection.
Initial reader compiler failure retained. All native processes and own groups
retired; controls stayed below lane budget.
Next experiment: fresh 18-cell exact 1,330-module matrix on repaired source,
then real-module same-process curves. Historical v4 is not relabeled current.
