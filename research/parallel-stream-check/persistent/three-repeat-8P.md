# Three-repeat full-closure 8P causal endpoint (other cells still pending)
Same new executable, flags0/1, no-M, P0-7, 4,449-module full Barrier closure.
Three complete plain observations per arm. These are medians[ranges], not a
confidence interval; other worker groups still have only two repetitions.

| Measure | Unmarked | Persistent frontier | Change of median |
|---|---:|---:|---:|
| wall_s | 314.838809 [312.803500,315.742105] | 298.674709 [297.015420,298.878024] | -5.134% |
| CPU_s | 722.297193 [719.111937,722.485572] | 620.239982 [620.171944,621.566499] | -14.130% |
| original_check_observer_CPU_s | 537.851294 [534.191385,538.143643] | 436.863603 [436.807651,436.885580] | -18.776% |
| mark_window_CPU_s | 0.006338 [0.006253,0.006473] | 0.279227 [0.274893,0.282698] | 4305.449% |
| sampled_peak_GiB | 3.253841 [3.202438,3.271324] | 3.245773 [3.162811,3.248085] | -0.248% |

All six endpoint runs retain exactly4,449 accepted IDs,237,863 observed
original checks and3,283,925,639 in-check allocation-counter units, matching
every frozen module vector. All18,990 marked bases remain persistent through
enqueue; all off bases become active MT after enqueue. No kernel/proof/input
change; representative replay-CI wrappers versus persistent compacted input
were distinguished in the separate native probe.

The marked endpoint uses materially less CPU, supporting a causal prototype
contribution. It does not eliminate residual4-to-8 growth or identify an exact
atomic-stall fraction. Marking also traverses/touches the graph and changes
deallocation/lifetime. Hardware counter/IPC/coherence comparisons have not yet
returned. RSS peaks are not retained-object bytes; aligned memory diagnostics
remain to execute. Original-check observer includes heartbeat/timing glue and
excludes other work/fallback/import/planning; its units are not whole-process
malloc counts. Stats must not be mixed with these plain times.

Old3.33x leaf/1.88x Grid curves are retained as unmarked prototype results.
This matched full-Barrier ablation cannot numerically replace their different
scope or serial baseline. Repeating their exact workloads with the corrected
frontier is needed before publishing corrected gains.
