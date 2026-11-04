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

Outputs include per-pool summary CSV, a booktabs table, a PGFPlots figure,
1,001 empirical quantiles per curve, provenance, and, after successful figure compilation, census-ready.tex.
Tectonic is optional for data/TeX generation; --tectonic compiles the figure.
Final output requires W's terminal to report complete cost measurement and
matching successful/configuration coverage. This is publication input validation,
not a new experimental threshold or a claim that the failed gate passed.

For a committed cutoff ledger, use the same command with --partial. Its
outcomes.json must retain the successful module identities, configuration units,
total_source_units and cost_measurement flag; complete may remain false.
The resulting paper macros say partial observed subset and report the frame,
successful native count, configuration count and units without completed costs.
CPU sums and quantiles describe successful observed modules only, separately
for P/E; unsuccessful attempts remain in the exported observations. No missing
cost is imputed and no subset is extrapolated to a whole-library total.
This is a final partial report, distinct from --preview, which never enters
the manuscript. If no successful costs exist, the generator refuses numerical
publication; report that outcome in prose instead.

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
and fixed-resume.json retain correctness/resumption scope. Native and ablation
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

## Manuscript wiring

Run both final generators, then compile docs/paper/main.tex with Tectonic.
The manuscript includes only generated/census/census-ready.tex and
generated/system/system-ready.tex final artifacts. Preview-prefixed files
are never inputs. Without final artifacts it prints explicit pending slots,
not invented figures or missing-value macros. The census figure replaces
the generic workflow diagram, keeping two figures and two tables.

The closure deadline is 6 November 2026, 20:00 UTC. Compilation ends by 04:00; a cutoff publication uses --partial if coverage is incomplete. Library checking reports its actually verified scope by the 14:00 hard stop, with no separate PlanarPacking comparison. Paper prose and scripts are due 5 November, 12:00; numerical integration is due 6 November, 16:00. All times are UTC.

Cutoff-mode validation: the retained 20-row numerical input was combined with explicitly synthetic coverage metadata outside Git. Complete-only mode refused incomplete coverage; --partial produced the correctly labeled subset and three uncompleted units, matched independently summed P/E CPU, and compiled the distribution. Preview mode still produced no publication marker. These validation counts are not census results.
