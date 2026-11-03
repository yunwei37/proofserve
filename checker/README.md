# ProofServe native checker
Build with Lean4.34.1 on Linux: lake build in this directory.
Run .lake/build/bin/proofserve-check /path/to/lake-project --json.
The project must already have compiled artifacts. No Workspace path is compiled
into the tool. Unknown project Lean versions fail explicitly. Default roots are
compiled project modules under .lake/build/lib/lean; custom layouts require
--root MODULE. The receipt enumerates the actual checked dependency closure.
Unbuilt source files are not silently claimed verified.

Default workers=min(4,available performance cores),reflecting measured saturation.
On Linux hybrid CPUs select available core_type=2 CPUs. Explicit worker counts
are permitted for evaluation. No Lean -M is passed; resource limits are external.
--checkpoint-dir D --segment-modules N retains successful segments(default500
new modules). Repeat the command to resume. --no-persistence and
--no-split-fallback are evaluation ablations,not defaults.

## Trust
Original Lean4.34.1 kernel checks all new safe/total declarations. The artifact
reader,local checkpoint provenance and FFI frontier adapter are additional trust.
C validates owner frontier before inserting only original-kernel checked values.
Token layout and private lean_environment_add symbol pin this to4.34.1.
Unsupported versions fail explicitly. Local checkpoint files must not be modified
by an adversary. Copied O checkpoint metadata uses Lean serialization/unsafeCast.
Acceptance is not axiom-free: sorryAx and other axioms retain Lean semantics.
Unsafe/partial exclusions are reported. Extensions/plugins/executable code are
not validated. Proof terms are not repaired. Persistence occurs only between
joined waves. Segmentation bounds newly persistent allocations,not the entire
imported prefix; enormous prefixes can still exhaust memory. This is not a
demonstrated260GiB-to16GiB whole-library solution.
Implementation is under qualification; no release speed/external-project claim.
