# Repaired Grid: true eight-worker first curve

Frozen v14 /8c62fc3, one repetition. All3,793accepted IDs equal O\'s planned
compute-grid cohort; no local context fallback. Every leaf trial uses the same
independently checked3,792-module prefix. All7,898new leaf CIs match serial.

| Leaf method | Wall s | Process CPU s | Mean cores | Serial / wall |
|---|---:|---:|---:|---:|
|serial|265.009820|264.853455|0.999|1.000|
|parallel1|270.263915|270.157625|1.000|0.981|
|parallel2|155.577084|310.739219|1.997|1.703|
|parallel4|94.183239|375.642908|3.988|2.814|
|parallel8|65.856253|523.784132|7.953|4.024|

True8-worker utilization7.953cores;4.024x leaf speedup,97.76% more CPU seconds
than serial. Do not attribute the extra CPU to instructions, reference counting
or bandwidth without a matched profile. One repetition; variance unknown.

Whole prefix+five-trial process1054.529s wall/2116.247s cgroup CPU. This is not
a complete single-configuration time. Native/controller/cgroup retired, no
memory/OOM stop. See compute-runs.csv for separate wait4/sample memory metrics.

The previous v12requested8/achieved4point is retained as scheduling-defective
historical evidence, not pooled into this repaired version. The original O
whole-closure serial point uses matching constructed artifacts, but the current
incremental curve cannot fill a not-yet-measured complete parallel configuration.
All computations here preserve source CIs completely; no chunk rewriting.
