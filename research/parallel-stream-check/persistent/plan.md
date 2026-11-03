# Causal ablation: persistent checked frontiers
RQ3 supporting/decisive test requested by the user: does the unmarked replay
frontier create most of the observed negative CPU scaling? No kernel change.

## Evidence before intervention
SDK4.34.1 commit5045d0056413266e57c625dcd7c365b10e377c52.
Original ParallelCore/Stream match frozen fd1e9be source and have no explicit
markPersistent. Compacted .olean payloads may already be persistent; do not
infer their RC status from the newly constructed environment. Inspect root
and actual base.find? ConstantInfo headers, plus original input CIs.
Matched SDK LeanChecker.replayFromImports uses importModulesCore and
finalizeImport(...false,false), not leakEnv=true. Default module parallelism
is IO.asTask per module, while replay itself is sequential. Therefore the
assertion that stock parallel leanchecker is already marked is not assumed.
Compare actual importer states for leakEnv=false/true and retain the source.

## Minimal intervention and safety
Same new executable in both arms, flag0/1. Before every checkedBatch enqueues
workers, a timed C adapter calls the exact official one-argument
lean_runtime_mark_persistent(base) iff enabled, returning the same base.
No worker is launched yet; all previous tasks joined. Matched runtime consumes
the task closure before publishing its result and completes recursive mark_mt
before m_value publication. Pending task bookkeeping does not revisit the base.
Kernel.Environment does not run user extension initializers in this stream.
No marking occurs while the current frontier is being checked.
Root/header diagnostics and timers are common to both arms; CI probes only
in the separate diagnostic qualification, not primary timing. Mark-window
times include clock-read overhead, with the off arm measuring that overhead.
No new checker or axiom. Existing trusted coordinator/FFI remains implementation
glue; an unchanged mathematical kernel is not a formal whole-TCB theorem.

## Qualification and actual build estimate
Prior exact five-command build took1.735/.156/.257/3.580/7.626s, peak~1.7GiB.
This similarly small source build/link is serial on E8-15, guarded as before;
allow180s per command, no whole Mathlib rebuild or source changes outside M.
Qualify real ComputeControl positive/bvar at1/8 workers in both modes, plus
stale/duplicate-token faults. Inspect existing CI persistence vs input CIs,
and actual MT/persistent state after task enqueue before the gate releases.
Bad proofs must still be rejected by the original kernel.

## Frozen full matrix
Full same4,449-module Barrier closure and frozen inputs. Workers1/2/4/8;
each arm at least3 plain repetitions and1 stat (32 full native cells).
Counterbalance arm order across repeats. Each cell separately acquires the
blocking P0-7 lock and releases on native exit; no concurrent M native/decode.
No-M; native1100s/outer1740s after lock; same14GiB sampled own-tree/charged
cgroup limits inside16GiB lane. Sampling is not a kernel hard RSS quota.
All output/source/binaries on PVC; raw perf/captures not Git. Disk<85%.

Record wall/user/system, original-kernel CPU/units/checks, mark-window CPU/wall,
peak sampled RSS/ru_maxrss/charged memory and actual PMU counts/IPC/coherence.
Fixed reference IDs/checks and in-kernel allocation units must match. If not,
retain the result as failed work equivalence, investigate rather than changing
the oracle or hiding it. Resource failures remain resource failures.
Report at least3-repeat median/range, one stat per cell is not a confidence
interval. Mark leaks memory by design: report measured overhead and explicit
full-library extrapolation limits, not a false saturated-service guarantee.

## Stock comparison and interpretation
Use the installed unchanged leanchecker for source-supported controls;
module-local/default and --fresh are different scopes from independent closure
replay and must be labeled. Normal single-root mode checks only the root after
trusting its imports. Do not compare that wall directly to4,449 independently
checked modules or claim identical heartbeat/check coverage without evidence.
Old3.33x/1.88x results stay historical. If persistence changes scaling, classify
the prior CPU behavior as a prototype property and state which old gains need
remeasurement; do not silently replace Grid from a Barrier ablation.
Retain negative results and faults; reviews are 自审. No additional Agents.
