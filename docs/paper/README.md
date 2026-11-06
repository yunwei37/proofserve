# Rebuilding the six-page paper

All analysis and compilation in the shared research Workspace run on CPUs 8–9.
The scripts also run with standard Python outside that Workspace; input data are
explicit arguments, with no development-machine paths embedded.

## Retired compilation artifacts

The cc5bcc18 publication is retired: 162,170/163,096 modules completed,
926 deferred by user, zero final failures or failed-dependency blocks.
Three physical intervals use two admission rules. No time cutoff or
whole-corpus estimate is applied.

    python3 docs/paper/generate_census.py --retired --data data/openai-math-4eaee875/census --out docs/paper/generated/census --tectonic tectonic

Input is W's retired modules.csv[.gz], summary.json, segment-totals.csv and
failed-attempts.csv[.gz]. Every executed interval ID, actual start/end and wall,
source/measurement commits, native costs and instructions remain bound.
All source identities remain in the inventory: successful, configuration,
native failure, failed-dependency blocked and deferred_by_user. An ordinary
not_attempted row cannot be published as exhausted runnable work. If the
actual final schema differs, adapt its real fields without inventing counts,
terminal clocks or scientific qualification criteria.

Every successful completion is counted, including records after the
withdrawn 01:30 and 03:00 boundaries. There is no final cutoff flag or time
clipping. CPU summaries separate P/E; census-segment-costs.csv also splits
segments. census-segments.csv retains complete retired operational intervals
including actual drain. Their sum excludes the separately recorded
transition gap; summed native-module wall is another clock. Unsuccessful
attempt CPU remains separate from successful module costs.

census-deferred-by-user.csv preserves the deferred rows;
census-outcome-summary.csv counts actual statuses separately. Keep supplied
reason, family prefix, trigger, dependency and timestamp, without inferring
status from namespace. Deferral concerns unfinished risk-family modules
and dependents; earlier successes in those namespaces remain measured.

Distributions and marker/default-graph cost shares concern successful
observed modules only, with full-frame label coverage separate. Dependency
order and memory deferral bias the subset toward less-memory-intensive
remaining work. P/E observed work supplies separate lower bounds; never
extrapolate from coverage, original42, strata or a model.

The old first-segment reference can still be reproduced independently:

    python3 docs/paper/generate_census.py --stopped --data /path/to/final-user-stopped --out /path/to/segment1 --tectonic tectonic

Only a retired campaign report emits CensusFinal=1. The historical
snapshot emits 0; --preview creates no ready marker and the real five-module
functional trial retains blank costs. Synthetic adapter fixtures exercise
scope and sum handling only; their outputs are not paper measurements.
The actual first-segment reduction and historical tests remain in evidence.md.

## System evaluation artifacts

The scoped retired matrix is publication 818f7422, native e000ed62, driver
cc5bcc18. It contains 61 returned attempts out of 71 planned, not a complete
original plan. Generate it independently while O timing is pending:

    python3 docs/paper/generate_system.py --matrix checker/results/release-e000ed62bbf4/matrix/fixed-cells.csv --matrix-only --out docs/paper/generated/system

Final matrix designation is either an explicit paper_eligible=true sidecar,
or this publication's verified retired collection-terminal handoff plus its
scoped acceptance assertions and exhaustive planned-status inventory.
An explicit paper_eligible=false fixture is refused. Incomplete original-plan
status remains false; no fictitious field is added to M's source.

Only three complete successful repetitions yield a final matrix median.
Successful under-repeated official samples retain their observed ranges and
counts but no three-repeat median. Strict Grid retains one censored timeout
and two unattempted repeats; strict-bounds.csv describes the observed timeout
relative to the matched default median, not a strict median or completed cost.
The returned final groups never mix executable, input context, workers or
policy. Archived failure rows already in the point table are not double-counted.
Expected kernel rejections and deliberate interruption retain their distinct
outcomes in retained-nonzero-attempts.csv; unattempted-cells.csv lists all ten
unrun identities.

system-table.tex shows complete native medians, with CPU and wall separate.
system-summary.csv retains counts and full ranges; scaling.csv, ablations.csv,
strict-costs.csv and strict-bounds.csv retain their exact within-tool ratios.
system-validation.json records independent arithmetic on all published points,
not independent native/correctness execution. system-provenance.json binds
publication, native/driver/input versions, acceptance, retired scope, actual
background condition and interruption data. CPU is closed native cgroup
whole-tree CPU, including the killed interruption leg.

The matrix writes matrix-ready.tex and system-metrics.tex. Table 2 is separate:
it requires external-ready.tex and remains pending until O returns final data.
After O publishes, use the same matrix and its actual measurements.csv:

    python3 docs/paper/generate_system.py --matrix checker/results/release-e000ed62bbf4/matrix/fixed-cells.csv --external /path/to/returned/measurements.csv --out docs/paper/generated/system

O must designate final timing in rows or timing-status.json. Unknown full CPU
remains blank. Its common local-root parity does not equal full-closure proof
obligations, and no official whole-ledger speed ratio is computed.
Native strict/default ratios require matching tool, input and worker settings;
old e155 previews never substitute. --preview uses preview- output names,
does not write ready markers, and cannot populate either final paper table.
The old fixture remains usable only for adapter validation.

## Manuscript wiring

Run both final generators, then compile docs/paper/main.tex with Tectonic.
The manuscript includes only generated/census/census-ready.tex and
generated/system/matrix-ready.tex and generated/system/external-ready.tex
for their separate final tables. Preview-prefixed files
are never inputs. Without final artifacts it prints explicit pending slots,
not invented figures or missing-value macros. The census figure replaces
the generic workflow diagram, keeping two figures and two tables.

The closure target is 6 November 2026, 20:00 UTC. W has retired all runnable,
non-deferred work without an early-stop cutoff. M has returned the scoped six-hour matrix; O external timing follows, then
M checks built artifacts. The checking
phase may be partial or unstarted and stops by 17:00; it is not a necessary
paper result. Root integrates actual numbers by 18:00. No PlanarPacking
comparison or missing-work estimate is added.

Policy-adapter validation: real preview rows plus explicitly synthetic strict labels exercised separate default/strict repeat groups, same-configuration CPU/wall ratios, no pairing across commits, isolated external policy rows, preview-only markers and refusal in final mode. Both table fragments compiled. These copied costs test grouping only; they are not strict-mode measurements and are not included in the paper.

The current post-census fixture export was also adapted in preview mode: both strict-key groups are recognized and the archived launch-126 row remains separate from one-observation point summaries. Final mode refuses its paper_eligible=false acceptance sidecar before considering timing medians. No fixture value is used as a real workload result.

Two-phase adapter validation uses twenty retained unreplicated gate records
with explicitly synthetic phase labels, clocks and terminal/failure metadata.
Independent per-phase/P-E CPU sums agree; two synthetic interrupted attempts
are retained but excluded from successful costs. The four-curve figure
compiles. Unassigned successful phases, overlapping wall intervals and early
stops are refused; old five-module functional inputs retain blank costs and
preview creates no ready marker. All adapter outputs stay outside Git and
none of these clocks or phase labels is a census result.

The latest physical execution registry has three interval IDs: fixed admission,
initial memory admission, and its deadline-free continuation after the old
finite boundary. There are still two admission rules. Final mode reads the
actual published interval count instead of assuming two; every cost row must
belong to its reported interval, and all transition gaps remain visible.

The current small summaries/figure and census-validation.json were independently
reduced from cc5bcc18 on CPUs 8–9. Duplicate large generated inventories remain
on PVC, not in Git. Deferred-family/trigger aliases match the published schema.
Interval 3 has no E-core successful jobs: its zero E cost is an empty observed
group, not imputation for an unmeasured module. The scoped M matrix is
integrated; only O external timing remains pending.
