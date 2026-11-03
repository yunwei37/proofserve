# Existing marked8P closure: partial wall attribution
自审,2026-11-03. All three complete JSON/stdout/terminal captures checked:
4449 ordered accepted IDs, native retirement, no budget interruption.
Raw: parallel-stream-persistence-20261103/full-plain-m1-P8-r{1,2,3}.
These are complete pre-reboot captures, not interrupted qualification data.

Median wall298.675s. Disjoint existing buckets with own run denominators:
read0.341s; dependency/context30.506s; plan10.990s; serial complex/cycle
fallback115.454s; checked batches122.565s; duplicate checking0.03468s;
unassigned17.841s. Marginal medians do not form a synthetic run;
CSV rows individually reconcile exactly. Unassigned includes event output,
origins/state bookkeeping, runtime/lifecycle and unobserved work; it is not idle.

Original-check interval union median116.570s is nested in batch wall, not
an additional phase. Per-wave maximum observed threadCPU sum84.169s.
Keeping other work and measured job costs fixed gives a barrier-schedule
floor259.011–260.790s, hence1.1453–1.1474 additional speedup.
This is a conditional fixed-cost scenario, NOT a universal Amdahl theorem or
true DAG longest path: successive heaviest wave jobs need not be connected.
It retains115s serial fallback, potentially a prototype restriction.
No intrinsic workload multicore ceiling is established.

C observer limits retained; no trace.profiler. New phase/job/dependency capture
and matching observer control remain pending.
