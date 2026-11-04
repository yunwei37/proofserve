# Final dependency completion and protocol-comparison limits

Preparation/function checks only; no cost observations, PMU run, P-core lease,
full census, or --execute. CPU 10–16, native child cgroup limited to 11 GiB
inside the 12-GiB lane budget. The original preparation deadline was retained.
No source, dependency pin, root manifest or declared compatibility patch was
changed. All new native/controller processes retired naturally and the own
cgroup was removed.

## Last dependency

The fixed-pin RellichKondrachov.Analysis.FunctionalSpaces.Sobolev.Euclidean.Rellich
target and its Lake-selected prerequisites built successfully with the same
root configuration. Package rellich-kondrachov remains at
70f85d4c1bf99c6e7d61e8be4daa6f3664d08d23, with the corpus's declared compatibility
patch. The 38 earlier targets were not restarted.

The smallest direct importer is
OAI.NumberTheory.CubicMoment.Theta.CubicThetaSupportedTangent (3,968 bytes,
chosen by source size then module name among four direct importers).
Its one functional compiler call stopped at the unbuilt internal
OAI.NumberTheory.CubicMoment.Theta.CubicThetaTangentVolume import. The actual
diagnostic is unknown module prefix OAI. This is dependency_not_ready, not a
source rejection or a failed Rellich build. No synthetic candidate or extra
internal corpus closure was compiled to conceal that distinction.

All 3,528 enumerated external import names now resolve to artifacts in the
verified real 44-entry root environment. The former 3,768-unit external-input
block is cleared. This is input availability, not native corpus acceptance.

| Current source-frame category | Count |
|---|---:|
| Source units present | 163,097 |
| Ordinary source modules | 163,096 |
| Root Lake configuration unit, not a proof root | 1 |
| Units inheriting an absent enumerated external artifact | 0 |
| Units inheriting an observed source rejection | 0 |
| Static initial fresh-census source frontier | 9,223 |
| Other source modules awaiting internal DAG prerequisites | 153,873 |

Across the two preparation segments there are 39 successful requested dependency
target calls. The 39 direct-import checks cover 36 distinct corpus sources:
nine successful calls across seven distinct sources, and 30 calls stopping at
unbuilt OAI imports. No source rejection, native panic, timeout or resource kill
was observed in these calls. Whole-corpus native build success remains unknown.

## Requested historical artifact comparison

The seven distinct successful functional sources have 21 retained current
products: olean, ilean and C for each. None has a usable historical counterpart
in the retained old twelve-path corpus cache or historical W captures searched.
The successful sources also have zero overlap with the original42 sample roster.

The discovery checked the canonical historical module paths, 47,641 plain
metadata files, 14 compressed metadata files and 4,076 generated-C headers.
The two plain metadata matches were full input manifests; compressed matches
were static import-set inventories/regime labels. They are not native execution
or artifact evidence. A positive control confirmed that the C-header parser
recognizes a current known module before the historical search was interpreted.
The search scope is explicit: it does not prove permanent loss or absence from
every possible external archive.

Consequently **zero artifact pairs / zero modules were byte-compared**.
artifact-byte-comparison.csv contains all 21 requested product rows with
not_compared_historical_unavailable and empty byte_equal fields.
artifact-byte-comparison.json uses an unresolved conclusion and null mismatch
count. There is no equality result and no measured mismatch to normalize or
repair. No new historical baseline was generated.

The existing gate's historical byte equalities were obtained using the old
captured twelve-path environment; they do not establish parity with the real
forty-four-path environment. Functional preparation used LEAN_NUM_THREADS=2
and no explicit -j8, whereas the original42 costs use eight threads and no -M.
The prepared full driver still statically specifies -j8 / LEAN_NUM_THREADS=8,
Lean 4.34.1, the fixed Mathlib pin, original source revision and no -M.
Matching this recipe definition does not prove identical resolved imports or
generated products.

## Technical state before a full census

- External input preparation is complete for the enumerated source graph.
  The default preparation-only preflight must now report
  environment_export_verified=true and dependency_inputs_ready=true. These
  fields do not mean a successful gate or a completed native build.
- Cross-environment product parity is still unestablished: the seven selected
  functional sources lack historical products, and their preparation thread
  setting is not the frozen cost protocol. A comparison using retained
  same-source references under the actual finalized full recipe is still
  missing. This round neither changes that recipe nor adds native runs.
- The prepared controller reads the real 44-entry export but constructs a
  first-hit symlink import-view and replaces runtime LEAN_PATH with that view.
  It therefore does not literally pass all 44 entries unchanged to each
  compiler. This existing implementation has not been exercised on this real
  corpus during the current task; its lookup/plugin behavior must not be
  assumed equivalent merely from a successful environment preflight.
- Existing qualification limits remain as documented in controller-readiness.md:
  the earlier tiny fixture checked flow/resume/status handling; real native
  interruption, memory-preemption/requeue and disk-stop fault injection were
  not demonstrated. This is an evidence-status disclosure, not a new threshold
  or a claim that those implementation paths failed.
- Internal corpus prerequisites are normal work of a fresh DAG build; their
  absence in the selected functional call is not a new external-package
  blocker. The full frame may still contain source failures not exposed by
  the small functional subset. No full-corpus success count is available.

This list contains technical state only. No extra experiment queue or new gate
is introduced. The original failed instruction-invariance gate is preserved
elsewhere; no conclusion from this preparation changes it.

Raw logs, immutable helper source, provider result, functional diagnostic and
historical discovery remain on PVC at
/workspaces/.agent-state/gpu-smt-captures/workloads/dependency-rellich-20261104.
rellich-completion.json preserves the small native records. No CPU or wall
numbers enter sample-costs.csv or a paper table. Review: 自审.

## Subsequent bounded real-controller attempt

The description above is the earlier 661a7c5c preparation snapshot.
The newly authorized five-module real-controller closure returned import-time
adapter failures. See [the complete subsequent report](controller-real-subset/README.md).
Historical counterparts are available for its three chosen gate targets, but
no current successful products exist, so byte parity remains unestablished.
The folded view now has a confirmed IR sidecar coverage defect. It was not
repaired or rerun, and the original failed gate remains unchanged.
