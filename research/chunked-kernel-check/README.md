# Chunking closed kernel computations

> Correction in progress (2026-11-01 UTC): the first lexical pass could borrow
> a previous explicit header for an inline inferred-target proof. The complete
> occurrence count/frame is unaffected, but its shape and record-hint ratios
> must not be used as certified target coverage. Original outputs remain in
> PVC lexical-census-v1. A direct-header-only pass is running; native helper
> type counts and native timing records are unaffected.


M-lane evidence for the two-cost-regime characterization, on pinned
OpenAI/math `4eaee87548250b2682affda7d05d947c05554bae`, Lean 4.34.1,
and Mathlib d13f. This is a research prototype, not an enabled serving feature.

The full lexical census finds **1,354,379** `decide +kernel` occurrences
in **5,848 / 163,097** source files. A universal-quantifier-only detector would
miss the main observed shape: **79.88%** of recovered headers are equalities
whose types the lexical pass does not resolve. In known interval-certificate
families, same-file type annotations nominate **321,470** record-equality sites
(**23.74%** of all occurrences). These remain conditional lexical candidates,
not a certified global splittable fraction.

Actual compiled helper types in Grid, UMoments9 and BarrierData41 contain
**7,018 / 7,092** known structurally decomposable targets. This selected hot
subset is not a representative library sample. Whole-module costs cannot
identify the time spent in each helper: the weighted results below explicitly
separate module exposure from a modeled helper allocation.

| Evidence | Files |
|---|---|
| Exact source frame, lexical counts and unresolved cases | [shape-method.md](shape-method.md), [shape-counts.csv](shape-counts.csv), [static-validation.json](static-validation.json) |
| Conditional record hints from two source families | [record-hint-summary.json](record-hint-summary.json), [record-hint-candidates.csv](record-hint-candidates.csv) |
| Actual helper types | [native-shapes.csv](native-shapes.csv), NativeCensus.lean, PVC native-panel logs |
| W's selected 31 complete module costs and explicit model | [cost-weighted-summary.json](cost-weighted-summary.json), [cost-weighted-panel.csv](cost-weighted-panel.csv) |
| Automatic real-target extraction and checked merge | generate.py, ChunkBase.lean, TargetEquivalence.lean, Driver.lean |
| Initial complete 15-cell curve, with output-boundary caveat | [step-001-report.md](step-001-report.md), grid-per-repeat.csv |
| Matched-output correction and pure-kernel instrumentation | v3-plan.json, v3-launch.json, analyze_v3.py |
| Prior work and overlap | [related-work.md](related-work.md) |

## Native prototype and acceptance boundary

The generator discovers a real Grid `PointBox.calc` equality, reads the
original record schemas, and partitions its 18 integer-field equalities into
k = 1, 2, 4, 8 closed groups. Constructor-based extensionality and a merge
theorem are checked by Lean. A separate theorem checks that the extracted
input and goal equal the original imported Grid input and goal.

Each child invokes the **unmodified C++ kernel** with checking enabled, then
exports a standard module. The final stage imports these checked modules and
kernel-checks the assembled theorem. No unchecked environment union,
`debug.skipKernelTC`, `native_decide`, sorry or new mathematical axiom is
used. The original and combined theorem dependencies are both [propext].
Clock FFI and stock initializer setup are metaprogram infrastructure; they do
not occur in the proof terms. A false-child control is rejected by the kernel.

Per-child heartbeats are finite. Aggregate heartbeat accounting equivalent
to a monolithic budget-limited request is **not implemented**; successful
target checks do not establish arbitrary timeout/resource-class equivalence.

The first 15-cell experiment is negative end-to-end (~1.85 s original versus
~5.5 s split), but the original arm did not export a final module. Preserve
that output boundary rather than presenting its ratio as matched.
V2 corrected output handling but failed ordinary import initialization after
two cells; its partial results remain on PVC. V3 fixes that setup and separates
pure kernel work, child export, normal import, final kernel check, audit and
final export. At the 00:54:53 UTC report boundary V3 had two completed accepted cells
(original and k=1, repetition1) and its next cell was waiting for the common
P-core lock. This is a partial matrix, not a completed result. Use its actual terminal and validation before
citing a corrected curve.

## Reproduction and raw data

Raw archive, per-site rows, native modules, logs, memory samples and failures:

`/workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check/`

Source scanning and metadata preparation use E8–15. All timed native cells
use P0–7 and the shared existing `pcore.lock`, without `-M`, with a
180 s self alarm, finite heartbeats and a 14 GiB sampled own-tree stop
(reserving 2 GiB within M's 16 GiB allowance). Sampling is not a hard RSS quota.
The finite matrix controller releases the common lock after each retired cell.

`classify_shapes.py` uses the pinned archive and W's exact source frame.
`refine_record_hints.py` resolves only declared record types and known
field projections in two source prefixes. `weight_costs.py` reads existing W
captures; it does not rerun them. These scripts use retained PVC paths and
are not advertised as a portable one-command library benchmark.
`analyze_v3.py` refuses incomplete matrices. It compares output bytes across
same-k repetitions; different k values intentionally have different proof
artifacts.

A later accepting result must still distinguish goal-level acceleration from
whole-module or whole-library gain. Prior work already covers parallel proof
checking, futures and certificate splitting; this directory makes no firstness
claim for those mechanisms.
