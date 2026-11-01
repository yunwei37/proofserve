# Native context controls completed; Falconer measurement prepared

Date2026-11-01UTC. Review: self-review.

The five-case matrix(ordinary duplicate theorem, corrupt duplicate,
unimported sibling reference, incompatible same-name definitions, private
helper names) completed15 native executions in boundary-v4. Audited replay
matched module-local replay in every case. Naive union accepted both the
corrupt duplicate and the unimported-reference case; it rejected individually
valid conflicting definitions. These controls confirm that original kernel
code alone does not make arbitrary union contexts equivalent.

The earlier v2/v3 full-Init qualification attempt remains a real failure:
a normal positive timed out; v2 then tried to parse truncated JSON.
v3 kept the timeout/partial record and was stopped after its positive had
already failed, because later adversarial cells could not qualify that source.
v4 uses minimal explicit Init.Prelude fixture dependencies. This reduces
irrelevant qualification work; it does **not** claim a full-Init performance
result. The duplicate-proof compatibility path can locally check a differing
theorem interface without quarantining all new declarations and descendants.
Different definitions and genuinely unimported references retain separate
native context. All such extra work is included in the measured checker.

The boundary source now uses stock constNames/ConstantInfo pairing.
The added header records aliased-name entries so that source-name assumptions
can be checked against actual typed input. Upstream unsafe/partial exclusions
and duplicate-theorem behavior remain explicit, not new no-axiom policies.

The measurement executable adds two required counters: actual unique
declarations in the checked kernel environment, and process VmHWM peak RSS.
Lean's empty environment starts in stage2, so counting map1 alone would be
wrong. The source counts both map stages with SMap.fold. The memory curve is a
separate profiling pass, sampled every100 completed modules plus the final
state. It records current RSS/PSS/shared/private pages, peak RSS, input and
eligible input entries, shared-kernel declarations and local-context checks.
Counting/profiling overhead is not subtracted or presented as free.
Primary timing disables memory checkpoints.

The updated telemetry binary compiled and passed one positive and one corrupted
proof control, with nonzero actual declaration counts and VmHWM present.
These are native engagement/contract controls, not full-library parity.

## Complete source graph

The completed stock external-artifact manifest expands the full Falconer
project to13,205 modules:2,461 Falconer plus10,744 dependencies. Every source
path exists. The actual project build/check point is
scale-study/falconer-project-20261101 under the existing PVC capture root.
No failed/incomplete old prelaunch directory was relabelled as new data.

Construction reuses only immutable successful typed artifacts and measured
compiler cells from the completed SAME experiment. It builds every missing
node and includes every closure member in its source-work denominator. Shared
compiler work is explicitly attributed once per containing closure. This is
not a new fresh-process reconstruction of common nodes or a historical
denominator borrowed from another resource/hardware point.

Next cells, under P0–7 and the existing FIFO flock, are missing-node source
construction, exact-artifact audited streaming, a separate memory profile and
complete module-local differential checking. Each native command and each
window has a self limit; no -M. Native child cgroup11.75GiB leaves256MiB for
O-line parents. Original source snapshots, completed cells, failures and
intermediate typed inputs remain on PVC.

## Memory inference

The reducer fits within-run peak RSS(VmHWM) against actual shared-kernel
declarations, reporting intercept, slope, R-squared and maximum residual.
Both variables trend with execution; mapped regions, proof-term size, audit
metadata and temporary kernel work also consume memory. The fit is descriptive,
not a causal per-declaration law.

Full-library conditional scenarios add1,2,4 or8 assumed new unique declarations
per remaining lexical theorem site to the measured complete Falconer closure.
They exclude its already included7,312 lexical sites from the remaining count.
Source sites are not actual typed declaration counts, and computation-heavy
parts of the population are not calibrated by this mathematical project.
Extrapolation beyond measured N is explicitly flagged. Any conflicting-context
segments/local checks are reported; this does not manufacture a one-environment
memory guarantee. The need for segmentation must follow the actual curve and
these limits, not a two-point assumption.
