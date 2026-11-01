# BarrierData41: complete first stream curve

Frozen v14 /8c62fc3. Raw: parallel-stream-check-v14/barrier-stream-r1.
One repetition, not a three-repeat median. Same one-process independently
checked4,448-module prefix for every leaf variant. All4,449 modules accepted;
no local context fallback. Each of the3,425 source leaf constants is new and
matches the same-process serial result structurally under all ordinary variants.
This is serial-leaf differential evidence; a separate entire-closure serial
reference for this4,449-module cohort has not yet been run.

| Leaf method | Wall s | Process CPU s | CPU / wall | Serial / wall |
|---|---:|---:|---:|---:|
| Original serial replay |53.960|53.934|1.000|1.000|
| Declaration1 |56.443|56.414|0.999|0.956|
| Declaration2 |29.829|59.529|1.996|1.809|
| Declaration4 |16.468|65.421|3.973|3.277|
| Declaration8 |10.186|80.155|7.869|5.297|

The eight-worker mean CPU utilization is now7.87cores, unlike the old ungated
Grid trial's four-core plateau. Original accepted typed constants remain
identical. Total CPU seconds increase48.62% versus this run's serial leaf;
this is not an instruction-count or clock-cycle attribution.

The whole finite process checks the prefix and all five variants:468.112s wall,
867.563s cgroup CPU,3,196.184MiB wait4peak RSS. Its sampled tree peak is
3,197.973MiB. These are whole-process metrics, not per-variant memory or a
complete single-production-configuration cost. Native group/controller retired;
no memory threshold, OOM event or native failure.

The original W leaf source-compiler observation is63.0296s, a distinct operation
including imports/elaboration/outputs. No complete matching source-build cost
for this4,449-module dependency closure has been measured here, and no full
construction/parallel-stream ratio is filled from the leaf result.
