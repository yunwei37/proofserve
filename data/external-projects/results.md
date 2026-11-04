# Three external projects: installed-form acceptance and cost

Review: 自审. One run per successful arm; no confidence interval or throughput claim.
All project and executable commits are recorded in projects.json, acceptance.json
and measurements.csv. These are released-form-tool measurements, not prototype results.

| Project (pinned upstream) | Local source / checked roots | Native checked dependency closure | ProofServe CPU / wall (s) | Official default CPU / wall (s) | Common-root acceptance |
|---|---:|---:|---:|---:|---|
| Newspeak (e2232d8f) | 105 / 105 | 754 | 70.556 / 35.714 | 63.663 / 32.915 | 105 / 105, equal |
| Solar EVM (f4f5c9a) | 32 / 12 | 2,368 | 135.215 / 76.078 | 10.966 / 7.116 | 12 / 12, equal |
| CrocSwap multitape (7c49fe32) | 64 / 64 | 3,166 | 211.261 / 114.783 | 103.858 / 105.221, serial pool | 64 / 64, equal |

**These columns have different proof obligations.** ProofServe checks each
compiled root and its dependency closure with the original4.34.1 kernel.
Official default replays selected local modules while trusting their imports.
Equality is of the common local acceptance set, not an official per-dependency
replay ledger. No speed ratio or claim that one accepted set is the complete
official dependency set follows. The same-protocol system matrix belongs in
checker/results/. Official --fresh has yet another final-environment and
duplicate-proof policy. Single-run costs are user-visible observations, not a
performance ranking across these different workloads.

## Input and installed-tool provenance

Sources are the three pinned subtrees in projects.json; retained source records
show no prior development measurements of these repositories. The installed
archive is703055a11b749013d7251d93bb7127bd5222a447, with the separately frozen
checker c8e7c615413819bee0931dde09450b8222c6d62a and original SDK commit
5045d0056413266e57c625dcd7c365b10e377c52. These commits remain separate; a
later release qualification does not relabel this executable. No research
prototype checker supplies the native cost cells.

CrocSwap's pinned subproject README explicitly discloses substantial OpenAI
Codex assistance. It is AI-assisted, not asserted wholly AI-generated:
[upstream disclosure](https://github.com/CrocSwap/integer-mult-bounds/blob/7c49fe32c55de02c2c873655c804b16e4c3fef0a/multitape-origin-return/README.md).
Authorship of the other two projects is not established.

All source preparation preceded timing, on E cores, with one compiler at a time.
Only artifacts reachable from declarative defaults were prepared (105,12,64
local modules respectively). CrocSwap's original dependency revisions were
preserved and its selective Mathlib cache fetched; Mathlib was not rebuilt.
Its upstream lock has an invalid, stale hyphenated package Name. One metadata
field was repaired to the quoted unchanged TOML package name, documented in
croc-setup-patch.json. Proof sources and dependency revision records are unchanged.
This case therefore required a disclosed setup repair, not an unmodified-input
claim for all three projects.

Runtime uses an extracted archive prefix, without the source repository on
the tool's search path. The compiled Lake project and its own dependencies are
required inputs. P0–7, shared flock, fresh checkpoints, four native workers,
no -M, one O native run at a time. Each native call has an11.75GiB charged-memory
cgroup with parent reserve and a1-second12GiB aggregate-RSS stop. Sampling can
overshoot; this is not a hard RSS quota. Wall includes process startup and
checkpoint work, excludes lock waits and untimed source preparation.

## The official-prefix resource failure is retained

The default official64-root batch stopped after75.043s when sampled aggregate
RSS reached13,782,695,936bytes. A diagnostic call of just the argument
MultitapeToolkit also stopped after9.015s at13,882,531,840bytes. It was not an
exact single-module call: the original source selects every module with the
target Name prefix and creates an IO task per selected module. See
official-prefix-semantics.json and its pinned official source link.
No proof rejection is inferred from either resource stop.

The completed fallback keeps the unchanged official binary, default prefix
selection and same64 roots, with LEAN_NUM_THREADS=1. It uses one process and
one runtime pool worker, not64 isolated processes. All64 verbose replay names
match the native local-root set. Peak sampled tree RSS was2,924,720,128bytes.
The runtime-default batches for Newspeak/Solar and this serialized fallback are
explicitly different configurations, so no cross-project speedup is inferred.

Original output, failed rows and successful fallback stay separate.
The interrupted timeout-parent wait4 CPU values (0.001787s and0.001578s) omit
orphaned descendant accounting after the group kill. They remain in raw columns,
while total CPU is **unknown**, not those tiny numbers. No retained cgroup CPU
counter was available after cleanup. Recovery's103.858s CPU does not include that
unknown failed CPU; its105.221s wall does not erase the failed75.043s and9.015s.
prefix-controls.csv retains both diagnostic outcomes. All successful native and
audit arms completed without a resource stop.

## What audit established

- Newspeak:105/105 local modules in the default import graph; reported-complete
  native receipt. Its declared-axiom list includes a project native_decide axiom.
- Solar:12/32 local source modules in that graph. The20 omitted files are proof
  inputs used by a custom EVM checking flow, not proven invalid or unverified by
  every possible command. This experiment did not execute that custom flow.
- CrocSwap:64/64 in the default graph; reported-complete native receipt after
  the setup repair.

Receipt axiom lists are declarations in checked closures, not minimal theorem
dependency closures. Presence of sorryAx or Lean.trustCompiler in such a list
does not by itself establish their use by a particular theorem; acceptance
does not certify an axiom-free result. The auditor explicitly reports that a
receipt lacks a source digest binding. Fresh pinned-source preparation controls
this experiment's inputs, not every future caller's source/artifact relation.
Per-module kernel CPU and per-theorem axiom dependencies remain unavailable.

Reproduce reductions with analyze.py --raw-root PATH_TO_RETAINED_CAPTURE.
Source trees, all raw stdout/stderr, lifecycle/resource records and failed
attempts remain on the PVC outside Git. After all controls retired, the
extractable SDK installation and CrocSwap selective Mathlib build cache were
removed as generated intermediates, with explicit cleanup records. The original
archive, project64 compiled outputs, pinned dependency sources and exact
selective-cache command remain; reconstruct dependencies before rerunning. The small public
CSV/JSON retains pins, scopes, costs, common acceptance IDs, resource failures,
declared axioms and source-coverage findings.
