# Standard task-pool growth and private job queues

## Source and real control
Lean v4.34.1 src/runtime/object.cpp, task_manager::enqueue_core, creates a standard
worker only if its idle-worker count is zero and the configured maximum has not
been reached. The SDK really reads LEAN_NUM_THREADS=8; no CPU quota or throttle
explains the preceding four-core curve.

PoolControl.lean and pool_spin.c make this visible in one native process.
Each trial drains 64 jobs, each spending 50 ms thread CPU (CLOCK_THREAD_CPUTIME_ID).
After warming four gated workers, the first ordinary eight-task launch assigns
[13,13,12,13,13,0,0,0] jobs: five workers do work. The following gated launch gives
[8,8,8,8,8,8,8,8]. Later ordinary launches also use eight because the pool has grown.
Raw v13, three ordinary/gated pairs, is a scheduling qualification control,
not a proof workload, independent speedup result, or three independent cold runs.
Ordinary first-launch CPU/wall=4.922; gated=7.717. This confirms a pool-growth
race can hide our private backlog; the exact preceding Grid race was not traced.

## Repair
For a frontier with more than one worker, enqueue one loop at a time and wait
until it enters a shared IO.Promise gate. Release the gate only once all requested
loops have started. Failed creation also releases the gate and joins every
launched task before propagating error. Queue borrowing remains short; kernel
checking happens outside the mutex. Token checking/commit and the mathematical
checker are unchanged. This is not a host setting or a runtime reinitialization.

Blocked task compensation can temporarily create extra sleeping OS threads.
Active declaration checks remain bounded by the requested worker count and P0–7
affinity. There is no assertion that the process contains only eight OS threads.
Startup synchronization has per-frontier cost; final real-workload curves must
measure it rather than assume free synchronization.

## Qualified scope
Frozen v14 compiles natively and passes all 20 declaration/fault controls and five
clock/curve paths. All ten exact source-selected Envelope parents, 80 child
proofs and ten merges pass the original mathematical kernel. The only recursively
collected axiom is propext; no sorry. Both loose-bound-variable corruptions fail
with explicit original-kernel rejection. The certificate control trusts stock
imported dependencies: it is not an independent whole-closure throughput run.

The same version replaces linear List.contains in import-visibility membership
with NameSet.contains, preserving iteration order. A missing Array.toList caused
an initial compiler rejection, retained in raw v14; the corrected build and
negative context controls pass. This is not evidence that the previous cold
Envelope memory failure is fixed.
