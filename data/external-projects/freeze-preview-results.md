# Installed-tool external acceptance: freeze preview

Review: 自审. All three cases completed on CPU 8–9. These are functional
previews, not final system timings. The tested archive records source 6618e734
with dirty O preview inputs and checker 3a56405f; the controller baseline is
83f4143f. Concurrent committed changes83→6618 did not change runtime paths.
The final release must be rebuilt from committed frozen sources.

| Pinned project | Local source files | Native checked closure | Official default local roots | Common local roots agree | Static default coverage |
|---|---:|---:|---:|---|---:|
| newspeak (e2232d8f) | 105 | 754 | 105 | yes | 105/105 |
| solar (f4f5c9a1) | 32 | 2368 | 12 | yes | 12/32 |
| samuelburbulla-proofs (3042904c) | 9 | 10753 | 9 | yes | 9/9 |

All projects declare Lean 4.34.1. The installed archive's original kernel checked
complete compiled dependency closures; the original SDK's official leanchecker
replayed the named local roots while trusting imported proofs. Equality here is
**the common local-root set**, not equal full-closure proof obligations or a
speedup measurement. Native receipts and official verbose lists are the evidence.
The small machine-readable outputs are freeze-preview-acceptance.json and
freeze-preview-measurements.csv. Full receipts and raw failed outputs stay on PVC.

## AI-generated case and boundary control

[samuelburbulla/proofs](https://github.com/samuelburbulla/proofs), pinned at
3042904c5f7e96732c1ff4ac01745a8be9ae91ff, explicitly describes the collection as
“AI generated proofs of open math problems”. Nine unmodified source files built;
all nine roots and their 10,753-module closure completed native checking. Official
default accepted exactly the same nine local roots; installed audit completed.
The upstream claim is collection-level. Model, per-proof attribution and human
editing fraction are undisclosed; this is not an independent authorship audit
or a claim of full autonomy. CrocSwap's older AI-assisted case is retained but
is not used to satisfy the AI-generated criterion.

The AI request exceeded two 1740-second caller windows. Its unchanged checkpoints
then completed in a third invocation. Both timeouts are operational interruptions,
not kernel rejections. Their partial CPU accounting cannot establish the complete
request cost; derived CSV CPU totals remain blank for those calls. The last
invocation's CPU/wall and the receipt's cumulative successful-segment CPU are
different quantities, neither substituted for a fresh end-to-end measurement.
No resource or disk stop occurred. The accepted result is functional evidence;
a fresh quiet-machine run is still required for final performance figures.

The separate public nightshift-formal input pins Lean 4.28.0 and attributes its
proofs to Aristotle. Installed check returned an explicit matching-toolchain
error (exit 2); installed audit succeeded. No 4.28 toolchain was available, no
migration/download was attempted, and no proof acceptance or official-set parity
is claimed. Exact quotes, links and exit diagnostics are in ai-provenance.json;
ai-project-search.csv records searched candidates and limited-search reasons.

## Audit findings and trust

Newspeak's 105 local modules and the AI collection's nine files are covered by
static declarative defaults. Solar covers 12 of 32 local source files; 20 proof-input
files are outside the static import graph and may be consumed by its custom EVM
flow. This is a coverage distinction, not proof invalidity. A compiled receipt
reports checked module names and declared closure axioms; it does not bind the
current source bytes or provide minimal per-theorem axiom dependencies.
Declared axioms remain visible in the small acceptance JSON. Kernel acceptance
is not a claim of axiom-free proofs or correct problem specifications.

## Reproduction and final boundary

Use the three fixed pins in final-manifest.example.json with already-built inputs,
then packaging/freeze.py. The current package was extracted into an independent
prefix and qualified outside the source checkout; its installed commands and SDK,
not a development binary, were used. Current local Debian 13 binaries are not a
claim of portability to older GNU libc; the Ubuntu 22.04 release recipe supplies
the advertised baseline. No release, crates.io upload or public image was made.
Final system timing waits for the census disposition and checker freeze; it uses
fresh checkpoints and the shared P-core lock. This preview remains separately
labelled and will not be relabelled as final.

Raw run: /workspaces/.agent-state/proofserve-o-line/freeze-preparation-20261104/freeze-preview-v3.
