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
The final three-repeat Nat.Basic strict point at eight workers costs 4.227×
wall and 2.501× CPU versus default eight workers (276.053 / 283.782 s).
Strict Grid timed out at 1,800.010 wall seconds; no strict repeat completed,
so no Grid strict multiplier is available. The older 22.1× replay/2.33×
attempt-CPU preview concerns superseded isolation, not the current multiplier.
[Final policy costs](../checker/results/release-e000ed62bbf4/matrix/README.md).

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

## Final qualification, measured scope and publication decisions

The [frozen package preview](FREEZE_E000ED62.md) rebuilt the immutable e000ed62
snapshot, relocated the archive, and passed the existing valid/invalid/version
controls and three external projects. The fresh image passed build-time and
standalone network-disabled controls without host mounts. Functional preview
costs remain ineligible as final timing; image caches were later reclaimed.

Final native 1→8-worker wall speedups are 1.697× for Nat.Basic (a 1,330-module
closure, not all Mathlib), 2.140× for Grid and 1.727× for Barrier, three repeats
per point. They compare the same input ledger within the tool. Official
default/fresh have different obligations. The finite matrix has unattempted
and incomplete cells; [the report](../checker/results/release-e000ed62bbf4/matrix/README.md)
defines its actual scope. No equal-obligation official speedup is inferred.

The [final external run](../data/external-projects/e000ed62-final/README.md)
completed all three projects in a freshly installed archive from runtime
818f7422, with the e000ed62 binary and new checkpoints. All 126 common local
roots agreed with official default. Native closures are 754/2368/10753 modules
versus official 105/12/9 roots. This does not establish an equal-obligation
speedup or whole-closure equivalence. Background workloads remained active;
the machine was not exclusively idle.

The built-subset campaign certified only **968/162,170 requested source
modules** in 15 complete batches (12,756 closure modules including dependencies).
Provisional segment events do not certify an unfinished batch; 161,202 requests
remain uncertified. Exit 124 was operational cutoff, not kernel rejection.
The 926 deferred unbuilt sources were outside the request. Neither whole-corpus
acceptance parity nor whole-corpus cost is established.
[Certified and provisional scope](../checker/results/release-e000ed62bbf4/corpus/README.md).

Receipts report axiom declaration inventories, not minimal used-axiom closures
or sorry-free guarantees. Source digests/Git metadata provide provenance, not
source-to-artifact correspondence. Document synchronization adds no checker
change or new measurement.

The [retained archive](RELEASE_ARCHIVE.json) is Debian13/glibc2.41-qualified.
The Ubuntu22.04 workflow build is a separate artifact, not the same bytes.
The [release checklist](RELEASE_CHECKLIST.md) lists pending public actions.
Pushing a v* tag triggers portable preparation and automatic crates publication:
a tag-only approval does not authorize the latter. No public release, crate
upload, image push or announcement has been executed.
