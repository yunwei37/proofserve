# 8P causal PMU endpoint: direct RC/coherence discrimination
One complete stat run per flag; whole-command user-mode counters,100% running,
not time-gated originalCheck samples and not a3-repeat stat interval.
All logical check/allocation vectors and4,449 accepted module IDs match.

| Event/ratio | Off | Persistent | Change |
|---|---:|---:|---:|
| cpu-cycles | 1969934773331.000000 | 1685877381562.000000 | -14.420% |
| instructions | 3343139005793.000000 | 3382326167887.000000 | 1.172% |
| IPC | 1.697081 | 2.006271 | 18.219% |
| cycles_per_refcycle | 0.874205 | 0.868641 | -0.636% |
| mem_load_retired.l3_miss | 532289687.000000 | 536343258.000000 | 0.762% |
| mem_inst_retired.lock_loads | 5818993726.000000 | 112656010.000000 | -98.064% |
| mem_load_l3_hit_retired.xsnp_hitm | 779885830.000000 | 43550844.000000 | -94.416% |
| ocr.demand_rfo.l3_hit.snoop_hitm | 517381271.000000 | 143426518.000000 | -72.278% |

The large locked-load and HITM changes support the intended shared-RC/coherence
mechanism. Ordinary L3 load misses do not fall; instructions rise about1.17%.
Do not explain the gain as less proof checking, identical retired instructions,
or uniformly better ordinary L3 hit rate. The cycle/refcycle ratio is slightly
lower marked, not evidence of higher calibrated frequency. It is not GHz.

Three-repeat plain endpoint results are separately reported: wall-5.134%,
CPU-14.130%. The stat observations have their own clocks and are not inserted
into those medians. Multiworker changed-counter events are consistent with
the intended intervention, not exclusive RC-stall attribution; marking also
touches graph data and changes reclamation. Load HITM and RFO HITM are separate
events and must not be added as if they count disjoint transactions.

Residual marked RFO HITM143,426,518 and load HITM43,550,844 remain. So this
does not eliminate all coherence overhead or explain the residual4-to-8 cost.
2/4P stat, aligned memory, installed stock scope and real-root bad-proof
controls remain pending. No kernel/proof/primary source or input flags changed.
