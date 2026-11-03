# ProofServe0.1.0 — prepared, not published

Scope: independent Lean project checking and audit. The existing Kimina
service remains available; no service feature was added in this closeout.

## Added

- Project check/audit CLI entrypoints that preserve backend receipts,
  diagnostics, Unix signals and exit codes.
- A relocatable Linux x86_64 bundle recipe with the original matching
  Lean4.34.1 SDK, checker, audit and a one-command installer.
- Explicit official-toolchain fallback for a different declared project version;
  an unavailable matching toolchain is an error, never an automatic migration.

## CLI migration

The former candidate JSONL check command is now batch. proofserve check PROJECT
means independent project checking. HTTP /check is unchanged.

## Qualification

Passed: real954665072-byte archive assembly, extraction into an independent
installation prefix, project check/audit and three malformed-proof rejections.
The actual test uses a compiled two-module project, not a performance workload.
Tool sources and retained failure corrections are in qualification-local.json.

The Ubuntu22.04 portable-release workflow41725630396 also passed on commit5de37517:
source tests, source-package dry-run, native checker contracts, standalone
archive installation, project check/audit, official default/fresh controls and
three actual malformed-proof rejections. See qualification-ci.json. It uploaded
Actions build artifacts only; it did not create a public release or registry upload.

Passed: complete Docker image build and network-disabled self-test on11835a92
(run41724086160), with the same4.34.1 SDK, Mathlib and rebuilt REPL. Both
full-Mathlib service imports, accepted/rejected/sorry responses, installed project
check/audit and mismatched-version error passed. Exact controls and CI-runner
observations are in qualification-container.json. The old prepared-parent timeout
is retained as a historical failure; this image uses the stock fresh REPL and
does not claim to repair or qualify that optional prepared adapter.

Pending: three previously unused external projects including an AI-assisted project;
official leanchecker accepted-set comparison; backend malformed-proof CI.
No performance improvement over official leanchecker is advertised before
those published-form measurements are complete.

The launcher change passed11local CLI contracts (8existing lifecycle/resource
contracts,3project-dispatch contracts). They are not native proof correctness
or a performance result. Raw logs remain on the research PVC.

Research data and complete Git history are retained. See repository-size.json
for pinned HEAD logical size, full reachable-history logical size and live
.git allocation; these are distinct measurements, not interchangeable
download sizes. No history rewrite, release, tag or registry upload occurred.

Rust full-workspace tests, doctests, clippy and release build passed locally. All four crates passed cargo publish --workspace --dry-run --locked. Engine CI41723961875 passed, including real original-kernel checker/resume/bad-proof and legacy service contracts. No package was uploaded.
