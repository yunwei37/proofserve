# Development qualification

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
