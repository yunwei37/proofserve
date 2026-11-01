# Actual full Barrier closure pair

This is the complete4,449-module closure, including425,463input entries and
3,595upstream unsafe/partial exclusions. Each arm starts a fresh native process
and empty checked environment, runs exactly one selected configuration and
finishes all native/cgroup cleanup. OS page cache is retained. No-M, P0–7lock,
same declared800s native budget and14GiB sampled/charged point inside16GiB lane.
One fixed-order pair, original O serial reference then repaired uniform4workers.

| Complete process | Wall s | Total CPU s | wait4peak RSS MiB |
|---|---:|---:|---:|
| Original O serial stream |474.850501|474.582037|2720.262|
| Repaired parallel4stream |304.861630|591.467022|3203.301|

Full-process speedup1.557594x,35.798% less wall,24.629% more CPU seconds.
Accepted module-ID sets equal each other and the full-prefix computational
curve:4,449/4,449. Input and upstream exclusion counts also agree. No resource
stop/native error; both groups/controller retired. This is actual measured
single-configuration whole-closure cost, not a sum of incremental leaf timers.

The earlier5.297x result is the eight-worker *leaf* curve. This full-cost result
uses uniform four workers and includes all dependency checks; these are different
resource configurations/scopes, not the same speedup with a different label.
A full uniform-eight point is not measured. No complete source-construction sum
for this precise4,449-node closure exists, so the63.03s leaf compiler observation
does not fill that missing cost-staircase cell.

Source: core8c62fc3, pair driverf1d987e; raw
/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v14 .
Complete timing/IDs/commands/memory events in full-cells.csv, full-pairs.csv and raw.
The coordinator/C ABI remain trusted implementation glue. Not a universal proof
of all malformed-input equivalence or a production-service throughput result.
