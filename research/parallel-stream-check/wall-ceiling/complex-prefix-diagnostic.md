# The115s fallback was a checker restriction, not a workload serial limit
自审,2026-11-03. Raw wall-hybrid-20261103; same executable flags0/1,
default persistence in both. This report covers the complete diagnostic pair;
plain3-repeat end-to-end result still pending.

## Cause and coverage
makePlan returned none for a whole module if any safe ConstantInfo was an
inductive, constructor, recursor or quotient, or ordinary graph could not be
planned. Full original replay then serialized unrelated ordinary declarations.
All1231 old fallback module names match the pre-reboot capture exactly.
All1231 remainders are now plannable: no ordinary-cycle remainder in this closure.
Of183645 incoming constants in them,168713 ordinary constants move to parallel
checking.14932 remain in original replay:1636 ordinary prerequisites,
3819 inductive CIs,5542 constructors,3931 recursors,4 quotient CIs.
These are CI counts, not numbers of inductive declarations or time weights.
Total observed parallel checks237863+168713=406576 matches exactly.

Matched diagnostic serial phase94.4787→1.7924s (98.10% reduction). Old115s is
a different pre-reboot timing, not substituted as a denominator.
Mathlib contributes549 fallback modules/65.340s of old phase, Init10.513s,
Lean8.064s, Std5.166s; full source-family CSV retained.
A mutual inductive group is one original-kernel construction unit, but distinct
groups need not all be serial. We have not measured a group-level DAG inside
the retained1.7924s. It is a conservative serial prefix, not1.7924s proved
intrinsically serial. Taking all of it away gives an explicit optimistic bound.

## Own-run wall reconciliation
Baseline:271.1808s=read4.1661+context25.5398+plan8.8974+serial94.4787+
batches112.9509+duplicates0.0285+unassigned25.1193.
Split:211.6749s=read0.3116+context25.6713+plan13.1729+serial1.7924+
batches141.0240+duplicates0.0287+unassigned29.6739.
Each row sums within floating serialization precision. Interpolation across
these runs or into the old299s denominator is not performed.
Split diagnosticCPU560.545s versus551.571s baseline: extra planning/observing
more parallel units is not free. Read cache differences also remain.
406576 observed checks/3968705445 units versus237863/3283925639 are DIFFERENT
observer coverage; the increase is not extra whole-workload allocation cost.
Both have identical ordered4449 accepts; mathematical declarations unchanged.

Inside split batches: kernel-active interval union133.9094s, mark0.2437s,
launch-with-no-check5.0490s, join-with-no-check0.7896s, validation0.2846s,
commitChecked0.2971s, observer/tail0.4506s. Sum141.0240s.
The commit is0.14% of overall wall: parallelizing it is not the promising target.
Context+planning38.844s is a much larger serial implementation opportunity.

## Structural model after removing the large avoidable class
Per-wave maximum CPU sum95.7757s; exact local-module DAG longest paths67.9515s.
Keep70.6509s outside batches: infinite-core barrier model166.4266s.
Even optimistically zeroing the whole unmeasured remaining prefix gives164.6342s,
so prefix uncertainty is only1.7924s. Under FIXED measured service costs,
module order, barriers and metadata/observer work, extra-core headroom is at
most1.2857x versus this211.6749s diagnostic. This supersedes the older1.15x
conditional scenario that retained the avoidable whole-module fallback.

Removing level barriers while retaining actual local DAG edges instead yields
138.6024s (136.8100s with zero prefix), up to1.5472x in the optimistic model.
This is not measured performance: it requires a different scheduler/commit
protocol and assumes unchanged node costs. Neither model is a universal DAG,
native-plain, hardware-independent, or GPU-route abandonment theorem.
Do not re-scale these diagnostic spans by a plain-run denominator.

29555 waves:4556 width1,13232 width2–8,9110 width9–32,2441 width33–128,
216 wider. Narrow1–8 consume51.436s of start-through-commit windows;9–32
consume44.357s;>32 consume44.780s. In particular a6-job Polynomial.Derivative
wave takes10.142s, almost all one declaration
Polynomial.iterate_derivative_derivative_mul_X (10.137CPU-s/10.166 total).
It cannot be shortened by adding declaration workers alone.
Conversely the3938-job Jet41 wave takes11.807s for81.600CPU-s; the1099-job
BarrierData41 wave7.593s for52.782CPU-s, using about7 cores effectively.
Thus the limit combines narrow/heavy waves and coordinator work, rather than
uniformly ineffective kernels. Width and dominant-job tables retain details.

No original mathematical kernel edited. Original replay validates constructors/
recursors; no temporary axiom skeleton. Existing reader/checked-token adapter TCB
and unsafe/partial exclusions remain; no stronger universal security claim.
