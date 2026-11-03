# Step061: causal multiworker RC/coherence endpoint
EXPERIMENT_GATE:28/32 complete, full1P and8P stat flag pairs.8P lock-load
5,818,993,726->112,656,010(-98.064%);load HITM779,885,830->43,550,844
(-94.416%);RFO HITM517,381,271->143,426,518(-72.278%). IPC1.69708->
2.00627;cycles-14.420%;instructions+1.172%;L3 load misses+0.762%.
Exact observed check/allocation work and accepted sets retained,100% counters.
Actual2P off stat child is next under the shared blocking lock.

WRITE_GATE: P8 intermediate report and actual small PMU/overhead CSVs. Ordinary
L3 miss increase and instruction increase remain explicit. Single stat clocks
are separate from the completed3-repeat plain matrix. Persistence avoids most
retired locked-load events while CPU growth shrinks; this supports a causal
prototype contribution but not an exclusive atomic-stall fraction.

REVIEW_GATE 自审: exact raw event names/counts/running percentages and
per-module work checked. HITM events not summed;near-zero1P control not ratio-
interpreted as meaningful contention. Effective cycle/refcycle ratios are not
calibrated GHz. Remaining marked coherence events and pending2/4P/memory/stock/
bad-root evidence explicit. No source hot-patch, new kernel or concurrent M job.
