# Portable release preparation

Nothing here tags, uploads to crates.io, creates a GitHub Release or publishes
an image. Publication is an operator action after qualification.

## Runtime

Linux x86_64, compatible GNU libc and Python3.11+. The prepared release workflow
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
with the same4.34.1 SDK; this compatibility must pass the real image test.
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
