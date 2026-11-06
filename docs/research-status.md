# ProofServe: current status

Deliverables: open-source ProofServe and a readable six-page empirical + system
paper; closure target **6 November 2026, 20:00 UTC**.

## Completed compilation

W published **cc5bcc18**: **162,170/163,096 modules (99.43%)** completed,
**926 deferred by user**, zero final native failures and zero
failed-dependency blocks. The configuration unit is separate. All runnable,
non-deferred work is exhausted, with the high-memory tail still unmeasured.

| Physical interval | Completed | P CPUh | E CPUh | Wall h |
|---|---:|---:|---:|---:|
| 1: fixed 22-slot admission | 128,331 | 134.651 | 256.668 | 24.625 |
| 2: memory admission / deferral | 33,788 | 32.718 | 45.731 | 6.179 |
| 3: continuation of the second rule | 51 | 1.587 | 0.000 | 0.726 |

Totals: **168.956 P / 302.399 E CPUh**, without conversion;
**31.529 wallh** across intervals. Calendar span is 33.086 h including
1.557 h of gaps. Failed/interrupted attempts (66) are separate from successful
CPU, while interval wall includes their actual elapsed work.

Root independently reduced all 163,097 rows and matched status counts,
P/E/interval/marker/default-graph sums and selected-user PMU coverage.
Product existence/size/closure checks remain W's self-review, not root byte
validation. The continuation supervisor/controller were observed absent;
W records lease release 04:59:12 UTC after retirement 04:57:20 UTC.

## Paper and remaining evaluation

The compilation section is complete. The current paper also integrates the
scoped M matrix, with Table 1 medians, default/strict costs, the censored Grid
point, all ten unrun cells, controls and actual interruption overhead.
Coordinator-reading corrections are applied: historical SubexponentialSAT
reference coverage14401/14721 with zero differences and320 unreferenced;
Barrier2/4 cut for the six-hour limit; abstract body-context difference and
Nat.Basic strict4.23 wall ratio; the opaque method-defect sentence removed.
All14 cited keys and their primary supporting passages were checked.
Lean4.35.0/lake check is confirmed by release notes; the earlier report's
outcome/timing/export-hash proposal is no longer mislabeled axiom receipts.
O publication 0516279d is now integrated into Table 2: Newspeak/Solar/AI
native CPU 109.055/167.209/2481.041 s and wall 110.639/169.321/2579.748 s;
official-default CPU 38.637/5.512/37.377 s and wall 38.736/5.539/40.993 s.
Each arm has one complete observation, one worker. All 126 common local roots
pass; native transitive closure and official local roots are unequal checking
obligations, so there is no equal-obligation speedup comparison. AI attribution
is an upstream collection-level declaration, proportions undisclosed.
The final manuscript includes W compilation, the M matrix, O external timings
and the bounded supplementary checking publication 5f491682. Final PDF: six pages /276380bytes; CPU8–9 compilation rc0 /2.034s, zero warnings\nand zero missing macros. All six final pages were visually reviewed; details\nare recorded in paper/evidence.md.
This remains root self-review, not independent paper or repaired-native review.
No interrupted-preview CPU enters Table 2.
The six-page paper now uses the returned distributions, interval/P-E costs,
user-mode instruction total/median/P95 and marked/unmarked/default-graph
partitions for the 162,170 measured modules. No earlier snapshot is presented
as final scope. Small derived artifacts bind cc5bcc18 and the independent
reduction; duplicate large inventories stay on PVC.

Dependency order and memory selection prevent extrapolation. The missing
high-memory tail may be more expensive; earlier successful family members
remain included. Only separate protocol-specific P/E work lower bounds are
reported. The total-instruction gate still failed; user-mode comparison was
selected post hoc, not a replacement passing gate.

M published 818f7422 after the 11:13 UTC six-hour boundary. All 30 scaling,
12 ablation and three Nat.Basic strict runs completed; the original 71-cell
plan had 61 returned attempts and ten unrun cells. Grid strict r1 timed out;
r2/r3 were unrun. Nat.Basic official fresh r3 was attempted but cut off by
the overall window, not counted among the ten unrun items.

At eight versus one worker, wall speedups are 1.70/2.14/1.73 for
Nat.Basic/Grid/Barrier; CPU increases 2.9/11.3/4.6%. Nat.Basic strict costs
4.23 wall / 2.50 CPU times default-eight. Strict Grid is only a censored
at-least-5.1 wall ratio, not a strict median. One real interruption costs
16.94% additional wall and 10.68% CPU with identical resumed scope.
All three original-kernel bad controls reject; nine complete official
samples accept their roots, with different ledgers and no whole speed ratio.
Root independently recomputed the point medians, ranges and ratios; M's
identity/acceptance assertions remain its scoped implementation-line evidence.
Protected zettai-dev work (~one P core observed before launch) is explicit:
this is not exclusively idle-host timing. The collection's raw failed/partial
terminal remains preserved alongside verified retired handoff. Root observed
the last collector PID absent and has not launched corpus checking.
O retired at 12:20:12 UTC; its controller and child were observed absent.
M's subsequent built-artifact result remains pending. The clarified original
brief stops new batches at 17:00 and allows the running batch at most
15 minutes to drain, with final forced retirement by 17:15.
M's supplementary campaign retired at the authorized 17:15 deadline
after stopping new batches at 17:00. Publication 5f491682 certifies 15 complete
batches: 12,756 distinct closure modules, including 968/162,170 requested
source modules. The remaining 161,202 requested modules lack complete batch
certification; 488 uncertified acceptance events (271 complete-segment /
217 in-flight) are separate, as are one attempted-without-verdict and
160,713 without observed verdict. There were no reported kernel rejections
or OOMs; exit124 denotes the operational deadline. Whole-library checking
is incomplete, with no official-reference comparison on this prefix.
The mixed-core native cost is 16,530.349 s wall / 16,194.749 s CPU,
including interrupted work, and peak sampled process-tree RSS8.878 GiB.
The 926 user-deferred modules and one configuration unit remain separate.
OAI has no compiled artifact; capacity was unmeasurable.
Root independently checked the source ledger and unioned all 15 certificates;
this does not establish editable-certificate integrity or replay their proofs.
No native execution is resumed. The final PDF is ready for coordinator reading.

Native e000ed62 shared-checked/strict policy and the crafted body-context
difference remain explicit. Two read-only reviews have regression repairs,
with no independent repaired-source runtime review. Historical O dirty-packaging functionality remains separate from these
new uninterrupted final costs and is not independent runtime review.
The final local bundle uses glibc 2.41; its AI command is memory-bounded
(888 memory.max events, no OOM kill/resource stop).
Prototype/fixture and
old-version costs do not populate final system tables.

All root Workspace reads/analysis/Git/PDF and children use **CPU8–9**.
Main-only owned-path commits preserve foreign work. No public release,
infrastructure change or host recovery is authorized here.

[Plan](research-plan.md) · [Evidence](paper/evidence.md) · [Index](../research/README.md)
