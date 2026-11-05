# ProofServe

**Independent checking and coverage audit for Lean projects.** Check compiled
proofs with the original Lean kernel; audit what the project actually covers.

The unpublished Linux bundle includes Lean 4.34.1, checker and audit tools.
With the prepared archive, installer and Python 3.11+, run without cloning:

~~~sh
python3 install.py --archive proofserve-0.1.0-linux-x86_64.tar.gz
~/.local/bin/proofserve check /path/to/built-lake-project
~/.local/bin/proofserve audit /path/to/built-lake-project --json -
~~~

**Trust:** original kernel, adapter, toolchain, declared axioms and protected
local checkpoints. This does not prove the specification, eliminate axioms,
sandbox project code, or safely parse arbitrary hostile binaries.

**Known default-mode difference:** a crafted artifact may be accepted while
official replay rejects its proof because it depends on another module's
theorem body. The statement still follows from kernel-checked proofs in the
checked closure. Use --strict-theorem-bodies for the tested artifact-context
agreement; unsupported native-evaluation inputs can still be refused.

**Cost:** retained Grid previews used 22.1× as many module-local replays and 2.33×
the CPU under the older strict-context strategy. This is historical evidence;
the new strict implementation has not been remeasured on Grid. [Policy data](checker/results/theorem-body-policy/).
**Speed versus official:** final same-obligation results are pending; preview
figures are not a release speed claim. [Trust and modes](packaging/INTERFACES.md).

Version 0.1.0 is prepared, not published. Other toolchains use a matching
official checker when available or fail explicitly; no silent migration occurs.

## Install without cloning

Use the prepared release archive and its installer:

~~~sh
python3 install.py --archive proofserve-0.1.0-linux-x86_64.tar.gz
~/.local/bin/proofserve check /path/to/lake-project
~~~

After the operator publishes the first release, the same installer can fetch
the matching asset automatically:

~~~sh
curl -fsSL https://raw.githubusercontent.com/yunwei37/proofserve/main/packaging/install.py | python3 -
~~~

That network command requires a published release and is not advertised as
working before one exists. Local archives install offline. Installation keeps
older versions and links only ProofServe commands; it does not replace a
system Lean or Elan installation.
[Bundle layout and build recipe](packaging/README.md) ·
[Prepared release notes](packaging/RELEASE_NOTES.md).

## Check a project

~~~sh
proofserve check ./project --workers 4 --checkpoint-dir ./project/.proofserve
~~~

The checker discovers compiled roots and checks their dependency closure.
The backend chooses its default from the visible CPU allocation. Checkpointed runs can resume
on the same input; backend receipts record acceptance, rejection, axioms,
module-set identity, CPU and wall time. The source project must be built first.
Use fresh state after an artifact, executable or policy change when the
checker reports an identity mismatch.

The supported bundled checker version is Lean 4.34.1. A different declared version uses its matching official checker when available,
otherwise returns an explicit error; the receipt identifies the execution path.
The checker's receipt format and correctness tests live in [checker/](checker/).

## Audit coverage

~~~sh
proofserve audit ./project --json audit.json --receipt ./project/.proofserve/receipt.json
~~~

The audit reports local source coverage, explicit kernel-computation syntax,
optional source-matched cost logs and recognized compiled evidence. It keeps
unknown default-build coverage and unavailable axiom/cost information explicit.
Lexical counts are not tactic executions or a kernel acceptance decision.
[Audit scope and format](tools/audit/).

## Container

The recipe pins one matching checker/SDK toolchain, Mathlib revision and REPL
source. Its public commands have the same shape:

~~~sh
docker run --rm -v "$PWD":/project proofserve:0.1.0 check /project
docker run --rm -v "$PWD":/project proofserve:0.1.0 audit /project --json -
~~~

These commands use a locally loaded prepared image; no public registry image
is claimed before publication. Builders can use docker build -t proofserve:0.1.0 .
The frozen e000ed62 preview passed a fresh image build and network-disabled
installed-form controls, including two Mathlib service imports, three existing
kernel-rejection cases, strict mode and version errors.
[Current qualification](packaging/qualification-e000ed62-preview.json).
These are functional previews with recorded dirty packaging inputs, not final
performance or an already published image. Older image results and failures
remain in [historical qualification](docs/releases/0.1.0.md).

## Existing Kimina-compatible service

~~~sh
docker run --rm -p 127.0.0.1:3000:3000 proofserve:0.1.0 serve --listen 0.0.0.0:3000
~~~

Submit batches to /check or use the existing [Python client](clients/python/).
HTTP routes and native response contracts are unchanged. An absent transport
error is not acceptance: inspect Lean messages and sorries.

In one retained miniF2F comparison at a four-core/48GiB resource point,
ProofServe was **1.24× faster** than four warm Kimina REPLs, with identical
final statuses and accepted IDs:

| 7,808 candidates | Elapsed | Accepted |
|---|---:|---:|
| Four warm Kimina REPLs | 25,176.49 s | 3,014 |
| ProofServe with Mathlib preparation | 20,323.01 s | 3,014 |

[Data and protocol](bench/lean-warm-resource/README.md) retain retry-order,
CPU-eligibility and raw-diagnostic differences. This service result is neither
an isolated COW gain nor a speed claim for the independent project checker.
No new service functionality is planned in this release.

## Source and Rust APIs

~~~sh
git clone --depth 1 https://github.com/yunwei37/proofserve.git
cd proofserve
cargo build --release --locked -p proofserve
~~~

Research data stays in this repository by design. A shallow clone omits old
history but still downloads the large current tree; use bundles or containers
for ordinary installation. [Pinned size accounting](packaging/repository-size.json)
separates logical HEAD size, reachable history and .git disk allocation.

| Component | Role |
|---|---|
| checker/ | Original-kernel checking, parallelism, checkpoints and receipt v1 |
| tools/audit/ | Source/build coverage and compiled-evidence audit |
| proofserve | Project CLI and existing HTTP/JSONL service |
| proofserve-core / engine / lean | Existing service types, resources and backends |

cargo install provides the Rust launcher/service, not the full Lean bundle.
The previous candidate JSONL check command is now batch; measure/compare remain
for retained captures. [CLI component contract](packaging/INTERFACES.md).

[Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [Apache-2.0](LICENSE) ·
[Research status](docs/research-status.md) · [Paper](docs/paper/main.tex).

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

Direct open-parameter reduceBool/reduceNat mentions are supported. Closed or
higher-order native-evaluation dependencies can be refused conservatively;
native_decide/bv_decide axioms are reported. Incomplete required module-system
parts fail explicitly, and official default/fresh can disagree on supplied
artifacts. [Policy and limits](packaging/INTERFACES.md#frozen-checker-boundary)
and [receipt schema](checker/docs/receipt-schema.md) describe these boundaries.
