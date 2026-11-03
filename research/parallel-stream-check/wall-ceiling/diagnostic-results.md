# Complete post-reboot8P diagnostic — 自审
Raw parallel-stream-wall-20261103/diagnostic, own wall294.587s and550.410CPU-s.
4449 ordered module accepts,237863 original-call observations and3283925639
allocation-counter units match complete pre-reboot1d742e3 exactly.
All four default-on positive/bad controls complete: two-module Waves scope,
native original-kernel malformed theorem rejected at1/8 workers.
Initial host-reboot-interrupted ComputeControl remains excluded.

## Exclusive wall reconciliation
Read/deserialization26.4169s; dependency/context26.1800s; planning8.8921s;
serial original-replay fallback94.3295s; checked batches111.6578s;
duplicate theorem rechecks0.0283s; unassigned27.0826s.
Sum equals294.587177446s, using this diagnostic's own denominator.
Post-reboot file reads are much more expensive than the pre-reboot warm cache;
do not substitute its94s fallback into the old299s denominator.

Batches partition into marked-frontier0.2591s, launch-with-no-check2.8957s,
join-with-no-check0.4950s, token validation0.1739s, commitChecked0.1812s,
original-call-interval union107.3749s, and native tracing/tail0.2779s.
These sum to111.6578s. The original-call union includes original-check wrapper
and clock/HB sampling, not an instruction-exact C++ type-checker filter.
No-check intervals include queueing, gate/runtime and postcheck work: not
necessarily OS-idle. Idle core-seconds are a different measure, not added to wall.
Unassigned includes JSON plan/dependency trace output, state bookkeeping and
lifecycle. Same-binary no-trace observer control is pending.

## Conditional spans
18990 waves,237863 jobs. Sum per-wave largest threadCPU74.5318s;
sum exact local-module DAG longest paths54.6950s. Heavy winners in adjacent
levels need not be connected, explaining the19.8368s difference.
Keeping182.9294s outside batches fixed yields257.4612s barrier floor or
237.6244s local-DAG floor. Both retain serial module order and94.3295s fallback;
both assume measured job CPU costs unchanged. They are model scenarios,
not an architecture-independent proof of maximum speedup.

Width1:3294waves/5.241s; width2–8:9061/37.471s;
width9–32:5267/31.622s; width33–128:1250/13.374s;
width>128:118/23.672s. Wave time here is native start-through-commit, excluding
trace flush tail. Narrow2–8 waves are important; few very wide waves also retain
160.054CPU-s of useful work and have only1.457s summed maximum-job span.
See heaviest-waves.csv and per-module CSV. No intrinsic dependency conclusion
about serial fallback: its whole-module eligibility restriction is under test.
