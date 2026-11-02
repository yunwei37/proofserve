# More heterogeneous workers do not accelerate this full closure
Fresh original-kernel stream, BarrierData41complete4,449-module closure, no-M.
Same frozen v16binary and inputs; one native process/configuration, fixed order
8/12/16/24, one repetition. Original-kernel per-target observer disabled.
Raw: /workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v16 .
All4processes/cgroups retired normally, no memory event or sampled stop.
All4accepted module-ID sets equal the independently retained serial reference.
This validates finite observed acceptance, not arbitrary corrupted-input equivalence.

| Workers | Allowed CPUs / hardware | Wall s | User s | System s | Total CPU s | Mean cores | Peak RSS MiB |
|---:|---|---:|---:|---:|---:|---:|---:|
|8|0-7 /8P|284.720|662.519|6.267|668.786|2.349|3367.1|
|12|0-11 /8P+4E|299.807|801.053|8.643|809.696|2.701|3415.3|
|16|0-15 /8P+8E|310.591|925.899|12.035|937.934|3.020|3577.2|
|24|0-23 /8P+16E|319.705|1154.981|17.492|1172.473|3.667|3744.2|

At24versus8, latency increases12.29%and aggregate CPU75.31%.
This is an allowed-affinity-footprint curve on8P+16E, not homogeneous strong
scaling. The process inherits each listed allowed mask; workers are not
individually pinned and may migrate. Live native thread snapshots confirm0-7,
0-11and0-15masks, with actual E-core placements at12/16. A24worker live thread
snapshot was not captured; its native process-launch affinity is recorded.
Per-thread CPU time by P/E group, external E-core load and clock frequency were
not independently controlled. Single repetition/fixed order means statistical
uncertainty and order effects remain unknown. No claim that this curve isolates
a hardware-independent worker-count cause or demonstrates cluster scaling.

## Where the complete-process wall goes
The categories below use each configuration's own kernel_workevents and native
wall denominator. They are disjoint per-module elapsed windows; outside time
includes reading, context/origin audit, coordination outside the recorded
window, startup and cleanup, not a direct profile attribution of every cycle.

| Workers | Upstream complex-or-cycle fallback | Parallel module path | Outside recorded kernel work |
|---:|---:|---:|---:|
|8|99.819s (35.06%)|138.175s (48.53%)|46.726s (16.41%)|
|12|100.601s (33.56%)|147.294s (49.13%)|51.912s (17.32%)|
|16|101.473s (32.67%)|153.844s (49.53%)|55.274s (17.80%)|
|24|101.626s (31.79%)|161.525s (50.52%)|56.554s (17.69%)|

Every configuration has1,231fallback modules and3,218parallel-route modules.
A fallback module may contain ordinary declarations too; the combined route
does not prove all its work is inherently serial. At8Pthe fallback plus outside
windows are51.47%of process wall. The parallel route also gets slower as the
worker footprint expands. Extra CPU is observed, but this experiment does not
separate pool/gate overhead, refcount/cache contention, heterogeneous scheduling
and other causes. Do not promote an unmeasured cause into the conclusion.

The measured result limits RQ3: existing dependency-frontier streaming gains up
to the previous P-core points do not imply continued whole-closure speedup when
adding E cores. It also does not contradict fast independent leaf checks: leaf
and full closure have different serial work and amortization.
