# Declaration-level original-kernel parallel replay

## Decision and evidence
UMoments9, BarrierData41 and Grid all have subsecond decide helpers in the completed hot-module native point. Do not partition these individual goals. Barrier's1,099-node fourth dependency frontier accounts for44.646s/47.138s measured declaration CPU. Sum of per-frontier maxima is0.200s, a compute-only infinite-worker bound, not a speedup claim.

## Prototype
ParallelReplay.lean directly reads the exact original .olean parts, imports only original dependencies, and builds an actual ConstantInfo dependency graph. It rejects unsafe/partial/inductive/constructor/recursor/quotient/cyclic forms rather than pretending to support them. Barrier has none of those forms.

One fresh process per dependency wave imports the previous wave's checked standard modules. A short Mutex protects only a job index; original kernel replay and export run outside it. Each worker checks singleton declarations through the official Kernel.Environment.replay, in a private persistent environment over the common checked frontier. Original Name objects and array indices are retained.

Only checked environments are exported with stock writeModule, with IR export disabled. Subsequent waves commit their artifacts by ordinary Lean import in worker-index order. Within an independent wave physical insertion order can differ from the input array; no source-elaboration diagnostic-order equivalence is claimed. The final audit walks the original array order and demands exact typed ConstantInfo identity and complete name/order equality. No temporary axioms, unchecked environment union, skipped type checking, new proof term, sorry, or replacement kernel is used.

The trust boundary matches ordinary checked-module export/import, not a new independently verified artifact parser. Imported original dependencies remain trusted as in stock single-module leanchecker; this is not independently checking all Mathlib dependencies.

## Baselines and costs
k=0 is direct official serial replay, with the same input reader/import/audit. k=1/2/4/8 use the wave pipeline. Every whole-cell clock includes graph construction, fresh process startup, repeated reading/importing, wave barriers, checking, standard export/reimport, and final audit. Native user+system CPU and peak child RSS are separate. Comparing k8 only to the deliberately more expensive wave-k1 is insufficient: report direct stock too.

Three repeats of each setting;15 cells. One finite P0–7 capture under the shared pcore.lock,1680s active budget/1740s external cap,<=14GiB own child cgroup/RSS guard within M16GiB; no-M; no second M native process. Insufficient remaining time stops with explicit partial receipts, not reduced cell caps or zero imputation. Do not submit before the current declaration distribution capture retires. Compilation/preparation on E8–15 is not timing evidence.

## Qualification before any curve
A small ordinary-definition/theorem fixture must pass direct stock and wave paths with exact typed constants. Three malformed proof expressions (loose bvar, unknown constant, sort) must be rejected by both paths. Dependency-frontier validation must reject an uncommitted dependency. No fixture success transfers acceptance to Barrier: every actual cell has its own full typed audit.
