# Complete plain causal matrix: full Barrier closure
All24 declared plain cells returned,3 repetitions per flag at1/2/4/8P.
Same executable, only PARALLEL_PERSIST_BASE0/1; no-M; shared blocking P-core
lock; same frozen4,449-module closure and source. All8 stat cells have now completed; see stat-results.md.

Each table entry is median[min,max]. CPU=user+system wait4 seconds;
original-check observer uses thread CPU including heartbeat/timer glue.
The observer is not all kernel work: fallback/import/planning and other work
remain in the rest of process. Allocation units are the observed original-call
counter, not whole-process malloc totals.

| P workers | Mark | Wall s | CPU s | Original-call observer CPU s | Peak sampled tree RSS GiB | Marker-window CPU s |
|---|---:|---:|---:|---:|---:|---:|
| 1 | False | 641.186241[636.587474,642.384065] | 640.426738[635.834487,641.667327] | 463.588340[460.621035,464.521362] | 2.954773[2.935966,2.956318] | 0.005982[0.005840,0.006009] |
| 1 | True | 628.271998[627.104680,628.718869] | 627.501808[626.381620,627.903750] | 451.756282[450.353499,452.090613] | 2.956097[2.954597,2.971619] | 0.278955[0.277120,0.283254] |
| 2 | False | 428.334062[426.456294,429.151795] | 622.163191[620.384551,623.377066] | 444.269036[442.343154,445.212436] | 2.990017[2.987629,3.005276] | 0.006247[0.006190,0.006318] |
| 2 | True | 411.766755[410.166600,412.886404] | 592.095568[590.205626,593.571225] | 415.569387[412.938151,416.141090] | 2.998905[2.988487,3.006420] | 0.280751[0.276207,0.282633] |
| 4 | False | 347.167592[344.733076,350.109186] | 652.585210[648.143251,657.423850] | 470.792621[467.716042,475.444137] | 3.077961[3.058170,3.094368] | 0.006356[0.006293,0.006475] |
| 4 | True | 331.977828[329.652874,332.168988] | 598.419631[595.387242,599.243471] | 418.902765[415.827367,419.373220] | 3.051357[3.050869,3.092522] | 0.280418[0.280250,0.281428] |
| 8 | False | 314.838809[312.803500,315.742105] | 722.297193[719.111937,722.485572] | 537.851294[534.191385,538.143643] | 3.253841[3.202438,3.271324] | 0.006338[0.006253,0.006473] |
| 8 | True | 298.674709[297.015420,298.878024] | 620.239982[620.171944,621.566499] | 436.863603[436.807651,436.885580] | 3.245773[3.162811,3.248085] | 0.279227[0.274893,0.282698] |

Every native cell has the same4,449 reference accepted IDs and exact module
vectors:237,863 observed original checks and3,283,925,639 in-check allocation
units. All18,990 marked roots remain persistent through enqueue; all unmarked
roots become active MT. Native applications/groups retired after each cell.
The finite primary matrix controller has now retired after all8 stat cells.

At8P, on/off medians change wall-5.134%,CPU-14.130%,observer CPU-18.776%.
The directly paired4-to-8 interaction removes a median65.21% of extra total
CPU and71.67% of extra observer CPU, with residual growth. See
[all three paired contrasts](three-repeat-interaction.md).
The marker window is about0.28s CPU on versus0.006s off, including clock
overhead. It is not a primitive-only instruction measurement.

This supports a causal prototype contribution to the old negative scaling,
not a general Lean limit. Persistence changes RC traffic, graph touches and
reclamation; Complete PMU outcomes are in stat-results.md. Peak RSS alone does not
quantify retained objects. Full anonymous-memory, stock scope and real-root
bad-proof diagnostics remain to execute. This same-pipeline1P is not asserted
to be the best stock serial baseline. Old Grid/leaf gains require their own
exact-workload corrected retest; no historical result is silently replaced.
