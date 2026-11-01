# Chunking closed kernel computations

> Corrected direct-header census: inline inferred targets are now unknown,
> not borrowed from a preceding proof. Both earlier scanners/raw outputs remain in PVC lexical-census-v1 and
> lexical-census-v2-complete. Typed universal binders retain their colons.


M-lane evidence for the two-cost-regime characterization, on pinned
OpenAI/math `4eaee87548250b2682affda7d05d947c05554bae`, Lean 4.34.1,
and Mathlib d13f. This is a research prototype, not an enabled serving feature.

The complete, corrected lexical census finds **1,354,379** `decide +kernel` occurrences
in **5,848 / 163,097** source files. A universal-quantifier-only detector would
miss the main observed shape: **42.82%** of recovered headers are equalities
whose types the lexical pass does not resolve; another **33.90%** of all
occurrences have embedded or otherwise unresolved targets. In known interval-certificate
families, same-file type annotations nominate **277,963** record-equality sites
(**20.52%** of all occurrences). An additional224,486explicit structural forms are nominated, mostly Fin
universals. The disjoint union is502,449sites (37.10%). These are conditional
lexical candidates, not a certified global splittable fraction.

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

The initial15-cell v1 point is retained, with its unmatched output caveat.
The corrected matched-output v3 point is now complete:15/15accept, same target,
no sorry/new axiom dependency, and same-k repeated artifacts byte-identical.
Original pure checking is146ms; flat k2/4/8 is141/152/178ms, with149/238/392ms
of aggregate worker CPU. The whole native pipeline is about5.9s split versus
1.97s original; standard module reimport alone adds about3.65s.
[Full curve and limitations](v3-result.md) separate pure kernel, export/import
and whole-process costs. This is a negative result for the flat partition on
one real target, not a rejection of all chunking or a whole-module claim.

The component-preserving Grid control completed before the later >=1s priority
change could withdraw it. Local k4 kernel span falls from151ms to79ms, but
whole-process time rises from1.98s to5.84s. All15accept;27 repeated artifact
byte comparisons differ, while all27 typed ConstantInfo comparisons agree.
No further small-goal trials are planned. See components-summary.csv and
step-005-report.md.

## Actual kernel cost distribution — complete retained panel
The31-artifact native distribution completed34/34 target units, all accepted;
stock/timed sets agree for the3hot-module pairs. UMoments9 has1,164 helpers,
BarrierData41 has1,320 and Grid has4,608. None reaches1s of original kernel
CPU: maxima85.5ms/164.6ms/185.7ms. These are many-small-goal modules.

EnvelopePsiB has10large helpers among40, consuming55.782s/58.006s decision CPU.
Across the unweighted panel, >=1s helpers consume10.09% of total checker-call CPU.
Using only29available probability-sample artifacts gives a conditional weighted
28.23% of checker-call CPU (34.93% of decision CPU);13original draws are absent,
so this is **not an unbiased whole-library estimate**. Purposeful Grid and
Amplitudes are excluded from weighting. Independent replay instrumentation
and one-pair observer controls do not establish unperturbed source-compiler
timing or zero overhead.

See [complete report](step-006-report.md), declaration-distribution.csv,
declaration-histogram.csv, declaration-observer-controls.csv and
declaration-estimate.json. Barrier's measured dependency frontier supports
testing declaration parallelism, while Envelope supplies a genuine >=1s
within-goal partition target. Neither mechanism has a measured curve yet.

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
