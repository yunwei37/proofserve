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
1,001 empirical quantiles per curve, provenance, and census-ready.tex.
Tectonic is optional for data/TeX generation; --tectonic compiles the figure.
Final output requires W's terminal to report complete cost measurement and
matching successful/configuration coverage. This is publication input validation,
not a new experimental threshold or a claim that the failed gate passed.

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
