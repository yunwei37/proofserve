# Direct whole-library original-kernel checking (RQ1)

2026-11-02 UTC. Review: 自审. Status: first real bounded segment submitted;
no full-library cost has been measured.

## Question and input
Measure actual native kernel CPU over the complete openai/math release, not
a transfer of Falconer ratios. Fixed source revision
4eaee87548250b2682affda7d05d947c05554bae: all163097released source modules,
including modules outside the default OAI root, plus required native dependencies.
The original Lean4.34.1 kernel and qualified CheckpointAudit are unchanged.
Source identity follows the publisher's Lake srcDir override for Hodge helpers.
No source/candidate is rewritten.

The full source archive has actually been extracted on PVC:163097files/
1785499363bytes. The initial immutable provider overlay contains2469source
module artifacts;160628source modules lack ready typed artifacts.
This is a source-to-typed-input prerequisite, not160628kernel rejections.
Forty-two external import names have no initial provider; package source setup
and source errors are distinct from kernel acceptance and remain explicit.
The upstream package file and pinned dependencies are retained. Providers are
the matching SDK/Mathlib/packages and exact B/Falconer compiler outputs from
the earlier fixed experiment; an unqualified partial W namespace is excluded.
Hardlinks make one complete namespace without copying/mutating provider bodies.

## Execution
whole-library-prepare.py performs untimedE8 archive/namespace preparation.
Its native child completed normally under the12GiB allocation; charged peak
3001090048bytes/noOOM. This is setup, not a checker cost.
whole-library-run.py window --cohort all first drains existing immutable terms.
The original checker traverses dependencies and exports a certified delta after
500new module acceptances. New segments import only the successful predecessor.
The first few500module segments may consist of dependencies; source and
dependency acceptance counts are always separate.

After available source roots are drained, separate bounded source-production
windows construct missing artifacts in source dependency order with the same
pinned compiler and authored autoImplicit=false, -j8, .olean output. These
preparation compiles do not supply a new W standard-artifact build denominator:
they omit its requested .ilean/C output and use this experiment's resource point.
Their actual CPU/wall/errors are retained separately from kernel CPU.
Missing/failed source prerequisites are propagated as unavailable inputs,
not proof falsity. Sorry warnings are recorded; original kernel/axiom policy
is retained, not silently changed to a no-axiom policy.

All timed native windows join the existing P0–7 flock behind prior waiters,
one task at a time, and release it after the task. No Lean-M is used.
Each native checker has1400s, source compiler600s, locked outer task1740s.
An owned child cgroup is11.5GiB, reserving512MiB for the larger full-frame
Python parent within12GiB. Every command/result/memory.events is retained.
Incomplete tasks stop rather than becoming cached rejection or zero cost.
Every bounded task is reduced and own small result files commit/push immediately;
the next task re-enters the shared lock, without a separate schedule/service.

The original kernel, visibility and structural duplicate audit are the same
ones qualified on Falconer. Source-mode errors/censors, kernel rejects,
timeouts, OOMs, missing terms and unvisited source IDs are separate.
A valid segment must exit0, emit checkpoint/complete, and have no reject or
malformed native record. Only those segments contribute acceptance IDs;
all attempted native CPU remains in actual cost accounting.

## Memory and partition fallback
Falconer13205modules reached10.368GiB process RSS; its26delta files total5.644GiB.
Checkpointing bounds lost work, **not** total imported-prefix memory or disk.
It does not make163097modules fit12GiB. Prefix import and delta metadata grow.
A resource failure stops the global episode with all raw data retained.
Continuation may use separate directory contexts: Combinatorics/Ramsey,
Analysis/MutuallyUnbiased, Analysis/PlanarPacking, MathematicalPhysics/Transonic,
Algorithms/SubexponentialSAT, and remainder. Each starts a fresh certified
chain; any repeated dependencies/failed attempts must be charged. This fallback
is aggregate full coverage only if every source ID and its dependency checks
are actually covered, not an uninterrupted single-environment time.
If an individual closure still cannot fit, record the uncovered part; do not
increase the cap or label it mathematically false.

Initial freePVC13.202GB after source extraction/provider hardlinks.
Disk and snapshot growth are an actual limitation: no unowned files are
deleted and the former Falconer raw records are untouched. A write failure
is an incomplete capture, not a completed full-library cost.

## Metrics and comparison
Record every segment's native wall, user+systemCPU, maximumRSS, accepted source
IDs, dependency IDs, snapshot predecessor, memory failures and native verdicts.
Snapshot restore/export/startup/normal exit are in the subprocess clock.
P-core queue waits, source production, controller/Git work and qualification
are separate. Compare the completed aggregate kernel CPU hours with W's
construction scenarios207.894666–630.701677CPUh.
The requested older checker transfer8.322086–41.555143CPUh and updated
source32transfer10.826785–41.839086CPUh are labeled separately.
Agreement would mean consistency with those scenarios for this checking
protocol; these scenario intervals are not calibrated confidence intervals.
Do not state “extrapolation validated” from a prefix, selective directory,
trusted-import target replay, or missing-artifact coverage.

## Raw outputs and resumption
All raw sources, provider links, frozen checker/runner, commands, stdout/stderr,
ledger, deltas and state are on the existing PVC:
 /workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/whole-library-20261102

Recompute small tables offline:
 taskset -c8 python3 research/decoupled-check/whole-library-run.py reduce

Continue a nonterminal episode (do not duplicate a live owner):
 taskset -c8 python3 <raw>/whole-library-run.py queue --cohort all

A directory episode uses the fully qualified --cohort names or remainder.
Source production does not count as a kernel verdict. The initial2469artifact
availability and all-source frame are distinct from observed coverage in
whole-library-progress.md and whole-library-coverage.csv.


## First launch fault retained and repaired
The first bounded native invocation returned126 in0.012940s: copyfile did not
preserve the qualified executable's0755 mode. No kernel item was checked.
Its original command/stderr/result/terminal are retained. The owned copied
binary's mode was restored to the original0755; prepare now uses copy2.
The next attempt has a distinct key and waits behind currentP-core users.
The original record is not rewritten or called a rejected proof.

whole-library-continue.py waits for the submitted first retry's actual PID/birth
exit, publishes its real result, then executes finite lock-per-task continuation.
It never starts a second task while one is alive. If a global native episode
stops, fresh directory episodes are attempted sequentially and reported as a
different partitioned protocol, charging repeated dependency work.
The aggregate coverage table spans all six source groups even when checking
fails or prerequisites are missing. A full-source acceptance union alone must
also retain the traversed native dependency graph before a whole-library claim.
