# Complete primary PMU matrix
All32 primary native cells completed:24 plain plus8 stat. Same executable,
source/inputs, no-M and blocking P0-7 lock. All56 stat counters100% running.
One stat observation per flag/worker set, no statistical confidence interval.
Counters below are whole-command user-mode aggregates, not per-worker means
or exact originalCheck-gated events. Raw values stay in the small CSVs.

| Workers | Mark | IPC | Cycles T | Instructions T | Locked-load M | L3-load-miss M | Load HITM M | RFO HITM M |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | False | 2.003533 | 1.666676 | 3.339240 | 5800.924030 | 435.651099 | 0.103913 | 0.000055 |
| 1 | True | 2.077194 | 1.626778 | 3.379134 | 98.707245 | 431.765309 | 0.079184 | 0.000455 |
| 2 | False | 1.923867 | 1.736321 | 3.340451 | 5806.664633 | 414.955692 | 271.730955 | 185.505442 |
| 2 | True | 2.019948 | 1.673268 | 3.379914 | 103.093416 | 541.439537 | 31.097076 | 81.156555 |
| 4 | False | 1.839413 | 1.816766 | 3.341784 | 5812.575590 | 524.695471 | 528.320675 | 344.214671 |
| 4 | True | 2.019344 | 1.674502 | 3.381395 | 107.208232 | 586.464279 | 43.938879 | 129.385129 |
| 8 | False | 1.697081 | 1.969935 | 3.343139 | 5818.993726 | 532.289687 | 779.885830 | 517.381271 |
| 8 | True | 2.006271 | 1.685877 | 3.382326 | 112.656010 | 536.343258 | 43.550844 | 143.426518 |

At8P the treatment removes98.064% of lock-load events,94.416% of load HITM,
72.278% of RFO HITM;IPC1.69708->2.00627,cycles-14.420%,instructions+1.172%.
L3-load misses+0.762%, not a general ordinary-cache-miss reduction.2P and4P
marked L3-load misses also increase; do not hide these different outcomes.

The4-to-8 scaling in this same stat matrix is:
| Event | Off change | Marked change |
|---|---:|---:|
| user-mode cycles | +8.431% | +0.679% |
| instructions | +0.041% | +0.028% |
| load HITM | +47.616% | -0.883% |
| RFO HITM | +50.308% | +10.852% |
| IPC | -7.738% | -0.647% |

Thus the old additional coherence traffic is largely a property of the
prototype's reconstructed shared object state. RC updates and ownership
transfers are consistent with the original hypothesis; marking also touches
graph data and changes reclamation, so no exact atomic-stall seconds follow.
HITM event types must not be added as disjoint transfers. Residual marked
RFO and other overhead remain. No claim of a universal Lean scaling limit.

Time is separate from these PMU counters: all plain medians/ranges are in
[plain-results.md](plain-results.md). Stat-vs-plain wall differences range
-0.389..+1.118%,CPU-0.134..+1.642%, including order/run variance; not isolated
observer-only overhead and never mixed into plain medians. All32 have the exact
4,449 accepted IDs/module work vectors:237,863 observed checks and3,283,925,639
in-check allocation units. CPU times include system time; user counters do not.

For the marked4/8 stat pair, total CPU603.388->623.604s, user597.268->613.551s,
system6.121->10.052s,while user cycles only+0.679%. The cycle/refcycle ratio
0.88404->0.86864 also changes. It is not calibrated GHz. Residual CPU seconds
therefore cannot all be called additional user-space coherence stalls; no
frequency/allocator causal ablation was performed. Keep these scopes distinct.

All primary applications/groups and controller596466/birth774557767 retired,
MATRIX_RETIRED0 observed. Qualifier13 controls stay preserved. Memory/stock/
real-root fault diagnostics follow separately; no auxiliary timing enters this
fixed32-key primary matrix. The first memory control is actually queued.
