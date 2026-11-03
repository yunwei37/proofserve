# Actual object-state evidence before full-closure timing
Matched SDK4.34.1commit5045d005. Direct borrowed-header reads use the shipped
lean.h:RC0 persistent;positive single-threaded;active negative MT;scalar;
sticky/frozen MT counted separately because it does not update RC.

Two completed ComputeControl P1 positive qualifications have2,365 frontier
calls each. Original compacted-input CI observations:462,919, all persistent
in both arms. These are repeated observations, not that many unique CIs.
Baseline bases are ST before sharing, then active MT in all2,365 post-enqueue
observations. Marked bases are persistent immediately after marking and in
all2,365 post-enqueue observations.

Direct base.find? probes distinguish replayed CI wrappers from original input:
baseline Nat.add/Nat.mul each have1 initial ST and2,364 active-MT observations.
With marking, each has1 initial ST before first mark and2,364 persistent;
all2,365 after-mark observations are persistent. c0/c1 are not present at these
probed frontiers; zero observations are not evidence about their final state.
Checks and per-module allocation units in both positive runs equal frozen
fd1e9be ComputeControl. No full-closure performance claim follows yet.

The exact stock-finalize probe reports kernel base ST (class1) when leakEnv
is false, and persistent (class0) when true. Original input100 CIs and imported
Nat.add/Nat.mul CIs are persistent in both. Both outer Lean.Environment wrappers
are ST, demonstrating why wrapper/base/CI layers must not be conflated.
Installed stock leanchecker module tasks use the false/false path, not the
assumed already-marked path. Its env is local to the module task, unlike our
cross-declaration shared base.

Marker-window raw total in this diagnostic P1 pair:off0.001896s/on0.033142s,
including timer overhead. No general performance/scale estimate is inferred.
Full timing disables CI probes; same executable on/off retains common timing
and root snapshots. Whole qualification sequence is still live or queued.

Build completed after one probe-only compile repair:CompactedRegion lacks an
Inhabited instance, so source now uses checked optional array access rather
than parts[i]!. Original failed source/logs are preserved on PVC; the stream
binary was already built successfully before that probe-only error.
