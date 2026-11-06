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

After M and O publish the approved final results:

    python3 docs/paper/generate_system.py --matrix checker/results/fixed-cells.csv --external data/external-projects/measurements.csv --out docs/paper/generated/system

The native matrix is M's actual completed-cell schema: key, commit, dataset,
workers, repeat, arm, returncode, cpu_s and wall_s. Its fixed-acceptance.json
and fixed-resume.json retain correctness/resumption scope. Final mode requires
paper_eligible=true in the acceptance sidecar; a fixture export cannot become
paper data merely by having the fixed-cells.csv filename. Archived
fixed-failed-attempts.csv rows are retained separately from current-point rows
and excluded from medians; --failed-attempts selects an explicit ledger. Native and ablation
points require three completed repeats in final mode. Groups never mix commits.
Official default/fresh points keep their distinct ledgers; no official speedup
or product of ratios is computed.

O's CSV retains project, upstream_commit, bundle_commit, checker_commit, arm,
returncode, CPU/wall, local-root parity and accounting validity. Final mode
requires O's explicit final timing designation, in rows or timing-status.json.
Interrupted requests with unknown CPU remain blank. Default official costs
are not treated as equal-obligation closure comparisons.

Use --preview with loaded-preview-cells.csv and freeze-preview-measurements.csv
to exercise the adapters now. All outputs then use preview- prefixes and no
system-ready.tex is created. Neither old release-cells.csv nor explicitly
nonfinal rows can populate the final matrix. The script generates compact
native/external TeX tables, full median/min/max CSVs, retained nonzero attempts,
commits, correctness evidence and any provided resumption result.

Validation on 4 November: existing M loaded previews and O freeze previews
produce 22 matrix groups and nine external groups. Native/ablation rows are
separated even where M's arm column says native; the key carries the ablation.
An independently recomputed Nat.Basic median agrees. The interrupted AI request
retains unknown full CPU. Both table fragments compile, and final mode rejects
the previews. These checks do not establish a quiet host or independent checker
review; those remain conditions of the owners' actual final evaluation.

The frozen native checker is e000ed62: shared-checked is the default and
--strict-theorem-bodies selects strict original-body isolation.
The generator reads theorem_body_policy/policy, a strict_theorem_bodies flag,
or strict command-key/arm labels. Matrix points keep policy and executable
commit separate. D/S in the compact table identify default/strict; default
means that recorded executable's default, so old previews are not renamed
as the new policy. Returned strict and default points with identical
dataset/arm/workers/commit produce strict-costs.csv with separate CPU and
wall ratios of medians. Missing strict points produce no invented cost.
Historical e155 isolation numbers are never substituted for new strict costs.
The compact matrix puts worker counts in columns and CPU/wall clocks on
separate rows, leaving unmeasured configurations as dashes rather than
inventing strict points. External summaries also separate policies; the compact external table uses
default ProofServe observations.

## Manuscript wiring

Run both final generators, then compile docs/paper/main.tex with Tectonic.
The manuscript includes only generated/census/census-ready.tex and
generated/system/system-ready.tex final artifacts. Preview-prefixed files
are never inputs. Without final artifacts it prints explicit pending slots,
not invented figures or missing-value macros. The census figure replaces
the generic workflow diagram, keeping two figures and two tables.

The closure target is 6 November 2026, 20:00 UTC. W has retired all runnable,
non-deferred work without an early-stop cutoff. M runs the final matrix after actual
retirement/quiet, then O external timing, then M checks built artifacts. The checking
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
group, not imputation for an unmeasured module. System tables still await
M/O's final approved results.
