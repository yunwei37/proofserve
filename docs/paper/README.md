# Rebuilding the six-page paper

All analysis and compilation in the shared research Workspace run on CPUs 8–9.
The scripts also run with standard Python outside that Workspace; input data are
explicit arguments, with no development-machine paths embedded.

## Census artifacts

After W publishes its final per-module CSV and complete outcomes.json:

    python3 docs/paper/generate_census.py --data data/openai-math-4eaee875/census --out docs/paper/generated/census --tectonic tectonic

The script reads module-costs.csv[.gz] or modules.csv[.gz]; use --csv for another
published filename. Required fields are module, status, pool (or cpu_class),
user_cpu_s, system_cpu_s, wall_s, source_revision and measurement_commit.
User-mode instructions may be user_instructions / instructions_user or the
active cpu_core_user/cpu_atom_user event inside counters. The active pool is
explicit; P and E CPU are never summed or converted. Successful modules are
unique; failures/interruption rows remain in the exported observations.
Summed native wall is labelled separately from machine elapsed wall.

Outputs include per-phase/per-pool summary CSV, a booktabs table, a PGFPlots figure,
1,001 empirical quantiles per curve, provenance, and, after successful figure compilation, census-ready.tex.
Tectonic is optional for data/TeX generation; --tectonic compiles the figure.
Final output requires W's exhausted full-campaign cost-measurement terminal and
matching successful/configuration/failed/blocked coverage. This is publication input validation,
not a new experimental threshold or a claim that the failed gate passed.

The two admission phases are separate reporting conditions. Supply the
published phase ledger with --phases /path/to/phases.json (default:
census/phases.json, or phases inside outcomes.json). Each phase entry names
phase (1 or 2), measured machine_wall_s, admission_policy, and optional
start_utc/end_utc and measurement_commits. A monotonic interval can instead
supply start_monotonic_s/end_monotonic_s. These are adapter field names:
if W publishes a different layout, normalize the actual published ledger
without inventing times, policy parameters or phase assignments.

Successful module rows use phase/census_phase/segment, or are assigned only
by an unambiguous published start/end interval or phase-specific measurement
commit. Legacy unphased previews remain unassigned. Final generation needs
both measured phase intervals and a phase for every successful cost;
overlapping intervals cannot be added as independent machine wall.

census-summary.csv groups phase and P/E pool. census-phases.csv retains phase
policy, clocks and attempt counts; total machine wall sums phase intervals,
including their drains/retries, while any handoff gap remains separate.
Native-module wall sums are a different clock. CPU curves separate all four
phase/pool combinations; cross-module instructions use one empirical curve
under the disclosed post-result user-mode criterion. Phase assignment does
not establish a new invariance result or remove the failed gate.

The actual separate failed-attempts.csv[.gz] ledger is read automatically,
or selected with --failed-attempts. census-failed-attempts.csv retains its
identities, interruption fields and recorded observations, but these never
enter successful-module CPU or distribution sums. Configuration/blocked
rows need no invented pool or cost. Current W field aliases marked and
default_graph retain source-proxy/coverage joins by phase and pool.

The campaign has no time cutoff. Final generation waits for its natural terminal:
full_census and cost_measurement must be true, stop must be null, and disjoint
successful/configuration/failed/blocked identities must account for the entire
source frame. W's complete field means all-native-success, not merely process
termination; genuine failed/blocked modules do not become successful.
The generator exports census-outcomes.csv with every module and its actual
classification and supplied reasons. It retains unsuccessful attempts separately.
CPU totals and distributions cover successfully costed modules; failure/blocked
costs are not invented, and no all-success total is claimed when they exist.
There is no partial-publication option. Preview mode remains validation-only.

For the actual five-module functional run (which deliberately has no costs):

    python3 docs/paper/generate_census.py --preview --preview-json data/openai-math-4eaee875/dependency-audit/controller-real-subset-fixed/attempts.json --out /path/to/preview

Preview outputs have a preview- filename prefix, produce no census-ready.tex,
and cannot replace final paper artifacts. Missing CPU/instructions stay blank;
the functional five-module data cannot validate numerical performance claims.
Existing gate data can additionally exercise numerical reduction, with --preview
and one unreplicated module/condition selection. It is never a corpus total.

Validation on 4 November: the actual five-module records yield five completed
modules and blank cost/instruction totals. Twenty unreplicated real gate rows
exercise both pools and match separate CPU and exact integer instruction sums.
Both generated PGFPlots figures compile. The same preview input is refused in
final mode, and no census-ready.tex is written. Preview artifacts/logs stay on
the research PVC outside Git and are not included in the manuscript.

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

The closure deadline is 6 November 2026, 20:00 UTC. Compilation has no cutoff and must run to completion; no deadline-selected subset is published. Library checking reports its actually verified scope by the 17:00 hard stop, with no separate PlanarPacking comparison. Paper prose and scripts are due 5 November, 12:00; numerical integration is due 6 November, 18:00. Library checking is supplementary: if no time remains after the matrix and external timing, report it as not attempted, with no invented cost or acceptance count. All times are UTC.

Completion-mode validation: the retained numerical records plus explicitly synthetic terminal categories outside Git produced an exhaustive success/configuration/failure/blocked inventory and unchanged P/E CPU sums. A stopped campaign and unattempted category were refused, the removed CLI option was refused, and preview still produced no publication marker. These validation identities and counts are not census results.

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
