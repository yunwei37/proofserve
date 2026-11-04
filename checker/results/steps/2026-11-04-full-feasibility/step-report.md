# Full-source feasibility and retained-case qualification

Review: 自审. Source implementation checkpoint: 2df1d9d7. Final results are a
development qualification, not the final paper performance evaluation.

## Goal and invariants
Bound retained kernel state by independent closures, avoid rechecking certified
shared dependencies, preserve actual import contexts and original-kernel
acceptance, and retain failures. Source edits stay under checker/. W inputs are
read-only. Initial runs used CPU 8–9 and 16 GiB; the user then authorized
E17–23, at most 40 GiB, and at least 8 GiB node memory available.

## EXPERIMENT
The 163,097-source request has one execution environment and two source-root
mappings. Static grouping/replay tables are complete for the known graph;
41 external edge sets remain unresolved. The original repeated-replay plan
exceeds a conservative runtime scenario and the legacy memory curve.
The completed-module receipt design checks new modules with the original
kernel and reconstructs only byte-bound checked imports.

The real 11,478-module identity scan matched 32,966 old input parts exactly.
The native contract passes three malformed proof classes, stale dependency
rejection, live changes, unused completed-input changes, scoped references,
canonical roots, partial resume, and cached imports across checkpoints.
Pure Python matrix/planner tests are explicitly stubbed.

The finite continuation completed 14,721 modules in 9 batches, with 14,720
module-check entries and 86,150 reconstructed import entries. Acceptance equals
the original 30-segment O stream. Raw reference reduction confirms 14,401
module-local original-kernel references, all accepted here, with 320 not
referenced. No full official CLI ledger is claimed.
The current invocation's sampled tree RSS peak is 26.062 GiB; maximum
single-process wait4 RSS is 25.864 GiB. It has no guard stop or OOM. Earlier
16-GiB stops and the known false rejection remain separate. This is not a
memory-saving result or a fresh timing comparison.

The real tiny workflow froze clean source commit 2df1d9d7, preserved actual
launch failure 126, retried explicitly, checked its three-module fixture,
called stock default/fresh, and exported nine rows. Its matrix/Planar labels
are fixture routes. All native children, cgroups and controllers retired.

## WRITE
The feasibility report gives grouping, cost assumptions, measured memory,
reference coverage, and a post-census command. The 62.4-GiB OAI value remains
a two-point extrapolation. A conditional largest-scope receipt checks all other
roots while leaving only a verified zero-own-declaration umbrella's context
pending; it is not full-project acceptance or an observed corpus result.
The current driver stops on capacity failure rather than silently reducing scope.

## REVIEW
Self-review only. The fixed SDK disproved the extension-loading attribution:
loadExts already defaults false. Its temporary refactor was removed.
The qualified native source snapshot exactly matches checkpoint 2df1d9d7.
No kernel changes, additional agent, upstream action, tag, release, full-corpus
run, final matrix or real PlanarPacking measurement was made.

## Outstanding
W's gate/full artifacts and user decision remain external prerequisites.
Actual OAI capacity, unresolved external edges, full-corpus acceptance,
quiet final performance matrix/official comparisons, matched interruption
overhead, and PlanarPacking are incomplete. O's independent review remains
separate. The present M task ends at this verified development boundary.
