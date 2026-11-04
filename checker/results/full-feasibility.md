# Whole-library feasibility before the build census

This is a static planning report and development qualification. Initial runs
used CPU 8–9 with a 16 GiB cap. The latest authorized continuation uses E cores
17–23, at most 40 GiB, and an 8 GiB node reserve. It is
not a final performance result. No P-core lease, full-corpus proof run, or final
matrix was started. The source frame is openai/math
4eaee87548250b2682affda7d05d947c05554bae, Mathlib
d13f23b723b8a846827a245b89c10fc7d3f11612, and Lean 4.34.1.

## Requested roots and contexts

W's manifest has 163,097 unique module names. There is one pinned execution
environment, with two compiler source-root mappings: 162,840 ordinary source
units and 257 nested Hodge source units. A different --root mapping is not a
second toolchain or a second independent Lake dependency environment. The
pinned Lake enumerators agree with the manifest. Context membership and the
actual requested-root files are preserved in the raw capture.

The extended static import graph has 174,537 modules and 660,205 edges. Of its
external nodes, 11,264 use source imports, 135 use retained .ilean directImports,
and 41 still lack import edges. Three of those 41 have compiled artifacts in the
frozen search path; 38 do not. This was artifact availability at the recorded planning lookup, not a claim
about subsequent W builds. Their edges remain unresolved in both cases.
These closure counts are therefore planning lower bounds for the known graph,
not evidence that all required artifacts exist.

## Grouping and repeated proof work

| Method | Batches | Largest loaded proof closure | Sum of module entries | Sum / 163,097 |
|---|---:|---:|---:|---:|
| Lexical, 500 roots, no empty expansion | 69 | 142,124 | 924,870 | 5.67 |
| Lexical, 500 roots, assumed empty umbrellas expanded | 208 | 44,660 | 2,518,486 | 15.44 |
| Lexical, 1 root, same expansion | 8,911 | 43,914 | 87,149,170 | 534.34 |
| Largest terminal closure first, 1 root | 1,714 | 43,914 | 17,061,109 | 104.61 |
| Dependency-first, 500 roots, replay all imports | 327 | 44,051 | 4,047,413 | 24.82 |
| Dependency-first, 500 roots, completed-module reuse | 327 | 44,051 | 174,537 first checks | 1.07 |

The last row still loads 4,047,413 module entries across original import
contexts. It does not reduce loading to 174,537 entries. Its largest batch has
11,244 first-time modules, rather than replaying a 44,051-module proof prefix.
The static empty-expansion model assumes 52 lexically import-only namespace
modules. Actual execution checks compiled private module data for every root,
including leaf Main modules; source text never establishes emptiness.

The existing native CPU calibrations span 0.0625–0.2309 seconds per module:
the 1,330-module Nat.Basic closure, the 10,744-module full Mathlib closure, and
the old 14,721-module SubexponentialSAT replay. These are different loaded
previews and workloads, not a fitted predictive model. Applied to lexical
500-root replay, they give 43.7–161.5 CPU hours, or 20.2 hours at ideal 8-way
speedup and 80.8 hours at an illustrative 2-way effective speedup. Thus the old
procedure is not safe to accept against a three-day operational target.

The new unique-replay model gives 3.03–11.20 CPU hours before imports, hashing,
planning, checkpoints and fallback overhead. Using the retained Nat.Basic
official-default CPU as an explicitly imperfect import/leaf proxy adds about
1.98 CPU hours, for an upper scenario of 13.17 CPU hours and 6.59 hours at
2-way effective speedup. These CPU scenarios are not upper bounds: the calibration does not represent
all expensive computation-heavy modules. This excludes heavy-tail uncertainty and the 41
unresolved external edges. It is a planning estimate, not a three-day guarantee
or an observed speedup.

## Implemented design and trust

The coordinator uses dependency-first batches. Only successful original-kernel
receipts can populate the local completed-module ledger. Before reuse, the
current closure's artifact parts must match their recorded ordinary hashes.
The stock importer loads the actual certified import context; new declarations
still reach the original kernel. Incompatible combined contexts use original
module-local checking for new modules. Shared proof bodies are not rechecked
solely to populate that context.

Receipts distinguish first module-check entries from trusted import entries.
The certificate store is trusted local checkpoint state, not a cryptographic
proof or remote attestation. An adversary who can forge this state is outside
the trust claim. Bad proofs before a first certificate, changed previously
certified dependencies, changed completed but later-unused inputs, and
unimported sibling references are covered by native negative controls.

Two real coordination defects found during qualification are preserved:
the child canonicalizes root order, so binding must compare canonical roots;
and a checkpoint following a reused base must preserve its imported context.
The latter caused a false rejection of Std.Internal.UV.TCP after a segment
boundary, with a missing NonemptyType. It is a tool failure, not a bad theorem.
The corrected writer records seed imports. The reader also restores older
successful local segments from their separately byte-validated certified base.

## Memory decision

Batching breaks accumulation of checked proof frontiers across batches. It
does not eliminate a module's real combined import context. In particular,
the lexical OAI umbrella reaches 142,124 graph nodes. Reducing --closure-roots
cannot remove that requirement.

Original-importer-only controls measured a wait4 maximum RSS of 5.954 GiB for
the 10,744-module Mathlib context and 7.283 GiB for the 13,835-module
SubexponentialSAT.Main context. Their two-point affine extrapolation to OAI is
62.415 GiB, exceeding the 53 GiB planning threshold. The old count-only
extrapolation from checked frontiers is even larger and is not an importer
measurement. Neither extrapolation establishes the actual OAI peak.

**Decision: whole-corpus capacity is not qualified.** Proof-replay work has a
bounded local-certificate design, but the largest actual import context is
still an unresolved capacity requirement. The prepared final command performs
a bounded original-importer capacity preflight on compiled-empty OAI before
starting whole-corpus proof checks. It must stop if that context does not fit.
It does not count imported proof bodies as verified during the preflight.
No matching full OAI artifact set is available yet, so this report cannot
honestly supply an actual capacity pass.

## Largest retained closure

Native outcome and acceptance comparison are recorded in
full-feasibility-qualification.json and full-feasibility-memory.csv.
The original O stream reference accepted 14,721 modules. Independently walking
the retained compiled import graph from the 3,977 target roots reaches exactly
those 14,721 modules, with no missing or unreachable frame entries. Its historic peak was
14.731 GiB in one native child; that wait4 maximum is distinct from a sampled
sum of RSS across a coordinator tree and from cgroup charged memory.

The separate O module-local reference audit did not complete: its retained
state reports 13,208 legacy references plus 1,193 later qualified entries and
a resource-budget stop at
reference-14401. A full official per-module acceptance ledger is unavailable.
It must not be inferred from the old stream's acceptance or from an official
final-map replay.

All failed, partial and resource-stopped runs are retained. None is used as a
complete capacity sample. This development run supplies functional and memory
evidence only; no duration from it enters the paper's final system table.

## One-command handoff

From the repository after W's real completion and retirement:

    python3 checker/bench/release.py /workspaces/.agent-state/gpu-smt-captures/checker-full-feasibility-20261104/final-release.json

Confirm the actual qualified W output/terminal/launch paths first. The saved
configuration currently names planned paths, not an invented completed census.
The workflow freezes a clean checker commit, executable, source tree and SDK;
binds the selected Lake artifacts to W's complete manifest; checks capacity;
then runs whole-library checking, the final fixed matrix and official controls,
and the single PlanarPacking comparison. Failed attempts remain separate, and
--retry-failed is explicit. The tiny qualification exports its own
workflow-qualification/ tables and is ineligible for performance claims.

What remains: complete W artifacts and the 41 unresolved external dependency
edges, the actual largest-context capacity result, full-corpus acceptance, the
quiet final matrix/official comparisons, and PlanarPacking. If the real largest
context exceeds available memory, the full run must remain stopped; this
implementation does not claim a bounded-memory replacement for the original
importer's entire environment.

To reproduce the static planning tables without a native build:

    taskset -c 8,9 python3 checker/bench/plan_full.py --manifest /workspaces/.agent-state/gpu-smt-captures/workloads/census-163097-20261104/manifest.json --out /workspaces/.agent-state/gpu-smt-captures/OWN-PLAN

Use a new owned output directory. The planner reads W inputs and writes only
its own tables, root lists and graph. Its source parser is static; the runtime
checker independently discovers actual compiled imports.

The current static graph has no incoming OAI edge. If its actual compiled
metadata are empty and all other requested roots complete, the maximum
verified declaration scope can include the other 163,096 source units while
OAI context compatibility remains explicitly incomplete. This is a planned
coverage expression, not a completed corpus result. See
../docs/large-library-checking.md for the existing root-file command, required
artifact checks, and the distinction between a subset native receipt and an
incomplete whole-frame coverage sidecar. No new kernel mechanism is proposed.

## Checkpoint before the authorized continuation

The 16-GiB revised run also stopped at a sampled peak of 16.033 GiB, without
OOM. It had preserved two complete batch certificates covering 11,216 modules;
it had not accepted the whole 14,721-module frame. The direct one-new-module
control completed at a sampled 6.654 GiB, so it is not a full-frame result.
No claim about an imported-extension cause is retained: the fixed SDK already
defaults loadExts to false. The temporary import refactor was removed.

The user has now authorized a continuation on E cores 17–23, at most 40 GiB,
with at least 8 GiB node memory available. It resumes the existing certificates
with the exact qualified build10 binary; no completed batch was restarted.
Its live identity and pending status are recorded in the qualification JSON.
These revised resource conditions are a separate qualification point.

The release workflow is prepared, and its real CLI PVC rejection has passed,
but its real portable end-to-end workflow qualification has not yet run.
The fixed matrix retry test uses explicit stubs and is not native evidence.
This checkpoint does not claim that either the largest frame or that workflow
has completed. Results will be added after the finite continuation retires.
