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
Table 2 remains pending O's returned external timing.
The current PDF is six pages / 306,731 bytes, with two figures, two tables
and 14 references. CPU8–9 compilation returned 0 in 2.250 s, with no
overfull/undefined warnings or evidence-placeholder macros. Changed pages
1–2 and 4–6 were visually checked; page 3 renders identically to the
previously reviewed compilation-final version. This is root self-review.
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
O timing follows,
then M may check actually built artifacts until 17:00. Partial/not-attempted
checking remains supplementary. Root targets integration by 18:00 and closure
by 20:00. No PlanarPacking comparison or root replacement measurement queue.

Native e000ed62 shared-checked/strict policy and the crafted body-context
difference remain explicit. Two read-only reviews have regression repairs,
with no independent repaired-source runtime review. Existing O functionality
is not immutable release acceptance or final timing. Prototype/fixture and
old-version costs do not populate final system tables.

All root Workspace reads/analysis/Git/PDF and children use **CPU8–9**.
Main-only owned-path commits preserve foreign work. No public release,
infrastructure change or host recovery is authorized here.

[Plan](research-plan.md) · [Evidence](paper/evidence.md) · [Index](../research/README.md)
