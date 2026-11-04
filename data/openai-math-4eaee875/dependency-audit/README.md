# Pinned dependency and build-context audit

Static preparation only, CPU 8–9. No full census, P-core lock, pin changes or
new cost measurement. The failed census gate remains failed.

All 163,097 source files are now present. Rechecking the same 3,528 external
import names against the captured search paths still finds **38 missing
compiled imports**, affecting **7,754 source units** through the corpus DAG.
The remaining 155,343 units have no missing external artifact in that captured
path; their internal dependencies still need building. This is not a count
of successful or proven-buildable modules.

Every one of the 38 imports has available fixed-pin source evidence:
26 package source files (five require nondefault srcDir), and 12 files supplied
by the corpus's pinned compatibility patches. Package ancestry was queried
for the 26 source files; patch ancestry for the other 12 is recorded separately.
No replacement pin/source was used. For example, ClassFieldTheory uses Lean4/
as srcDir; BernoulliRegular is vendored in AINTLIB at
projects/FltRegularBernoulli/. A root-path-only lookup falsely misses those.
Standalone upstream toolchains/manifests do not override the corpus's
Lean 4.34.1 root manifest: its own 24 compatibility patches are part of the
declared root build context.

The complete upstream archive contains only the root lean-toolchain,
lakefile.lean and lake-manifest.json as Lake configuration files. There is
one declared Lake context, with two source roots from the root custom library
facet. HodgeConjecture helper source-root identity is retained in the CSV.
The universe also includes one lakefile.lean configuration source unit:
163,096 ordinary Lean source modules plus one configuration unit. It must not
be silently presented as an ordinary proof root in a checker receipt.

## Files for M

- module-contexts.csv.gz: exactly 163,097 source-qualified rows. Join context_id
  to build-context.json. It preserves source path, actual module name,
  source-root, toolchain, manifest, import-blocker list and source-evidence
  status. Each blocked unit lists the exact missing external imports inherited
  through its internal dependencies. Do not join only on module strings.
- missing-imports.csv: all 38 imports, owning package/pin, source or patch path,
  ancestry commit, source availability and affected-unit counts (overlapping).
- build-context.json: declared root identity, fixed manifest, patches and
  original captured compilation search path. context_export_verified=false
  is deliberate: an actual Lake environment export has not been executed.
  Configuration elaboration bootstraps 11 packages, so we did not turn a
  static audit into unbounded package acquisition/building.
- summary.json: static coverage, not native acceptance or cost.
- planning.json: planning only, excluded from paper measurement tables.

A source-compatible reference is not a successful build: **the exact number
of modules that compile under the pins remains unknown without compilation**.
All 38 blockers are missing local artifacts, not demonstrated missing source.
The 7,754 affected units can be prepared from the pinned packages/patches;
their successful compilation, transitive external closure and actual Lake
search-path order remain unverified. M must obtain the actual exported Lake
context and produced artifacts before treating these rows as checker inputs.
Do not describe the captured partial search path as a fresh Lake export.

The internal source graph is acyclic, with longest path **451 modules /
450 edges**. External-package build graphs are outside this count. Planning
uses the old 279.12 P-core sampled CPU-hour estimate only: ideal eight-P capacity
gives 34.89 hours; 22-core service scenarios give 12.69–18.61 hours if E cores
provide 1 to 1/2 P-core service. These assumptions omit setup, IO, memory
admission and DAG tails. They are neither measured wall times nor a conversion
of mixed-core census results. Weighted critical-path wall cost is unknown;
the static path length alone cannot determine it.

Evidence was collected from immutable upstream archives, the corpus's own
root Lake configuration, dependency configs/srcDir, and GitHub pinned ancestry.
Raw metadata/patches and acquisition scripts are retained on PVC under
/workspaces/.agent-state/gpu-smt-captures/workloads/dependency-audit-20261104.
No new native costs enter sample-costs.csv or the paper.
