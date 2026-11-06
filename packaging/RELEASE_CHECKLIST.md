# ProofServe 0.1.0 operator release checklist

Prepared only; **none of these publication commands was executed**.
Review: 自审. Run from the owning Workspace checkout on main. The operator
must approve each public effect below for the exact release commit/targets.
This document is a plan, not standing authorization to publish.

## Artifact choice and provenance — user approval required

Proposed minimum: publish the already measured local archive with its explicit
Debian13/glibc2.41 qualification scope. Do not advertise it as the Ubuntu22.04/
glibc2.35 workflow build; compatibility with older glibc is unverified.

- File: **proofserve-0.1.0-linux-x86_64.tar.gz**
- Size: **954,865,527 bytes**
- SHA-256: **5c49603e3f8e34b72b89e7959b00a74fbcc910c534da90dcb342dae01381da61**
- Local path: /workspaces/.agent-state/proofserve-o-line/freeze-e000ed62-20261105/final/prepared/proofserve-0.1.0-linux-x86_64.tar.gz
- Embedded runtime:818f74229434b888702a2d72b370cb2e07c79b36.
- Frozen checker:e000ed62bbf4b9c420bd99d0273a5d21829b4edc; Lean 4.34.1.
- Metadata dirty=false; embedded checker equals the qualified binary;
  169 qualified source files match the e000ed62 snapshot.

[Machine-readable provenance](RELEASE_ARCHIVE.json) records the actual inspection.
The SHA is publication provenance only; no new install/acceptance gate is added.
The measured tarball is immutable: latest release notes are an external sidecar.

Shell variables for the later approved operations:

~~~sh
REPO=yunwei37/proofserve
TAG=v0.1.0
RELEASE_COMMIT=$(git rev-parse main)
CAPTURE=/workspaces/.agent-state/proofserve-o-line/freeze-e000ed62-20261105/final
ARCHIVE="$CAPTURE/prepared/proofserve-0.1.0-linux-x86_64.tar.gz"
INSTALLER="$CAPTURE/prepared/proofserve-0.1.0-linux-x86_64/share/proofserve/install.py"
git show --no-patch --oneline "$RELEASE_COMMIT"
sha256sum "$ARCHIVE"
stat -c '%s bytes' "$ARCHIVE"
~~~

Before any write, the user approves the displayed full RELEASE_COMMIT, not an
unspecified future main. The local installer exists and matches the current
packaging/install.py bytes. The source tag will be newer than the measured
runtime because final results/docs were committed later; the archive keeps
its actual runtime/checker metadata. No runtime change since 818f7422 was found
in crates, Cargo manifests, launchers, audit.py or Dockerfile at preparation.

If the user instead requires the Ubuntu22.04 workflow artifact, approve that
replacement separately. It will have a different hash/size/source metadata:

~~~sh
gh workflow run release-build.yml --repo "$REPO" --ref "$RELEASE_COMMIT"
gh run list --repo "$REPO" --workflow release-build.yml --commit "$RELEASE_COMMIT"
# Set RUN_ID to the returned successful run, NEW_DIR to a new destination.
gh run download "$RUN_ID" --repo "$REPO" --name proofserve-prepared-linux-x86_64 --dir "$NEW_DIR"
sha256sum "$NEW_DIR/proofserve-0.1.0-linux-x86_64.tar.gz"
~~~

This creates public Actions logs/build artifacts, not a GitHub Release.
Complete that artifact's own qualification/provenance before choosing it;
never reuse this local package's SHA or call it already qualified at this pin.

## 1. Tag and automatic crates publication — coupled user approval required

**Existing side effect:** publish.yml and release-build.yml both match v* tag
pushes. Pushing v0.1.0 automatically starts cargo publish --workspace --locked
after source tests/dry-run, using CARGO_REGISTRY_TOKEN if configured. Tag-only
approval does not authorize registry publication. An absent token is not a safe
way to separate approvals: another authorized operator may have configured it.

Approve the tag **and all four crate uploads together before pushing**.
No workflow/secret was changed or credential inspected in this task.
Do not disable workflows, delete a secret, or force-move a tag to work around
this coupling.

User supplies the crates.io token and authorizes its repository-secret binding.
If needed, the user performs the interactive secret entry (no token in files,
arguments, Git or this checklist):

~~~sh
gh secret set CARGO_REGISTRY_TOKEN --repo "$REPO"
~~~

This stores a credential with the repository's GitHub Actions authority.
It is a separate explicit user decision, not implied by source-package dry-run.

After the combined approval:

~~~sh
set -e
git tag -a "$TAG" "$RELEASE_COMMIT" -m 'ProofServe 0.1.0'
git push origin "refs/tags/$TAG"
gh run list --repo "$REPO" --workflow publish.yml --commit "$RELEASE_COMMIT"
gh run list --repo "$REPO" --workflow release-build.yml --commit "$RELEASE_COMMIT"
~~~

Public effects: immutable version reference/commit, public workflow logs and
Actions artifacts, and **crates.io source packages** via the automatic job.
The tagged GitHub source archives include retained research data; the binary
bundle does not require downloading those archives.

### Exact crates and registry command

All four versions are 0.1.0, Apache-2.0, Rust 1.98+. Registry packages include
their declared source/test/docs/license files, not the repository's datasets
or the Lean SDK. docs.rs may build public documentation after publication.

Dependency order:

1. proofserve-core 0.1.0
2. proofserve-engine 0.1.0
3. proofserve-lean 0.1.0
4. proofserve 0.1.0

Existing automatic workflow commands:

~~~sh
cargo publish --workspace --dry-run --locked
cargo publish --workspace --locked
~~~

No manual second upload after automatic success. If the automatic job did not
publish and the user explicitly chooses manual publication instead, the exact
dependency-order commands are:

~~~sh
cargo publish -p proofserve-core --locked
cargo publish -p proofserve-engine --locked
cargo publish -p proofserve-lean --locked
cargo publish -p proofserve --locked
~~~

These require the user's token through normal Cargo credential handling.
Registry version publication is persistent; no token is supplied/used here.

## 2. GitHub Release and binary assets — separate user approval required

After the approved tag exists, publish a normal GitHub Release, using the
chosen exact archive above and its qualified installer:

~~~sh
set -e
gh release create "$TAG" --repo "$REPO" --verify-tag \
  --title 'ProofServe 0.1.0' --notes-file packaging/RELEASE_NOTES.md \
  "$ARCHIVE" "$INSTALLER"
~~~

Public effects: release page/notes, downloadable 954,865,527-byte archive and
install.py; notes disclose the SHA, build/checker pins, tested ABI scope,
partial corpus coverage and trust limits. --verify-tag prevents accidentally
creating another tag as an implicit release side effect. No release was created.
If the Ubuntu variant is chosen, replace ARCHIVE/INSTALLER and update notes
with that actual artifact's metadata before this separately approved upload.

## 3. Container registry — optional; no push in the minimum release

Proposed destination **only if the user wants and approves an image**:
**ghcr.io/yunwei37/proofserve:0.1.0**. The user approves registry namespace,
package visibility and credentials. No image registry destination is currently
configured for automatic publishing. Existing Docker evidence is functional
qualification, not an available current-tag image: old cache/layers were removed.

On the approved source commit, a future bounded local rebuild/qualification
can use the existing Dockerfile and smoke test. Temporary build state belongs
on the PVC; the builder below is removed after the test. No such build is run now.

~~~sh
set -e
IMAGE=ghcr.io/yunwei37/proofserve:0.1.0
docker buildx create --name proofserve-release-test --driver docker-container \
  --driver-opt cpuset-cpus=8-9 --driver-opt memory=10g
docker buildx build --builder proofserve-release-test --load --tag "$IMAGE" .
docker run --rm --network none --cpuset-cpus 8-9 --memory 11g \
  --entrypoint python3 "$IMAGE" /opt/container_smoke.py --self-test
docker buildx rm proofserve-release-test
# Only after the separately approved registry login and successful qualification:
docker login ghcr.io
docker push "$IMAGE"
~~~

Public effects: image layers with the Rust CLI, original Lean SDK, checker,
audit, pinned Mathlib and REPL, and the versioned tag. The operator chooses
public visibility through registry settings under that same approval.
The Dockerfile publishes no service endpoint; deploying a service is outside
this release plan. Do not call earlier preview image IDs the new release.

## 4. Verify the actual public assets after approved publication

Read back the release and install **downloaded public bytes**, not a PVC copy:

~~~sh
PUBLIC_SMOKE=$(mktemp -d)
gh release view "$TAG" --repo "$REPO"
gh release download "$TAG" --repo "$REPO" --dir "$PUBLIC_SMOKE"
python3 "$PUBLIC_SMOKE/install.py" \
  --archive "$PUBLIC_SMOKE/proofserve-0.1.0-linux-x86_64.tar.gz" \
  --prefix "$PUBLIC_SMOKE/installed"
"$PUBLIC_SMOKE/installed/bin/proofserve" --version
"$PUBLIC_SMOKE/installed/bin/proofserve" check /path/to/already-built-lake-project \
  --checkpoint-dir "$PUBLIC_SMOKE/checkpoint" --json
"$PUBLIC_SMOKE/installed/bin/proofserve" audit /path/to/already-built-lake-project \
  --receipt "$PUBLIC_SMOKE/checkpoint/receipt.json" --json "$PUBLIC_SMOKE/audit.json"
~~~

The project path is an operator-chosen built input, not a hidden Workspace
runtime dependency. Record actual public receipt/version and any platform
failure; upload completion alone is not installed-tool success.
For crates, a clean `cargo install proofserve --version 0.1.0 --locked` can verify
the public launcher; it does not install the full checker/SDK.
For an approved image, pull the published tag and repeat its network-disabled
smoke. No public smoke can be claimed before those public assets exist.

## Current handoff

- Version/schema/source pins known; frozen native/runtime and final results retained.
- Native scaling and strict costs are scoped; external common roots agree,
  but no equal-obligation official speedup is claimed.
- Corpus certified 968/162,170 only; provisional/missing scope is explicit.
- Archive choice/ABI disclosure, coupled tag+crates effects, user token binding,
  GitHub Release assets and optional image destination await user decisions.
- All commands above are **unexecuted publication steps**. No tag, release,
  registry upload, image push or announcement occurred.
