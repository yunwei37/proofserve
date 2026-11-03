# Avoidable whole-module fallback experiment
Source: matched SDK Lean/Replay.lean, original kernel unchanged.

makePlan previously rejected the entire map at its first nonordinary ConstantInfo,
or when the ordinary dependency graph has a cycle. One inductive/constructor/
recursor therefore serialized unrelated ordinary declarations too.
The partition experiment is explicitly off by default (PARALLEL_SPLIT_COMPLEX=1).
Default persistence remains on and is not the intervention.

Seed all safe nonordinary constants; close transitively over used local constants.
This contains every local inductive, its mutual companions, constructors and
recursors. Send the closed prefix through original Kernel.Environment.replay,
which constructs inductive declarations and checks postponed constructor/recursor
metadata. Then plan/check the remaining ordinary declarations with the existing
original-kernel token path. If remainder cannot be planned, original replay handles
it. No expected theorem/constructor is silently accepted by the partitioner.

Why conservative: ordinary prerequisites and all nonordinary groups are serialized
in this implementation. They are not all intrinsically serial; only an individual
mutual inductive group must be checked as the original declaration unit.
Independent inductive groups might admit future parallel work, not implemented.
Counts and prefix CPU/wall are measured; class counts are not time weights.
The experiment cannot label all prefix time a fundamental DAG lower bound.

Qualification uses a tiny inductive+ordinary module, good and corrupted theorem,
both flags at1/8 workers. Full paired8P arm0/1,3 repeats, same executable,
same ordered4449 accepted IDs. Own CPU/wall denominators and C observer costs.
Source frozen on PVC before build; previous matrix source unaffected.
Prepared source is not a completed experiment. No novelty or kernel change.

Experimental HybridCore.lean is copied to the PVC build tree as ParallelCore.lean; canonical ParallelCore remains the qualified default-persistent checker. One diagnostic pair and three separate no-profile/no-trace pairs are planned; second plain repeat reverses arm order. The wait-only v1 continuation was retired before any native/build, leaving the active Grid run untouched. Native runs continue one at a time.
