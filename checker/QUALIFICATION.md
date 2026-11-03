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
module ledger. The current stable Lean 4.35.0 also builds and passes the small contract.\nA 4.34.1 executable also successfully routes a 4.35.0 project through its\nofficial checker, with the fallback path and limited coverage explicit.
No claim is made that reviewing one symbol proves ABI compatibility.

These controls do not replace the release performance matrix, complete Mathlib
scale test, real interruption experiment, external-project acceptance, or CI
closure. Segmentation still retains a cumulative checked prefix on restoration.
