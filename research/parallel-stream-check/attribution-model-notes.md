# What the attribution model can establish

This is an interpretation note for the frozen v2 experiment, not a new result
or a claim about an inherent serial fraction. Full observations have one
fixed-order run per configuration; the resident hardware leaf has three repeats.

## Matched denominators

Let T be native process wall time, D the measured read/context windows, G the
plan windows, F upstream complex/cycle serial replay, and U duplicate checking.
Let K be the sum, across sequential frontiers, of the union of intervals with
at least one original kernel call active. Let B be joined-batch elapsed time.
Then the recorded decomposition is exactly

T = D + G + F + U + K + (B - K) + R,

where R = T - D - G - F - U - B. The signed delta of these seven terms between
two complete configurations must reproduce delta T. A negative contribution is
a saving; positive signed shares can exceed 100% when other terms improve.
This identity localizes a measured difference; it is not a causal model.
D/G/F/U are serialized by this implementation. F includes mathematical work;
it is not all graph dependency handling. No claim that these intervals are
inherently nonparallelizable follows.

K is elapsed occupancy, including descheduling inside a call, not summed CPU.
Original-check thread CPU is measured separately. Batch process CPU minus
original-check thread CPU narrows the cost of launching/gating/joining tasks,
the work-queue mutex, representation validation, checked commits, and observer
merge. R additionally includes stream startup, bookkeeping, reporting and
uncovered code. Native wall ends at wait4; Python post-wait cgroup cleanup is
outside T. The phase/controller elapsed time is a different denominator.

## Amdahl fit versus measured work/span

Fit S + P/n only to corrected same-implementation complete P1/P2/P4/P8 runs.
The fitted S is an effective parameter. Inspect residuals; do not reuse leaf
points or a different serial implementation. A fitted asymptote is not a proof
of the best possible checker speedup. Amdahl's original discussion explicitly
includes housekeeping and problem irregularity; the present fit is a modern
two-term approximation, not an exact property of Lean.
[Original paper](https://www.cs.cmu.edu/~18742/papers/Amdahl1967.pdf).

The sum of maximum observed job CPU in each frontier is an algorithmic
wave-span proxy. It imposes the prototype's wave barriers and module order,
and uses configuration-dependent measured CPU costs. It is not a traversal
of the inherent dependency DAG and cannot establish its critical path.
Work/span scheduling analysis motivates keeping these concepts separate;
the fully strict work-stealing bound is not directly a theorem for this
prototype's shared-queue/frontier scheduler.
[Blumofe and Leiserson](https://www.cs.utexas.edu/~venkatar/sys_perf_analysis/ws_theory.pdf).

## Why slower added cores alone cannot explain regression

For fixed S and P >= 0 and positive E/P effective work rate r,
S + P/(8 + 16r) <= S + P/8. Thus the older unpinned 24-worker slowdown cannot
follow solely from giving the original eight P cores extra positive E
capacity. A change in placement, per-job execution cost, coordination cost,
available P capacity or uncontrolled run conditions is needed.

Compare P-only, E-only and mixed with their actual per-check core IDs.
The mixed explicit map is P-first: waves with at most eight jobs use P cores.
This is a deliberate placement policy. Same-binary profile-off pinned and
unpinned comparisons distinguish it from the OS scheduler and from observation.
A one-node NUMA topology excludes cross-NUMA as an explanation here, but does
not exclude shared-cache contention, atomic reference-count traffic or DVFS.

The hardware leaf measures the same 50 computation helpers alone on CPU0,
alone on CPU8, and inside 24-worker checking, with fixed input and repeated
order reversal. Its E/P rate characterizes those helpers, not all kernel,
planning or memory operations. Per-core checks/second for the full closure
are job-mix dependent; allocation-count/CPU rates also remain workload specific.
Linux likewise cautions that relative microarchitecture performance depends on
the operation mix. [Kernel capacity documentation](https://docs.kernel.org/scheduler/sched-capacity.html).

## Acceptance and determinism scope

Require full 4,449 accepted module IDs, completion event, native retirement and
cgroup retirement for every included full point. Analyze nonzero-check modules
only when comparing observed heartbeat work; fallback zeros are unobserved.
The real resident check adds 50 targets under P1/E1/mixed24 x3, with verdicts,
allocation counts and actual serialized .olean bytes. Stable allocation counts
are not stable elapsed time or stable native kernel poll counts. Existing
unsafe/partial and extension-payload trust limitations remain unchanged.
