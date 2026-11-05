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

## Frozen-checker functional preview

The checker pin is e000ed62bbf4b9c420bd99d0273a5d21829b4edc. Run before the
final timing window, on CPU 8–9 without the P-core lock:

    python3 packaging/freeze.py --preview --checker-commit e000ed62 \
      --lean-sysroot /path/to/lean-4.34.1 --manifest /path/to/projects.json \
      --out /path/to/new-preview

This rebuilds Rust, dry-runs packages, builds the frozen checker snapshot,
runs the existing contracts, assembles/relocates the archive, checks all three
external projects, builds the container and runs it without network. Preview
costs are ineligible for final system timing. No tag or registry upload occurs.
Uncommitted O inputs are explicitly recorded; checker source comes only from
the immutable Git snapshot, not M's live build.

Python 3.11+, Docker/buildx, Rust, the matching SDK and cgroup-v2 delegation
are maintainer build/evaluation prerequisites. Installed users need neither
the research checkout nor its paths. The archive ABI is the builder's ABI;
the Ubuntu22.04 workflow supplies the advertised GNU libc2.35 baseline.

## One-command final external timing

Only after W's complete census has retired and M has finished the quiet-machine
matrix, from committed O runtime inputs:

~~~sh
PATH=/usr/local/cargo/bin:$PATH RUSTUP_HOME=/usr/local/rustup CARGO_HOME=/usr/local/cargo CARGO_BUILD_JOBS=1 \
CARGO_TARGET_DIR=/workspaces/.agent-state/proofserve-o-line/freeze-e000ed62-20261105/cargo-target \
taskset -c 8,9 python3 packaging/freeze.py --final --checker-commit e000ed62 \
  --prepared-from /workspaces/.agent-state/proofserve-o-line/freeze-e000ed62-20261105/preview \
  --lean-sysroot /workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux \
  --manifest /workspaces/.agent-state/proofserve-o-line/freeze-e000ed62-20261105/final-manifest.json \
  --out /workspaces/.agent-state/proofserve-o-line/freeze-e000ed62-20261105/final \
  --lock /workspaces/.agent-state/gpu-smt-captures/pcore.lock \
  --results-dir data/external-projects/e000ed62-final
~~~

These are maintainer host paths, not end-user dependencies. The command requires
a completed preview for the identical checker and unchanged project manifest.
It reuses only the already qualified frozen checker build, validates its source
snapshot, rebuilds the committed Rust launcher, creates a new archive and
relocates it into a fresh installation. Existing bundle controls rerun.
Native external checks then use fresh checkpoints; interrupted previews and
their costs are never reused as final samples. Container/contract cold builds
are excluded from this **two-hour** window because they were qualified earlier.
No Docker daemon is needed for this final prepared path.

Preparation stays on E8–9. Each external cell acquires the supplied existing
P0–7 lock; the complete window is bounded to 7,200 seconds, including lock wait
and preparation. The remaining global budget is passed to the external cell,
allowing the AI closure an uninterrupted call rather than the preview's
1,740-second windows. There is no additional shorter final per-project cutoff.
Overall deadline failure retains partial output with complete false.
The three projects and their roots are not reduced to meet the bound.

Planning estimate from the completed frozen CPU8–9 preview: **95–115 minutes**
for the prepared final command. The three external cases used about 92.9 minutes
of accumulated command wall time, including the AI case's two interrupted
1,740-second windows. Fresh archive/install qualification and contingency take
the estimate above that observed sum. Full AI CPU remains unknown; this is
neither a continuous end-to-end sample nor a measured P-core speed prediction.
A quiet P-core run may be faster, but no such ratio is assumed.

No project or root set is trimmed. The cold container build and complete
source/contract qualification were moved out of the final window; this is the
necessary reduction in work, rather than weakening native closure coverage.
The global 7,200-second bound retains any failure honestly. If scheduling
evidence later puts the estimate above two hours, prepare the newly committed
archive/install qualification before the allocation; do not silently reuse an
interrupted preview checkpoint or call partial AI acceptance complete.

Both modes export small acceptance JSON and measurement CSV to --results-dir.
Official default replays common local roots and trusts imports, so those costs
are not an equal-obligation speed comparison with native full-closure checking.
No unrequested project/arm is added to the final evaluation.

A failed command retains its log and complete false in freeze.json. A preview
may resume only the same frozen runtime inputs; a final run never resumes a
partial preview. Local checkpoint certificates remain trusted state. Source
and checker commits, dirty preview status, policies and execution scopes must
remain explicit in any published result.
