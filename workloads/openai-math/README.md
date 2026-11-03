# OpenAI math: source coverage and native stratified measurements

## Current timing convention (2026-10-31 direct user decision)

All new timed runs omit the Lean -M option. Memory protection is external:
owned temporary cgroups, with resource events and sampling scope preserved.
All earlier-Mcosts/profiles are legacy methodology evidence, excluded from
new whole-library CPU estimates. No old data is deleted or retrospectively
relabeled as a native workload property.
See memory-option-methodology-26/ and the fresh noM capture documented in
W058. The original42draw frame and missing hard draws remain unchanged.


Pinned repository: [openai/math](https://github.com/openai/math/tree/4eaee87548250b2682affda7d05d947c05554bae),
commit4eaee87548250b2682affda7d05d947c05554bae (2026-10-30T00:35:35Z).
Lean4.34.1; Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612.
The root and lean licenses are Apache-2.0; third-party dependencies retain their
licenses. Every manifest dependency revision is in static-4eaee875/dependencies.csv.

## Current no-M source-cost evidence (2026-11-03)

[Source38](final-seven-20261102/collection-remaining-six-20261103T0325/source38-TrackedTestBounds/)
has38/42 completed original costs and19/21 complete strata, representing
161034/163097modules;2063(1.2649%) remain in incomplete cells.
NativeCodeAssembly,PhysicalFieldPopulationLimit and TrackedTestBounds have
actually returned under the same no-M/P0–7/shared-lock/authored-heartbeat/
three-output-facet convention. Tracked source CPU5.412330s, native elapsed
5.198824s; retirement and cgroup cleanup checked. Prerequisite E-core work
is excluded from source cost and receives no sample weight.

The full-frame observed-class min/max missing-draw scenario is
**247.55–270.24construction CPUh**, with16.85–23.91serial and22.92–32.54parallel
transferred checker CPUh. These are **assumption scenarios, not95%CIs or
actual full-library costs**. [Calibration and staircase](final-seven-20261102/collection-remaining-six-20261103T0325/source38-TrackedTestBounds/latest-staircase/)
uses complete segmented Falconer6.3124%/Mathlib8.9514% serial CPU ratios,
older computational/parallel protocols and explicit fixed-factor transfers.
Parallel wall gains do not imply lower CPU resource-hours; summed module
durations are not library makespan. Source CPU excludes separate native C
compilation/linking, package acquisition and full Lake orchestration.

The narrowed missing-cost envelope is **not total-cost precision**: the19-cell
nominal source-sampling95% interval is43.99–449.74CPUh(df2.13), excluding
missingness/calibration uncertainty and fragile under n=2/heavy tails.
[Sampling-uncertainty audit](final-seven-20261102/collection-remaining-six-20261103T0325/source38-TrackedTestBounds/sampling-uncertainty.md)
identifies two cells supplying90.02% of estimated variance.

Computation-proxy source share is21.2946–23.2461% in these missing-cost
scenarios. Static markers are not dynamic attribution. n=2 per stratum and
fixed calibration ratios still leave sampling/model uncertainty after all
originals complete. The scenario endpoints can change when a new original
changes observed class extrema. [Source35](noM-next84-source35-KL/),
[source36](final-seven-20261102/source36-NativeCodeAssembly/) and
[source37](final-seven-20261102/collection-remaining-six-20261103T0325/source37-PhysicalFieldPopulationLimit/)
remain historical evidence, not discarded or relabeled observations.
The [31target-only trusted-import replays](native-replay31/) are separate
from closure streaming. [Half-cost quotas](noM-next84-source35-KL/half-cost-quota/)
remain model counts; n2 bootstrap is not a populationCI.

Four originals remain: AllocatedForecastPrimitiveCapBound,PacketLocality,
GroundMainFinalStructuralRefinementOutputs,PreparedModularCanonicalDetectorPositive.
The finite continuation has moved to Allocated E-core prerequisites;
[Wstatus](../W-status.md) gives actual launch provenance. Do not restart
healthy raw controllers based on a historical paragraph. All native failures,
clipped-window censors and earlier budget recoveries remain in raw captures.

## Historical native evidence (separate resource conventions)

Lean4.34.1 and pinned Mathlib cache are prepared on the existing PVC.
No full-library build or globally finite CPU-hour confidence interval has
completed. Static source coverage and successful native compilation are
different measurements.

| Evidence | Scope |
|---|---|
| [Standard compiler artifacts](standard-artifact-native-a/) |26/42 original random draws;11/21 complete strata; .olean/.ilean/.c,M9216,j8,authored options|
| [Locked original cohort C](locked-original-c-results/) |543compile/1remainder censor;29/42costs,12cells; strict locked8costs,3cells|
| [Locked recovery cohort](locked-recovery-results/) |27/42native-setting costs,11/21cells;1cost strictly locked;13new compile successes|
| [Earlier target costs](partner-native-results/) |25/42 draws;10/21 cells; M8192,.olean-only; kept separate|
| [Whole Amplitudes](amplitudes-native-complete/) |180.276s at100kHB/j8 replay point|
| [Whole Grid](grid-native-complete/) |634.280s at its100kHB/j8 replay point|
| [Retained-type census](native-type-keys-363/) |363objects,42,610global Expr types; not a population total|
| [Source/helper audit](native-type-attribution/) |multi-goal expansion breaks site/check equivalence|
| [Native hardware/call-stack profiles](native-profile-five/) |5real files/20completed units; heterogeneous hotspots, no population phase weights|
| [Precision extension plan](precision-panel-plan/) |6new random draws in largest observed-variance cell; prepared,not launched|
| [Observed artifact expansion](artifact-expansion-observed/) |54.7x in A26/43.0x in B61; selected/incomplete,not population forecasts|
| [Original sampling/build model](build-planning-4eaee875/) |fixed42-draw design; static8/24-core scenarios remain assumptions|

The42primary probability targets span21source-size/import-depth/kernel-token
strata. Dependencies and purposeful stresses receive no extra population
weight. Missing/censored/budget-exceeded observations remain in the frame;
they are not zero-cost outcomes or replaced by easier sources.
[Current W state](../W-status.md) records sole active capture ownership.

At the historical -M standard-artifact point,26unchanged sources compiled without
sorry. Sum native CPU712.009670s; group471.845673s. Largest complete cell
(45,251small non-kernel/depth11–100modules) estimates74.1775CPUh with a
fragile cell-only nominal95%interval[0,623.1803]. This is not a full-build
estimate or CI. All16pending random draws and incomplete strata remain
visible in its coverage tables.

For a complete stratum, the Horvitz–Thompson total is N*samplemean, with
SRS-without-replacement finite-population variance. Nominal t intervals use
Welch–Satterthwaite degrees of freedom and assume approximately normal costs.
Two observations/heavy tails do not justify a confidence guarantee.
The [precision plan](precision-panel-plan/) specifies an independent
conditional-remainder sample rather than naively pooling an adaptive n8.

Compiler-artifact timing excludes Lake driver/setup, external caches and
linking. It is not a measured full Lake build or an8/24-core throughput run.
No native clocks/costs are pooled across HB,SDK,threads,profiling,artifact
or memory-guard points. Historical child self timers worked despite denied parent signals.
After the user-authorized privileged restart, owned-process signals work and
EPFL13733 is retired; historical censored records remain unchanged. -M is cooperative RSS checking
and1s sampled whole-tree RSS is not a kernel hard quota.

## Complete source coverage

163,097 .lean files /1,785,499,363bytes are enumerated and content-scanned.
The recursive Git tree was truncated; partial entries were discarded and
discipline subtrees enumerated completely. The old53,554/474MB observation was
a lower bound, not corpus size. Files are source blobs, not accepted proofs.

| Source group | Files | Source bytes |
|---|---:|---:|
| OAI/Combinatorics/Ramsey |444|222,614,562|
| OAI/Analysis/MutuallyUnbiased |3,386|205,200,466|
| OAI/Analysis/PlanarPacking |562|141,680,548|
| OAI/MathematicalPhysics/Transonic |466|83,494,755|
| OAI/Algorithms/SubexponentialSAT |3,977|35,509,858|

The inventory has744 source-directory groups, not744 independent Lake projects.
The publisher supplies one large library. Median file size is4,400bytes;
p99 is80,781bytes. The largest1.6%of files (2,610files) account for40.11%of
source bytes. This is a size statistic and says nothing about73%of runtime.

## Computation and tactic identifiers

Counts exclude nested comments and string literals; they are lexical
occurrences, not executed calls or checked theorem counts.

| Identifier/form | Occurrences | Files |
|---|---:|---:|
| decide (including +kernel) |1,686,012|16,766|
| decide +kernel |1,354,379|5,848|
| native_decide |0|0|
| bv_decide |0|0|
| direct ofReduceBool |0|0|
| simp |675,366|96,034|
| rfl |520,550|80,335|
| norm_num |183,572|35,471|
| omega |169,870|31,343|
| grind |650|128|

The number of theorems with transitive ofReduceBool axiom dependence is
**unknown**: zero direct tokens does not prove zero dependency through imports,
macros or generated proof terms. It requires version-matched compiled
#print axioms or equivalent native dependency inspection. The static stage did not build;
the later native subset has not established full axiom closure.

This release exposes much more source-level kernel-evaluation work than the
old arithmetic-proof corpus. The five-file native panel finds heterogeneous checker/Meta/import hotspots;
its purposeful selection cannot establish population shares. Identifier density
is not a speedup opportunity in seconds.

## Import graph and reuse exposure

The graph resolves the pinned Lake srcDir override for HodgeConjecture.
All163,097 modules are topologically ordered;370,864internal import edges.
The longest unit-weight chain has451modules. The largest same-depth layer has
9,225modules; this is structural width, not safe CPU/RSS concurrency.
The OAI root reaches130,834modules /1,397,800,941source bytes.
[Build-domain audit](default-build-scope/) finds451,008of1,354,379kernel tokens
outside that root, including allPlanarPacking/Transonic source modules.
These static counts do not measure runtime/checks.
External dependency sources/timings are excluded. The initial path-only graph
is preserved in summary.json as a superseded calculation.

25,264cross-group fingerprints cover78,473 lemma/theorem source occurrences.
These compare exact comment-masked declaration bytes using lexical boundaries.
They are candidates for inspection, not elaborated theorem equality, duplicate
kernel work, matching dependencies or safe cross-context proof reuse.
Namespace/options/attributes and dependency obligations are not certified.

## Files and reproduction

- inventory.py enumerates complete Git trees and metadata for an immutable pin.
- scan.py streams the public archive without extracting the1.785GBsource tree.
- static-4eaee875/files.csv.gz and projects.csv contain paths, sizes and groups.
- static-4eaee875/content/ contains compressed per-file metrics/import edges,
  small project/tactic/size summaries, critical path, duplicate candidates,
  complete receipt and the interrupted first-attempt log.
- [Representativeness and native sampling](../../docs/workloads-audit.md).

Use inventory.py --pin with the full revision and --out for metadata, then
scan.py --inventory with that metadata directory and --out for content metrics.
Only small derived tables are committed. Complete source journals remain on
the existing PVC; no upstream candidates are generated or rewritten.

## Execution and limitations

The first G10 attempt was interrupted by Workspace replacement after52,000
logged files, without a completed metric artifact. Its raw progress is retained.
The same Workspace/PVC later appeared on phobos-vt; W made no placement,
credential, security or quota change. A distinct static-only second attempt
completed in697.87analysis seconds with2,140,936KiB process peak RSS; these
are parser costs, not Lean verification times, and clocks are not combined.
The second attempt checkpoints1,000-file compressed journals.

The original static stage stayed below its W5GiB allocation and ran no Lean
or inference. Later partial native work uses W16GiB/8cores, a separate point.
No full project build has completed.
The only observed public workflow is lock-prs.yml; no public build CI was found
at the pin. Whole-project acceptance/axiom closure and the population1.6%/73%runtime
hypothesis remain unknown; native costs exist for the stated subset.
Review is same-chat self-review, not an independent audit.

Exact import-name-set population and limitations: [import-set-reuse](import-set-reuse/README.md).

Current source-defined cost domains and uncertainty: [cost-regimes-noM](cost-regimes-noM/README.md).
Timing submission now uses one stockflock command at a time;the former
profile-priority/nonblocking-defer hold is superseded by the direct user rule.
