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

Explicit Lean.reduceBool / Lean.reduceNat references can currently be refused
even without an actual evaluation. Incomplete module-system artifact parts are
also refused; official default and --fresh can differ on such inputs. No blanket
equivalence with both official modes is promised. See the
[current review boundary](#current-checker-review-and-release-boundary)
and [receipt schema](../checker/docs/receipt-schema.md) before using receipts.

## Current checker review and release boundary

Status recorded on 2026-11-04, against checker source in 2628d727. This is a
release-readiness disclosure, not a new execution review. The original
[e0c92d51 review](checker-review-e0c92d51.md) and
[2628d727 review](checker-review-2628d727.md) are code-only reviews. Their proposed
counterexamples must be distinguished from actual native observations.

The [e0 repair qualification](../checker/results/e0-review-repair/README.md)
and [finding ledger](../checker/results/e0-review-repair/finding-status.csv)
record reproduced e0 defects and repairs: segregated axiom reporting, artifact
shadowing, duplicate/context handling, event/exit dominance, empty-context
coverage, unsafe sibling borrowing, publication/coverage and receipt provenance.
The expanded CI runner actually executed 90 command records; these are not
90 independent defect classes. The supplied native-printing event attack and
Quot difference were not reproduced. Green CI does not close the second review.

Known behavior and limits that users must account for:

- Native safe declarations referencing Lean.reduceBool or Lean.reduceNat,
  including wrappers, can be refused conservatively. This can include a
  mention-only statement, not just execution. The second review also flags
  name-based taint across unrelated modules; its proposed cases await native
  confirmation. This boundary does not mean native_decide or bv_decide are
  generally unsupported: their native-computation axioms remain visible.
- --official selects the matching official checker with --fresh, not default
  leanchecker. It is an explicit trusted-code path, not a guaranteed workaround
  for native IR refusal; the second review questions whether project IR can be
  reconstructed there. No silent fallback or mode equivalence is claimed.
- A module-system artifact requiring exported/server/private parts is refused
  when required parts are incomplete. The original O prefix-only certificate
  seed therefore no longer qualifies. For supplied incomplete/stale-part
  artifacts, official default and --fresh have different behavior. The repaired
  native selection follows the module flag; this is not an arbitrary binary
  layout validator or a promise to match both official procedures.
- Local checkpoints and their serialized metadata remain trusted. Input hashes
  detect ordinary stale files and part-inventory changes, not malicious
  collisions or deliberately forged acceptance/axiom metadata. Do not accept
  another party's checkpoint directory as a proof.
- The fresh repaired SubexponentialSAT frame accepted 14,721 modules with 15
  axioms. It agrees with all 14,401 available module-local official references;
  the other 320 have no completed module-local reference. This is separate from
  O's historical partial comparison, and does not establish whole-library or
  adversarial-input equivalence.
- A receipt's Git revision does not bind compiled artifacts to that source
  revision. Module-entry counts are not exact kernel-call counts. Non-complete
  receipts do not certify the requested closure or its final axiom union.

### Waiting on M before release freeze

The second code-only review is open. O has not executed new adversarial cases
in this documentation/cleanup step and has not verified M's ongoing repairs.
Track the following against a new immutable checker pin and actual evidence:

1. Unsafe/partial duplicate declarations bypassing shared-frontier conflict
   detection (potential wrong acceptance).
2. Earlier same-interface theorem bodies retained in the frontier, including
   the proposed false-rejection and crafted wrong-acceptance directions.
3. Conservative primitive refusal, name-taint ordering, and the real scope of
   --official for project IR; missing/corrupt IR artifact comparisons.
4. Import-only rejection exit classification, accept/reject overlap on partial
   receipts, and default-checkpoint project_dirty attribution.
5. The unconfirmed crafted Quot case, escaped-name discovery, empty-root
   context disclosure and --max-segments resume wording.

No item above is marked repaired solely because code changed. Once M records
the actual outcomes and fixes, rebuild the archive and container from the
frozen pin, rerun installed-form correctness/CI and external-project acceptance,
and collect the agreed final system measurements when the census is finished
and the machine is quiet. Old qualification JSON remains historical evidence.
No release, tag or registry upload is authorized by these preparations.
