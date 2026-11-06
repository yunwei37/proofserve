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

The PDF is six pages / 304,611 bytes, two figures / two tables / 14 references;
CPU8–9 compile returned 0 in 2.243 s, with no overfull/undefined warnings or
evidence-placeholder macros. All six pages were visually reviewed.

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

Root now observed the actual matrix at
checker-final-e000ed62-20261106T050828/matrix: controller2998979,
birth22442843, running during the 05:52 UTC heartbeat, native e000ed62 and clean
driver snapshot cc5bcc18. Final matrix/external values remain out of the paper.
M's protected-background-condition.json records retained zettai-dev work
using about one CPU core; its preflight was not a fully idle host.
These actual conditions must accompany returned times/ranges; do not label
this run fully idle or infer that source-census retirement removed all load.
No background task was stopped or rebound by root.
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
