# Parallel original-kernel streaming checks

Lean 4.34.1 research prototype for the two-cost-regime characterization. It reads
compiled artifacts in one process, checks independent declarations in dependency
frontiers, and optionally partitions ten expensive Fin31 proof computations.
The mathematical checker is the original Lean C++ kernel.

| Completed evidence | Serial wall s | Parallel wall s | Scope |
|---|---:|---:|---|
| Mathlib.Data.Nat.Basic |68.605|45.050 (8 workers)|Complete1,330-module closure;3 repeats,1.523x|
| BarrierData41 |53.960|10.186 (8 workers)|Incremental leaf;1 repeat,5.297x|
| Grid full closure |557.568|296.293 (4 workers)|Complete3,793-module closure; 1 interrupted pair,1.882x|
| Grid leaf |265.010|65.856 (8 workers)|Incremental leaf; 1 repeat,4.024x|
| EnvelopePsiB |61.913|17.539 declaration8;13.299 chunk8|Incremental leaf;1 repeat,4.655x;1.319x extra from chunks|

Mathlib total CPU seconds increase36.3%; Barrier48.6%; Envelope chunk8adds66.2%
versus its serial leaf, or5.2% versus declaration8. These are CPU seconds, not
instruction-count attributions. Mathematical and leaf scopes are not pooled.
The fresh [repaired Grid](grid-repaired-results.md) actually uses7.95mean cores.
Its8-worker CPU seconds increase97.8%; the historical requested8/achieved4point
is retained separately, never pooled with the repaired curve.

## Results and cost boundaries

- [Repaired Mathlib matrix](v14-math-results.md), all18cells and1,330accepted IDs
  equal the serial reference. [Construction/serial/parallel table](v14-cost-staircase.csv):
  source compiler work sum622.379s ->serial stream68.605s ->parallel845.050s.
  Construction is a sum of per-module compiler invocations, not parallel Lake wall.
- [Barrier](barrier-stream-results.md):4,449modules independently checked once,
  then five leaf variants on the same4,448-module prefix.
- [Envelope](envelope-stream-results.md):10,752modules, then nine leaf variants.
  Complete process1665.530s is prefix plus *all nine*, not one configuration.
- [Repaired Grid](grid-repaired-results.md), [historical Grid](grid-stream-results.md), [worker-start correction](worker-start.md),
  and [compute tables](compute-summary.csv). Variance is unknown for one-repeat
  computational curves. The first complete [Barrier pair](full-barrier-results.md) now has4,449equal
  accepted IDs. Other complete computational cost pairs and repetitions remain.
- [Selection and generation scope](selection-scope.md). Certificate generation is
  excluded from checking curves; reading/support/child checks/merges are included.
  The optional stock-imported diagnostic is prepared/short-control-qualified but
  not used to replace completed independent-prefix measurements.

The mathematical cohort does not enable chunk rewriting. Computational prefix
policy is four workers; leaf variants request1/2/4/8. Do not call the whole
computational process a uniform eight-worker run or a production service gain.

## How checking works

ParallelCore.lean plans ordinary acyclic declarations before committing anything.
Workers call original Kernel.Environment.addDeclCore 0 0 on an identical immutable
frontier. A short mutex only lends job indices. Started-worker promises prevent
the Lean standard pool from hiding the private backlog. All tasks join before
errors propagate; typed payloads, index coverage and frontier identity are checked.

checked_commit.c inserts only those checked tokens, in source-index order within
an ordinary frontier. Global order is topological; certificate support/children
precede their checked parent merges. Complex inductive/constructor/recursor/
quotient modules or cyclic plans use upstream replay. Context conflicts retain
O's isolated module-local path. Differing compatible duplicate proofs are checked
under fresh names; local cycles never use a prior sibling's binding.

The optional generator extracts source-supported finite universal predicates,
writes untrusted child terms for k1/2/4/8, and proves merge support. Full incoming
CI equality selects a frozen known target. The consumer rechecks support,
150children and40merges across the four completed Envelope variants. Root axiom
closure is[propext], no sorry. Ordinary proofs remain unchanged; ten certified
proof bodies intentionally change while preserving original types/names/levels.

**Implementation trust:** the coordinator, C ABI adapter and eligibility metadata
are trusted glue. Keeping the original mathematical kernel is not a claim of an
unchanged implementation TCB or a formal theorem of universal input equivalence.
See [correctness obligations](correctness.md). This does not validate source
elaboration or every serialized environment extension. Unsafe/partial exclusions
follow upstream policy. Original artifact axioms retain the original Lean policy;
only generated certificate roots are qualified as propext-only/no-sorry. Binary-format hardening and byte-identical diagnostics
are outside this experiment. No external numerical solver is trusted.

## Reproduction and retained attempts

[Protocol](protocol.md), build.py, run.py and curve.py operate from frozen copies
under the PVC; paths and exact commands are in each raw command/launch record.
All timings use the shared blocking P0–7flock, no-M, one bounded native task.
Native1680s/outer1740s, own sampled RSS stop14GiB plus charged cgroup memory limit,
inside the16GiB lane. A sampling stop is not a hard RSS quota: Envelope wait4peak
14.0187GiB exceeded the14GiB threshold between1s observations while samples
peaked13.9712GiB. Native/groups/controllers retired after each completed point.

Primary repaired raw:
 /workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14
Prepared untrusted payload:
 /workspaces/.agent-state/gpu-smt-captures/parallel-stream-assets/all-envelope

Twenty native positive/fault controls and actual-source certificate controls
qualify the core; corrupt original/chunk proofs are rejected. These finite tests
are not a general correctness proof. v4's18-cell valid-input table is historical:
it accepted an indirect duplicate cycle subsequently fixed. v10's cold Envelope
resource failure is retained, not relabeled a rejection or erased by v14success.
That prior point had different source and eight-worker prefix; no isolated
causal memory-fix attribution follows.

Full.py and [remaining full-cost protocol](full-closure-protocol.md) prepare
single-configuration costs and additional full-cohort comparisons. They are
not measured results until an actual bounded native cell completes.
Raw perf/captures/build outputs remain on PVC, never in Git. Only M-owned
research paths are edited; the O reader was copied read-only. No novelty is
claimed for proof parallelism, reflection, certificate splitting or shared imports.

[Current complete-closure cost staircase](cost-staircase-current.csv) keeps unknown
source-construction cells explicit. The complete Barrier process pair costs
474.851->304.862s; it must not be replaced by the5.297x incremental leaf result.

## Interpreting the prototype

Declaration waves address many independent short computations; finite-goal
partitioning addresses a small frontier of expensive parent computations.
Envelope's extra chunk gain is measured against *already parallel* declaration
checking. Its slower k2case prevents a blanket "more chunks is faster" conclusion.

The wall reductions consume more aggregate CPU seconds. Grid's eight-worker
leaf nearly doubles CPU seconds, so these latency curves do not establish
higher throughput for a saturated multi-module verification queue. Hardware
causes of extra CPU time require a separate matched profile.

Incremental checking describes a resident verified prefix. Full closure pairs
also include rebuilding that checked prefix from artifacts. The large difference
between Barrier's leaf and complete-closure gains makes this amortization
boundary observable. No persistent service or workload-amortization claim is
filled with an unmeasured projection.

The ten certificate targets use one source-supported finite family; earlier
weighted large-goal coverage is sensitive to one file and missing observations.
The contribution under discussion is characterization plus a measured system
prototype, not firstness of proof parallelism, futures, reflection or splitting.

The complete [Grid pair](full-grid-results.md) now costs557.568->296.293s,
1.882x at uniform4workers, with3,793equal accepted IDs. Its retained serial arm
and resumed parallel arm have a disclosed controller-repair gap. The full
source-work staircase is3878.707->557.568->296.293s. The next missing complete
cohort reference is Envelope; do not fill it from the nine-variant process time.

## Beyond-eight heterogeneous footprint
The new [full Barrier curve](extended-results/heterogeneous-scaling.md)
8P /8P+4E /8P+8E /8P+16E completes with identical4,449accepted IDs,
but wall increases284.720->319.705s and CPU668.786->1172.473s.
One fixed-order repetition; allowed masks, migration and phase limitations are
explicit. This is not additional scaling or cluster evidence. The parallel
heartbeat/artifact experiment is separate and pending.
