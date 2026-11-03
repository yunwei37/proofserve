# Draft observations for Lean upstream

This note has not been sent. It describes engineering observations on Lean
4.34.1, not new kernel properties. The referenced timings are research prototype
results and are not release-form ProofServe speed claims.

## Official fresh replay

LeanChecker.replayFromFresh imports the target and calls
Kernel.Environment.replay once. Replay.replayConstants processes constants
serially. A minimal command comparison is:
~~~sh
LEAN_NUM_THREADS=1 leanchecker --fresh ROOT
LEAN_NUM_THREADS=8 leanchecker --fresh ROOT
~~~

One Barrier observation took 534.698 and 580.090 seconds, respectively, with
about one CPU core active. These single observations do not establish an
intrinsic negative scaling effect. Default leanchecker checks selected leaves
against trusted imports; its 65.423 seconds cannot be divided into the time of
a 4,449-module stream with module-wise context checks.

## Marking reconstructed shared frontiers

Sharing a reconstructed frontier without quiescent Runtime.markPersistent
caused atomic reference-count traffic in our prototype. A same-binary causal
control reduced 8-worker CPU by 14.13% and wall time by 5.13%. This was a prototype
defect, not evidence that Lean checking intrinsically scales negatively.

Core.batch demonstrates the minimal ordering: join the previous wave, mark the
frontier with the official primitive, then enqueue the next wave. No worker may
access the frontier while it is marked. Checkpoint and FFI trust remain explicit.

## Splitting a conservative whole-module fallback

Our old planner replayed a whole module serially if it contained an inductive
declaration. The replacement serially replays the nonordinary dependency closure
and schedules remaining ordinary declarations by dependency waves.

On the same 8-worker Barrier closure, three-repeat median wall time changed from
257.659 to 196.669 seconds. CPU changed from 542.369 to 542.942 seconds, with the
same 4,449 accepted modules. This 1.310x prototype ablation does not establish a
release result or a result for Grid or Mathlib. Core.makePlan, complexPrefix, and
parallelReplay show the implementation without changing the kernel.

The upstream source is LeanChecker.lean, Lean/Replay.lean, and
Lean/Environment.lean in the v4.34.1 SDK. The artifact reader, checkpoint metadata,
and checked-frontier FFI adapter are additional trust; no kernel edit is proposed.
