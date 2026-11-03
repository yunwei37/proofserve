# Causal audit of shared replay-frontier persistence

The hypothesis is substantially supported for this prototype and the full
4,449-module BarrierData41 closure. Marking each quiescent checked frontier
with the existing Runtime.markPersistent primitive removes most of the extra
4-to-8P CPU cost. The previous result is not an intrinsic scalability limit
of the original Lean kernel. No kernel/runtime SDK source or on-disk proof
was modified. This is a known runtime technique and a prototype causal audit,
not a novel proof-checking algorithm.

## Protocol and object-state evidence

Machine phobos-vt, Intel(R) Core(TM) i9-14900K, P0-7 only for native measurements.
SDK4.34.1 commit5045d0056413266e57c625dcd7c365b10e377c52. One new executable,
flag0/1; all other settings/input files fixed. Workers1/2/4/8,3 plain repetitions
and1 stat each:32 complete native cells. No-M, blocking P0-7 lock, native1100s/
outer1740s after lock,14GiB sampled own-tree/charged guards inside16GiB lane.
Sampling is not a hard kernel RSS quota. Preparations/analysis use E cores.

Original compacted input CIs are already persistent. Newly reconstructed
replay bases and representative Nat.add/Nat.mul wrappers are different:
the base is ST before sharing and active MT after enqueue off. All18,990
marked bases per full run are persistent through enqueue. Whole primary CI
enumeration is disabled during timing; representative CI probes were separate.
The primitive is called before current workers exist, after joining prior tasks.
Matched task publication consumes the closure and completes mark_mt first;
remaining bookkeeping does not revisit this graph. This source argument is
bounded to this checker, not arbitrary extension tasks or a formal memory-safety
proof. See [layers/source](source-and-scope.md) and [protocol](plan.md).

## Three-repeat plain results

| Full closure8P | Off median [range] s | Marked median [range] s | Change |
|---|---:|---:|---:|
| wall |314.839 [312.804,315.742]|298.675 [297.015,298.878]|-5.134%|
| total CPU |722.297 [719.112,722.486]|620.240 [620.172,621.566]|-14.130%|
| original-call observer CPU |537.851 [534.191,538.144]|436.864 [436.808,436.886]|-18.776%|

Median paired4-to-8 growth falls66.527->23.147 CPU seconds; a median43.380s
is removed,65.21% of the off growth [61.80,71.76% across3 pairs].
Observer growth63.399->17.961s,71.67% removed [66.54,75.03%].
These are paired estimators; they need not equal differences of independently
aggregated group medians. All raw paired differences are committed.

All32 primary runs retain exactly the same4,449 accepted IDs and every
module's observed work vector:237,863 original checks and3,283,925,639 in-check
allocation-counter units. This is not whole-process malloc/instruction identity.
Observer thread CPU includes timing/heartbeat glue and system CPU; it excludes
fallback/import/planning and other work. Full tables: [plain](plain-results.md),
[paired interaction](three-repeat-interaction.md).

## Hardware discrimination, not converted stall seconds

At8P one complete stat per flag gives lock-load events-98.064%,load HITM
-94.416%,RFO HITM-72.278%,IPC1.69708->2.00627,cycles-14.420%.
Instructions increase1.172% and ordinary L3-load misses increase0.762%.
2/4P marked L3 misses also increase; the gain is not uniformly better ordinary
cache hit rate or less proof checking.

From4 to8P, off user cycles+8.431%,load HITM+47.616%,RFO HITM+50.308%;
marked user cycles+0.679%,load HITM-0.883%,RFO HITM+10.852%.
This supports the shared-RC/coherence mechanism. Marking also touches graph
data and changes lifetime/reclamation; it does not isolate exact RC stall
seconds or all residual overhead. HITM events are not disjoint counts to sum.

These are whole-command user-mode aggregates,56 actual counters100% running,
one stat observation per setting, not3-repeat confidence data. Stat clocks do
not enter plain medians. Stat-vs-plain observed wall differences-0.389..1.118%,
CPU-0.134..1.642%,including run/order variation. Marked4->8 system CPU also
rises6.121->10.052s and the cycle/refcycle ratio changes; CPU seconds cannot
all be called additional user-space stalls. See [complete stats](stat-results.md).

## Lifetime and memory cost

Primary marker-window CPU is about0.28s per whole closure versus0.006s off,
including clock reads. Persistent subgraphs are pruned and PHashMap structure
is shared; there is no whole-environment copy per frontier.

Two separate memory diagnostics align all4,449 module boundaries, including the last:
final Anonymous+6.98MiB,RSS+7.35MiB; wait4 peak3.261->3.268GiB off/on.
These are one pair of net resident observations, not exact retained-object
bytes. Prefix deltas are nonmonotone due to allocator/transient state.
Primary3-repeat wait4 peak medians are3.269/3.282GiB; all raw ranges/capture
methods are in CSV. All observed runs are far below the lane budget.

The4449 smaps reads per diagnostic add substantial system CPU(63..69s versus
about10s primary); these clocks are excluded from performance results.
The same-density Mathlib/primary-family projection is~7.4GiB before extra
dependencies/heaps, not a completed full-library fit test.1299 compiled OAI
modules are not the163,097-file source frame; the earlier~260GiB scenario is
biased and not a forecast or bound. Objects remain until process exit:
an unbounded resident whole-OAI service is not demonstrated.
See [memory](memory-results.md) and [estimate assumptions](memory-estimate-method.md).

## Original SDK and negative controls

The stock-already-leaked premise is incorrect at the importer boundary of this
SDK: LeanChecker uses finalizeImport false/false; kernel base ST, imported CIs
persistent. Later Replay StateRefT/intermediate RC was not header-probed.
Do not replace the premise with an unproved claim that all stock new objects
stay ST or have no atomic RC.

Actual unchanged SDK controls finish: default8 leaf65.423s;fresh1 final-imported
environment534.698s;fresh8 580.090s. Each averages about1 CPU core; source
Replay is sequential. Preserve the slower fresh8 observation without assigning
an isolated thread-count cause. These procedures lack our module/check/HB
ledger and differ in duplicate policy. No cross-scope stock speedup is claimed.
See [stock source/scopes](stock-results.md).

Two real negative controls replace the first root theorem proof by a loose
bound variable in memory. Both flags accept the same ordered4,448-module prefix
and reject the root with the identical original-kernel error for
OAI.SepticProfile.ExteriorCertificates.C41.fourth226. Native exit1 is expected,
not a resource failure. The13 earlier qualifications remain preserved.
See [actual full-prefix errors](bad-root-results.md). No logical axiom/rule or
kernel bypass was added; unsafe coordinator/FFI remains trusted implementation
glue. Finite controls do not prove universal implementation correctness.

## Interpretation and provenance

Keep the old3.33x leaf/1.88x Grid and mixed-P/E measurements as observations of
their unmarked prototype/version. They cannot define a native Lean scaling
limit or be reused as corrected gains. Exact-scope serial/parallel retiming
is needed before claiming corrected gains. Do not multiply the old gains by
this full-Barrier5.134% wall change or borrow another run's denominator.

All32 primary plus7 auxiliary natives and launchers actually retired; no
unexpected stop/resource failure. Primary controller596466/birth774557767 and
all7 auxiliary identities are retired. Recomputing after all auxiliary files
exist leaves all10 primary CSV tables byte-identical: observers/negative tests
do not contaminate the3-repeat denominators. All raw/source/failed/partial
records remain on PVC; no new raw deletion. Disk~71%, below85%.

Raw point:
 /workspaces/.agent-state/gpu-smt-captures/parallel-stream-persistence-20261103
Frozen primary source5f2e64f; core/runtime adapter5fd4814; qualified step052.
Auxiliary source7b92e72; subsequent changes only analysis/documentation.
Reviews are 自审. This finite causal task is collected; the research goal
and paper acceptance are not marked complete.
