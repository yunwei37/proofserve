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

Pending: real bundle relocation/install; complete Docker Mathlib qualification;
three previously unused external projects including an AI-assisted project;
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
