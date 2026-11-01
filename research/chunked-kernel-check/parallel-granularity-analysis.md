# Why the module curve differs from a tiny-goal split

This is offline analysis of the completed Barrier point, not another capture.
The heavy frontier has1099independent declarations. Worker-loop elapsed
medians (maximum across workers within a repetition, then across3repetitions)
for1/2/4/8workers are43.543/22.284/12.141/6.328s. These loops include replay
setup, map/audit and queue access; they are not pure C++ checker timers.
The8worker loop maximum improves6.88x over the1worker loop maximum, while
whole pipeline improves3.33x against direct stock. The denominators differ;
neither number substitutes for the other.

At8workers, slowest/fastest heavy-frontier worker-loop medians are6.328/6.219s;
dynamic queue assignment leaves little elapsed imbalance in this case.
Do not divide those elapsed values into total CPU as if they were exact
simultaneous spans: task starts differ and exports may overlap other checking.

The complete heavy stage is7.361s, including reading/importing and exporting.
Whole stage minus the maximum individual check+export duration is about1.032s.
Because the individual duration is no larger than the enclosing parallel span,
this difference is **only an upper bound** on time outside worker intervals;
it is not an exact import/system-call cost attribution.

Other small frontiers cost about1s each despite tiny checking work, and the
final audit another1s. This makes repeated fresh stages a real cost. Coalescing
small dependency frontiers could remove some repeated setup, but has not been
implemented or measured; do not subtract those seconds as guaranteed gain.

The earlier Grid146ms goal showed the opposite regime: separate module export,
reimport and process setup overwhelmed its small amount of checker work.
Barrier amortizes those costs across thousands of unchanged proof declarations.
The queued Envelope6.163s goal will test the third case: a large single
computation split into whole per-index groups. Its answer remains pending.

This does not prove source-build speedup. In particular, do not subtract this
point's serial replay seconds from W's independently measured source compile
wall clock, nor add the result to a different frontend run. A source-build
or service claim needs its own matched end-to-end experiment and denominator.

Reproduce on E cores:
 taskset -c 8-15 python3 research/chunked-kernel-check/analyze_parallel_workers.py \
 /workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check/parallel-barrier-v1

## Existing module parallelism is already a baseline
The installed pinned4.34.1 SDK's src/lean/LeanChecker.lean line108creates an
IO.asTask(replayFromImports m) per matching module. Line33replays one module's
constants through the official serial kernel replay. Therefore upstream already
offers module-level concurrency. The positive Barrier curve concerns parallelism
*within one compiled target*, not the invention of parallel checking or an
existing whole-library mode comparison.

An explicit fixed-work model on the retained31-artifact panel uses588.773s
serial native-call CPU. The largest module, Grid, accounts for265.919s.
Ignoring all overhead/memory/contention,8processor whole-module work bound
is73.597s, but the unbroken-module straggler bound is265.919s. LPT reaches that
bound in this idealized panel. Even making Barrier free leaves this dominant
bound unchanged. These are CPU-work scheduling model units, not observed
concurrent wall clocks; no measured14.127s wall is substituted for a CPU weight.
The panel contains purposeful modules and excludes13original draws, so it is
not representative library throughput. See module-granularity-bound.json.

This limits the next claim: single-module3.33x cannot be promoted to library
throughput without a stock module-concurrent baseline and representative
straggler coverage. It does support a concrete source of parallelism inside a
cost-heavy target while preserving original checked constants.
