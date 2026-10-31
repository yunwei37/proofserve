# Completed native controls (all 90 cells)

Self-review, 2026-10-31. All 30 (module, configuration, instrumentation)
triplets completed. Every run returned 0, produced a byte-identical `.olean`
and byte-identical diagnostic log relative to that module's baseline plain r1,
with no error/panic/sorry warning. **210/210 artifact comparisons** pass
(90 `.olean`, 60 `.ilean`, 60 C files).
The recorded PID/birth identities are retired; no cgroup max/OOM/OOM-kill
event was recorded. Data are the frozen original matrix, not new reruns.

All values below are **median [minimum, maximum], n=3**. Seconds are native
wall / user / system; memory is wait4 maximum RSS in GiB. These are independent
metric medians: user+system medians need not equal the median total. Full
unrounded per-repeat values, sampled own-tree RSS peaks, faults and switches
are in [native-per-repeat.csv](native-per-repeat.csv); all modes and ranges
are in [native-summary.csv](native-summary.csv). No profiler-mode clocks
are pooled with plain runs.

| Module | Configuration | Wall s | User s | System s | Peak RSS GiB |
|---|---|---:|---:|---:|---:|
| Grid | baseline | 621.936 [612.777, 633.650] | 385.525 [381.749, 396.113] | 436.151 [431.615, 445.192] | 7.511 [7.497, 7.526] |
| Grid | noM | 305.693 [303.203, 320.612] | 371.815 [363.118, 391.521] | 107.412 [101.354, 213.346] | 7.441 [7.435, 7.448] |
| Grid | threads1 | 710.292 [709.726, 712.171] | 373.456 [373.125, 373.819] | 459.832 [459.184, 464.453] | 7.764 [7.436, 7.765] |
| Grid | mmap_high | 622.072 [620.342, 623.884] | 382.778 [382.139, 382.911] | 440.558 [438.129, 443.261] | 7.536 [7.509, 7.540] |
| Grid | trim_high | 623.923 [618.162, 626.824] | 382.402 [382.076, 383.868] | 442.987 [437.037, 446.581] | 7.486 [7.485, 7.498] |
| UMoments9 | baseline | 141.739 [141.479, 146.116] | 119.732 [119.627, 124.983] | 100.597 [99.963, 101.842] | 7.737 [7.406, 7.761] |
| UMoments9 | noM | 88.211 [87.682, 88.278] | 117.932 [117.868, 118.269] | 42.305 [42.262, 42.833] | 7.431 [7.400, 7.785] |
| UMoments9 | threads1 | 174.765 [173.566, 177.201] | 115.287 [114.954, 115.350] | 96.902 [96.774, 100.345] | 7.990 [7.662, 8.402] |
| UMoments9 | mmap_high | 142.735 [141.682, 142.763] | 120.269 [119.596, 120.690] | 101.055 [100.493, 101.575] | 7.348 [7.272, 7.401] |
| UMoments9 | trim_high | 141.862 [141.760, 142.808] | 119.664 [119.509, 120.414] | 101.143 [100.604, 101.162] | 7.703 [7.502, 7.757] |
| EnvelopePsiB | baseline | 64.447 [64.123, 66.985] | 63.091 [62.632, 64.393] | 2.669 [2.544, 3.769] | 7.595 [7.595, 7.598] |
| EnvelopePsiB | noM | 63.518 [63.321, 63.646] | 62.585 [62.515, 62.967] | 1.960 [1.863, 2.113] | 7.605 [7.601, 7.607] |
| EnvelopePsiB | threads1 | 64.968 [64.791, 65.002] | 62.425 [62.342, 62.484] | 2.665 [2.585, 2.671] | 7.582 [7.576, 7.584] |
| EnvelopePsiB | mmap_high | 64.568 [64.558, 66.536] | 63.067 [63.062, 64.014] | 2.674 [2.667, 3.702] | 7.604 [7.595, 7.605] |
| EnvelopePsiB | trim_high | 64.555 [64.306, 66.820] | 63.058 [62.923, 64.177] | 2.684 [2.560, 3.808] | 7.597 [7.591, 7.600] |

Baseline: j8 and native -M8192 (Grid) / -M9216 (others). noM removes only native -M; the constant temporary outer native cgroup is 15 GiB in all arms. threads1 changes j8/LEAN_NUM_THREADS=8 to j1/1 while retaining -M. mmap_high and trim_high separately set glibc.malloc.mmap_threshold or glibc.malloc.trim_threshold to 134217728. No combined noM+threads1 arm exists.
