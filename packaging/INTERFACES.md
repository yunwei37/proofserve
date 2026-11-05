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
not CPU, memory, declaration count or a proof-search budget. The current backend
can reuse previously checked imports across batches using trusted local
certificates and matching input identities; reused proof bodies are not replayed.
--replay-shared-imports requests repeated closure checking. Acceptance and axioms
are deduplicated; entry counts and cumulative CPU can include historical work
and repeated imports. This is not a cryptographic or portable proof certificate.
An unfinished batch or changed input is not complete verification.

Use --strict-theorem-bodies to select strict artifact-context policy. The
launcher passes it unchanged; help and receipt theorem_body_policy identify
the choice. ABI 6 / independent-closures-v8 state cannot be reused across
policies or changed executables.

## Frozen checker boundary

The checker is frozen at e000ed62bbf4b9c420bd99d0273a5d21829b4edc (Lean 4.34.1),
superseding e1557c77. The earlier code-only reviews at
[e0c92d51](checker-review-e0c92d51.md) and [2628d727](checker-review-2628d727.md)
now have [recorded repair qualification](../checker/results/e0-review-repair/)
and [replacement-policy evidence](../checker/results/theorem-body-policy/).
They are no longer an unassigned "waiting on M" list. Repairs and interpretation
are M's self-review; O's package execution below does not become an independent
soundness proof.

Default shared-checked retains an already kernel-checked theorem body for the
same interface. Later distinct bodies are checked in their declared contexts,
including an explicit fresh-name kernel check for imported duplicates that
stock replay skips. A crafted downstream artifact can nevertheless pass in
the shared checked environment while stock original-context replay rejects it.
The accepted proposition still follows by the original kernel from checked
proofs and the reported axioms. This is closure derivability, not a guarantee
that every serialized proof replays in its original module context.

--strict-theorem-bodies isolates differing bodies and dependent contexts. It
matches the supplied artifact-context controls, but is not universal parity
for malformed metadata and does not override unsupported native evaluation.
In the retained 3,793-module Grid preview, the historical e155 isolation
strategy used 3,465 module-local replays versus 157 with replacement default
(22.07×), and 3,508.94 attempt CPU seconds versus 1,507.06 (2.33×).
The old isolation run includes an interruption and its clocks are separate.
The new strict implementation also checks skipped duplicate bodies explicitly;
it has not been rerun on Grid. These are historical, background-load previews,
not a measured current strict-mode multiplier or official speed comparison.

Additional limits remain:

- Direct open-parameter reduceBool/reduceNat mentions work. Closed/higher-order
  evaluation dependencies and some passive higher-order uses are refused with
  operational exit 2. Checks are scoped to declared dependencies; no silent
  native-to-official fallback executes project code. native_decide/bv_decide
  native-computation axioms remain visible.
- --official uses matching stock --fresh. Its imported final-environment
  procedure differs from stock default and native per-module checking, and
  may itself lack required project IR. It is not a guaranteed workaround.
- Required exported/server/private parts and IR inputs are bound by identity.
  Incomplete module-system inputs are refused. Supplied stale/incomplete parts
  can yield different stock default/fresh results.
- Local certificates and Lean-serialized checkpoints are trusted editable
  state. Noncryptographic hashes detect ordinary stale artifacts, not deliberate
  collisions or forged acceptance/axiom metadata. Artifacts must stay stable
  throughout a call; foreign checkpoint directories are not portable proofs.
- Git revision/dirty metadata does not attest source-to-artifact correspondence.
  Module-entry counts are not kernel-call counts. Incomplete or operational
  results do not certify the requested closure or its final axiom union.
- The older repaired SubexponentialSAT frame accepted 14,721 modules against
  14,401 available module-local references; 320 references remain absent.
  That historical ABI does not qualify the frozen ABI 6 checker or whole corpus.

## Release qualification and remaining gates

The frozen native source and supplied regression outcomes are documented in
[theorem-body-policy](../checker/results/theorem-body-policy/).
[This completed package preview](FREEZE_E000ED62.md) rebuilt that immutable
snapshot, relocated the archive, and passed the existing valid/invalid/version
controls and all three external projects on CPU 8–9. The fresh image passed
build-time and standalone network-disabled controls without host mounts.
Both archive and image verified strict-mode forwarding and the three existing
bad-proof categories. All costs remain previews during W's ongoing census.
Historical archive/image passes stay pinned to their original versions.

After the preview completes, final external timing uses a freshly installed
archive of the committed launcher/audit and the same qualified frozen checker.
Only external cells acquire the existing P-core lock, after M's final matrix.
Container/correctness work is already qualified before that two-hour window.
No publication follows automatically: tags, registry uploads and announcements
still require the user's release decision.
