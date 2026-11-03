# Memory estimate: distinguish the closure, Mathlib, and the OAI source frame
Untimed metadata snapshot2026-11-03T09:30:43Z: the actually checked4,449
closure resolves13,307 artifact parts totaling3,194,226,992 logical bytes
(2.975GiB). First8P sampled RSS is3.248GiB marked/3.254GiB off. This is
not yet a retained-object measurement; two aligned smaps diagnostics remain.

Available compiled Mathlib8530 modules occupy5,604,826,360 logical bytes.
Init/Std/Lean add1,664,032,688bytes. A simple same-density projection from the
observed closure gives about7.4GiB RSS for these primary families, before
other dependencies and any larger per-check working heap. This is an estimate,
not a guarantee or completed full-Mathlib test. It does not establish that
all future marked frontiers can live forever inside14GiB.

The currently resolved OAI compiled subset is only1299 modules/2,211,613,376
logical bytes. Earlier complete lexical source frame at pin4eaee875 has
163,097 files/1,785,499,363 source bytes (see [the complete source census](../../chunked-kernel-check/static-summary.json)). It must not be called fully
compiled. Extending this selected compiled subset's mean artifact density to
that source-file count would suggest roughly260GiB, not a16GiB resident
library. This is deliberately a conditional, selection-biased scenario, not
a confidence interval, lower bound, or proven full artifact size. Source files
are a module-count proxy, and compiled target selection is very nonuniform.

markPersistent intentionally prevents deallocation until process exit; old
persistent-map versions can remain even when peak RSS appears unchanged.
The stage2 PHashMap shares structure, so retaining a frontier is not copying
the entire environment each time. Neither fact proves zero heap cost.
The memory pair records Anonymous/Pss/Rss after every matched module boundary,
including the actual final heavy modules. Net RSS differences include allocator/
resident-page effects and must not be described as exact retained-object bytes.
Finite process-per-closure work can release mappings at exit; an unbounded
resident whole-OAI service is not established by this ablation.


Actual aligned pair in memory-results.md: endpoint Anonymous+6.98MiB,RSS
+7.35MiB; wait4 peak3.261/3.268GiB off/on. Across-frontier net differences
include allocator/transient state and are not exact retained-object accounting.
Do not promote the selected OAI subset's~260GiB scenario into a whole-library
forecast. The primary marker-window cost is~0.28s; finite closure fits, unbounded
service/full-source-library fit remains unproven.
