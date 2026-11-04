# Native compilation census: qualification first

**Full census has not started; this gate never starts it automatically.**
The 2026-11-04 instruction replaces the proposed E-first/P-later launch and all
E/P conversion. All 163,097 source files are present. Precision sampling is
permanently superseded (7/12 returned); all partial/original records are retained.

## Frozen candidate protocol

openai/math 4eaee87548250b2682affda7d05d947c05554bae,
Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612, Lean 4.34.1.
Per module: lean --root=<source-root> -j8 -DautoImplicit=false
-o <module.olean> -i <module.ilean> -c <module.c> <source.lean>;
LEAN_NUM_THREADS=8, no -M, unchanged authored heartbeats.
These are the original 42 samples' compiler settings and three output kinds.
Gate sources are pinned originals; outputs have fresh per-attempt paths.
CPU includes imports and Lean-generated C, excludes separate C compilation,
linking, Lake and cache acquisition. It is not independent kernel verification.

If later authorized, both pools start together: eight P workers on CPUs 0–7,
fourteen E workers on CPUs 10–23. Each compiler/thread remains in its pool;
CPU 8–9 is for the other chats. Unrelated Workspaces stay unrestricted.
-j8 stays for comparability; 22 compilers can oversubscribe OS threads.
CPU seconds are reported by pool with no conversion or extrapolation.
The pcore lease covers the whole qualification and is then released.

Every second the guard samples cgroup actual charge and node MemAvailable,
with a response margin above the required 8-GiB available reserve. A breach
kills the largest own charged compiler, records it, and stops the gate.
RSS is recorded but never summed for admission. Sampling is not a hard global
free-memory guarantee. PVC output only; 85% disk usage stops new work.
A future census must keep unsuccessful attempts and blocked modules separate;
failed/preempted CPU cannot silently become successful-module cost.

## Qualification (self-review / 自审)

Twenty original samples, ten ordinary and ten explicit-kernel-marker modules,
362–625,596 source bytes. Historical P wall sum 135.49 s, each selected module
under 25 s. Cached prerequisite closures are present. This purposeful protocol
check is not a new probability sample. Exact IDs/hashes are frozen in CSV.

Three repetitions of P quiet, P loaded, E quiet and E loaded give 240
foreground compilations. Loaded conditions maintain 22 real Lean jobs (8 P,
14 E, including foreground), replacing completed background jobs while
foreground runs. They use identical settings and bounded measured inputs.
Background jobs finish naturally at condition boundaries. Retain per-core
busy time, actual concurrency, charge, available memory, and background
outcomes; saturation is measured, not inferred. A 180-s gate deadline never
becomes a successful cost. Any failure/preemption stops the gate.

Separate counter-on/off quiet controls alternate treatment order, three
repetitions on each pool and each module (240 more calls). Pre-exec
perf_event_open counters inherit into threads; separate sysfs cpu_core and
cpu_atom retired-instruction events count user/kernel mode. Record
enabled/running time; an inactive PMU's zero is expected. No silent multiplex
scaling. A pthread control checks both PMUs and exited-thread inheritance;
it is instrumentation setup, not a Lean measurement.

Requested thresholds stay unchanged: median cross-condition instruction
deviation <=1%, P95 <=3%, byte-identical outputs, no failures/kills, overhead
<=1%. Report per-module condition medians and max/min spread, deviations
relative to P quiet, CPU and wall overhead, and P/E loaded/quiet CPU inflation.
Inflation never corrects census totals. Noise or missing conditions yields
an inconclusive result, not a pass.

Each attempt binds measurement Git commit, source revision/content hash
(provenance only), toolchain, argv, attempt, start/end UTC, pool, wait4
user/system CPU, wall/RSS, cgroup peak/events, and instruction coverage.
Raw data stays on PVC; small summaries enter Git.
census_full.py is an unexecuted obsolete draft, not a qualified launch path.
This gate has no code path that launches a full census.

## Retained earlier methodology

The six-module E-only pilot is not a census conversion. In its two-worker arm
the old summed-RSS guard killed one compiler at 16.06 GiB mapped RSS although
recorded own cgroup charge was only 2.06 GiB. It was not a node OOM.
The new protocol drops that RSS cap. All failures/setup errors remain.
The nealmcb report concerns a different revision and module set; its ~330 CPU
hours extrapolate 26 modules rather than measuring pinned per-module CPU.
