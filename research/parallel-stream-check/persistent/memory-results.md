# Aligned memory diagnostics, separate from primary timing
Two complete8P native controls, flags0/1, same4,449-module closure and same
checked/allocation/accepted vectors. Existing compiled smaps hook reads at
all4,449 module boundaries per process. The native/controller groups retired
with no stop/OOM/max event; no swap in any of8,898 checkpoints. One observation
per flag, not a repeat distribution or measurement of exact retained objects.

| At final matched boundary | Off MiB | Persistent MiB | Difference MiB |
|---|---:|---:|---:|
| Rss_bytes | 2986.117188 | 2993.468750 | 7.351562 |
| Pss_bytes | 2967.976562 | 2975.698242 | 7.721680 |
| Anonymous_bytes | 503.460938 | 510.437500 | 6.976562 |
| Private_Dirty_bytes | 503.476562 | 510.453125 | 6.976562 |

The endpoint holds425,463 input entries/237,863 observed checks and18,990
marked/off frontiers. It is after the heavy final module, not an earlier
every100 endpoint. Extra Anonymous is6.98MiB; native RSS7.35MiB. Net resident
differences are not exact leaked bytes: allocator arenas/layout and transient
working storage differ. Across matched module boundaries the Anonymous delta
ranges about-208..+265MiB, not monotonically increasing and not a confidence
interval. Original complete JSON/full aligned CSVs stay on PVC; small every100
plus first/final samples are committed.

| Observer-enabled run | Wall s | User s | System s | wait4 peak RSS GiB | Sampled tree peak GiB |
|---|---:|---:|---:|---:|---:|
| 0 | 379.479 | 717.944 | 68.551 | 3.261086 | 3.248150 |
| 1 | 355.149 | 613.138 | 63.182 | 3.267864 | 3.246525 |

smaps is costly: system CPU grows to63..69s in these diagnostics versus about
10s in the primary8P runs. These clocks do not enter the plain/stat primary
matrix. The observed memory pair's timing is not a production speedup.
Sampling is1Hz and can miss a peak; wait4 high-water/native snapshots/tree
samples are distinct measures. All are far inside this16GiB lane/14GiB guards.

Primary3-repeat marker-window CPU median is about0.28s per whole closure,
versus0.006s off, including clock reads. Already-persistent subgraphs are
pruned; stage2 PHashMap shares structure, so this is not copying the whole map
every wave. Persistent objects nevertheless do not reclaim until process exit.

The same-density whole-Mathlib/primary-family resident projection is~7.4GiB
before extra dependencies/heaps, not a measured full-library acceptance result.
Available OAI compiled1299 is not the full163,097-file source frame; the earlier
~260GiB scenario is explicitly biased and must not be used as a forecast/bound.
Neither small observed net heap cost nor an estimated Mathlib fit establishes
an unbounded resident OAI service. Finite process-per-closure reclamation is
the measured scope. See memory-estimate-method.md for assumptions.
