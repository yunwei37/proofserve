# Draft only,not sent
Lean4.34.1; prototype engineering observations,not kernel properties.
1. LeanChecker.replayFromFresh calls Kernel.Environment.replay once.
Replay.replayConstants loops serially. Reproduce:
LEAN_NUM_THREADS=1(or8) leanchecker --fresh ROOT.
One Barrier control534.698/580.090s wall,near1CPU. Default CLI checks selected
leaves and trusts imports; its65.423s cannot compare to4449 per-module records.
2. Reconstructed shared frontiers without quiescent Runtime.markPersistent
caused atomic RC traffic. Same-binary causal controls reduced8P CPU14.13% and
wall5.13%. This was our prototype defect,not intrinsic negative scaling.
Invoke official primitive before enqueue and after joining all previous tasks.
3. Whole-module fallback on any inductive was avoidable. Serial-replay the
nonordinary dependency closure,then parallelize remaining ordinary declarations.
Same8-worker Barrier median257.659→196.669s,CPU542.369→542.942s,4449 same accepts.
1.310x is a prototype ablation,not release or Grid/Mathlib evidence.
Core.makePlan/complexPrefix/parallelReplay are minimal implementation.
Checked-frontier FFI and checkpoint metadata remain additional trust. No kernel
edit proposed; final imported-map duplicate policy differs from per-input replay.
