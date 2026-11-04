# ProofServe checker

ProofServe independently rechecks a Lean project's compiled declarations with
the original Lean kernel. It visits the requested dependency closure, checks
independent declarations in parallel, and saves checkpoints for resuming a run.

The native backend currently targets Linux. On other platforms, use a Linux
container. Build with the matching Lean toolchain:
~~~sh
cd checker
lake build
.lake/build/bin/proofserve-check /path/to/project --json
~~~

Build the target project with Lake first. The command prints a JSON receipt and
saves it in the project's .proofserve directory. The receipt identifies the
actual checked modules, Lean version, Lake lock, axioms, CPU time, and wall time.
Performance results and their scope are documented in results/. A complete
release performance comparison is not yet available.

The original kernel decides whether mathematical declarations are valid.
ProofServe additionally trusts its artifact reader, checked-frontier FFI adapter,
and locally generated checkpoints. Acceptance does not mean axiom-free, free of
sorryAx, or that every source file was built. Use the audit tool to inspect source
coverage. ProofServe does not validate tactic plugins or executable code.

## Running and resuming

~~~sh
proofserve-check /path/to/project --workers 4 --checkpoint-dir /path/to/state --json
~~~

Repeat the command to resume successful segments. The default segment contains
at most 500 new modules. A nonzero --max-segments value stops after that many newly executed
segments in this invocation and returns an incomplete receipt. Saved segments
do not consume the next invocation's allowance. A live process holds a lock on
its checkpoint directory. Inputs, the checker executable, Lean identity, the Lake manifest, and checkpoint configuration
must match before earlier successes can be reused.

By default, roots are the compiled project modules under .lake/build/lib/lean.
Repeat --root MODULE, or pass --root-file FILE with one module name per line,
to select explicit roots or a custom Lake layout. Every
requested root's transitive imports are checked; missing artifacts are errors.
Uncompiled source files are not silently counted as verified.

The default worker count is the smaller of four and the available performance
core count, reflecting measured saturation in the prototype. On Linux hybrid
CPUs, default runs select available CPUs with core_type 2. Explicit worker counts
are available for evaluation. No Lean -M option is used. Memory limits belong to
the caller. Segments release newly persistent process allocations. Inside one batch,
restoring an enormous accumulated prefix can still exceed available memory.

## Large projects

When a request has more than 500 roots, the CLI checks independent batches of
at most 500 requested roots. Each batch uses a fresh process and checks new
modules in its actual dependency closure, with previously checked imports
reconstructed from local receipts. Later roots already covered by a
completed batch are skipped. Roots are ordered by dependencies before grouping. A metadata ledger, rather than every previous
kernel environment, stays in the coordinator.

~~~sh
proofserve-check /path/to/project --root-file modules.txt --closure-roots 100 --json
~~~

The root manifest avoids operating-system argument limits on large libraries.
Lower --closure-roots to reduce the union of dependencies held by one batch.
Use --closure-roots 0 to retain the original single-frontier procedure.

All roots of a batched request are inspected from compiled artifacts, including
leaf import-only modules such as Main. If the most
private module data contain no own declarations, their imports are checked in
separate closures. Before recording the empty umbrella, the original importer
and empty replay still validate its combined declared context. Source text and
file naming never establish emptiness. Contexts with conflicting imports are
not accepted.

Completed shared dependencies are reused from local original-kernel receipts
only after their artifact bytes match. The original importer loads the real
combined context; new modules still reach the kernel. This avoids repeating
shared proof checks while bounding the retained frontier by the current batch.
--replay-shared-imports disables this reuse for comparison. One dependency closure can still exceed memory; batching alone does not
solve that case. Full coverage of the 163,097-module corpus is not yet established.

Complete batches save an atomic local certificate containing the native receipt
and input identities, then remove their own regenerable prefix snapshots.
Interrupted batches retain ordinary segment checkpoints. On resume, certificates
are reused only after their recorded input files and complete part inventory
are checked again. The inventory includes .ir.sig and .ir: when a signature
exists, its IR file must also be readable by the original artifact reader. Keep the
build artifacts unchanged during a run and protect the checkpoint directory.
These are local trusted checkpoints, not portable proof objects or signatures.
Manually editing a certificate can forge acceptance or omit axioms; see
[certificate trust and validation](docs/large-library-checking.md#certificate-trust-and-validation).
Reuse receipts state this limitation explicitly.
A changed shared dependency is rejected during later-batch validation or resume.
Conflicting unions of valid import contexts use original module-local checking
for new modules rather than treating the union as a valid environment.

The --no-persistence and --no-split-fallback switches are evaluation ablations.
Each timed evaluation needs a fresh checkpoint directory. Reusing a completed
receipt is not a fresh verification run.

## Lean versions

| Toolchain | Native parallel path | Official fallback |
|---|---|---|
| 4.34.0 | Matched-toolchain build and small native contract passed | Available with a matching Lake environment |
| 4.34.1 | Matched-toolchain build and small native contract passed | Tested on the native contract |
| 4.35.0 | Matched-toolchain build and small native contract passed | Uses the project's matching official toolchain |
| 4.32.2 and 4.33.1 | Relevant exported symbol reviewed; native build not qualified | Uses the project's matching official toolchain |
| 4.36.0-rc2 | Relevant exported symbol reviewed; native build not qualified | Uses the project's matching official toolchain |

The current second-review repair has local small-fixture qualification only on 4.34.1. The other
native contract entries above predate that repair and do not qualify the new
source. The independent-closure path has so far been exercised on 4.34.1. Other rows
include earlier matched-build qualification, not a new-path whole-library test.

Source review is not ABI or native execution qualification. Rebuild with the
target SDK (for example, elan run leanprover/lean4:v4.35.0 lake build);
never reuse a native binary to decode another version's artifacts.
The source audit is in docs/version-source-audit.json.

A mismatched project version uses the project's official leanchecker --fresh
only when Lake actually selects the declared toolchain. Missing or mismatched
tools produce an explicit error; ProofServe does not install them implicitly.
--official explicitly selects that path. It prints a warning and writes
execution_path: official-leanchecker with parallel: false. Its receipt reports
accepted roots, not an invented module ledger or axiom set. This final-imported-
environment procedure is distinct from ProofServe's per-module proof checks;
official fallback results are never counted as parallel performance results.

## Trust and implementation limits

The C adapter verifies frontier ownership and inserts only values returned by
original-kernel checks. Its own token layout and the upstream private
lean_environment_add symbol require a matched SDK build. Persistent marking
happens after all prior workers have joined and before new workers begin.

Project setup through Lake and the selected toolchain are trusted local code.
This tool does not sandbox project configuration. The native adapter allows direct open-parameter mentions of Lean.reduceBool
and Lean.reduceNat. It conservatively refuses closed or higher-order calls
through those deprecated primitives and their declared-context wrappers.
This syntactic boundary is not a decision procedure for whether an arbitrary
expression will execute IR, so some passive higher-order uses remain unsupported.
Unrelated modules do not share name-based dependency labels.

The native path does not silently execute refused terms through an official
fallback. --official selects the actual stock --fresh procedure, which may also
lack the IR needed by a proof that passes the stock default procedure. It is not
a guaranteed escape from native-evaluation refusal. Inspect such a development
with its own trusted toolchain. Unsupported inputs return 2 and are not
mathematical rejections.

Checkpoint files must be local trusted outputs, protected from modification by
an adversary. Their Lean-serialized metadata uses unsafeCast. Hashes detect
ordinary stale artifacts, not malicious collisions or tampering.

Upstream unsafe and partial proof exclusions are preserved, while their
declaration names still participate in import-conflict detection. Distinct
theorem payloads use original module-local replay and stay outside the combined
frontier; dependent modules keep their original contexts. A shared-frontier
kernel failure is confirmed through original module-local replay before it can
be reported as a verification rejection. Only a successful final path emits
acceptance, and receipts do not list one module as both accepted and rejected.
Upstream Replay can itself skip a redundant imported theorem body with an equal
interface. This is not a byte-for-byte audit of every redundant serialized
proof or a proof of equivalence for arbitrary malformed metadata. Axioms retain their Lean
meaning and are reported for the accepted closure, including segregated modules.
No proof term is repaired or rewritten. This is not a demonstrated solution for
checking a 260 GiB environment inside 16 GiB.

See docs/receipt-schema.md for the API, docs/release-evaluation.md for the frozen
evaluation workflow, QUALIFICATION.md for development evidence,
and results/ for release-form evaluation. No release has been published.


The [large-library trust statement](docs/large-library-checking.md#repair-of-the-e0c92d51-review-findings)
describes editable local certificates, noncryptographic file and executable
identity, and explicit refusal of proof terms that require project native IR.
A Git revision is provenance, not a binding from source commit to built artifacts.
See the [receipt schema](docs/receipt-schema.md#input-identity-and-per-module-evidence)
for per-module evidence and the limits of module-entry counts.

The checker excludes only its own untracked checkpoint output from
project_dirty. Tracked modifications and untracked files elsewhere remain
visible; project_revision still does not bind source to built artifacts.

The native reader requires primitive quotient tags and matching names for
Quot, Quot.mk, Quot.lift and Quot.ind. Ordinary axioms or definitions under
those reserved names are unsupported, including inputs that would not use
quotient reduction. No private quotInit field is rewritten. This check does
not establish equivalence for every possible forged metadata payload.

## Known differences from stock checking

The [second-review oracle table](results/review-2628-repair/official-comparison.csv)
lists exact fixtures and scopes. Exit 2 below means an operational or unsupported
input, never acceptance or a claim that a proposition is false.

| Input | Stock default | Stock --fresh | Native ProofServe |
|---|---:|---:|---:|
| Closed primitive evaluation using imported IR | 0 | 1 | 2, unsupported |
| Higher-order use of the same primitive | 0 | 1 | 2, unsupported |
| Missing or corrupt required dependency IR | 1 | 1 | 2, artifact-load error |
| Ordinary axiom tags under reserved Quot names | 1 | 1 | 2, unsupported metadata |

On the repaired controls, unsafe conflicts, honest and swapped WellFounded
proof bodies, and incompatible empty import contexts match stock acceptance.
That is fixture qualification, not a proof of identical behavior on arbitrary
malformed artifacts. Official fallback reports roots from the stock final
imported environment; native checking reports a per-module ledger.
