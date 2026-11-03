# ProofServe project audit

Read-only, Python 3.11 or newer, standard library only. No Lean process, build,
network access, package installation or Workspace-specific path is required.

```sh
python3 tools/audit/audit.py /path/to/lake-project --json audit.json
python3 tools/audit/audit.py /path/to/lake-project --build-roots MyLib Main --json -
python3 -m unittest discover -s tools/audit -v
```

The JSON schema is `proofserve-audit/v1`. The Python entry point is
`audit(project, build_roots=None, receipt=None, cost_log=None, lake_config=None)`; O can wrap the
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

## Executable Lake configuration

Lake itself can export evaluated declarative configuration. Supply that export
instead of trusting a regex interpretation of lakefile.lean:

```sh
# From the project directory. Choose an output that does not already exist.
lake translate-config toml /absolute/path/to/new-export.toml
python3 /path/to/proofserve/tools/audit/audit.py . --lake-config /absolute/path/to/new-export.toml --json audit.json
```

Always pass the explicit output filename: Lake's no-output form renames the
original configuration. The audit never runs this command or evaluates Lake
itself. The supplied export's path/provenance stays in the report and its
coverage is labeled supplied_declarative_config. Matching the export to the
current project/configuration is the caller's responsibility. Custom targets
that cannot be represented remain unknown. This path follows Lake 4.34.1
CLI/Main.lean translateConfig and CLI/Translate/Toml.lean; it is not a claim
that arbitrary scripts reduce to an exact build inventory.

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

`--receipt checker-receipt.json` consumes M's `schema_version=1` checker
receipt. Complete receipts report the checked compiled closure's accepted
modules, rejection events, axiom set, module hash and CPU/wall clocks.
Incomplete/rejected receipts explicitly label axioms **last successful prefix
only**; they never establish a full closure. `cpu_ns` is the current invocation
and `cumulative_segment_cpu_ns` includes reused segments, when supplied.
No per-module costs are derived from aggregate clocks.

Receipt v1 does not bind compiled evidence to the current source digest.
The JSON reports that source binding is not established; supplying an old
receipt does not certify current source. Unknown schemas remain uninterpreted,
malformed known schemas fail explicitly, and checker errors remain errors.
The adapter imports reported evidence; it does not independently certify
the checker or remove its documented trust boundary.

## Trust and supported scope

This is an audit of source/configuration and supplied observations, not a checker
or a sandbox. It neither verifies nor rejects proof terms. It does not evaluate
Lake scripts, infer generated modules, scan dependency package source, follow
external directory symlinks or guess dynamic target configuration. A missing
receipt or executable configuration is an explicit evidence gap.

The lexical masker descends nested block comments and skips ordinary strings
raw strings and character literals. This is not Lean's parser: unusual quoted identifiers,
macro-generated imports and raw/interpolated string syntax may require compiler
evidence. Do not treat the lexical counts as exact elaborated statistics.

## Native JSON compatibility evidence

The adapter accepts Lean UInt64 clock values as either unsigned JSON integers
or unsigned decimal strings. The byte-preserved real native-v1 fixture covers
M's completed 1330-module Nat.Basic closure receipt; parsing it is not a new
verification run. Official fallback receipts have accepted roots rather than a
per-module ledger, and expose neither axioms nor per-module CPU. They retain a
separate reported_official status, including operational official_failure.
The axiom set on the native path is declarations in the accepted module closure,
including segregated modules; it is not minimal per-theorem axiom dependence.

## Reported verification coverage

With a supported declarative source-root map and a native receipt, the
verification_coverage field lists local module names present in the reported
compiled ledger and local names absent from it. This is **name comparison**,
not source certification. Accepted names without a local source file may be
dependencies or stale artifacts; the audit does not guess which.

For an unevaluated executable Lake configuration, module identity is advisory
and this comparison is unknown until a declarative export is supplied.
Official fallback, unknown receipts and missing receipts have no native module
ledger, so the missing-local list remains null rather than an invented empty
list. These cases are distinguished from zero missing names.
