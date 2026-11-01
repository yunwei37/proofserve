# Grid in one checked stream: first complete run

This is one repetition, not a three-repeat median. Frozen v12 raw:
`/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v12`.
All five trials start from the same independently checked 3,792-module prefix;
the leaf is OAI.Analysis.PlanarPacking.Grid. The complete accepted module set
equals O's 3,793-module compute-grid cohort (traversal order differs).
All leaf constants match the serial check. No fallback, budget stop or rejection.

| Method | Requested workers | Leaf wall s | Leaf process CPU s | CPU / wall |
|---|---:|---:|---:|---:|
| Serial original kernel | 1 | 265.785 | 265.660 | 1.000 |
| Declaration waves | 1 | 282.181 | 282.039 | 0.999 |
| Declaration waves | 2 | 156.246 | 312.081 | 1.997 |
| Declaration waves | 4 | 93.662 | 373.548 | 3.988 |
| Declaration waves | 8 | 95.431 | 380.706 | 3.989 |

Four workers reduce incremental leaf wall time 2.838x, with 40.61% more CPU.
The requested-eight trial uses only about four cores on average; it is not an
eight-core scaling result. The requested-one trial is 6.17% slower than serial.
Each wave contains the same 7,898 jobs over eight dependency frontiers.

The whole process checks the prefix once and runs all five variants: 1,097.592 s
wall, 1,988.629 s CPU, 2,774.938 MiB wait4 peak RSS. It is not the wall time of
one selected production configuration. Sampled tree peak is 2,771.273 MiB.
Native processes and own cgroup retired; no memory events were recorded.
No per-variant peak memory is available.

## Why eight needs qualification

The actual SDK reads LEAN_NUM_THREADS=8; container and ancestor CPU quotas are
unlimited and there is no throttling. Lean v4.34.1 runtime object.cpp grows the
standard pool on enqueue only when no existing worker is idle. This prototype
enqueues a few long-lived worker loops and hides its remaining jobs in a private
queue. After a four-worker prefix, enqueueing eight loops can leave only four
standard workers processing the entire private queue. This is a source-supported
hypothesis, not yet a proven diagnosis. A short start-synchronization control is
the next qualification step. No host runtime setting has been changed.

The prior cold Envelope resource failure remains in compute-runs.csv, with
unknown native CPU after the parent was killed. It is not a rejected proof.
Historical v4 Mathlib timings predate the indirect-cycle fix and cannot serve
as final correctness-qualified performance evidence.
