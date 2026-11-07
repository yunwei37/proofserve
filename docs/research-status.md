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

## Current paper handoff

The 7 November request replaces the ledger-like manuscript with a normal
empirical + system narrative: abstract and contributions, background, method,
result-led findings, concise ProofServe design/evaluation, consolidated
limitations, related work and conclusion. The author's908d0702 line is unchanged.
The three requested user quotations are recorded verbatim in user-instruction.md.

The current PDF is six pages /82288bytes, two figures/two tables/fourteen
references. CPU8–9 final Tectonic returns0 in1.856s with zero warnings and
zero evidence-placeholder macros. The manuscript and final page renders have
been self-read and visually checked. This is writing/arithmetic self-review,
not independent paper or repaired-native runtime review.

Newly selected committed observations include cost concentration and median
module cost; the small but costly UltraExpectationFull example; import-only
controls and import hotspots; native memory-guard system accounting; official
checker search-path costs; and controlled default/fresh coverage differences.
Source-size/CPU rank correlation is positive (P .615/E .604), so the paper
does not repeat the proposed claim that they are unrelated.
The new CPU-share figure and unrounded offline reductions are under
paper/generated/observations/; paper/README.md maps every result to committed inputs.
No Lean experiment, profile, checker run, new agent, queue or service was started.

Development review history, exact runtime versions, failed/unrun configuration
lists, compilation intervals and the small supplementary certified prefix are
retained in the artifact guide and original ledgers. Main text reports that
whole-library rechecking did not finish, without presenting it as complete.
The matrix and external table still use the same installed-tool results;
no historical memory-guard profile substitutes for release performance.

## Completed measurement state

Compilation, the scoped matrix and external timings are retired.
The supplementary checker also retired under its authorized budget:
15 complete batch certificates /12756 distinct closure modules, including
968 of162170 requested sources;488 other acceptance events are uncertified.
There is no whole-source verdict or corresponding official-reference parity.
Detailed times, deferrals, nonzero returns and limitations are in the source reports.
Nothing is resumed for this paper revision.

The new narrative awaits coordinator reading before replacement of the
eunomia.dev PDF. This pass makes no website change, announcement or upstream issue/PR.
All root Workspace reads/analysis/Git/PDF and children use CPU8–9.
Main-only owned-path commits preserve foreign work. No infrastructure or
runtime change is part of this task.

[Plan](research-plan.md) · [Evidence](paper/evidence.md) · [Index](../research/README.md)
