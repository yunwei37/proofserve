# Release component contract

The Rust CLI forwards these commands without interpreting verification results:

- proofserve check PROJECT [OPTIONS] -> proofserve-check PROJECT [OPTIONS].
- proofserve audit PROJECT [OPTIONS] -> proofserve-audit PROJECT [OPTIONS].

Components are resolved beside the executable, then on PATH. The checker
emits receipt v1 JSON on stdout; stderr and native exit status are unchanged.
The W audit report is its own format, not a Lean acceptance receipt. Bundle
entrypoints use the original checker executable and unmodified audit.py.

The bundle contains the matching original Lean4.34.1 SDK. Its check launcher
compares the project's declared lean-toolchain with the bundled version before
putting that SDK on PATH. A different declaration delegates to the frontend official fallback using the
project matching toolchain. If that toolchain is unavailable, it fails with exit2;
no silent migration or download occurs. The project must be built already. Checkpoints
are trusted local state; the backend owns input-change invalidation and resume
qualification. Packaging does not infer acceptance or axiom sets.

Python3.11+ is needed by audit and the portable entrypoints. No Rust compiler,
repository clone, original Workspace path, or external native oracle is needed
at runtime. All three binaries and libexec/ must stay together.

The existing candidate JSONL command moves from check to batch. HTTP /check
and serve semantics are unchanged. This pre-release CLI migration must appear
in release notes.

Native release qualification must cover the installed archive, version
rejection, three malformed proofs, and external projects using the original
official leanchecker. Mock launcher tests do not establish those properties.
