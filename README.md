# ProofServe

**Independent checking and coverage audit for Lean projects.** Check compiled
proof terms with the original Lean kernel, using parallel workers and resumable
local checkpoints. Audit what the project builds and what its receipt covers.

The prepared Linux bundle includes the matching Lean4.34.1 SDK, checker and
audit tool. No Rust compiler, repository clone or Workspace path is required.
Use Python3.11+ and an already-built Lake project declaring that Lean version:

~~~sh
bin/proofserve check /path/to/lake-project
bin/proofserve audit /path/to/lake-project --json -
~~~

Trust: the original Lean kernel, artifact/frontier adapter, declared axioms and
trusted local checkpoints. Acceptance does not prove an axiom-free development,
the intended specification, or a safe parser for hostile binary artifacts.

**Speed versus official leanchecker:** release-tool external evaluation is
being prepared; no numerical speed claim is made yet. Research prototypes
are not substitutes for that comparison.

Version0.1.0 bundles and containers are being qualified, **not yet published**.
Other declared toolchains use their matching official checker when available,
or fail explicitly. The bundled compiler never silently migrates a project.

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
Workers default to the available CPU allocation. Checkpointed runs can resume
on the same input; backend receipts record acceptance, rejection, axioms,
module-set identity, CPU and wall time. The source project must be built first.
Use a fresh checkpoint directory after changing input artifacts until the
backend's input-invalidation contract is qualified.

The supported bundled checker version is Lean4.34.1. An unsupported declaration
returns an explicit error rather than checking under a different compiler.
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
The full image test must pass its Mathlib service imports and installed-form
project controls before release. Earlier service-only image failures remain
in [historical qualification](docs/releases/0.1.0.md).

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
