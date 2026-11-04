# Development qualification

> **Superseded correctness qualification:** O's review of 2df1d9d7 found false
> acceptance in certificate reuse without modifying certificate contents.
> The historical 14,721-module result used that logic. Its qualification is
> superseded by the [fresh e0c92d51 replay](results/certificate-reuse-fix/subexp-fresh-e0c92d51/README.md).
> Old raw results and memory observations remain preserved; they do not qualify
> the repaired checker or establish final performance.

> **Current review repair:** the fresh e0c92d51 result above is historical.
> A later code-only independent review identified additional adapter defects.
> The new qualification is tracked in [e0 review repair](results/e0-review-repair/README.md).
> No repaired-source independent execution review or release freeze is claimed.

Self-review, 2026-11-03. Raw development attempts remain on the existing PVC in
checker-package-20261103. They are not formal P-core performance measurements.

The package integrates the original-kernel parallel stream with a writable copy
of O's checkpoint reader. Persistence and split fallback are enabled by default.
The CLI and receipt format are documented separately.

Initial build attempts exposed missing C headers, an ambiguous Options name,
missing UInt32 JSON instances, and a host fscanf symbol unavailable in the
matched SDK linker. These attempts are retained. The C reader now uses portable
character input. Later builds succeeded.

An initial import-heavy E-core control reached its 90-second limit. It does not
establish semantic success or library performance. The subsequent small fixture
uses two prelude-only modules. Its first attempts exposed a missing Lake library
declaration and a missing mutation enum entry; both were corrected.

Final native controls pass: the two-module closure, equal acceptance and axiom
sets at 1, 2, and 4 workers, stock CLI acceptance parity, rejection of loose
variables, unknown constants, and wrong sorts, bounded checkpoint/resume parity,
and explicit errors for a mismatched declared toolchain. Native processes and
their cgroups retired without resource stops.

The matched Lean 4.34.0 build and the same small contract also pass. The official
fallback is exercised separately and reports roots rather than inventing a
module ledger. Lean 4.35.0 also builds and passes the small contract.
A 4.34.1 executable also successfully routes a 4.35.0 project through its
official checker, with the fallback path and limited coverage explicit.
No claim is made that reviewing one symbol proves ABI compatibility.

At that initial qualification boundary, the release performance matrix,
complete Mathlib scale test, real interruption experiment, external-project
acceptance, and CI closure remained open. The later preview and preparation
below supersede only their explicitly reported functional checks. Segmentation
inside one batch still retains a cumulative checked prefix on restoration.

## Ablation repair before the final matrix

The first frozen evaluation, c8e7c615, completed ordinary native points but its
no-split switch was found to disable parallelism in ordinary-only modules too.
That is a protocol defect for the requested ablation. The collector is retired
at a native task boundary, with all original records preserved. Its data are
not used to fill the repaired version's final matrix.

The repaired branch computes the complex prefix first. Disabling split fallback
replays the whole module only when that prefix is nonempty. Ordinary-only
modules continue through the same dependency-wave path as the default.
Both release ablations are included in the portable correctness contract.

The repaired executable remains fixed at ba316991. The collector is continued
at a native boundary to give its upcoming real-prefix negative controls the
project's Lake environment. Its completed native measurements are retained,
not rerun or replaced. Collector source and executable source revisions are
recorded separately; this does not change a measured native command.

## Census-period correctness preparation

The user reclassified the ba316991 matrix as a nonfinal preview under background
load. Its existing native leg finished before the controller was retired at a
task boundary. The remaining attempts were shortened to one repeat. The native
binary was unchanged; all original data remain on the PVC.

The preview completed the full Mathlib library: 8,529 directory modules plus
the umbrella module, with 10,744 accepted modules including dependencies.
Four Grid/Barrier official controls stopped before checking because the official
CLI canonicalizes symlink paths while naming modules. They are path failures,
not kernel rejections. The future harness appends the real artifact root after
the original overlay, preserving lookup precedence.

Independent closure batching is a new coordinator path. Its native child still
uses the original-kernel streaming procedure. The portable contract verifies
acceptance and axiom parity, certificate reuse, a partial-batch resume, stale
input rejection, root-file handling including official fallback, coverage of
later roots by an earlier complete closure, and independent modules that declare
conflicting names. Existing three bad proof controls still reject.

On CPU 8-9, a real Nat.Basic / Int.Basic preparation checked 1,360 modules with
the single-frontier and two-closure procedures. Acceptance, declared axioms, and
module hashes match. The subsequent covered-root optimization reuses the real
Int.Basic certificate and correctly skips the already covered Nat.Basic root.
This is small-scale functional qualification, not evidence of whole-corpus
capacity or final performance. Raw attempts are in
checker-closure-batches-20261104 on the existing capture PVC.

The empty-umbrella extension addresses the top-level OAI source module without
assuming its compiled declaration count. Only actual compiled zero-declaration
modules are eligible. Their original combined import context must still load
and pass the upstream empty replay, so independently valid conflicting imports
cannot bypass context validation.

Build attempts 4 and 5 exposed a list/array pipeline, an unavailable String
helper, and a multi-line record syntax issue. Their logs remain intact. Later
builds succeeded. The portable contract now also checks default namespace-root
expansion, stale empty-plan rejection, three actual malformed serialized theorem
bodies below an empty parent, and incompatible combined import definitions.
These are untimed CPU 8-9 controls. No new P-core run was started.

## Completed-module reuse qualification

CPU 8–9 controls in checker-full-feasibility-20261104 exercise the new
byte-bound local module ledger, dependency-first grouping, empty leaf expansion,
canonical root binding, and a cached base across successful segment boundaries.
The portable native contract includes three malformed proof bodies before
certificate creation, changed certified dependencies on resume and between live
batches, a changed completed but subsequently unused artifact, and a malicious
reference to an unimported checked sibling. Incompatible valid combined imports
fall back to original module-local checking and retain their accepted sets.

A real standard-library false rejection exposed missing certified imports after
a segment checkpoint. The writer now includes that seed context, and restoration
also recovers older successful local segments using separately input-validated
cache metadata. The successful cross-segment regression is not a proof that all
private ABI paths or the full corpus are qualified. Failed attempts are retained.

The planning decision, largest retained closure result, remaining capacity
limit, and one-command post-census handoff are in results/full-feasibility.md.
None of the current CPU 8–9 values is a final paper performance result.

The next 16-GiB attempt also stopped, at a sampled tree peak of 16.015 GiB,
without an OOM. Completed batches covering 11,216 modules were preserved.
Its peak sample contained about 1.84 GiB in the frontend and 14.07 GiB in a
native worker. Subsequent code removes overlap with the metadata scan and
redundant compacted-data loading during cached provenance construction.
The portable native suite passed again, and the real 32,966-part identity
comparison passed before any kernel continuation. The largest-closure outcome
is reported separately rather than inferred from those controls.

The fixed SDK source disproved a proposed extension-initialization attribution:
importModules already defaults loadExts to false. Its temporary refactor was
removed; source-build10 is the qualified retained source. No resource reduction
or causal conclusion is claimed from that discarded hypothesis.
The latest 16-GiB run stopped at 16.033 GiB; a separate one-new-module direct
control completed, which is not a full-frame pass. The authorized 40-GiB,
E17–23 continuation is a separate resource point and preserves earlier success.

## Completed retained-frame and workflow qualification

The E17–23 / 40-GiB continuation completed all 14,721 retained frame modules
with nine batch certificates. Its sampled tree peak was 26.062 GiB and its
maximum single-process wait4 RSS was 25.864 GiB. No guard fired. The native
source snapshot exactly matches commit 2df1d9d7. Acceptance equals the full
retained O stream, and all 14,401 available O module-local reference judgments;
320 module-local references remain unavailable. This is not full official CLI
coverage. The larger observed memory peak is not presented as a memory saving.
All prior failures remain preserved.

The actual tiny workflow completed from clean source commit 2df1d9d7: binary
freeze, preserved launch failure 126, explicit successful retry, native checking,
stock default/fresh calls, and result export. It uses a three-module fixture;
its matrix/Planar labels do not represent those real datasets. Controllers and
all guarded native children retired. No new full-corpus or final-matrix run
was started. O's independent review and final performance evidence remain open.


## 2026-11-04: e0 review repair qualification

Source 3fe83c5a passed the complete local contract and the existing CI
checker-contract at cdf86d68 (87 review-runner command records, not 87 defect
classes). The fresh 3,977-root SubexponentialSAT frame then completed 14,721
accepted modules, no rejections and the same 15 reported axioms, with a new
checkpoint directory and no resource stop. The sampled process-tree peak was
29.810 GiB on E cores 10–23 with two workers. Its 36,209 resolved input parts
match the old frame. Acceptance matches O's full stream and the 14,401 available
module-local references; 320 module-local references remain unavailable.
The focused optional-part presence regression also passed after retirement.
See results/e0-review-repair/ for exact controls, limitations and raw locations.

These are 自审 and mechanical CI evidence. The supplied independent review
concerned old e0 source only; this repaired source has not had independent
execution review. No release freeze, full-library capacity or final performance
claim follows. Matching theorem-body/Quot proposals not reproduced remain
bounded limitations; unsupported native-IR evaluation is explicitly refused.
