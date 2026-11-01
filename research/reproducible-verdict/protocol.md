# Budget and replay contract

Experimental interface, not a production verifier replacement.

## What is recorded

Probe receives exact candidate source, target theorem, the requested Lean
maxHeartbeats option, frontend mode and observer. It emits verdict, executing-
thread allocation observations, diagnostics, theorem presence and axiom policy.
replay.py binds these rows to the *whole ordered request list*, declared Lean/
Mathlib identities, frozen probe revision and native process result. Unreturned
requests remain missing even when a timeout terminated the process.

A replay reruns Lean and compares these fields. It does not accept a remote
verdict as a logical certificate. Source hashes are not an acceptance gate.
The full source and pinned repository revision remain necessary; source text
alone omits imported environment, metaprogram code, options and process history.

## Two work-counter families, not a single universal clock

The pinned source has distinct mechanisms:
- IO.getNumHeartbeats and Lean.Core.checkMaxHeartbeats use current-thread
  small-allocation work. Core contexts carry a start point; wrapAsync explicitly
  propagates previously spent work into the child.
- [runtime/interrupt.cpp](https://github.com/leanprover/lean4/blob/v4.34.1/src/runtime/interrupt.cpp)
  increments the native check_heartbeat counter at explicit check_system polls.
  [Kernel.Environment.addDeclCore](https://github.com/leanprover/lean4/blob/v4.34.1/src/kernel/environment.cpp)
  receives a native heartbeat limit; Lean/AddDecl.lean passes the option-derived
  limit. Our allocation deltas are **not** a direct observation of that counter.

Summing arbitrary child deltas can double-charge inherited prefix work. Reading
only the blocked parent omits child work. Poll counts, allocation counts and
wall time are not interchangeable. The current receipt sets complete work
accounting to false; native kernel poll count remains unmeasured/null.
The requested global candidate-budget interface is therefore **not yet complete**.
The working interface exposes stock option budgets and partial unit observations.

## Normalization under investigation, not an invented guarantee

A viable contract would need fixed verification units, stable input/environment
and per-unit counters on the actual executing thread. Shared/lazy initialization
must have a specified owner or exemption. Observer work must be measured
separately without mutating the useful-work account. Merge order must not change
unit identity or diagnostics. A canonical reference execution can be replayed;
that alone does not prove a different parallel execution has identical cost.

Our eight-task control has invariant40110 summed allocation units but moves a
14-unit first-use charge between task identities. This does not justify subtracting
14 from real proofs. Upstream's shared-thunk accounting fix already addresses this
class of issue. No new generic normalization algorithm is claimed.

Monotonicity B-pass implies larger-B-pass requires the same useful execution.
Arbitrary Lean metaprograms can inspect the option or remaining budget and take
a different path. run_extra.py includes an intentional budget-aware True proof
control; this is not a frequency estimate for real candidates.

## Logical trust boundary

Probe's frontend classification is an observation, not an independent proof
checker. In particular candidate code can change options such as
debug.skipKernelTC; merely finding a theorem object does not establish that the
kernel checked it.

ReplayProbe.lean consequently starts again from the pinned imported base and
rechecks all ordinary new declarations in dependency order with the *original*
Kernel.Environment.addDeclCore, then requires the target theorem and existing
sorry/new-axiom checks. It never calls addDeclWithoutChecking or mutates the
kernel. Complex groups/cycles are explicitly unsupported by this prototype.
A deliberately forged theorem under skipKernelTC is a prepared negative control.
Compilation of this variant is complete; native qualification must still run.

This adds an audited coordinator and repeats checking, but adds no logical axiom
or alternate kernel. It is not a claim that every candidate remains supported
or that replay costs no extra time. Kernel replay allocation work is a separate
field, outside the original frontend observation; kernel poll units remain null.

## Cache/hardware conditions

Scoped input-cache controls evict only the benchmark's own request JSON with
posix_fadvise and confirm page residency via mincore. They are not globally
cold SDK/Mathlib runs. No host drop_caches or sysctl mutation is authorized here.

Lab is Ready with no pressure in the read-only cluster observation, but there is
no matched second-machine execution in these results. Existing Workspace placement,
other Pods, CronJobs, credentials and PVC scheduling remain unchanged. Portable
requests can be replayed once the matched execution environment is available;
do not substitute E cores, version drift or a different theorem for this result.

## Input policy and experimental scope
The current request option does not override arbitrary source-level options.
Experimental selected inputs remove their top-level maxHeartbeats setting before
injecting B; proof bodies stay the same. A general candidate can reset options
or inspect budget. Therefore source policy and a global authority budget are
still unresolved; the prototype does not claim to enforce a global B against
arbitrary metaprograms.

Likewise miniF2F membership alone does not prove search-dominated execution.
The selected cohort includes a tiny closed-modulo/reflexivity control. Its
'mathematical' label means the tactic input stream here, not a measured phase
share for every source. Computational kernel replays measure the kernel stage
explicitly; absolute stage costs are not directly compared with full frontend.
