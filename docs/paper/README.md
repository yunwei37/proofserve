# Rebuilding the six-page paper

All analysis and compilation in the shared research Workspace run on CPUs 8–9.
The scripts also run with standard Python outside that Workspace; input data are
explicit arguments, with no development-machine paths embedded.

## User-stopped observed compilation artifacts

The user stopped compilation at 128,331/163,096 executable modules; the
second phase did not execute native compilations. The earlier requirements
to finish the frame or publish a two-phase total are superseded.
Read W's formal stopped export:

    python3 docs/paper/generate_census.py --stopped --data data/openai-math-4eaee875/census --out docs/paper/generated/census --tectonic tectonic

The actual input is modules.csv[.gz] (or module-costs.csv[.gz]), summary.json,
segment-totals.csv and failed-attempts.csv[.gz]. --csv and --failed-attempts
select explicit alternatives. The CSV retains all source-unit identities,
including configuration and unfinished modules; observed successful modules
are unique. summary.json identifies the user stop, one executed segment and
no native second phase, scope counts and real final failures. The adapter
checks those counts against the inventory instead of calling a partial frame
complete. Long unfinished-dependency CSV fields are read without truncation.

Successful records require explicit P/E pool, user_cpu_s, system_cpu_s,
wall_s, source_revision, measurement_commit and user instructions
(instructions_user/user_instructions, or active PMU counters). No P/E
conversion or pooled CPU total is computed. segment-totals.csv supplies the
actual launch-to-retirement wall boundary, including drain/retry time.
Unsuccessful-attempt CPU remains separate from successful-module costs.
A resource-interrupted attempt is not a final failed module.

Outputs include observed P/E summaries, user-instruction/P-E CPU quantiles
and their two-panel figure, scope/provenance, the unmeasured inventory and
original unfinished reasons. Coverage by marker/default graph reports the
full label frame and observed/unmeasured counts separately; cost shares
use observed modules only. No inverse-coverage, sample, stratum or model
extrapolation fills missing costs. Separate observed P/E work is a lower
bound, not a full-library cost estimate or a random-sample confidence bound.
Only successful figure compilation produces census-ready.tex.

For preview validation:

    python3 docs/paper/generate_census.py --preview --preview-json data/openai-math-4eaee875/dependency-audit/controller-real-subset-fixed/attempts.json --out /path/to/preview

Preview outputs use preview- prefixes and never produce a ready marker.
The five functional modules lack costs and remain blank. Twenty retained
unreplicated gate rows plus explicitly synthetic stopped-scope metadata
validate separate P/E sums, unfinished identities, attempt/final-failure
separation and preview isolation; none supplies census numbers. Actual
128,331-row reduction was separately checked against W's retained stopped
export, including exact user-instruction integer sums. See evidence.md for
the source/provenance and formal-publication status.

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

The closure deadline is 6 November 2026, 20:00 UTC. Compilation is stopped
and will not resume under this decision. M runs the final matrix, then O
external timing, then M checks only actually built artifacts. The checking
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
