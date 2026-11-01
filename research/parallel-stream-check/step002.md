# Step 002 — real closure exposes duplicate-proof dependencies (自审)

## EXPERIMENT
The first frozen v3 matrix has one completed O reference cell (66.024s, 1330
accepted modules) and one genuine audited rejection after 135 accepted modules.
The incoming compatible duplicate List.drop.eq_def refers to a newly generated
splitter in Init.Data.List.TakeDrop; validating before the module's new constants
exist gives unknown-constant rejection. This is an implementation defect, not bad
input, and no speedup/acceptance parity is claimed for v3.

Move incoming duplicate-proof checking after checking the module's new constants.
It still happens before module acceptance and does not overwrite the existing
binding. Add the DupDeps fixture: a duplicate theorem uses a new local helper.
The frozen v4 native control result is 18/18 qualified at workers 1 and 8.

The exact 1330-module closure now completes for original O reference, audited
serial, and parallel1, with identical full accepted module sets and 132484 input
entries, 2269 upstream unsafe/partial exclusions. This qualifies the dependency
repair. Remaining performance repeats/worker counts are still running in the
same finite blocking-flock window; no median or gain is claimed here.

## WRITE
Preserve both v3 failed and v4 fixed raw captures on PVC. Own working-tree chunk
integration remains uncompiled preparation and is not part of this commit.

## REVIEW — 自审
The new regression recreates the dependency ordering omission. Full real closure
supplies the larger positive control; a timeout/crash is not counted as kernel
rejection. Small controls alone were insufficient. O source remains unchanged.
