# Release component contract

The Rust CLI forwards these commands without interpreting verification results:

- proofserve check PROJECT [OPTIONS] -> proofserve-check PROJECT [OPTIONS].
- proofserve audit PROJECT [OPTIONS] -> proofserve-audit PROJECT [OPTIONS].

Components are resolved beside the executable, then on PATH. The checker
emits receipt v1 JSON on stdout; stderr and native exit status are unchanged.
The W audit report is its own format, not a Lean acceptance receipt. Bundle
entrypoints use the original checker executable and unmodified audit.py.

The bundle contains the matching original Lean 4.34.1 SDK. Its check launcher
compares the project's declared lean-toolchain with the bundled version before
putting that SDK on PATH. A different declaration delegates to the frontend official fallback using the
project matching toolchain. If that toolchain is unavailable, it fails with exit2;
no silent migration or download occurs. The project must be built already. Checkpoints
are trusted local state; the backend owns input-change invalidation and resume
qualification. Packaging does not infer acceptance or axiom sets.

Python 3.11+ is needed by audit and the portable entrypoints. No Rust compiler,
repository clone, original Workspace path, or external native oracle is needed
at runtime. All three binaries and libexec/ must stay together.

The existing candidate JSONL command moves from check to batch. HTTP /check
and serve semantics are unchanged. This pre-release CLI migration must appear
in release notes.

Native release qualification must cover the installed archive, version
rejection, three malformed proofs, and external projects using the original
official leanchecker. Mock launcher tests do not establish those properties.

## Independent closure batches

For a large already-built project, pass a UTF-8 file with one module name per
line; the Rust launcher forwards the options and receipt unchanged:

    proofserve check /path/to/project --root-file roots.txt --closure-roots 500

The closure-roots limit bounds requested roots per independent closure batch,
not CPU, memory, declaration count or a proof-search budget. Each new batch checks
its complete import closure; shared dependencies can be checked repeatedly.
Receipts deduplicate accepted modules and axioms but CPU includes repeated work.
Local input-validated batch certificates allow resume and remain trusted local
state; they are not portable adversarial certificates. An unfinished batch or a
changed input is not a complete verification. See checker/docs/receipt-schema.md
for v1 types, context_strategy, batches and the distinct cumulative CPU field.
