# Pinned dependency and actual Lake-context audit

Preparation and functional checks only. Initially CPU 8–9, migrated without
restarting existing tasks to CPU 10–16 after the latest user allocation. The whole W-lane budget was 12 GiB. No P-core lock, full-census execution, pin/source substitution, cost
measurement or paper data were introduced. The census gate remains failed.

## Actual environment

The root project's official Lean 4.34.1 `lake env` was executed successfully.
All 42 package checkout commits match the fixed root manifest. The ordered
actual LEAN_PATH has 44 entries, compared with
12 in the earlier captured partial path. The actual root path uses its own
package build directories and corpus build output, rather than the old global
Rellich/corpus artifact caches. See search-path-comparison.csv and
lake-environment.json for the exact order; paths are observed Workspace
locations for the shared checker inputs, not portable installation defaults.

The pinned corpus declares **23 actual .patch files**, plus one patches/README.md.
The earlier “24 patches” counted that README and is corrected here.
We acquired every dependency by the root manifest's exact commit, checked
package origins/HEADs, and applied only those declared patches using the
root's guarded git-apply/check/reverse-check procedure. The 11 pre-resolution
patches are checked by root configuration elaboration. The other 12 declared
post-update patches were applied by the same guarded commands before loading;
we did not invoke an unrestricted lake update or move inherited inputRev
branches. The manifest itself is unchanged. Private copies of the already
available matching Mathlib cache were used; no shared cache was modified.

The temporary preparation SDK overlay serialized native compilers and used
the same real compiler/libraries. The published environment was then exported
again with the real SDK, without that overlay. LEAN_NUM_THREADS=2 was a
preparation resource setting, not the frozen census's -j8 measurement protocol.

## Preparation and functional outcomes

| Observation | Count |
|---|---:|
| Requested original missing imports | 38 |
| Original 38 artifacts present after preparation | 38 |
| Returned target build calls (38 earlier + final Rellich) | 39 |
| Successful target build calls | 39 |
| Direct-importer functional checks returned | 39 |
| Distinct source units compiled successfully in those checks | 7 |
| External import artifacts still absent in the actual context | 0 |
| Source units inheriting an absent external artifact | 0 |
| Source units inheriting an observed source rejection | 0 |
| Source units with no currently known blocker, including configuration | 163097 |
| Static initial fresh-census frontier (source modules) | 9223 |

Functional categories: {"dependency_not_ready": 30, "functional_compile_success": 9}.

The first segment requested the 38 named module targets; the final segment
requested the explicitly included Rellich target, all with
`+Module.Name:olean`. Lake selected only their transitive dependencies.
Neither segment ran the default/full corpus build.
Preparation and the functional continuation share the single original
12-hour deadline; neither controller repair nor the CPU migration reset it. Deadline/resource interruptions are operational and retained, not
source rejections. The original JSON-parser defect occurred after a successful
Lake environment call; its raw logs and terminal remain on PVC.

For every requested import we selected the smallest direct corpus importer
by source bytes, breaking ties by module identity, and ran the original source
once in the actual Lake environment. The functional outputs are separate
from corpus build artifacts. These checks have a 600-second operational
timeout each, also bounded by the original shared deadline;
heartbeat/recursion/memory failures are also separate from
source rejection. A missing internal parent is dependency_not_ready, not
evidence that the pinned source is invalid. No native cost fields enter these
results. A successful compiler exit with a sorry warning is retained explicitly
and is not a claim of independent proof acceptance.

**No-known-blocker is eligibility for a future compile attempt, not build success.**
Most corpus internal prerequisites and sources were not compiled this round.
The static initial frontier counts modules with no internal prerequisites and
no known blocker; other eligible modules become ready only after their DAG
prerequisites. It is not an additional native success count.
The exact number accepted by a full pinned build remains unknown. Distinct
functional source outcomes and all 38 import-target outcomes are exposed
separately; an artifact can exist as a transitive product even if its own
target call was never reached.

## Source-qualified interface for M

All **163,097 source units** are present: **163,096 ordinary source modules
plus one root lakefile.lean configuration unit**. The archive declares one
root Lake context and two source roots; HodgeConjecture helpers preserve
their original module names under the second root. Do not join solely on a
module name or treat lakefile.lean as a proof root.

- module-contexts.csv.gz: one row per source-qualified unit, source/root,
  toolchain/manifest identity, context_export_verified, actual environment
  reference, every inherited missing external import, inherited functional
  rejection, functional check status, and direct internal prerequisite count
  for a fresh census. Unchecked rows remain unchecked.
- internal-prerequisites.csv.gz: 370,865 source-qualified internal edges, one
  edge per row. This avoids oversized cells for root aggregators and reads
  with the standard-library CSV defaults.
- lake-environment.json: fresh official export, compiler version, exact
  package commits, manifest identity, patch application evidence and timestamp.
- build-context.json: declared root identity and two source roots; the
  earlier partial path is retained in historical_capture_search_path; the
  legacy capture_search_path field now points to the actual exported path.
- provider-builds.json: all 38 original imports and the final Rellich target, native return or
  explicit unattempted/interrupted state, actual artifact presence and raw log.
- functional-importers.json: direct-import source evidence, source identity,
  command, outcome, diagnostics and sorry-warning flag for each check.
- actual-missing-imports.csv: all current absent external imports and
  propagated affected-unit counts, including newly visible gaps.
- missing-imports.csv: the historical 38-import source/pin/ancestry audit;
  its old missing-artifact observations are not silently rewritten.
- rellich-completion.json: fixed-pin last-target build and minimal importer record.
- artifact-byte-comparison.csv/json: requested products and unavailable historical pairs.
- final-preparation.md: current technical readiness and unresolved comparison scope.
- summary.json: current static/functional eligibility categories and terminal
  records, never a whole-corpus successful-build count.
- planning.json: historical planning only, excluded from measurement tables.

Static artifact presence does not prove artifact validity or runtime library
completeness. Axioms/acceptance require the independent checker's receipt.
The previously absent Euclidean.Rellich artifact has now been built at its
unchanged pin. Its former 3,768-unit external-input block is cleared.
The minimal direct-importer check still needs an unbuilt internal OAI parent;
that is not a source/pin failure. All 163,096 ordinary source modules now have
no known enumerated external-input/source-rejection blocker, but only 9,223
are in the initial fresh DAG frontier; 153,873 await internal prerequisites.
The additional configuration unit is separate. Native corpus success is unknown.

The requested historical comparison remains unresolved: none of the seven
successful functional sources has a usable historical product in the locations
searched. All 21 requested product rows are retained; zero pairs were compared.
This must not be described as byte equality or no mismatches. See
[final-preparation.md](final-preparation.md) for the search scope, the j2/j8
distinction, the existing import-view adapter, and remaining technical
qualification limits. No discrepancy was silently adjusted.

The instruction-invariance gate remains failed. Input readiness does not
resolve the missing byte-parity evidence or qualify the full driver.
census_controller.py defaults to this actual export and rejects unprepared
external artifacts before native execution.

## Reproduction and retained evidence

At the pinned corpus root, install the exact manifest commits and apply only
its declared compatibility patches as above. Export with
`lake env python3 export-env.py` (record LEAN_PATH/LEAN_SRC_PATH and compiler
variables), then use `lake build +IMPORT:olean` for each historical missing
import. Functional checks use `lake env lean --root=SOURCE_ROOT
-DautoImplicit=false -o OUT.olean -i OUT.ilean -c OUT.c PINNED_SOURCE`.
The precise actual argv, source hashes (provenance only), logs and statuses
are in the corresponding small JSON files.

Raw package acquisition, patch checks, exported environments, failed driver
logs, dependency builds and functional diagnostics remain on the existing PVC:
`/workspaces/.agent-state/gpu-smt-captures/workloads/dependency-native-20261104`.
The earlier source/history audit remains at the sibling dependency-audit-20261104.
No raw logs, private caches or large package/build trees were copied into Git.
Review: 自审.

## Real-corpus subset qualification — 2026-11-04

The explicitly authorized bounded controller attempt has returned. Three gate
targets with retained references had a five-module internal closure. Using the
unchanged 44-path export/folded-view recipe, three dependency-ready modules
failed at import time (six calls including retries), and two were blocked.
No current target products were produced: nine references are available but
zero artifact pairs could be compared. Equality remains unknown.

The folded view omits .ir/.ir.sig siblings that are present beside the original
Batteries and SDK olean files; pinned Lean source resolves IR beside its selected
olean. This is a confirmed view coverage defect consistent with the diagnostics,
without a changed-recipe repair comparison. No recipe or threshold was changed.
See [the bounded native report](controller-real-subset/README.md).
This is functional evidence only, not costs or a passed census gate.
Full census was not launched; all W-owned validation processes have retired.
