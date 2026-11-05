# ProofServe 0.1.0 — prepared, not published

Scope: independent Lean project checking and audit. The existing Kimina
service remains available; no service feature was added in this closeout.

**Checker source is frozen at e000ed62; the new package/container functional
preview passed.** Final quiet-machine external timing is still pending.
Older results below remain historical and cannot be relabelled as current. [Current policy and trust boundary](INTERFACES.md#frozen-checker-boundary).

## Added

- Project check/audit CLI entrypoints that preserve backend receipts,
  diagnostics, Unix signals and exit codes.
- A relocatable Linux x86_64 bundle recipe with the original matching
  Lean 4.34.1 SDK, checker, audit and a one-command installer.
- Explicit official-toolchain fallback for a different declared project version;
  an unavailable matching toolchain is an error, never an automatic migration.

## CLI migration

The former candidate JSONL check command is now batch. proofserve check PROJECT
means independent project checking. HTTP /check is unchanged.

## Historical qualification (not current freeze acceptance)

Passed: real954665072-byte archive assembly, extraction into an independent
installation prefix, project check/audit and three malformed-proof rejections.
The actual test uses a compiled two-module project, not a performance workload.
Tool sources and retained failure corrections are in qualification-local.json.

The Ubuntu22.04 portable-release workflow41725630396 also passed on commit5de37517:
source tests, source-package dry-run, native checker contracts, standalone
archive installation, project check/audit, official default/fresh controls and
three actual malformed-proof rejections. See qualification-ci.json. It uploaded
Actions build artifacts only; it did not create a public release or registry upload.

Passed: complete Docker image build and network-disabled self-test on11835a92
(run41724086160), with the same 4.34.1 SDK, Mathlib and rebuilt REPL. Both
full-Mathlib service imports, accepted/rejected/sorry responses, installed project
check/audit and mismatched-version error passed. Exact controls and CI-runner
observations are in qualification-container.json. The old prepared-parent timeout
is retained as a historical failure; this image uses the stock fresh REPL and
does not claim to repair or qualify that optional prepared adapter.

Passed: all three installed-tool external check/audit cases, including the publicly
AI-assisted CrocSwap case. Common local acceptance IDs match official leanchecker;
imported-proof obligations differ. CrocSwap needed a disclosed manifest-name
repair and a one-worker official runtime fallback after retained RSS stops.
See [external results](../data/external-projects/results.md). Backend malformed-proof CI also passed.
Those external defaults retain their C8 executable pin; its superseded no-split
ablation cells do not enter the replacement formal matrix. No old timing is
silently relabelled with the latest release commit.

Latest portable archive qualification41740681358 passed onadf816ae, including
actual relocation and three original-kernel rejection controls. The current
Docker qualification41740685837 also passed on the sameadf816ae source: full
Mathlib imports, accepted/rejected/sorry responses, installed project check/audit
and explicit version-mismatch rejection, with networking disabled for the final
test. Raw controls are retained alongside the earlier11835a92 image result.

Pending: same-proof-obligation performance conclusions from checker/results/.
No performance improvement over official leanchecker is advertised before
those published-form measurements are complete.

The launcher change passed11local CLI contracts (8existing lifecycle/resource
contracts,3project-dispatch contracts). They are not native proof correctness
or a performance result. Raw logs remain on the research PVC.

Research data and complete Git history are retained. See repository-size.json
for pinned HEAD logical size, full reachable-history logical size and live
.git allocation; these are distinct measurements, not interchangeable
download sizes. No history rewrite, release, tag or registry upload occurred.

Rust full-workspace tests, doctests, clippy and release build passed locally. All four crates passed cargo publish --workspace --dry-run --locked. Engine CI41723961875 passed, including real original-kernel checker/resume/bad-proof and legacy service contracts. No package was uploaded.

## Freeze preparation update

The CLI forwards --root-file and --closure-roots to the original checker.
Installed-archive qualification now exercises independent closure batches,
resume, receipt-v1 integer/string types and unchanged diagnostics. A maintainer
can run packaging/freeze.py for one-command archive/container/external-project
qualification; --preview remains distinct from final system evaluation.

CI execution audit is ci-execution-audit.json. A green ordinary push does not
mean its manual-only container job ran. All publication remains pending.

The3a56405f installed-bundle preview actually passed the root-file path with
spaces, independent closure batches, resumed batches, and receipt-v1 decimal
UInt64/integer fields. Its three malformed-proof controls all reached original
kernel diagnostics and were rejected. The local workspace Rust tests, clippy,
source-package dry-run for all four crates, frozen Lean contract and20 audit
tests passed. See ci-execution-audit.json for separately verified CI execution;
six local legacy native-REPL tests remain ignored and are covered by that CI
job, not counted as local native runs.

The source-size snapshot and an actual public depth-one clone are documented
in REPOSITORY_SIZE.md. A shallow clone still occupies6.55GiB including its Git
object store; the standalone bundle avoids cloning retained research data.
Nothing was moved or removed to obtain that measurement.

The earlier 3a56405f CPU 8–9 freeze preview completed, including a full fresh image build,
network-disabled image-build controls, image export/load, and the same controls
in a standalone container with no host directory mounts. Both full-Mathlib
requests, native accepted/rejected/sorry responses, installed project check/audit
and mismatched-version error passed. Temporary builder cleanup returned 0 and
the private test daemon and its runtime processes retired. See
qualification-freeze-preview.json for source/checker pins, controls and image ID.
The image is local preparation only; nothing was pushed to a registry.

The retained first attempt hit the smoke script's5GiB RSS override at about
5.37GiB, rather than the 180-second request timeout. The corrected **test-only**
8GiB service budget passed inside the10 GiB builder and11 GiB runtime container;
the O capture tree stayed below its12 GiB ceiling. No production default was
changed. The first corrected build-time Mathlib request took about 69 seconds;
this is a functional-preview observation, not a system-performance figure.

The replacement external set is Newspeak, Solar and upstream explicitly
AI-generated samuelburbulla/proofs. All installed checks/audits and official
common-local-root comparisons completed. Its nine project roots are accepted
within a 10,753-module native closure. Two bounded preview interruptions remain
recorded; complete end-to-end AI cost is unknown. Final timing still requires
fresh checkpoints, committed checker freeze and a quiet evaluation machine.
The current archive records dirty preview inputs, not an immutable final release.

## Frozen checker update — 2026-11-05

The earlier review defects have recorded repairs; the replacement native freeze
is e000ed62bbf4b9c420bd99d0273a5d21829b4edc, child ABI 6 and independent closures
v8. Old checkpoint state requires a fresh directory. Native receipts add
theorem_body_policy: shared-checked by default, strict with
--strict-theorem-bodies; official fallback reports official-fresh.
The CLI forwards the strict flag unchanged.

Default mode proves statements in a shared kernel-checked environment. A crafted
artifact depending on another module's theorem body can be accepted even when
official original-context proof replay rejects it. The statement still follows
from checked proofs relative to reported axioms. Strict mode preserves the
supplied artifact-context controls, with the unsupported-input limits disclosed
in [INTERFACES](INTERFACES.md#frozen-checker-boundary).

Historical Grid isolation used 22.1× as many module-local replays and 2.33×
attempt CPU versus the replacement default preview. The historical run was
interrupted, and the current strict implementation has not been remeasured;
neither number is a current strict-mode or official speedup result.

Direct open-parameter native primitive mentions now work. Closed/higher-order
native evaluation can still fail explicitly; --official is not a guaranteed
IR workaround. Incomplete required artifact parts are refused and stock default
and --fresh may differ. All local checkpoints remain trusted state.

The new installed-bundle/container and external-project controls are previews,
not final quiet-machine system timing. Final external measurement follows M's
matrix and uses fresh checkpoints; the full build census is allowed to finish.
Nothing here tags, publishes to crates.io or pushes an image.

## Completed e000ed62 functional acceptance

The CPU8–9 preview finished on 2026-11-05, without the P-core lock.
[Acceptance report](FREEZE_E000ED62.md) and
[small qualification record](qualification-e000ed62-preview.json) identify the
frozen checker, dirty packaging inputs, controls, image metadata and raw path.

Passed: new archive installation/relocation; check/audit; the three existing
kernel-rejection classes; explicit version refusal; default and strict
theorem_body_policy, ABI6 and per-module/operational fields; a cold full image
build and a standalone network-disabled run without host mounts. Both container
phases exercised the same existing three bad-proof categories and strict flag.

Local Rust tests: 100 passed, 6 legacy native-REPL tests ignored; clippy, fmt,
release build and all four crate dry-runs passed. The frozen checker executed
the existing 90- and 142-command suites and core contracts; audit ran20 tests.
The frozen-source CI jobs separately executed native/checker contracts; its
container job was skipped and is not counted as this image qualification.

Newspeak, Solar and the upstream explicitly AI-generated samuelburbulla/proofs
all completed installed-tool check/audit and official common-root comparisons.
Native closures contain754 /2368 /10753 modules; official common roots
contain105 /12 /9. The equal common-root acceptance sets are not equal-obligation
full-closure performance comparisons. Solar reports20 omitted source modules.
AI required two bounded preview interruptions: its full CPU cost is unknown,
and the tail invocation is never substituted for whole-case cost.

All measured costs are previews; source/checker pins and scope accompany the
small CSV/JSON in data/external-projects/e000ed62-preview/. O's sampled owned
capture peak was7.524GiB within12GiB. Temporary builder/daemon retirement was
verified and no owned native runtime remained.

This Debian13 development archive records its actual libc in metadata; it is
not advertised as the Ubuntu22.04/GNU libc2.35 public build. The existing
release workflow builds that target. Nothing has been tagged or published.

The prepared --final command uses fresh checkpoints and a new archive install,
with one global two-hour bound and no extra shorter per-project cutoff.
Planning reserve is95–115minutes based on92.9minutes of accumulated E8–9
preview command intervals plus preparation/contingency, not a measured P-core
speed claim. Cold container/full-contract preparation is outside that window.
The final run follows the completed census and M's final matrix.
