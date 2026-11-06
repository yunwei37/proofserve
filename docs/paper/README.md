# Rebuilding the six-page paper

All analysis and compilation in the shared research Workspace run on CPUs 8–9.
The scripts also run with standard Python outside that Workspace; input data are
explicit arguments, with no development-machine paths embedded.

## Cutoff-completed compilation artifacts

The latest coordinator decision stops segment 2 early. The campaign has two
admission segments; paper statistics include only native completions by
**6 November 2026, 01:30 UTC**. Final N is not the old 128,331-module snapshot.

    python3 docs/paper/generate_census.py --cutoff 2026-11-06T01:30:00Z --data data/openai-math-4eaee875/census --out docs/paper/generated/census --tectonic tectonic

The input is W's retired modules.csv[.gz], summary.json, segment-totals.csv
and failed-attempts.csv[.gz]. Module segment IDs, end_utc, source/measurement
commits, native costs and instructions remain bound. The full source inventory
includes successful, configuration, failed, blocked, deferred_by_user and
unattempted identities. A running snapshot or missing segment is not final N.
If W's final published schema differs, adapt its actual fields without
inventing terminal times or counts.

The generator retains completions/outcomes after the cutoff separately,
without adding their CPU, instructions or identities to the cutoff-success
set. Exactly-at-cutoff completion is included. Original native status and
costs survive in census-after-cutoff.csv; deferred reasons and unfinished
dependencies remain in the outcome inventory. No missing cost becomes zero.

CPU summaries keep P/E separate, while census-segment-costs.csv splits each
segment and pool. census-segments.csv retains retired operational wall,
reporting wall and post-cutoff drain. A segment ending before cutoff keeps
its recorded wall; a straddling interval uses recorded UTC start to cutoff,
with the remainder separate. The reported total sums segment reporting
intervals and excludes transition gaps. Native-module wall sums are another
clock. The early-stop decision supersedes the former 03:00 admission /
03:30 drain schedule. Neither its notification nor approximate progress
counts replace actual terminal and quiet-machine evidence for M.

User deferrals are a distinct outcome. census-deferred-by-user.csv keeps
the raw deferred rows and census-outcome-summary.csv counts each actual
status separately. The outcome inventory retains reason, family prefix,
trigger, dependency and timestamp when supplied by W; missing metadata is
left absent rather than invented. Final macros report deferred module count
separately from failure and failed-dependency blocking. Deferral concerns
the unfinished portions of risk families plus their dependents; earlier
completed modules in those namespaces remain observed.

All distributions and marker/default-graph cost shares concern cutoff-success
modules only. Full-frame label coverage is separate. This dependency-ordered,
selectively deferred subset is not random and favors less-memory-intensive
remaining modules; P/E observed-work sums are lower
bounds, never extrapolated from coverage, original42, strata or a model.

Until final cutoff returns, the historical first segment remains explicit:

    python3 docs/paper/generate_census.py --stopped --data /path/to/final-user-stopped --out /path/to/segment1 --tectonic tectonic

Its ready file sets CensusAtCutoff=0; final --cutoff sets it to 1 only for a
returned two-segment ledger. This keeps the manuscript's first-segment figure
and costs from masquerading as final cutoff N. --preview never creates a
ready marker, and the real five-module functional trial retains blank costs.

Validation: twenty real retained gate values plus synthetic segment times,
retirement metadata and deferred/missing identities exercised separate P/E
and segment sums, exactly-at-boundary inclusion, timezone equivalence, late
outcome retention, excluded transition/drain wall, missing-segment refusal
and preview isolation. The figure compiles. Synthetic values are not paper
results. The actual first-segment CSV was independently reduced against W's
retained export; exact totals and the pending formal-data provenance are in
evidence.md.

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

The closure deadline is 6 November 2026, 20:00 UTC. W continues segment 2
with a 01:30 reporting cutoff. M runs the final matrix after actual
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
