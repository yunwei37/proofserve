# Receipt format, version 1

The executable prints one JSON object and saves the same object as receipt.json
in the checkpoint directory. Native exit codes are 0 for complete checking,
1 for a native verification rejection (inspect its kernel or importer diagnostic),
and 2 for an unsupported configuration or an operational
failure. An interrupted process may leave successful segment records without a
final receipt; these are not a complete verification.

## Native path

The execution_path field is proofserve-parallel and parallel is true. The fields
are schema_version, lean_version, mathlib_manifest (the unaltered Lake lock),
roots, accepted (ordered module names), rejected (kernel diagnostics), status,
module_set_hash, module_set_hash_algorithm, axioms, workers, cpu_ns, wall_ns,
cumulative_segment_cpu_ns, segments, and trusted_local_checkpoints.

The module hash is Lean's deterministic 64-bit hash of sorted accepted names.
It is not cryptographic. The axiom list contains declarations in the accepted
closure, including accepted segregated modules; it is not a minimal per-theorem
axiom dependency set.

cpu_ns measures this invocation's CPU, including waited child processes.
cumulative_segment_cpu_ns also includes reused successful segment work.
wall_ns includes this invocation's discovery, input identity checks, checkpoint
imports and exports. Each segment entry identifies whether it was reused.
These quantities must remain separate when reporting resume overhead.

No complete receipt is produced for an unfinished requested closure. Input-part
hashes and the Lake manifest must match before a success is reused. This detects
ordinary stale inputs, not adversarial checkpoint modification.

## Official fallback

The execution_path field is official-leanchecker and parallel is false. A warning
is written to stderr. The receipt contains accepted_roots, rejected_roots,
official_results, coverage, version, CPU and wall time. accepted, rejected,
module_set_hash, and axioms are null because the official CLI does not expose the
corresponding per-module ledger or axiom report.

Official --fresh checks a final imported environment per root. It has a distinct
duplicate-proof policy and must not be presented as identical to the native
per-module procedure. A failed official invocation is official_failure. Stock exit 1 is propagated
as exit 1; other nonzero tool statuses return operational exit 2. Its actual
per-root diagnostic is retained without claiming that every tool error means
a false proposition.

## JSON types

UInt64 values are decimal strings, following Lean's JSON instances. In particular,
cpu_ns, cumulative_segment_cpu_ns, checker_binary_hash, and module_set_hash are strings, not JSON
floating-point numbers. wall_ns, workers, schema_version, and segment indices
are JSON integers. Consumers should parse decimal strings losslessly.

| Field | Native type | Official fallback type |
|---|---|---|
| execution_path | proofserve-parallel | official-leanchecker |
| parallel | true | false |
| project_revision | string or null | string or null |
| mathlib_manifest | object or null | object or null |
| roots | array of strings | array of strings |
| accepted | array of module names | null |
| rejected | array of diagnostic objects | null |
| module_set_hash | decimal UInt64 string | null |
| axioms | array of declared axiom names | null |
| workers | positive integer | absent |
| segments | array of {segment: integer, reused: boolean} | absent |
| accepted_roots | absent | array of strings |
| rejected_roots | absent | array of official-result objects |
| official_results | absent | array of {root, exit_code, stdout, stderr} |

A native rejected diagnostic identifies a module that did not verify; inspect
its error text before classifying the cause. It does not mean the theorem's
statement is false. Configuration errors can instead produce only an error JSON
object on stderr and no new receipt. A caller must respect the process exit code
and must not treat an older receipt file as the output of that failed invocation.

## Independent closure batches

Large native requests can add context_strategy: independent-closures and
checkpoint_kind: input-validated-local-certificates. closure_roots is the
positive integer root-batch limit. batches lists the selected roots, covered
module count, status, local certificate path, and whether each batch was reused.
segments then has an additional integer batch field; segment remains a unique
integer within this top-level receipt.

accepted and axioms are deduplicated unions of the actual native child receipts.
Every requested root must occur in accepted before status can be complete.
A child checks new modules in their actual import closure. Already checked
imports can be reconstructed by the original importer from input-validated
local certificates. A requested root covered by an earlier complete closure
needs no new batch. Merely compiling an import never certifies its proof bodies.

cpu_ns counts this invocation, including all waited descendants and input
validation. cumulative_segment_cpu_ns includes import reconstruction and old successful
work reused from local certificates. Legacy --replay-shared-imports can also
repeat shared proof checks across batches. This field is not the cost of
checking each unique declaration once. Certificate validation
hashes an unchanged file once per invocation, so artifacts must remain stable
for the duration of that invocation.

A complete batch certificate preserves both its native receipt and input
identity. Generated environment snapshots may then be retired; interrupted
batches keep their partial segment state. This retains the existing assumption
that local checkpoints are trusted and input hashes detect ordinary changes,
not adversarial tampering. Extra fields are additive within schema version 1.
Native receipts now include checker_checkpoint_abi: 5. The JSON schema version
and the internal checkpoint ABI are different contracts. Receipt Lean version
and child ABI must match before a completed batch can be reused.

import_only_modules is an optional array of module names. Each member has zero
own declarations in the inspected compiled private data, all actual imports
have been checked, and the original importer plus empty replay has accepted the
combined context. It does not mean an unbuilt source file was accepted by a text
heuristic. Input-validated closure plans are trusted local checkpoint metadata.
Incompatible import contexts are not complete verification results.


## Reusing completed imports

Independent batches add reuse_checked_imports, module_check_entries, and
trusted_import_entries. The last two are module-entry counts, not declaration
counts or heartbeat units. module_check_entries counts original-kernel module
entries represented by batch receipts, including successful old work reused on
resume. trusted_import_entries counts imports loaded from completed local
certificates across batches; the same dependency can be loaded several times.
Imported proof bodies are not rechecked in those entries.

trusted_import_basis identifies this extra local trust. Child receipts include
certificate_reused_modules. Files are bound by the local completed-module
receipt and matching noncryptographic artifact hashes. This is not a portable,
adversary-resistant proof certificate. The --trusted-module-cache argument is
an internal coordinator interface to trusted local state, not an untrusted
proof upload interface.

The checkpoint metadata ABI is child ABI 5 / independent-closures-v7. Old checkpoint configurations produce an
explicit mismatch error; they are not decoded using a new unsafe layout.


Reuse binds the original canonical project, toolchain, manifest, search path,
checker options and complete currently resolved artifact-part inventory. An
optional private or server part appearing after certification invalidates
reuse even when the recorded exported file has not changed. The
trusted_import_basis text explicitly warns that manual certificate edits can
forge acceptance or axiom reports. It is a trust disclosure, not a cryptographic
attestation.

Receipt publication checks writes and file synchronization before atomic
rename, then synchronizes the parent directory. Failure returns nonzero without
complete stdout; a prior receipt may remain. Callers must pair the receipt
with the current invocation's exit status, not merely parse an old file.

## Input identity and per-module evidence

Native checkpoint identity includes checker_binary_hash, the Lean 64-bit
noncryptographic hash of the current executable's bytes. A changed executable,
Lean identity, child ABI, canonical project, manifest, search path, or resolved
artifact inventory refuses old state. This is change detection for trusted local
state, not authentication against deliberately chosen collisions or forged JSON.

project_revision is the Git HEAD when discoverable. project_dirty is a Boolean
or null when Git cannot determine it. project_revision_binds_artifacts is false:
the revision does not attest that the checked artifacts were built from that
commit. Actual artifact identities are recorded separately.

module_verifications lists each module's current evidence. action is
kernel_replay, interface_or_empty, certificate_import, checkpoint_reuse,
certificate_reuse, or empty_context. An interface_or_empty entry inserted no
new declarations into the shared frontier. safe_input_constants counts safe
input entries where available; frontier_insert_candidates counts the shared
replay's candidate map, not successful kernel calls. kernel_call_count is null:
the adapter does not expose an exact per-module kernel-call count. These counts
must not be used as unique declaration counts. new_module_check_entries counts
current kernel_replay rows, while module_check_entries retains the historical
module-entry meaning including earlier successful work.

Every listed import_only_modules entry now has an actual original-importer
context check in this invocation, even if a dependency visit previously accepted
its module name. Single-frontier completion additionally requires every requested
root and every discovered closure module to occur in accepted.

Worker events use a dedicated checked event file, not arbitrary stdout.
A nonzero child exit or any rejection prevents complete regardless of terminal
events. Raw stdout remains diagnostic output. Receipt-related text and JSON
writes use checked durable publication. Old complete files must still be paired
with the current process's exit status.

The native adapter allows direct open-parameter mentions of Lean.reduceBool
and Lean.reduceNat, including ordinary open bridge proofs. It conservatively
refuses closed or higher-order evaluation dependencies through them or their
declared-context wrappers. Some passive higher-order uses remain unsupported;
this syntactic check does not decide arbitrary evaluation. Refusal is
operational exit 2, not a false theorem. Explicit --official runs stock --fresh
only with trusted project code; it may itself lack the required IR. There is
no silent fallback from native refusal.

operational_errors preserves failed worker exit codes and stderr, with batch or
segment identity. An unsupported native-evaluation refusal therefore remains
visible in the primary receipt. An incomplete receipt does not certify a final
axiom union for its unfinished requested closure.


## Second-review repair semantics

The native child ABI is 5 and the independent-closure identity is v7.
Old state is not reused: the executable identity and these ABI values must match.
Input inventories bind existing exported/server/private parts and IR files,
including the absence of optional parts. If .ir.sig is present, the same
original reader also reads .ir. Missing/corrupt inputs produce operational
failure; they cannot produce complete. Stock CLI exit 1 for an artifact-load
error need not mean the mathematical proposition is false.

An original import-context rejection returns verification exit 1, including
the import-only context path. An official checker exit 1 is propagated as 1 with
execution_path: official-leanchecker and its actual per-root result; its limited
coverage is unchanged. Other nonzero tool statuses remain operational exit 2. A receipt never lists the same module in accepted and
rejected, and successful per-module evidence excludes rejected names.

project_dirty includes tracked changes and untracked files outside the active
checkpoint directory. Only the checker's own untracked output there is excluded;
it does not write a .gitignore into the target project.

Native primitive handling is conservative and scoped to declared imports.
Direct open-parameter mentions are supported; closed and higher-order native
dependencies may be refused with 2. The stock --fresh fallback can itself lack
the IR available to stock default mode. Its selection is not a promise that a
refused native-evaluation proof will pass.
