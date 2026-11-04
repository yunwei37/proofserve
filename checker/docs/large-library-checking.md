# Checking a library without retaining every prior kernel object

The coordinator divides requested roots into independent complete dependency
closures. Each native child uses the same original-kernel checker in a fresh
process. Previously checked imports can be loaded from byte-bound local
certificates; new proof bodies still require original-kernel checking.
After a child completes, the coordinator keeps
its receipt and input identities, not its mathematical environment. Later
requested roots already in a completed closure are not scheduled again.

This aims to avoid a single checked kernel frontier containing the union of all
163,097 source modules; the whole-corpus run remains pending. Live proof data belong to the current batch; the global coordinator
retains module names, file identities, and receipt metadata. The relevant bound
is the largest batch dependency closure or combined original import context
plus this metadata, not the sum of all previous proof terms. Inside a batch, normal segment checkpoints still operate.

The default limit is 500 requested roots per batch. --closure-roots 1 minimizes
the union to one requested root's dependency closure. --closure-roots 0 preserves
the old single frontier. A single large dependency closure can still exceed
available RAM. This design alone does not solve that case, and whole-corpus
capacity is not yet established.

The default coordinator now reuses completed modules with matching input bytes.
Before a later batch starts, its required previously checked imports are bound
to local completed original-kernel receipts. The original importer loads their
actual combined context. New modules still reach the original kernel. A receipt
separates module_check_entries from trusted_import_entries. Reuse trusts local
certificate metadata and ordinary input hashes; it is not a cryptographic proof.

The --replay-shared-imports switch retains the earlier full-closure replay mode.
That mode can repeatedly check shared dependencies. The static planning results
show why it is unsuitable as the default whole-corpus procedure.

A new invocation validates completed certificates again. A child also compares
the bytes of reused imports in its actual closure against the recorded inputs.
A changed shared dependency between live batches cannot silently gain reuse.
If independently valid import contexts conflict when combined, the checker
falls back to original module-local checks of new modules; it does not replay
certified dependency proof bodies merely to combine unrelated contexts.

A complete batch atomically saves a local certificate with its actual native
receipt and full input identity. Only then are its own generated environment
snapshots removed. Incomplete batches keep their segment checkpoints. During
resume, the coordinator validates recorded files, using a per-invocation hash
memo for shared inputs. Builds must remain unchanged during an invocation.
This keeps the existing trust in local checkpoint state; it is not a portable
proof certificate or a cryptographic attestation.

The root-file interface accepts one module name per line. An empty root file is
an error, not a request to check only whatever artifacts happen to be available.
For the corpus run, use W's complete pinned source-module manifest. Missing
artifacts must remain errors. A receipt can be complete only when every requested
root occurs in the accepted set.

CPU 8-9 qualification covers the portable correctness contract, disjoint modules
with conflicting declaration names, root-file selection including the official
path, changed-input rejection, partial-batch resume, and already-covered roots.
A real Nat.Basic / Int.Basic pair gives the same 1,360 accepted modules, axioms,
and module hash as the single-frontier procedure. Completed snapshots are
retired, and a later resume validates the real certificate without new kernel
segments. This is functional evidence, not whole-corpus scaling evidence.

After W's gate and full build finish, first run the entire pinned manifest and
record actual coverage, CPU, wall time, peak memory, batch count, and any
operational failures. Only then run the final performance matrix and
PlanarPacking. Current preparation takes no P-core lock.

## Corpus coverage identities

The corpus number counts source units, not an unqualified set of module-name
strings. Before the full run, join W's produced artifacts to source paths and
their actual Lake toolchain, manifest, and search path. Run the public checker
separately for distinct build contexts. Nested source roots must not be silently
merged merely because their module names look alike.

Within one Lake context, --root-file names the complete intended module set.
Across contexts, coverage is keyed by the source unit and build context, not
only by module_set_hash. The checker receipt's project, toolchain, manifest, and
input identity must remain attached to each component receipt. Whole-corpus
coverage cannot be claimed from a count of whatever artifacts happen to exist.

## Empty umbrella modules

The pinned source frame contains lean/OAI.lean. Treating an import-only umbrella
as one ordinary root could pull the full library back into a batch. Every selected batch root, including an import-only Main leaf, is inspected.
A metadata child reads actual most
private ModuleData and requires both constants and constNames to be empty.

Only such compiled-empty modules can be expanded into their actual imports.
All imported modules must be checked before the umbrella is accepted. The
original upstream module-local importer and empty replay are still run to check
that the combined declared context is valid; individually valid imports can
conflict when combined. No imported proof body is rechecked in that final empty
replay, because those proofs have already been checked in the earlier closures.

The local plan records input identities for empty modules and validates them on
resume. Missing, changed, cyclic, or incompatible contexts do not produce a
complete acceptance. The importer can still need substantial memory to load a
large combined context. The practical peak is bounded by the largest active
proof batch or import-only context, plus the metadata ledger; this is not a
guarantee that every possible closure fits this machine.

Qualification includes three malformed imported theorem bodies beneath a
compiled-empty parent and an empty parent with incompatible import definitions.
Both original single-frontier and expanded checks refuse those malformed inputs.
Whole OAI capacity is not established until its actual compiled artifact and all
source-qualified dependencies are available from the census.

## Planning limits and evidence

The complete source frame has 163,097 unique resolved module names. There are
two source --root mappings (162,840 and 257 sources), with one pinned
toolchain/options/search-path environment. This is not a claim that arbitrary
Lake projects can share certificates merely because their module names match.
The later artifact binding must still match every requested source unit.

The static graph currently has 174,537 nodes, including external dependencies.
Forty-one external modules have unresolved dependency edges. Closure totals are
therefore lower bounds for that frame, not proof of input readiness. Fifty-two
namespace aggregators are lexically import-only; runtime expansion still
requires actual compiled zero-declaration metadata.

The lexical 500-root independent replay model requires 2,518,486 module-check
entries. Dependency-first grouping has 327 batches, a maximum loaded closure
of 44,051 modules, and 4,047,413 loaded module entries. It bounds first-time
modules in a batch to 11,244 in this static frame; it still repeats imports.
The completed-module design reduces first kernel replays to the unique closure,
while retaining the repeated import-loading work. Its planning model excludes
unmeasured import, input hashing, checkpoint, and context-fallback overhead.
A single large import context can still exceed memory. The 53-GiB planning
threshold is not established by a count-only extrapolation or a tiny control.

The current development step and results directory distinguish the static
model, the largest-existing-closure memory test, and final measurements. No
whole-corpus or final performance run starts during W's gate or census.

The prepared post-census workflow first loads the compiled-empty OAI umbrella
with the original importer under the same outer memory protection. This is a
capacity check, not verification of imported proof bodies. It must complete
before whole-corpus proof checking starts. The 142,124-module lexical OAI context
has no complete native capacity result yet; reducing proof replay does not make
this combined-context requirement disappear.

## Metadata lifetime

Input identity scanning runs in a short-lived child. It finishes before replay
starts, so its compacted module regions do not remain resident beside a kernel
worker. Hash ordering and identity fields are unchanged. A real 11,478-module,
32,966-part scan matched the earlier identities exactly.

Cached provenance uses ModuleData already retained by the original importer,
rather than reading a second compacted copy of every cached module. The input
scan first verifies that the import names in all artifact parts match the
exported header. An unsupported layout produces an explicit error. These are
lifetime and representation changes; no original kernel code is modified.
They do not establish the capacity of the full OAI combined import context.

## Maximum scope if the OAI context does not fit

The 62.4 GiB figure is a two-point planning extrapolation, not an observed OAI
peak. No full-corpus capacity failure is inferred from that number.

There is a useful scope between no result and a complete library verdict.
Check every other source module and its actual dependencies with the original
kernel, and leave only the compiled-empty OAI umbrella's combined import
context unverified. This does not change the kernel or replace an expensive
proof with a new certificate. A compiled-empty umbrella has no own proof body
to replay; its compatibility check is nevertheless part of full module
acceptance and must remain visible.

This scope is conditional on actual artifacts. First use the existing
--internal-module-meta interface to establish that both private constants and
constant names are empty. Source text alone is insufficient. Also inspect the
actual import graph for consumers of OAI. The current static graph has no
incoming edge to OAI, so it is a sink request rather than a dependency of the
other 163,096 source units. This static fact must be confirmed from produced
artifacts. If a proof-bearing module requires that oversized context too, it
also remains incomplete; it cannot be counted as checked.

The current CLI already supports this explicit scope through --root-file.
Create a root list containing all requested source names except the verified
empty umbrella, then run:

~~~sh
proofserve-check PROJECT --root-file all-except-OAI.txt --checkpoint-dir STATE --json
~~~

A successful native receipt is complete for that selected root set only.
Do not relabel it as a complete result for the original 163,097 requests.
Retain the original-importer context check as a separate bounded task. A
resource stop, an unattempted check, and an incompatible import context all
remain non-acceptance of that umbrella; the diagnostics distinguish them.

A coverage sidecar can express the full requested scope as follows. This is
a conditional example, not a measured result and not additional fields
already emitted by the native v1 receipt:

~~~json
{
  "scope": "whole pinned source frame",
  "status": "incomplete",
  "expected_source_units": 163097,
  "verified_source_units": 163096,
  "declaration_coverage_complete": true,
  "module_acceptance_complete": false,
  "native_subset_receipt": "checked-subset/receipt.json",
  "pending_contexts": [{
    "module": "OAI",
    "compiled_own_declarations": 0,
    "all_imported_proofs_checked": true,
    "context_status": "not_checked",
    "reason": "combined context exceeds the available resource point"
  }]
}
~~~

The numeric coverage fields and booleans may be set this way only after joining
the actual subset receipt to the complete source manifest and binding the
empty module to its current artifact bytes. If the context task has not
actually exceeded its budget, use not_attempted rather than claiming a
measured resource failure. Other rejected or pending modules must be listed
too. The umbrella never enters accepted until its original combined context
check succeeds. An incomplete whole-frame sidecar is not a full-project
verification receipt.

At present this describes the maximum planned coverage, not completed corpus
verification: W's full artifacts are not available. The frozen evaluation
driver currently stops on its failed capacity preflight; it does not silently
generate this conditional sidecar or continue with a reduced denominator.
