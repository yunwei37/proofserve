# First causal PMU pair: 1P, one stat observation per flag
Both full-closure native runs complete with exact reference IDs/check/unit
vectors. All14 actual counters have100% running time. Whole-command user-mode
counts, not time-gated originalCheck samples and not3-repeat confidence data.

| Measure | Off | Persistent |
|---|---:|---:|
| cycles | 1,666,676,090,741 | 1,626,777,977,341 |
| instructions | 3,339,240,343,207 | 3,379,133,715,519 |
| IPC | 2.003533 | 2.077194 |
| cycles/refcycles | 0.820416 | 0.820691 |
| retired lock-load event | 5,800,924,030 | 98,707,245 |
| L3 load misses | 435,651,099 | 431,765,309 |
| load HITM forwarding | 103,913 | 79,184 |
| RFO HITM | 55 | 455 |

Locked-load event falls98.30%, while cycles fall2.39% and instructions rise
1.195%. Do not claim instruction-identical runs or equate counter change with
removed stall seconds. Marking intentionally changes RC/lifetime behavior;
observed check/allocation units remain identical. At1P the modified-line
transfer counts are near zero;55->455 is not evidence of a meaningful
contention regression. Multiworker coherence comparisons remain pending.

The cycle/refcycle ratio is a normalized hardware ratio, not calibrated GHz.
L3 misses/kinstruction is retained alongside raw counts. Stat clocks remain
separate: wall versus3-repeat plain median is+0.280% off/-0.133% on; CPU
+0.260% off/-0.134% on. These single observations include run variance/order,
not an isolated estimate of observer-only overhead. No historical PMU values
were borrowed. Native applications/groups retired;32-cell matrix continues.
