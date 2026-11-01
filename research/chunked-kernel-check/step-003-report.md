# Step 003 — corrected direct-header coverage and finite native continuation

2026-11-01 UTC; M lane; same-thread 自审. The two-regime paper direction
remains fixed and root owns paper changes. This step corrects a real analysis
error and completes that corrected static evidence boundary.

## EXPERIMENT

The previous lexical scanner borrowed the nearest explicit header even if an
inline proof argument had its own inferred target. Grid exposes the error:
each point has two explicit record equalities and a third inline Check proof;
native types identify the third as a conjunction, while the old scanner
incorrectly reused the preceding PointBox equality. Old source/results are
preserved in PVC lexical-census-v1 and record-hints-v1. The step002 historical
report has an explicit forward correction; no old record is made to appear
freshly verified.

The corrected scanner accepts an explicit header only when the text between
its assignment and decide is whitespace/by. An inline argument or a goal
changed by an earlier tactic is unresolved. Actual Grid controls yield
3072equality headers and1536unknown inline goals. The complete fixed frame was
scanned again on E cores, no native timing slot used, with a1800s self limit.

### Complete corrected results

All163,097files and1,785,499,363source bytes match the pinned frame.
The total remains1,354,379sites in5848files, with zero per-file count
disagreements against W's canonical metrics. Reaggregation of every raw row
matches both class and module CSVs.

| Direct recovered form | Sites |
|---|---:|
| Equality, type unresolved |816321|
| Embedded/inferred/otherwise unresolved |459167|
| Universal, inferred domain |37602|
| Atomic comparison |21004|
| Application/other |9316|
| Universal, membership/subset domain unresolved |5875|
| Existential/mixed |3245|
| Nested universal, unresolved domain |1311|
| Conjunction |508|
| Universal, explicit Fin |26|
| Universal over List |4|

The explicit structural nomination is538sites (0.03972%). The finite-interval,
explicit nested-Fin and Boolean-all recognizers have zero matches; this does
not prove those semantic computations absent. Equalities account for60.2727%
and unresolved targets33.9024% of all occurrences. These are lexical counts,
not runtime or semantic completeness claims.

The corrected record-hint pass nominates277,963sites (20.5233%globally):
193460CBox,1543PointBox,2960RBox,80000Box. Together with the disjoint explicit
forms it nominates278501sites (20.5630%). Namespace/shadowing and successful
elaboration remain conditions. This is not a certified semantic lower bound.

A crosscheck initially assumed every native UMoments9 CBox helper had a direct
source header. That assertion failed:1152hints versus1164native helpers.
Source inspection found the remaining12calls after change and simp_rw, so
leaving them unknown is correct. The failed assumption and real contexts are
retained under record-hints-v2/native-crosscheck-first-assumption.json.
Native selected modules still have7018/7092known structural goals; the direct
record hints cover5470of them. Aggregate type-count corroboration is not
per-call precision measurement over the corpus.

### Native matrix lifecycle

V3's original finite controller (PID154071/birth754571435) retired after its
configured1740s queue deadline with two accepted native cells and no terminal.
Its exact controller exit code is unknown. All recorded native PID/birth
identities were checked retired; the third queued directory has no result.
This is consistent with its outer deadline, not a native proof rejection.

At01:01:49UTC a finite continuation (PID173655/birth754749286) queued only the
missing cells, retaining both completed cells and the exact frozen native
Driver/ChunkBase/C library. It uses the same existing lock for a bounded
continuation window; each native cell still has180s self alarm, finiteHB,
no-M/P0–7,14GiB sampled own-tree stop. The runner can borrow the *same open file
description* from the window controller, so its own flock does not deadlock.
A short naturally exiting Python child tested that descriptor behavior on an
ephemeral PVC file; this is plumbing validation, not Lean acceptance.

At01:09:14UTC the continuation was genuinely waiting behind holder166882.
No full matched curve is claimed at this boundary. Queue and controller
durations will not be combined into native throughput; only actual cell
captures can populate the final matrix. The analyzer now reads the explicit
continuation manifest rather than assuming a result-directory naming pattern.

## WRITE and literature

README and shape-method.md now use corrected counts and retain the limits.
The weighted native panel is unaffected: its source occurrence denominators
and actual compiled types did not change. Its58.89–84.24%wall proxy remains
explicitly model-based, with five unknown mixtures; it is not measured savings.

Focused primary-source follow-up confirms a stronger prior-art overlap:
Self-Certification sections7.2–7.3already discuss certificate splitting and
substantial loading costs between pieces. A Lean matrix-certificate author
also reports row decomposition, but the demonstrated path uses native_decide
and enlarges trust. These are not reproduced systems or new performance data.

Pinned Lean source shows separate checker caches per theorem and a fresh
constant-map/extension rebuild during ordinary imports. They explain plausible
costs to inspect, not an attribution of all added CPU or a fundamental import
lower bound. No cache or unchecked environment union was added to our checker.

## REVIEW and disposition

Self-review checked corrected raw totals, the known Grid counterexample,
field-projection controls, aggregate native/source comparisons, preserved
failures and actual controller retirement. All owned Python sources compile.
No independent review, whole-library semantic fraction, whole-module speedup,
new mathematical axiom or generic novelty is claimed.

The corrected static result is ready to push. Keep the finite native point
active; the next result must report actual pure-kernel span/threadCPU and full
pipeline costs at each k, including negative curves and all output checks.
