# Remaining serial work in the first repaired Mathlib repetition

Data-only analysis of v14 math-parallel8-0, not a new timed/native task.
858 modules take declaration frontiers; 472 use upstream complex-or-cycle
fallback. These are module-level categories. They do not establish that every
declaration in a fallback module itself needs serial execution.

Observed aggregate frontier path wall: 16.180435 s. Aggregate upstream
complex/cycle path wall: 22.933520 s, out of 45.291915 s total process wall
(the exact total remains in the raw/cell CSV; rounded here). Context scanning,
graph planning outside a path, reading, startup and cleanup are additional.
Do not rescale these phases to O's earlier 65.7 s observation or the source
construction work sum.

The largest upstream paths are Init.Data.BitVec.Bitblast (2.596 s),
Std.Data.DTreeMap.Internal.Model (1.510 s) and Operations (1.254 s).
The CSV ranks all 472 entries. The combined category does not distinguish
genuine cycles from a single inductive or generated recursor in an otherwise
ordinary module. Full repeated measurements are still pending.

Pinned SDK Lean/Replay.lean shows why splitting this path is not a trivial
unchecked optimization: mutual inductives gather every member in info.all and
all constructors; generated constructors and recursors are postponed and checked
against the kernel-generated values. A mixed-declaration extension would have to
preserve those group obligations, not treat their CIs as independent ordinary
definitions. It is not part of frozen v14 and no speedup is imputed for it.
