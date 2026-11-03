# ProofServe checker

ProofServe independently rechecks a Lean project's compiled declarations with
the original Lean kernel. It visits the requested dependency closure, checks
independent declarations in parallel, and saves checkpoints for resuming a run.

Build with the matching Lean toolchain:
~~~sh
cd checker
lake build
.lake/build/bin/proofserve-check /path/to/project --json
~~~

Build the target project with Lake first. The command prints a JSON receipt and
saves it in the project's .proofserve directory. The receipt identifies the
actual checked modules, Lean version, Lake lock, axioms, CPU time, and wall time.
Release performance evaluation is in progress; no release speedup is claimed yet.

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
at most 500 new modules. A nonzero --max-segments value stops a batch after that
many segments and returns an incomplete receipt. A live process holds a lock on
its checkpoint directory. Inputs, the Lake manifest, and checkpoint configuration
must match before earlier successes can be reused.

By default, roots are the compiled project modules under .lake/build/lib/lean.
Repeat --root MODULE to select explicit roots or a custom Lake layout. Every
requested root's transitive imports are checked; missing artifacts are errors.
Uncompiled source files are not silently counted as verified.

The default worker count is the smaller of four and the available performance
core count, reflecting measured saturation in the prototype. On Linux hybrid
CPUs, default runs select available CPUs with core_type 2. Explicit worker counts
are available for evaluation. No Lean -M option is used. Memory limits belong to
the caller. Segments release newly persistent process allocations, but restoring
an enormous accumulated prefix can still exceed available memory.

The --no-persistence and --no-split-fallback switches are evaluation ablations.
Each timed evaluation needs a fresh checkpoint directory. Reusing a completed
receipt is not a fresh verification run.

## Lean versions

| Toolchain | Native parallel path | Official fallback |
|---|---|---|
| 4.34.0 | Matched-toolchain build and small native contract passed | Available with a matching Lake environment |
| 4.34.1 | Matched-toolchain build and small native contract passed | Tested on the native contract |
| 4.35.0, current stable | Matched-toolchain build and small native contract passed | Uses the project's matching official toolchain |
| 4.32.2 and 4.33.1 | Relevant exported symbol reviewed; native build not qualified | Uses the project's matching official toolchain |
| 4.36.0-rc2, current prerelease | Relevant exported symbol reviewed; native build not qualified | Uses the project's matching official toolchain |

Source review is not ABI or native execution qualification. Rebuild with the
target SDK (for example, elan run leanprover/lean4:v4.35.0 lake build);\nnever reuse a native binary to decode another version's artifacts.
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

Project setup through Lake and the selected toolchain are trusted local code.\nThis tool does not sandbox project configuration.\n\nCheckpoint files must be local trusted outputs, protected from modification by
an adversary. Their Lean-serialized metadata uses unsafeCast. Hashes detect
ordinary stale artifacts, not malicious collisions or tampering.

Upstream unsafe and partial exclusions are preserved. Axioms retain their Lean
meaning and are reported for the accepted closure, including segregated modules.
No proof term is repaired or rewritten. This is not a demonstrated solution for
checking a 260 GiB environment inside 16 GiB.

See docs/receipt-schema.md for the API, QUALIFICATION.md for development evidence,
and results/ for release-form evaluation. No release has been published.
