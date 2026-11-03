# Frozen release evaluation

The release executable is built once from the commit containing this plan.
The prior observation from commit 51769793 is preserved separately and will not
fill any cell in this matrix.

The native matrix contains three repeats at 1, 2, 4, and 8 workers for each of:
Mathlib.Data.Nat.Basic, OAI.Analysis.PlanarPacking.Grid, and
OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41. At 8 workers,
Mathlib.Data.Nat.Basic and Grid also receive three repeats without persistence
and three without split fallback. Arm order reverses in the second repeat.

Official default and --fresh CLI controls receive three repeats per root using
the same toolchain and artifact search path. Default leaf checks trust imports;
fresh mode replays a final imported map. Neither is silently called an identical
per-module proof ledger. Their costs and selected scopes are reported separately.

Three bad terms are checked after a real Mathlib prefix. One Mathlib run is
actually interrupted after its first certified segment and then resumed.
Its total CPU and wall costs are compared with the uninterrupted 4-worker runs.

A separate run requests every one of the 8,529 Mathlib source modules at commit
d13f23b723b8a846827a245b89c10fc7d3f11612. All matching input artifacts exist.
It uses default workers and the normal 500-module segment size. If memory fails,
one retry uses 100-module segments. Failure remains an operational result.

Every native cell acquires the existing P-core lock, runs on CPUs 0–7 without -M,
and retires before the next. The sampled process-tree RSS stop is 15.75 GiB,
reserving 256 MiB for the small controller inside the 16 GiB M-lane allowance.
A 16 GiB charged-memory cgroup provides an additional, distinct safeguard.
Ordinary native cells have an 1,100-second limit and full-Mathlib attempts have a
1,700-second limit. These finite limits remain explicit in failed results.

Large reproducible output snapshots are retired only after a complete receipt,
acceptance vector, command, and native result are retained. Input artifacts,
interrupted prefixes, logs, and failures are kept. Cleanup paths are recorded.
No per-cell commits or new profiling experiments are performed.

The full-library input manifest includes the top-level Mathlib umbrella module,
in addition to the 8,529 modules under the Mathlib source directory. This avoids
silently presenting a directory-only manifest as every Mathlib module. Its
collector is continued only at a completed native-cell boundary; the executable
and completed performance measurements remain unchanged.
