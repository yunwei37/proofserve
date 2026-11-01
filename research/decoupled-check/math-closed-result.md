# First complete same-artifact cost comparison
Self-review; this is one complete closure on one hardware/resource point.
Mathlib.Data.Nat.Basic has1,330 dependency modules and132,484 declaration entries.
Every source module was constructed with the stock4.34.1 compiler; the streaming
checker then consumed those exact newly emitted artifacts from one empty stock
kernel environment. All1,330 module acceptances match per-module native replay.
The three invalid proof controls also remain rejected by both paths.

- Full serial source compiler work, including per-module imports:622.379412s.
- Same-artifact streaming check total process wall:65.692644s.
- Cost ratio:0.105550799 (10.56%); construction/check cost ratio about9.47.
- Stream user/system CPU:65.508931/0.162724s.
- Stream peak RSS:754,252KiB (0.7193GiB).
- Source compiler maximum per-process RSS:753,736KiB.
- No timeouts, memory failures or sorry warnings in source construction.
- P cores0-7, outer child cgroup11.875GiB plus128MiB parent reserve, no-M.

These are different tasks (produce artifacts versus validate artifacts), not
a9.47x speedup of the whole original pipeline or of ProofServe serving.
The denominator is summed actual serial compiler subprocess wall; it is not
parallel Lake wall time or the C++ toolchain build. Lock wait is excluded.
The whole closure includes standard/compiler libraries, not just mathematics:
matched check kernel time includes Init49.72s, Std8.83s, Lean5.80s and Mathlib0.849s.
math-namespace-costs.csv separates these; the namespace split is descriptive.
This matters when interpreting small target-proof costs versus a checked base.

For the ordinary Nat.Basic root itself, read+map+kernel after verified
dependencies is0.026844s versus0.410718s production (6.54%). This is an incremental
component ratio, excluding process startup/shared base, not standalone latency.
The other whole closures and computational roots are still pending. No value
is substituted for them. Whole-run repetition/uncertainty is not yet measured.

Within this particular closed input, the80 Mathlib-namespace modules have
0.848916s pure kernel replay versus49.606740s source compiler work (1.711%).
That namespace contains tactics/helpers as well as mathematics; it is not a
population estimate of all mathematical modules. Its kernel-component ratio
cannot replace the whole-process, complete-closure10.555% comparison.
