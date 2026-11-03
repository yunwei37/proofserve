# Step060: first directly measured causal PMU pair
EXPERIMENT_GATE:26/32 native cells complete.1P off/on stat both retain full
reference vectors;14 counters100% running. Lock-load count5,800,924,030->
98,707,245(-98.30%),cycles-2.39%,instructions+1.195%,IPC2.00353->2.07719.
Near-zero single-core HITM/RFO values are not interpreted as contention.
Multiworker counter effects are still pending.

WRITE_GATE: actual small counter/summary/overhead CSVs and P1 intermediate
report. Offline helper also derives normalized cycle/refcycle and L3 misses/
instruction ratios, without calibrating GHz. Clarify source-ready read:
multiworker gate waits, single-worker ready read may overlap checking.
The actual mark site remains before enqueue in either path; no running
native source/binary/flags are edited.

REVIEW_GATE 自审: counter availability/running percentages/work-vector equality
verified from actual completed records. Report instruction increase explicitly;
fixed check/HB work does not imply instruction equality. Locked-load events
include runtime operations and are not exclusively labeled RC stalls.
Stat-vs-plain variation is not a clean observer-only causal estimate. Eight
stat cells remain the declared plan,2 complete; no duplicate collection.
