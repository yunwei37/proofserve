# Step037: fresh ordinary4→8CPU expansion is inside original kernel calls
EXPERIMENT_GATE: P8ordinary-before completes4,449reference accepted IDs and
identical237,863checks/3,283,925,639allocation units. Wall315.390s,
CPU722.326s, measured ordinary CkernelCPU537.622s.
Relative to the two fresh P4ordinary controls, extra totalCPU is63.316–70.167s;
extra original-kernelCPU62.776–65.894s, accounting for93.91–99.15%of the
extra CPU. These are separate same-work observations/brackets, not replicated
confidence intervals or rescaled historical clocks. P8after/stat/record still
needed for final comparison.

Per-namespace actual ordinary costs/checks/allocations are retained. Against
P4after, OAIordinary kernelCPU172.816→212.989s(+40.173s);
Mathlib226.506→241.600s(+15.094s);Init49.117→57.891s(+8.774s).
Counts/allocations match per namespace as well as globally. OAI16andMathlib2059
are nonzero ordinary-profile modules, not all imported namespace modules or
a universal computation-versus-math classification. Fallbacks are outside
these ordinary-kernel figures.

WRITE_GATE: this independently confirms the location of CPUexpansion on fresh
plain runs while keeping perf/native clocks separate. Namespace location does
not identify operations: the forthcoming call stacks must discriminateRC,
lookup,allocation and normalization. No RCcausality assigned from this table.

REVIEW_GATE 自审: three actual complete same-native plain outputs, per-namespace
work and exact source sums verified. Earlier e77301895.96%is not borrowed as
a new denominator. Data genuinely narrow extraCPUto original-kernel calls;
they do not prove an inherent serial fraction, numerical-LPbottleneck or
source-tactic behavior. Fullmatrix5/16returned; continue blocking collection.
