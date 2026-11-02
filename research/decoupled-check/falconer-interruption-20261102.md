# Falconer terminal diagnosis, 2026-11-02 UTC

Self-review. Prior 11,679-node message was stale. Current source frame and
progress contain all 13,205 nodes, with 8,128 new compiler successes, 5,077
successfully built exact common nodes charged once per closure, one recovered
source fault (0.053097 s), and no unresolved source failure.
Successful compiler wall sum is 22,077.770248 s; with that recorded source
fault it is 22,077.823345 s. These are summed invocations, not parallel
Lake build time or uninterrupted elapsed time.

The checker did NOT finish. primary.result.json records rc124 at1500.210998 s,
1473.495198 user +9.467307 system CPU s, memory.events oom=oom_kill=0.
Only8,942 full accept events /8,943 headers survive in stdout; an incomplete
last line causes JSONDecodeError at line72 of falconer-window.py. The
coordinator then exits1 with status "window exit without terminal".
The acceptance prefix is a lower bound on completed observations, not a
full-closure verdict. No full stream/build ratio exists at this point.

Raw directory (unchanged):
/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/scale-study/falconer-project-20261101

Recovery directory: bounded-recheck-v1 underneath it. Fixed-cost source work
is retained, not rerun. IndexedAudit caches import-reachability using bit
masks, retaining every kernel replay and module-local context fallback.
An untimed independent DFS over all13,205 source nodes confirms the masks
match the old graph relation. This alone is not native semantic qualification.

Recovery uses independently executable <=1740s cells, each with a terminal
file, external11.75GiB child cgroup plus a small parent, P0–7 lock and no-M.
Native boundary/corruption controls precede a1500s full check. Module-local
oracle chunks retain complete accept lines and can resume after one chunk
dies; interrupted checking is not a rejection. The native full-check estimate
is still unknown until the optimized adapter is exercised; the source gap
is zero, not another hour of compilation.

See admission-control-reconciliation.md for the separate17 vs14.33 CPU-replay
control: the all-serial control retains type-level upper admission, uses less
CPU per Grid request and therefore completes more. It is evidence against
incremental CPU-budget benefit from type-selected parallel checking.
