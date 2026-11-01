# Envelope: both forms of parallel checking in one stream

Frozen v14 /8c62fc3; one repetition. Raw envelope-stream-r1. A single process
independently checks10,751dependency modules, then compares all nine leaf variants
against the identical checked prefix. Prefix policy4workers; requested leaf
workers1/2/4/8. This is not uniform8workers throughout the entire closure.

| Leaf method | Wall s | Total CPU s | CPU / wall | Serial / wall |
|---|---:|---:|---:|---:|
| serial |61.912856|61.888676|1.000|1.000|
| parallel1 |61.470238|61.443676|1.000|1.007|
| parallel2 |33.855939|67.203696|1.985|1.829|
| parallel4 |22.514725|76.541515|3.400|2.750|
| parallel8 |17.538824|97.815207|5.577|3.530|
| chunk1 |61.852441|61.815274|0.999|1.001|
| chunk2 |37.919688|72.995404|1.925|1.633|
| chunk4 |20.767752|80.182180|3.861|2.981|
| chunk8 |13.299242|102.887564|7.736|4.655|

Declaration8=17.539s. Chunk8=13.299s:1.319x additional speedup,24.17% less wall,
with5.19% additional CPU seconds. Against serial61.913s, chunk8=4.655x, with
66.25% more CPU seconds. Chunk2is slower than declaration2; more splitting is
not automatically useful. These are one-run observations, not repeat medians.

All110leaf source types/names/levels match serial. Ordinary paths retain original
proofs; chunk paths deliberately replace ten matching source proof bodies.
All source-selected CIs match the pinned eligibility reference. Across k1/2/4/8:
10/20/40/80children,40parent merges total; every support/child/merge passes
the original C++ kernel. Root axiom closure is[propext], with no sorry.
The full accepted module count is10,752,785,706input entries,4,444upstream
unsafe/partial exclusions and no module-local context fallback. A separate
whole-closure serial reference is not yet measured; leaf differential equality
must not be relabeled that missing full-cohort comparison.

## Complete process and resource scope

The process includes prefix verification and all nine leaf configurations:
1,665.530s wall,2,772.428s cgroup CPU. Sum of leaf trial walls331.132s;
the residual1,334.398s includes prefix, reading/audit, startup and cleanup.
It is not the time of one selected full configuration. The14s remaining before
the1,680s native limit is not a reason to silently extend that limit.

wait4peak RSS14,355.125MiB=14.0187GiB. Independent1s tree samples peak
13.9712GiB; no sample exceeded the14GiB sampling stop, but wait4shows an
instantaneous peak above14GiB. This is a sampling guard, not a hard RSS quota.
The native peak remains inside the16GiB lane; small controller/analysis overhead
uses the reserved headroom. Charged cgroup memory is a different metric.
No stop reason/OOM event. All native processes, controller and cgroup retired.

Prior v10failed at its resource stop before the leaf. It used different source
and an8-worker prefix; this repaired run uses a4-worker prefix. The prior failure
is preserved. This one success is not an isolated causal proof that a particular
patch fixed memory or that the close-to-budget configuration is robust.

## Ancestor omitted by the original leaf panel

WaveExpData is an additional128-entry computational dependency. Its measured
kernel-route wall is44.990s under the four-worker prefix policy. It is not part
of the ten profiled Envelope leaf goals. The source scan finds45lexical decide
sites and24direct Fin31calculator lemmas, without per-goal cost qualification.
Do not impute their cost or count into the earlier ten-target coverage ratio.

Preparation/generation is excluded from these checking curves. Payload reading,
support replay, child checking, merges and ordinary leaf proofs are included.
The mathematical kernel is unchanged; coordinator/C-commit and eligibility
metadata remain explicit implementation trust. Not a production-service gain.
See selection-scope.md, correctness.md and v14-math-results.md.
