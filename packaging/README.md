# Portable release preparation

Nothing here tags, uploads to crates.io, creates a GitHub Release or publishes
an image. Publication is an operator action after qualification.

## Runtime

Linux x86_64, compatible GNU libc and Python 3.11+. The prepared release workflow
builds on Ubuntu22.04 (GNU libc2.35 baseline); build_libc in bundle.json records
the actual builder. The development archive was built and tested on Debian13,
so it is a local qualification artifact rather than a portability claim. The archive carries the original matching Lean
SDK, so the checker does not depend on the build Workspace, Elan, Rust or a
source checkout. A project must already have its compiled Lake artifacts.
Only the three ProofServe commands are linked into the user's bin directory.

The bundle's check entrypoint compares the declared toolchain before selecting
its embedded SDK. A different version uses the native frontend official fallback
with the project matching toolchain; missing tools fail explicitly. No SDK is
installed implicitly. Then it execs the original checker. No proof verdict is
synthesized by the installer or Rust launcher. Audit is the unmodified W tool.

## Build a prepared bundle

From committed sources, using the toolchain in checker/lean-toolchain:

    cargo build --release --locked -p proofserve
    lake -d checker build
    python3 packaging/bundle.py --rust-bin target/release/proofserve \
      --checker-bin checker/.lake/build/bin/proofserve-check \
      --lean-sysroot "$(lean --print-prefix)" --out "$HOME/proofserve-packages"

The SDK is copied with build-filesystem hardlinks when available; the tar
contains regular standalone files and relative SDK symlinks, not links to the
original SDK directory. Upstream SDK licenses are preserved. Failed/prepared
outputs are not overwritten; choose a new output directory for another build.

## Offline install and relocation test

    python3 packaging/install.py --archive /path/to/proofserve-0.1.0-linux-x86_64.tar.gz \
      --prefix "$HOME/proofserve-installed"
    "$HOME/proofserve-installed/bin/proofserve" --version
    "$HOME/proofserve-installed/bin/proofserve" check /path/to/built-project
    "$HOME/proofserve-installed/bin/proofserve" audit /path/to/built-project --json -

The installer stages on its destination filesystem, preserves older versions
and refuses to replace an unrelated existing executable. A prepared local
archive uses no network. Without --archive, it discovers an operator-published
GitHub Release asset; before a release exists that path fails explicitly.

## Container

Dockerfile derives its SDK version from checker/lean-toolchain and requires
Mathlib's declared toolchain to match. REPL v4.34.0 source is explicitly built
with the same 4.34.1 SDK; this compatibility must pass the real image test.
The unqualified prepared-parent adapter is not included. The existing service
uses its stock fresh-REPL default.

The final network-disabled image test exercises two complete Mathlib service
imports, native accepted/rejected/sorry responses, an installed project check,
audit and an unsupported declared version. Those are package correctness
controls, not performance measurements or a complete Mathlib kernel census.

## Evidence and release conditions

Use RELEASE_NOTES.md to distinguish completed checks from pending ones. The
three external-project measurements belong in data/external-projects/ and must
use this installed/release shape, with source/tool commits recorded. Prototype
research figures do not qualify the release evaluator.

The current tree and full-history size census is repository-size.json. These
are logical uncompressed blob sizes and live Git disk storage respectively,
not promised download sizes. Research inputs/history are retained unchanged.

## One-command freeze

After the census disposition is resolved and the checker is committed/frozen,
use one fresh output directory and a JSON manifest of already-built pinned
projects (name, project, source_audit, upstream_commit, optional workers and\nAI-generated attribution); see data/external-projects/final-manifest.example.json:

    python3 packaging/freeze.py --final --lock /path/to/shared-pcore.lock \
      --lean-sysroot "$(lean --print-prefix)" --manifest /path/to/projects.json \
      --out /path/to/new-freeze

This rebuilds Rust, dry-runs all crates, builds the committed checker snapshot,
assembles and installs the archive, runs the relocated-bundle kernel contracts,
rechecks the external projects, builds the pinned container and runs it without
network. No tag, release or registry upload is performed. Docker/buildx, the
matching Lean SDK and Rust are build prerequisites. Runtime users need none of
the source checkout or build paths. Archive ABI depends on the builder; use the
Ubuntu22.04 release workflow for the advertised GNU libc2.35 baseline.

Before that boundary, use the same command with --preview instead of --final
and omit --lock. Preparation and preview commands use CPU 8–9; preview external
numbers are explicitly ineligible for final system timing. Pending O edits are
recorded as dirty preview inputs, with cargo's --allow-dirty used only for
dry-run packaging, never publication. Final freeze requires committed runtime
inputs; unrelated research documentation/data can remain dirty.

A resumed preview uses --preview --resume with its original output directory\nand unchanged compiled inputs. It only continues a timed-out native invocation\nwhen another original-kernel segment completed; resource failures or a window\nwithout progress stop. Failed raw output stays intact. Final timing never resumes\nan interrupted preview. Its fresh command requires a new output directory.\n\nEach command has a retained log and exit status in freeze.json. A failed step
leaves complete and partial outputs intact and the overall result false.
Independent closure certificates are trusted local state, not portable proof
certificates. Short temporary socket aliases point to the output filesystem
and are removed on exit; captured results stay under --out.

On success the command also writes freeze-preview/final-acceptance.json and
freeze-preview/final-measurements.csv under data/external-projects; use
--results-dir to select another small-result destination. Each CSV row records
its project pin, checker/bundle commits, AI attribution, module scope and cost
arm. A successful final invocation is required before final timing eligibility.
Interrupted preview CPU remains unknown rather than zero.

This freeze driver is for the declared evaluation host: preparation/preview
uses CPU 8–9 and final external cells use the supplied P0–7 lock. It needs writable
cgroup-v2 delegation for bounded evaluation, plus Docker/buildx. Those are
maintainer-evaluation prerequisites, not requirements for installed ProofServe
users. The image smoke test uses an 8 GiB service budget inside the10 GiB builder
and11 GiB runtime test container; its older 5 GiB resource failure is retained.
The product's automatic resource defaults are unchanged. Builder retirement is
checked before the workflow reports complete; cache removal may take longer
than a small image build command.
