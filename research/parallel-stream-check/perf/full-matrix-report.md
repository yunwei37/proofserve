# Full Barrier closure: why original-kernel calls become costlier with workers

The original16-cell matrix and all four record decodes have returned. Every
native point accepts the same4,449 reference module IDs,237,863 checks and
3,283,925,639 allocation-counter units; no native budget stops. Original
series/foreground/last-native processes were verified retired.

**Finding:** the largest sampled4P→8P growth is the environment lookup path.
Its owning FFI wrappers contain RC metadata accesses and atomic updates.
Nearly fixed instructions/locked-operation counts plus greater modified-line
traffic support ownership/cache-coherence cost participating. This does not
identify an exclusive cause or a removable CPU fraction. No Lean change.

## Frozen native and ordinary timing

Same fd1e9be executable and full BarrierData41 closure, Lean4.34.1. Order:
workers4,8,1,2; each plain-before/stat/record/plain-after. Blocking P-core
lock, CPU0–7, per-frontier jobs pinned0..n-1/coordinator0. A pool TID can
start different checks on different cores: not fixed TID/core placement.
No-M,1100s native/1740s outer after lock, same14GiB sampled own-tree and
charged-cgroup controls inside16GiB M allocation. Sampling is not a hard
RSS quota. Serial offline decoding on E8–15.

| Workers | Ordinary wall range s | Ordinary CPU s | Original-kernel C interval CPU s |
|---:|---:|---:|---:|
| 1 | 644.237–653.783 | 643.488–647.394 | 465.913–469.327 |
| 2 | 435.382–436.603 | 628.884–630.023 | 447.468–448.316 |
| 4 | 347.710–360.887 | 652.159–659.010 | 471.729–474.846 |
| 8 | 315.390–320.868 | 722.326–728.427 | 537.622–541.667 |

Across the four ordinary4P/8P pairings, 91.70%–99.15% of extra CPU
lies inside measured original-kernel calls. This updates the earlier before-
only subset; it does not borrow historical e773018 clocks. The C interval
includes runtime operations inside the original call, not just reduction.
Individual user/system/RSS/cgroup values remain in results/native-timings.csv.

## Whole-command user-mode PMU counters

All seven stat selectors report100% running. These cover the whole command,
not the originalCheck interval. L3 miss is the retired L3-miss-load selector,
not every LLC transaction. HITM/RFO are traffic, not RC-specific stall counts.

| Workers | Cycles T | Instructions T | IPC | L3-miss loads M | Locked loads B | L3 modified-line forwarding M | RFO snoop-HITM M | Cycles/ref |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.699 | 3.338 | 1.964 | 548.381 | 5.800 | 0.095 | 0.000 | 0.82075 |
| 2 | 1.763 | 3.338 | 1.893 | 533.774 | 5.805 | 275.337 | 184.308 | 0.88581 |
| 4 | 1.821 | 3.340 | 1.834 | 523.881 | 5.811 | 531.790 | 344.815 | 0.88562 |
| 8 | 1.973 | 3.341 | 1.694 | 586.639 | 5.818 | 778.599 | 516.380 | 0.87408 |

4P→8P: cycles+8.31%, instructions+0.040%, locked loads+0.117%,
L3-miss loads+11.98%, modified-line forwarding+46.41%, RFO snoop-HITM+49.76%.
Cycles/ref decreases1.30%; nominal caps hide actual frequency differences.
Extra instruction work and frequency alone do not explain this combination.
P1 still performs billions of locked operations with near-zero modified-line
traffic. Counting atomics is insufficient to quantify their cost.

## Sampled original-kernel families

Units: billions of recorded cycle-sample periods, not exact hardware counts
or seconds rescaled from another arm. Each sample has one nearest-operation
family. Lookup/whnf can contain inline RC. SDK C++ inline debug is incomplete.

### Strict checkOne plus C++ kernel ancestry

| Family | 1P | 2P | 4P | 8P | 8P minus4P |
|---|---:|---:|---:|---:|---:|
| Allocation/free | 77.343 | 74.365 | 68.477 | 76.992 | 8.516 |
| Environment/hash/cache lookup | 262.802 | 258.773 | 266.395 | 311.380 | 44.985 |
| Other type inference | 104.861 | 83.415 | 87.945 | 92.923 | 4.978 |
| Other/unresolved | 0.130 | 0.064 | 1.216 | 0.085 | -1.132 |
| Explicit RC/destruction | 87.889 | 82.688 | 88.560 | 107.170 | 18.610 |
| whnf/defeq, unresolved inlines | 140.998 | 128.719 | 140.837 | 149.643 | 8.806 |

### Additional worker plus kernel ancestry, missing checkOne

| Family | 1P | 2P | 4P | 8P | 8P minus4P |
|---|---:|---:|---:|---:|---:|
| Allocation/free | 28.332 | 29.580 | 29.108 | 32.593 | 3.485 |
| Environment/hash/cache lookup | 147.362 | 164.305 | 179.078 | 241.127 | 62.049 |
| Other type inference | 4.747 | 5.068 | 4.827 | 5.071 | 0.245 |
| Explicit RC/destruction | 27.231 | 27.215 | 34.107 | 44.546 | 10.439 |
| whnf/defeq, unresolved inlines | 129.228 | 130.556 | 141.620 | 151.349 | 9.729 |

Lookup represents53.07% of strict sampled growth; combining the two scopes
makes it62.70%. Explicit RC/destruction is21.95% or17.02%, respectively.
These are conditional sampled-mass shares, not exact CPU shares. Lookup
is not pure hash arithmetic, so this does not imply RC is absent.

Strict fraction of the two worker/kernel scopes: 1P 66.67%, 2P 63.78%, 4P 62.70%, 8P 60.86%.
Changing stack coverage can bias comparisons. This is not coverage of all
true original-check CPU. Other worker/truncated, serial kernel and outside
scopes remain in CSV. No normalization to a separate stat arm or partial READ.

## Where lookup-path growth lands

In this exact binary, lean_environment_find grows26.751→60.129 G strict
sampled cycles, C++ environment::find7.760→15.082 G and lean_dec_ref_cold
87.418→103.667 G. Disassembly shows RC-header loads/MT atomic updates in
these wrappers. Source-labeled positions at/immediately after those accesses
grow83.159→135.735 G: +52.576 G, about62.0% of strict sampled growth.
See ownership-localization.md and the complete offset table. This grouping
is post-hoc and binary-specific. Skid, inline omissions and captured-stack
limits prevent treating adjacent PCs as exact atomic latency.

[Matched Lean lookup bridge](https://raw.githubusercontent.com/leanprover/lean4/v4.34.1/src/kernel/environment.cpp)
uses owning argument conversion, consistent with the measured increment
paths. Runtime data addresses were not sampled. Same-object contention,
false sharing, moving worker/private heaps between cores and other cache
effects remain unseparated. Equal entry/exit CPUs do not prove no migration;
aggregated worker lists are not an ordered migration trace. There is no
causal-elimination experiment and no Lean optimization in this study.

## Per-worker counts and the actual evidence defect

results/observed-worker-counters.csv retains every checking TID, READ sums
and completeness flags. TIDs are historical pool threads, not a claim that
more than n checks run simultaneously. Counts cover thread lifetimes, not
PMUs gated exactly at originalCheck entry/exit.

P1 has1 complete checking TID; P2 has3, IPC1.936–1.962. P4 has5 TIDs whose
shard completeness is unknown after earlier raw cleanup. P8 has9 TIDs:
4 complete and5 incomplete final READ sets. Affected IPC/miss ratios stay
blank. Every P8 worker has cycle samples on all expected CPU-shard IDs, so
missing READs are not inactivity. Zero reported sample loss does not certify
complete exit counters. Per-CPU enabled/running contexts are not blindly
scaled as multiplex ratios.

A separate official record -n -s count-only repair was queued only after
the original16 retired. Same Lean/native inputs/placement, without unneeded
sampling/DWARF. Its counts carry their own label and are not substituted
into original sample tables or overhead estimates. Original incomplete P8
raw remains. The earlier uncompressed-only proposal was never executed.

## Perf overhead, kept separate

| Workers | Plain wall range s | Stat wall s | Record wall s | Record vs observed plain range |
|---:|---:|---:|---:|---:|
| 1 | 644.237–653.783 | 662.582 | 662.333 | 1.308–2.809% |
| 2 | 435.382–436.603 | 435.860 | 438.799 | 0.503–0.785% |
| 4 | 347.710–360.887 | 350.946 | 349.724 | -3.093–0.579% |
| 8 | 315.390–320.868 | 314.385 | 319.636 | -0.384–1.346% |

Negative endpoints mean observed drift, not negative instrumentation cost.
One before/after pair plus one stat/record point is not a confidence interval
or three repetitions. CPU/user/system and both-arm brackets remain in CSV.
Ordinary and perf timings are not mixed as speedup evidence. The same C
observer remains on in every arm; this study does not claim it is free.

## Scope and retained evidence

One complete real4,449-module closure, not all openai/math or Lean workloads.
The single cohort, shared-host preparation, frequency differences and stack/
READ limits bound generality. Namespace OAI/Mathlib is not itself a regime
label. Resource guards, controls and test success are not novel contributions.

Primary PVC: /workspaces/.agent-state/gpu-smt-captures/parallel-stream-perf-20261103.
Frozen original16 input tables: publication-original16. Native commands,
stdout/stderr, lifecycle/memory, attrs, decoded READs, complete compressed
address/offset aggregates and the exact binary remain. Analyzed original
P4/P1 raw was removed only after published analysis; those DWARF dumps cannot
be freshly unwound/reclassified. Incomplete P8 and failed attempts remain.
Cleanup entries are exact in cleanup-20261103.csv. Code/small CSVs are in Git.

Generate tables: comparison_tables.py POINT/analysis-progress OUT, after
original16 completion; it selects the original r1 keys. Review: 自审 only.
This supplies evidence to the root paper owner, not paper acceptance.
