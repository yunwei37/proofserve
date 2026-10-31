# Final attribution: the native memory guard can dominate system CPU

**Completed 90/90 native cells, 30 triplets; same-thread 自审, 2026-10-31.**
The large OS fraction in Grid and UMoments9 mainly comes from repeated native
resource-accounting checks, followed by synchronization. It is not mainly
mmap/munmap traffic. This is a characterization of the specified benchmark
configuration, not an intrinsic cost of all Lean verification or a new engine
speedup. EnvelopePsiB provides the low-system-time counterexample.

## Native outcomes and controls

[The full native table](native-results.md) gives all five configurations for
all three modules, with wall/user/system/peak RSS median and min–max (n=3).
[Artifact checks](artifacts.csv) verify **all 90 decisions, 90 diagnostics,
90 entire .olean files, 60 .ilean files and 60 generated C files** agree
with the corresponding baseline. All return codes are 0; no error, panic or
sorry warning, budget event or surviving recorded native PID/birth was found.
This is exact output agreement on these three passing modules, not proof that
two memory-limit policies classify every failing workload identically.

| Module | Baseline wall median s | no-M wall median s | Baseline/no-M ratio | Baseline system s | no-M system s |
|---|---:|---:|---:|---:|---:|
| Grid | 621.936 | 305.693 | 2.0345 | 436.151 | 107.412 |
| UMoments9 | 141.739 | 88.211 | 1.6068 | 100.597 | 42.305 |
| EnvelopePsiB | 64.447 | 63.518 | 1.0146 | 2.669 | 1.960 |

Grid's baseline system share is 53.07% of its native user+system CPU.
UMoments9 is 45.52%; EnvelopePsiB is 4.09%. Removing native -M reduces
wall medians by 50.85%, 37.76%, and 1.44%, respectively. The low-OS module
has only about 0.71 s less system CPU; this is small in its 64 s request.
Thus “-M is expensive” needs a workload qualifier.

The physical outer native cgroup remains **15 GiB in every arm**, with the
same M-lane 16 GiB sampled-tree budget. Baselines additionally have native
-M8192 (Grid) or -M9216 (others). noM removes only this cooperative check,
not outer protection. These are different enforcement policies; the selected
passing cases stayed below their native guard. No host or parent quota was
changed. Sources/dependencies/SDK/output scope are fixed. Native heartbeats
remain original (Grid's point uses 100k); there is no source rewrite.
Every timed run uses P cores0–7 and the shared pcore.lock; all analysis runs
on E cores. Native self wall is at most1200 s. The finite matrix took hours;
it is not presented as a sub-30-minute job.

The Grid no-M system times span **101.35–213.35 s**, although walls span
303.20–320.61 s. Preserve this substantial scheduling/CPU variability rather
than giving a single gain as if deterministic. Separate metric medians are not
an additive phase budget. Ordered repetitions and shared-node effects are
not a randomized confidence interval. Queue waits and controller cost are
retained in raw records and excluded from the native denominator.

## On-CPU system attribution

Three baseline records per module; percentage is **within kernel sampled
cycle periods**, median [min,max]. It is not a fraction of request wall and
is not multiplied into an unrelated plain-run denominator. The independent
flat report matches all decoded native sample and period totals for all nine
records. Sampling uses99Hz cycles, DWARF8192, no inline expansion, max48frames.

| Module | Resource accounting | Futex synchronization | Page faults | Mapping/advice | Other kernel |
|---|---:|---:|---:|---:|---:|
| Grid | 74.98% [74.92, 75.26] | 20.42% [20.33, 20.72] | 0.78% [0.66, 0.85] | 0.14% [0.11, 0.15] | 3.35% [3.29, 3.47] |
| UMoments9 | 59.36% [58.38, 59.43] | 34.10% [33.96, 35.07] | 0.98% [0.84, 1.04] | 0.11% [0.07, 0.14] | 5.13% [5.02, 5.25] |
| EnvelopePsiB | 20.66% [15.84, 23.03] | 1.11% [0.74, 1.81] | 37.65% [36.71, 39.24] | 7.65% [6.63, 9.20] | 31.95% [30.54, 33.99] |

“Mapping/advice” includes mmap/munmap/madvise stacks, not only mmap.
Other includes unclassified kernel paths; scheduler/wakeup and identifiable
PMU paths are separate rows in [operations-summary.csv](operations-summary.csv).
Independently summarized category medians need not sum to exactly100%.
The [per-repeat user/kernel top20](top20-per-repeat.csv) and nine individual
top20 CSVs retain symbols and DSOs. [Per-repeat operation categories](operations-per-repeat.csv)
include user allocation/free, reference counting, hashing, residual kernel
checking, IR execution and synchronization. They are ordered visible-operation
labels, not additive semantic phases: a hash/RC operation inside the kernel
checker is classified before residual kernel checking.

Grid's observed path is getrusage → libc → lean::check_memory →
lean::check_system → type_checker reduction/checking (with a smaller resolved
IR-interpreter origin). The SDK's actual check_memory disassembly compares the
counter with200 and calls getrusage; native max-memory zero disables that
path. RUSAGE_SELF aggregates process thread-group resources. Accumulated trace
thread summaries are **not simultaneous live thread counts**. The much larger
per-call time in the certificate cases is consistent with expensive accounting,
but this experiment does not isolate a law relating live-thread count to cost.

Grid record r3 resolves kernel→libc but not the application guard caller.
Its stable kernel accounting share remains usable; the missing application
caller is unresolved, not evidence of no guard cost. Native user inlining and
truncated stacks limit operation labels. EnvelopePsiB has only a small absolute
OS budget: page faults take the largest sampled kernel category, unlike the
resource-accounting-dominated certificate modules. “Other kernel” remains
about32% there and is not assigned to a convenient mechanism.

## System calls and the no-M residual

The table reports **observed calls / cumulative elapsed seconds**; each entry
is median [min,max] from three Lean-comm summaries. These elapsed seconds include
sleep/preemption and overlap across threads. In particular futex elapsed time
can exceed request wall and total CPU by orders of magnitude. It cannot be used
as exclusive system CPU or added to the sampled fractions above.

### Grid

| Config | Call | Calls median [range] | Elapsed s median [range] |
|---|---|---:|---:|
| baseline | getrusage | 4010856 [4010848, 4010865] | 309.266 [306.655, 327.540] |
| baseline | futex | 52366009 [51753963, 52717904] | 874905.585 [874369.219, 904104.682] |
| baseline | mmap | 20579 [20577, 20588] | 0.074 [0.073, 0.075] |
| baseline | munmap | 204 [139, 204] | 0.008 [0.007, 0.008] |
| baseline | madvise | 53094 [49409, 56115] | 0.511 [0.496, 0.552] |
| baseline | read | 18966 [18966, 18967] | 0.024 [0.023, 0.024] |
| noM | getrusage | not observed (3/3) | not observed (3/3) |
| noM | futex | 50521174 [50144481, 50979789] | 413913.778 [412399.908, 420878.309] |
| noM | mmap | 20531 [20522, 20535] | 0.073 [0.072, 0.074] |
| noM | munmap | 193 [186, 193] | 0.008 [0.007, 0.008] |
| noM | madvise | 34555 [34389, 34715] | 0.289 [0.269, 0.339] |
| noM | read | 18966 [18966, 18968] | 0.024 [0.023, 0.024] |

### UMoments9

| Config | Call | Calls median [range] | Elapsed s median [range] |
|---|---|---:|---:|
| baseline | getrusage | 1022147 [1022143, 1022149] | 55.843 [55.542, 56.162] |
| baseline | futex | 19003914 [18659318, 19843619] | 151316.195 [151217.093, 157301.167] |
| baseline | mmap | 26617 [26609, 26630] | 0.095 [0.086, 0.101] |
| baseline | munmap | 157 [141, 167] | 0.003 [0.003, 0.003] |
| baseline | madvise | 12432 [12227, 12600] | 0.109 [0.107, 0.114] |
| baseline | read | 25405 [25403, 25407] | 0.032 [0.031, 0.037] |
| noM | getrusage | not observed (3/3) | not observed (3/3) |
| noM | futex | 18166388 [18115068, 18193599] | 83384.667 [83383.933, 83410.033] |
| noM | mmap | 26580 [26565, 26582] | 0.085 [0.084, 0.085] |
| noM | munmap | 146 [120, 165] | 0.003 [0.003, 0.003] |
| noM | madvise | 9358 [9246, 9486] | 0.072 [0.072, 0.074] |
| noM | read | 25405 [25405, 25407] | 0.032 [0.032, 0.033] |

### EnvelopePsiB

| Config | Call | Calls median [range] | Elapsed s median [range] |
|---|---|---:|---:|
| baseline | getrusage | 600149 [600145, 600151] | 1.418 [1.401, 1.437] |
| baseline | futex | 65492 [65406, 65698] | 2983.390 [2979.753, 2984.532] |
| baseline | mmap | 53857 [53850, 53865] | 0.152 [0.151, 0.153] |
| baseline | munmap | 53 [46, 67] | 0.002 [0.002, 0.002] |
| baseline | madvise | 6671 [6633, 7724] | 0.096 [0.083, 0.101] |
| baseline | read | 53747 [53744, 53749] | 0.066 [0.066, 0.067] |
| noM | getrusage | not observed (3/3) | not observed (3/3) |
| noM | futex | 63602 [61636, 64688] | 2842.669 [2837.672, 2851.173] |
| noM | mmap | 53862 [53855, 53863] | 0.152 [0.150, 0.153] |
| noM | munmap | 47 [40, 53] | 0.002 [0.002, 0.002] |
| noM | madvise | 5097 [4517, 5315] | 0.081 [0.062, 0.081] |
| noM | read | 53750 [53747, 53754] | 0.065 [0.065, 0.067] |


No getrusage row was observed in any of the nine no-M Lean summaries, whereas
baselines show about4.01M /1.02M /0.60M calls. That agrees with the disabled
memory-guard call path. Missing summary rows are not manufactured exact zero
census entries in the CSV. Grid baseline trace lost16,749/7,348/0events, no-M
348/0/0; all other trace captures report no LOST events. Even without a LOST
warning, paired-entry/exit summaries need not be a perfect syscall census.
[Trace quality](trace-quality.csv) retains these facts.

After removing -M, system CPU remains **107.41 s Grid /42.31 s UMoments9 /
1.96 s EnvelopePsiB** (plain medians). Grid and UMoments9 still have about
50.52M and18.17M observed futex calls, near baseline52.37M and19.00M.
Mapping/advice elapsed times remain small. This supports persistent
synchronization as the main **evidenced** remaining path in these two modules,
not allocation/VM syscalls as an explanation for all residual time.

**The matrix contains no no-M perf-record arm.** The residual's exact on-CPU
futex/page-fault/mapping percentages therefore remain unmeasured; baseline
fractions cannot be subtracted from no-M seconds. no-M stat/trace are supporting
counterfactuals with their own observer costs, not substitutes for those stacks.

## Single-factor controls and measurement cost

Setting j1 and LEAN_NUM_THREADS=1 while retaining -M makes Grid **14.2% slower**
and UMoments9 **23.3% slower** in wall median; EnvelopePsiB changes by about0.8%.
The system CPU does not collapse. j1 controls Lean workers, not every auxiliary
OS thread. This rejects “just use one worker” as a fix for these measured cases.
There is no combined no-M+j1 arm, so their interaction is unknown.

The separate128MiB glibc mmap and trim thresholds change wall medians by at
most0.71% here, with overlapping ranges and no stable improvement. No general
allocator tuning benefit is demonstrated. The pinned SDK uses mimalloc for Lean
objects, so glibc thresholds do not control its whole allocation path.

Profiler overhead is measured in **separate triplets**:
[all ratios](profiler-overhead.csv), [all counters/IPC medians and ranges](stat-summary.csv).

| Module/config | Mode | Wall change vs own plain median | System CPU change vs own plain median |
|---|---|---:|---:|
| Grid/baseline | stat | +1.47% | +33.10% |
| Grid/baseline | record | +1.57% | +11.47% |
| Grid/baseline | trace | -0.86% | +18.25% |
| Grid/noM | stat | +7.25% | +126.98% |
| Grid/noM | trace | +0.82% | +74.12% |
| UMoments9/baseline | stat | +5.22% | +41.77% |
| UMoments9/baseline | record | +4.22% | +17.60% |
| UMoments9/baseline | trace | +6.09% | +30.42% |
| UMoments9/noM | stat | +3.43% | +94.42% |
| UMoments9/noM | trace | +1.22% | +59.09% |
| EnvelopePsiB/baseline | stat | +0.44% | +1.17% |
| EnvelopePsiB/baseline | record | +0.88% | +5.84% |
| EnvelopePsiB/baseline | trace | +4.99% | +107.52% |
| EnvelopePsiB/noM | stat | +0.64% | +7.88% |
| EnvelopePsiB/noM | trace | +1.78% | +71.23% |

For example, Grid baseline stat has only+1.47%wall but+33.10%systemCPU;
Grid no-M stat has+7.25%wall and+126.98%systemCPU. Observer cost is material.
Do not pool plain/stat/record/trace clocks or call the profiler free merely
because wall perturbation is small. Hardware counters include the constant
short launcher plus native; stack tables select Lean samples. Counter
multiplex running ratios remain in the per-repeat CSV.

## Scope, reproduction and next population measurement

Pinned OpenAI/math4eaee875, Lean4.34.1/5045d005, Mathlibd13f. Full raw
commands, source copies, native receipts, perf.data, syscall traces, artifacts,
memory and terminal records remain on the PVC under:

    /workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime/

The original matrix is frozen in matrix-v3; priority-grid-v1 promoted twelve
**existing** cells only after the current native retired, without adding or
duplicating cases. Both controllers completed. Original failed setup controls
and the earlier Grid interim report remain separate historical evidence.

Rebuild small tables inside the existing Workspace, on E cores:

    taskset -c 8-15 python3 research/profile-2026-10-31/systime/analyze_final.py

No Lean measurement is launched by that command. Raw independent flat reports
are in final-analysis on PVC. An initial offline flat decode used inline
expansion and was stopped in favor of explicit no-inline; its partial file is
retained. A later SSH observation disconnect did not mean decode failed:
all nine finished outputs, exact total matches and process retirement were
subsequently checked. No native source, policy or captured timing was changed.

[W's paired-panel design](w-handoff-design.md) fixes26 already-returned random
draws (with24 remaining new pairs after reusing the two completed sentinels),
keeps the original42-draw inclusion frame, and specifies one unprofiled no-M
run per ready target with an adjacent fresh baseline where needed.
It gives paired CPU-delta estimators and explicitly retains incomplete strata,
runtime noise and artifact/outcome changes. The design is **not launched here**.
The three selected modules alone cannot establish a full-library cost correction,
a full-build makespan, or an OSDI-level acceleration claim.

Primary implementation context, already checked against the pinned SDK:
[Lean memory checks](https://github.com/leanprover/lean4/blob/v4.34.1/src/runtime/memory.cpp),
[getrusage semantics](https://man7.org/linux/man-pages/man2/getrusage.2.html),
[upstream Linux implementation](https://github.com/torvalds/linux/blob/v7.0/kernel/sys.c).
The last is upstreamv7, not a complete audit of the Ubuntu7.0.0-29 distribution.
