# Changelog

## Unreleased — preparing 0.1.0

### Independent project-tool closeout

- Add project check and audit CLI delegation; preserve backend receipts,
  diagnostics, exit codes and Unix signal delivery.
- Move the former candidate JSONL check command to batch. HTTP /check and
  serve behavior remain unchanged.
- Prepare a relocatable bundle with the matching Lean 4.34.1 SDK and explicit
  matching-official-checker fallback or error for other declared versions.
  Installed archive qualification and three external-project functional previews,
  including an upstream AI-generated-proof collection, pass; final timing and
  publication remain pending.
- Retain all research data/history. The older service-only qualification
  entries below describe their original version points; current readiness is
  tracked in [prepared release notes](packaging/RELEASE_NOTES.md).


### Added

- Root-file forwarding, independent closure batches and receipt-v1 installed
  qualification, including resumed batches and three original-kernel bad-proof
  controls.
- One-command unpublished freeze preparation with separate functional-preview
  and final-timing paths, retained operational failures and small external CSVs.

- A minimal Python batch client with no runtime dependencies.
- A pinned Lean/Mathlib/REPL Docker recipe and real endpoint smoke test;
  qualification evidence is linked from the prepared release notes.
- Source package metadata, docs.rs settings, and a tag-triggered publishing
  workflow with tests and dry-run verification.
- A Linux binary build artifact in CI. This is not a published release binary.

### Changed

- Rename the four crates and executable to ProofServe. See the
  [migration table](docs/releases/0.1.0.md#source-migration) for breaking imports
  and CLI names. HTTP routes and native response schemas are preserved.
- Present user setup and API examples first; retain research details in
  [research status](docs/research-status.md).
- Detect CPU and memory capacity automatically; explicit research resource
  settings remain optional.
- Exclude research data and reports from Cargo packages and Docker context
  without deleting or relocating them.

### Existing capabilities included in this first release

- Core Kimina compatibility and typed batch/stream APIs.
- Resource admission, exact candidate reuse and all/first-success modes.
- Public Rust extension traits and native differential CI.

### Qualification status

- Complete Rust, four-crate packaging dry-run and native differential CI pass.\n- The CPU 8–9 freeze preview passes archive, three external projects and full\n  network-disabled container qualification. Retain the prior 5 GiB smoke-budget\n  failure; the corrected 8 GiB test budget does not change production defaults.
- Historical optional-adapter evidence: two bounded full-image attempts failed
  during full Mathlib preparation; raising
  the test budget to 180 seconds does not resolve it. The network-disabled small
  native batch passes acceptance, native rejection and sorry checks.
- Restore the existing fresh-REPL default in the Docker entrypoint. Matching-SDK,
  full-Mathlib image qualification passed in the recorded release-form CI; the
  optional prepared adapter is not included or claimed repaired.

No release, tag, package or image is published by this change. Tactic failure
replay remains off by default and requires backend qualification. Resource and
cache primitives are infrastructure; they are not scientific contributions by
themselves.
