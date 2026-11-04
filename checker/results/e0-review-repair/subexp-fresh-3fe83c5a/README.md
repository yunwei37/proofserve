# Fresh retained-frame replay after the e0 review repair

Source: 3fe83c5a80ea29f9ea5911d144806ffe70836d18, unchanged build10.
Lean 4.34.1; two workers; E cores 10–23; a new empty checkpoint directory;
3,977 retained roots. This is a correctness preview, not the final
system evaluation, a whole-corpus run, or an independent execution review.

The actual native process returned 0 and produced complete, with all 14,721
modules accepted, no rejection and no operational error. All nine batches and
their kernel segments were new in this invocation. Completed dependencies were
still reused within the invocation; 14,720 module replay entries and one
import-only context acceptance must not be relabelled as exact kernel calls.
There were 86,150 trusted import entries. The native stdout and durable receipt
match. The controller, native processes and owned cgroup retired without a
resource stop or OOM event.

| Reference | Scope compared | Acceptance difference | Axioms |
|---|---:|---:|---|
| Previous defective 2df checker | 14,721 | 0 | Same 15 names |
| Fresh e0c92d51 checker | 14,721 | 0 | Same 15 names |
| O's 30-segment stream | 14,721 | 0 | Not recorded in retained stream events |
| O's module-local reference | 14,401 | 0 | Not recorded in that ledger |

The missing 320 module-local references remain missing. Matching the full
stream does not fill that oracle gap. The 36,209 input-path/hash pairs match
the retained older frame exactly. This is ordinary noncryptographic identity
checking, not collision-resistant attestation. The retained O references were
revalidated from their actual completed raw records before comparison.

The 15-name axiom set is listed in axioms.txt. No axiom was added or removed
relative to fresh e0. In particular, sorryAx and native-evaluation axioms remain
reported: this frame is not an axiom-free or sorry-free verification claim.
The requested historical fallback reasons different_constant,
unimported_reference and segregated_dependency were all absent in fresh e0;
its 60 fallbacks were duplicate_proof_requires_native. The missing-axiom bug
was reproduced in the small segregated fixture, but did not change this
particular retained frame's axiom union.

Sampled process-tree RSS peaked at 29.810 GiB, within the 40 GiB limit.
The wait4 single-process peak was 29.485 GiB and charged-cgroup peak 20.569 GiB;
these count shared mappings differently and are not interchangeable measures.
The preview wall time was 11,832.879 s and cgroup CPU 12,988.378 s.
Do not derive a speedup from older previews: affinity, source and context
validation work differ. The node retained its 8 GiB reserve throughout sampling.

Raw receipt, input ledger, segment events, controller wait4 result, memory
samples, exact binary and collection scripts are retained at:
/workspaces/.agent-state/gpu-smt-captures/checker-subexp-review-repair-3fe83c5a-20261104

Earlier 2df/e0 qualification is superseded for the current adapter by this
fresh run, but its historical records are unchanged. Repair review and result
inspection are 自审. Independent execution review and freeze remain pending.
