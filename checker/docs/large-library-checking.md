# Checking a library without retaining every prior kernel object

The coordinator divides requested roots into independent complete dependency
closures. Each native child uses the same original-kernel checker and starts
from an empty kernel environment. After a child completes, the coordinator keeps
its receipt and input identities, not its mathematical environment. Later
requested roots already in a completed closure are not scheduled again.

This aims to avoid a single checked kernel frontier containing the union of all
163,097 source modules; the whole-corpus run remains pending. Live proof data belong to the current batch; the global coordinator
retains module names, file identities, and receipt metadata. The relevant bound
is the largest batch dependency closure plus this metadata, not the sum of all
previous proof terms. Inside a batch, normal segment checkpoints still operate.

The default limit is 500 requested roots per batch. --closure-roots 1 minimizes
the union to one requested root's dependency closure. --closure-roots 0 preserves
the old single frontier. A single large dependency closure can still exceed
available RAM. This design alone does not solve that case, and whole-corpus
capacity is not yet established.

Common dependencies may be checked repeatedly across independent closures.
Cumulative CPU includes that work. No unchecked imported proof is accepted in
place of a kernel check merely because an earlier module was built.

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
as one ordinary root could pull the full library back into a batch. Namespace
names select inspection candidates only. A metadata child reads actual most
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
