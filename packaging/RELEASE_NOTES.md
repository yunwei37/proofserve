# ProofServe 0.1.0 — published GitHub Release

Review: 自审. Frozen native checker **e000ed62bbf4b9c420bd99d0273a5d21829b4edc**,
Lean **4.34.1**, ABI6 / independent-closures-v8. Measured archive runtime:
**818f74229434b888702a2d72b370cb2e07c79b36**. Later documentation commits are not
substituted as its build provenance. All finite campaigns ended; not every
planned point or requested module completed. The [GitHub Release](https://github.com/yunwei37/proofserve/releases/tag/v0.1.0)
is public with the qualified archive and install.py.

## Product and CLI migration

check PROJECT checks requested compiled-root dependency closures with the
original kernel, parallel workers, local checkpoints and receipt v1. Source
must already be built; default roots do not cover every source file.
audit PROJECT reports static coverage, explicit computation syntax, optional
supplied costs and compiled evidence; unavailable information stays explicit.
serve keeps the Kimina-compatible behavior. The former candidate JSONL check
command is now batch; no service feature was added.

Bundle: original matching SDK/checker/audit, Linux x86_64, Python 3.11+.
cargo install provides the Rust launcher/service, not the complete SDK.
Different declared Lean versions use their matching official toolchain when
available or fail explicitly. No silent migration or download occurs.

## Final native matrix

Median seconds, three completed repeats per point. Same native input ledger;
**within-tool speedups, not speedups over official leanchecker**.
Nat.Basic is a 1,330-module closure, **not all Mathlib**.

| Closure | 1-worker wall | 8-worker wall | 1→8 wall speedup | CPU, 1 / 8 |
| --- | ---: | ---: | ---: | ---: |
| Nat.Basic (1,330) | 110.809 | 65.312 | 1.697× | 110.246 / 113.455 |
| Grid (3,793) | 753.992 | 352.349 | 2.140× | 751.162 / 835.761 |
| Barrier (4,449) | 735.591 | 425.906 | 1.727× | 732.639 / 766.344 |

Nat.Basic/Grid also completed 2/4-worker points; Barrier 2/4 were not planned.
Of 71 planned cells, 61 attempts returned:10 unattempted and two incomplete.
No partial sample fills a median. [Final matrix](../checker/results/release-e000ed62bbf4/matrix/README.md), commit 818f7422.

Strict Nat.Basic at 8 workers costs **276.053 wall /283.782 CPU s**:
**4.227× wall /2.501× CPU** versus default 8. Strict Grid timed out124 after
**1,800.010 wall s**, with 1,803.564 cgroup CPU s. No strict Grid repeat completed;
the other two were not run. No completed-run Grid strict multiplier exists.

Stock default trusts imports; --fresh replays a final constant environment,
not the complete module-local proof ledger. Discovery also differs.
Their observations do not establish an equal-obligation official speedup.

## Final installed-package external evaluation

All 3 projects and 9 native/official/audit arms completed in **52.42 minutes**,
with fresh checkpoints, one worker and n=1 per arm. No interrupted preview
cost was reused.

| Project | Native closure / official roots | Native CPU / wall s | Official CPU / wall s |
| --- | ---: | ---: | ---: |
| Newspeak | 754 /105 | 109.055 /110.639 | 38.637 /38.736 |
| Solar | 2,368 /12 | 167.209 /169.321 | 5.512 /5.539 |
| samuelburbulla/proofs | 10,753 /9 | 2,481.041 /2,579.748 | 37.377 /40.993 |

All **126 common local roots** agree. **No same-obligation external speedup or
full-closure official equivalence is established**: native checks the closure;
official default trusts imported proofs.
[Final data/pins](../data/external-projects/e000ed62-final/README.md), commit 0516279d.

AI upstream says “AI generated proofs of open math problems”: a repository-wide
claim, with per-proof/model/human-editing fractions undisclosed, not an independent
authorship audit. Audit coverage: Newspeak 105/105, Solar 12/32 (20 outside the
static default graph), AI 9/9. Lexical proxies are not executions/cost estimates.
Source binding/minimal used-axiom closure are not established.

Timings used P0–7/shared lease; preparation E8–9, no Lean -M.
zettai-dev/agentsight-dev kept running; not an exclusively idle host.
The 12 GiB external policy remained; AI recorded 888 memory.max events, no OOM/kill.

## Supplementary corpus check: incomplete certified prefix

Certified **968/162,170 requested built source modules** in **15 complete
batches**, with **12,756 closure modules** including dependencies.
**161,202 requests are uncertified**. Another 271 complete-segment accepts and 217
in-flight accepts are provisional; one header has no verdict. No kernel rejection
was reported. Operational deadline exit124 keeps collection completion false.

Native cgroup cost: **16,194.749 CPU /16,530.349 wall s**, including unfinished
work; neither completed-corpus cost nor extrapolation. Requests excluded 926
user-deferred unbuilt sources and one lakefile configuration unit. The prefix
is dependency-order-dependent, not representative.
[Exact coverage](../checker/results/release-e000ed62bbf4/corpus/README.md),
commit 5f491682. A successful segment is not a completed batch receipt.

## Trust and known differences

Trust includes original kernel, adapter/toolchain, reported axioms and protected
local checkpoints. Default shared-checked can accept a crafted proof depending
on another module's theorem body that official original-context replay rejects;
the proposition follows from checked dependencies and reported axioms.
Strict matches the supplied controls, not universal hostile-artifact parity.

Local certificates/serialized environments are editable trusted state, not
portable cryptographic proofs. Noncryptographic identities detect ordinary
staleness, not forged metadata/collisions. Inputs must stay stable.
Incomplete/operational results do not certify the request; Git/source digests
do not bind source to artifacts. No sandbox for arbitrary hostile binaries.

Open-parameter reduceBool/reduceNat mentions work; closed/higher-order native
evaluation may be refused. --official is not a guaranteed IR workaround.
Incomplete required module parts are refused. Axiom fields are declaration
inventories, including sorryAx/compiler/runtime names, not minimal used-axiom
closures or sorry-free guarantees. [Boundary](INTERFACES.md#frozen-checker-boundary).

## Exact qualified archive

- File: **proofserve-0.1.0-linux-x86_64.tar.gz**
- Size: **954,865,527 bytes**
- SHA-256: **5c49603e3f8e34b72b89e7959b00a74fbcc910c534da90dcb342dae01381da61**
- Embedded Lean 4.34.1 / checker e000ed62 / runtime818f7422; dirty=false.
- Native executable equals the qualified frozen binary; 169 qualified source
  files match Git's e000ed62 snapshot.
- **Debian13/glibc2.41-qualified only**. Older-glibc compatibility is unverified.
  Ubuntu22.04 workflow output is a distinct artifact with separate provenance.

[Archive path/provenance](RELEASE_ARCHIVE.json). SHA-256 is requested publication
provenance, not a new install/acceptance gate. Embedded documentation stays
at 818f7422; these notes are its updated sidecar, not a mutated measured tarball.

## Functional qualification and publication status

Frozen archive/container preview passed relocation, check/audit, strict/default
forwarding, version refusal and all 3 existing kernel-rejection classes.
Cold image and standalone network-disabled tests included two Mathlib imports
and accepted/rejected/sorry responses. [Evidence](FREEZE_E000ED62.md).
Image caches were reclaimed; retained evidence is not an available image.

Procfs ESRCH race fixed at 7a931ad9: 102 local Rust tests, fmt/clippy, four crate
dry-runs; CI separately ran 6 native tests. Ordinary push CI skips its manual-only
container job; a green push alone does not qualify an image. Historical
passes/failures retain their pins in qualification JSONs.

The v0.1.0 annotated tag, GitHub Release and both assets are public; anonymous
download, fresh installation, version, small-project check and audit passed.
[Publication record and asset hashes](releases/v0.1.0.md).
The four crates remain unpublished because the tag-triggered upload lacked
CARGO_REGISTRY_TOKEN; no alternate credentials or workflow changes were used.
No container image or announcement was published. [Release checklist](RELEASE_CHECKLIST.md).
Research data/history stay in Git.
