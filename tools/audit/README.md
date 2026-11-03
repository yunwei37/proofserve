# ProofServe project audit

Read-only, Python 3.11 or newer, standard library only. No Lean process, build,
network access, package installation or Workspace-specific path is required.

```sh
python3 tools/audit/audit.py /path/to/lake-project --json audit.json
python3 tools/audit/audit.py /path/to/lake-project --build-roots MyLib Main --json -
python3 -m unittest discover -s tools/audit -v
```

The JSON schema is `proofserve-audit/v1`. The Python entry point is
`audit(project, build_roots=None, receipt=None, cost_log=None)`; O can wrap the
CLI or import it for `proofserve audit`. JSON goes to the selected file; when
`--json -` is used, stdout contains JSON and stderr contains the summary.
Exit 0 means the audit ran without source/cost parsing errors. **It never means
Lean accepted the project.** Exit 1 reports per-file/cost errors with partial
results; exit 2 reports invalid configuration/input or an I/O error.

## What it reports

- All local source files, imports, bytes and reproducible BLAKE2b provenance
  digests. Hidden build/dependency directories, symlinks and lakefile.lean are
  excluded; this is local source inventory, not compiled dependency closure.
- For declarative lakefile.toml with literal defaultTargets, lean_lib/lean_exe
  roots and supported globs, the source import closure and omitted local modules.
  Library globs default to individual roots, **not every file in the directory**,
  following Lake 4.34.1 LeanLibConfig and Glob source definitions.
- For executable lakefile.lean, custom default targets or unsupported configuration,
  default coverage is **unknown**, not an empty omissions list. The tool does not
  execute arbitrary configuration. Use --build-roots for an explicitly supplied
  root import closure; that result is not relabeled as Lake's default.
- Comment/string-masked lexical counts for decide, decide +kernel, native_decide,
  bv_decide, ofReduceBool, omega, simp, simp_all, norm_num, grind and rfl.
- The W sampling proxy: a module with any explicit decide +kernel site is labeled
  computation_certificate; otherwise ordinary_mathematics. These names identify
  a **static proxy**, not a cost prediction or a proof of absent computation.
  Generated syntax, tactic macros and all elaborated execution remain outside
  lexical accounting. Source errors and ambiguous module identities are retained.
- Costs only when supplied by an explicit source-matched log. No default
  milliseconds or runtime estimate is fabricated.

## Cost logs and compiled receipts

`--costs costs.csv` accepts these exact columns:

```csv
module,source_digest_blake2b,status,user_cpu_s,system_cpu_s,wall_s
```

Obtain the digest from a prior audit of the same source. Select one measurement
per module; duplicates, source mismatch and negative/non-finite costs are reported
as errors. Costs carry the supplied status, source filename and line, and do not
turn a rejected/unfinished proof into an accepted one. CPU is user + system;
wall time is separate. Hardware/protocol comparability remains the log producer's
responsibility.

`--receipt checker-receipt.json` currently retains the supplied JSON as
**uninterpreted compiled evidence**. The final M checker v1 adapter is pending
its schema. No axiom closure, accepted module set or native cost is inferred
until that contract is implemented. In particular, spelling ofReduceBool in a
source file does not establish transitive axiom dependence. This limitation is
visible in both JSON and summary.

## Trust and supported scope

This is an audit of source/configuration and supplied observations, not a checker
or a sandbox. It neither verifies nor rejects proof terms. It does not evaluate
Lake scripts, infer generated modules, scan dependency package source, follow
external directory symlinks or guess dynamic target configuration. A missing
receipt or executable configuration is an explicit evidence gap.

The lexical masker descends nested block comments and skips ordinary strings
and character literals. This is not Lean's parser: unusual quoted identifiers,
macro-generated imports and raw/interpolated string syntax may require compiler
evidence. Do not treat the lexical counts as exact elaborated statistics.
