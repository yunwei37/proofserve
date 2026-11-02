# Stable allocations and exact bytes during real parallel streaming
The actual foreground v16process reconstructed the4,448-module dependency
prefix, then repeated the entire BarrierData41leaf at1/4/8/16workers,3repeats
each, on that independently verified resident prefix. The final completed
closure contains4,449modules. No-M; original Lean4.34.1mathematical kernel.
**100/100sampled computation helpers have zero allocation-heartbeat range;
all1,200target checks accept. P95and maximum per-target range are both0%.**
All12serialized .oleanoutputs are byte-identical to one another **and to the
original9,160,440-byte input .olean**. There are no server/private companion
parts for this particular input; no missing companion is counted as equal.

## What was actually checked
- Full prefix is reconstructed from compiled artifacts and original-kernel checks,
  not silently stock-imported in place of checking. Final closure:4,449accepted
  modules,425,463input entries,3,595upstream unsafe/partial exclusions and zero
  module-local context fallbacks.
- Each leaf trial checks all3,425ordinary declarations in6dependency waves.
  The100observed helpers are evenly spaced in the sorted original
  of_decide_eq_truehelper list, including endpoints. They overlap the prior
  Barrier census; they are not100additional independent workload families.
- Independent original-kernel calls run simultaneously on equal immutable
  wave frontiers, with ordered checked-token commit. Each trial's entire
  checked payload is compared structurally to the first1workertrial.
- Allocation deltas and CLOCK_THREAD_CPUTIME_IDare read on each executing
  worker around a forced noinline original-kernel IOcall. Observer logs only
  these100targets. Native kernel poll-count remains unobserved.
- saveModuleDataPartssubstitutes all3,425checked constant infos into the original
  module metadata and serializes a real .olean. It does not merely copy the
  input bytes. Full12file equality is checked by actual bytes. Serialized
  extension metadata retains the input policy and is not independently validated.
  The original mathematical kernel is unchanged; coordinator/CABI/token glue is
  still trusted implementation code. Byte identity does not prove a universal
  malformed-input or whole-elaborator equivalence theorem.

Raw: /workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v16 .
The100targets x12counts are condensed in
[parallel-target-heartbeats.csv](parallel-target-heartbeats.csv); full1,200rows
and native stdout remain on PVC. All12repeat/worker combinations and target
identities were also matched independently from raw curve_begin/unit_checkevents.
No partial JSON line from a live read was counted as a failure; completed raw
stdout parses fully. Process and cgroup retired normally, no memory event.
Native wall556.858s and CPU1,651.508s include the prefix, all12trials and all
serialization work, not one configuration's end-to-end cost. Peak RSS3,425.2MiB.

The allowed CPU footprint is0-15(8P+8E)for the whole determinism process.
The prefix uses8workerfrontiers, leaf caps1/4/8/16. Workers may migrate and the
standard task pool may assign different OSthreads across the6waves. For example,
1workertrials have2distinct observed TIDs across waves, and16workertrials17;
these are unions over time, not simultaneous concurrency or claimed core counts.
Leaf process CPU/wall confirms about1.00/3.98/7.88/15.40mean active cores.

## Observer-enabled resident-leaf costs
Median [minimum,maximum], seconds, across3actual repeats; the middle repeat
uses reversed worker-count order. Preparation/reading/audit inside the leaf
curve window is included; .oleanserialization follows that timer. These are
observer-enabled leaf diagnostics, not replacement unprofiled full-process
throughput results.

| Per-wave workers | Leaf wall s | Leaf CPU s | Sum CPU inside100sampled original-kernel calls |
|---:|---:|---:|---:|
|1|50.358[50.326,50.618]|50.334[50.307,50.591]|3.575[3.566,3.604]|
|4|16.003[15.642,16.029]|63.646[62.096,63.741]|4.472[4.393,4.592]|
|8|10.321[10.301,10.386]|81.333[81.032,81.819]|5.830[5.688,5.876]|
|16|9.033[8.971,9.048]|139.099[136.474,140.816]|9.941[9.552,10.099]|

Leaf latency1->16improves5.575x, using substantially more aggregate CPU.
Even inside the original100kernel-call windows, total CPU rises about2.78x
while allocation counts remain fixed. This is evidence that stable allocation
work does not imply fixed CPU cost; it cannot be attributed solely to external
reading/serialization. Heterogeneous core placement, cache/refcount contention
and other runtime effects have not been isolated causally by these timings.
The two-context result must be kept intact: resident independent leaf checking
can exploit parallelism, while the fresh complete-closure heterogeneous curve
gets slower beyond8P. No cluster experiment or production-service gain follows.

## Determinism boundary
The measured prepared computational checks can execute in parallel with stable
per-target allocation counts, verdicts and serialized mathematical payloads.
No work-normalization scheme was needed for this observed sample. This does
not establish cost-free observability or an all-input/observer/machine theorem:
logging/wrappers have costs, all trials use finite external process limits and
a generous/unlimited native declaration-check budget. Allocation-count P95=0%
does not guarantee any future near-threshold stock maxHeartbeats verdict.
The prior mathematical source-elaboration variation is a different stage;
prepared mathematical theorem rechecking was stable too. Subject matter alone
does not establish the determinism boundary.

## Reproduction
Build from build_extended.pyinto a fresh PVCpoint with frozen source copies.
extended.pyqualificationtests the adapter; scalinganddeterminismare separate
bounded foreground tasks under the shared pcore.lock. Actual launch commands,
pid/birth, native argv, allowed CPU masks, memory and terminals are retained at
the raw point. The captured v16driver is frozen. Post-run source fixes preserve
the old0-7default when an explicit legacy environment lacks a new affinity
option; all actual v16calls supplied explicit options and are unaffected.
A complete artifact byte mismatch is now recorded as a comparison outcome,
while missing artifacts remain incomplete. No running frozen file was hot-edited.
Five Python contract regressions pass; these are not extra scientific observations.
