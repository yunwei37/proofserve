# Pinned source explains a synchronous boundary; no source patch measured

Authority: installed Lean4.34.1 SDK under
/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux/src/lean.
This is read-only source inspection on E cores, no native experiment.

1. Lean/Elab/Tactic/Decide.lean104–118: doKernel builds a decision proof, then
   creates its auxiliary lemma with Elab.async explicitly false at116.
   Its comments explain type-indexed auxiliary-lemma caching and reuse of the
   already checked theorem afterward. Therefore a +kernel invocation has an
   intentional synchronous original-kernel check even when other elaboration
   work is asynchronous.
2. Lean/AddDecl.lean169–179: the generic async declaration branch maps its
   check action from env.checked at172. That is an explicit dependency on the
   checked environment, not evidence that arbitrary ready declarations are
   forked into independent kernel environments. It does not imply every
   elaboration or kernel path is sequential.
3. LeanChecker.lean33and108: upstream launches one IO task per matched
   compiled module; inside each module it uses the official replay API.
   Module-parallel checking is already present and must remain a whole-library
   baseline. Our measured improvement is inside a single target module.

The completed Barrier DAG/curve supplies separate empirical evidence that a
large set of its closed original constants can be checked in independent
frontiers with exact final typed constants. Source inspection identifies an
intentional synchronous boundary consistent with low utilization; it does
**not** quantify its share of W's compiler clocks, isolate every bottleneck,
or establish source-build acceleration.

Simply removing the async=false option is not this prototype. A tactic must
observe a failed decision when deciding whether to backtrack or try another
alternative. Delaying that failure can change source-control-flow behavior.
We have not measured such a source patch and make no parity/performance claim
for it. Compiled replay instead starts after metavariables, tactic choices and
proof terms have already been fixed; invalid original terms still reject.
This distinction is why the single-module recheck result must stay separate
from accelerating proof search or a live Lean verification service.

No upstream source was changed, no new proof kernel implemented, and no
competitor installed. Parallel checking and asynchronous proofs are established
prior work; the new evidence is the workload-specific cost and scaling curve.
