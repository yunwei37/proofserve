# Step052: all persistence correctness controls returned; freeze full matrix
EXPERIMENT_GATE:13 native controls actually returned/retired:1 importer-state
probe,4 positive replays (flag0/1×P1/P8),4 corrupt-bvar proof replays and4
stale/duplicate coordination faults. Positive accepted sets and every module
check/allocation-unit pair equal original fd1e9be. All marked frontiers
remain persistent through enqueue; unmarked frontiers become active MT.
Corrupt proofs fail original-kernel c0 checking; coordination faults retain
their distinct invariant failures. No resource stop or missing native exit.

WRITE_GATE: small qualification/state CSVs; same-binary32-cell schedule
prepared at5f2e64f:3paired plain repetitions and one stat per flag×1/2/4/8,
counterbalanced arm order, diagnostics off. First full cell is marked P8 to
observe complete-closure memory behavior early; it is part of the frozen
matrix, not a selectively repeated result. Each separately gets blocking
P-core lock/no-M/same14GiB controls; source/events/oracle frozen before run.

REVIEW_GATE 自审: real controls, inherited exact old-work reference, actual
object headers and retirements checked. Small controls do not establish full
memory/cost or a general correctness theorem. Whole mathematical kernel
unchanged; coordinator/FFI and unsafe quiescence obligation remain explicit.
Full matrix still needs actual native execution, not a queued-success claim.
