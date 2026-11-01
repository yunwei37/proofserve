# Corrected matrix: thread stability is not observer stability

2026-11-01 UTC; M/B lane; self-review (自审).
Corrected v2 Probe, Lean4.34.1 and matching Mathlib. Selected16sources, not a
population estimate. Historical4.9 and defectivev1 points are kept separate.

## Complete execution

1536/1536observations:16sources x2budgets(1000/3000) x2frontends(stock async/sync)
x3observers(off/native profiler/allocating trace) x4threads(1/2/4/8)
x2repeats(reverse observer order).

Qualification2completed10real observations: True accepted, false decide rejected,
sorry incomplete, parse error rejected with matching diagnostics, new axiom
detected as incomplete. Earlier escaped-newline controls are retained/excluded.

Controller247273and all17native cells retired, returned0; no OOM/RSS stop/timeout.
Native walls sum165.091187s, maximum wait4 RSS8,847,076KiB. No -M; P0-7/flock.
Raw: /workspaces/.agent-state/gpu-smt-captures/reproducible-verdict-v2.

| Comparison | Pairs | Verdict differences | Acceptance differences | Sync raw-HB differences |
|---|---:|---:|---:|---:|
| threads1 vs2/4/8, off |384|0|0|0|
| threads1 vs2/4/8, native profiler |384|0|0|0|
| threads1 vs2/4/8, trace profiler |384|0|0|0|
| off vs native profiler |512|0|0|4|
| off vs trace profiler |512|24|8|256|
| stock vs sync frontend |768|8|8|not comparable|
| repetition/reversed order |768|0|0|68|

Pairs are source/configuration observations, not independent sources.
Raw totals:accepted664,lean_error512,budget_exhausted360.

At B1000 minif2f-1041 sync/off is accepted (theorem command833553rawHB);
sync/trace exhausts budget (1134535rawHB). Four thread counts x2repeats give
8acceptance differences. Stock/trace accepts it, so sync accounting is NOT a
transparent stock budget replacement even after fixing parser-message loss.
The remaining16off/trace classification changes are minif2f-2797 at B3000,
ordinary error becoming budget exhaustion in both frontends; never accepted.

## Two-regime implication

These mathematical tactic candidates show stable same-observer heartbeat
vectors and verdicts across thread counts. No scheduling-induced mathematical
instability is demonstrated here. Observer/history effects are separate axes.
Thus 'deterministic budgets are needed only in the mathematical regime' is
NOT established. Computational-regime data must measure actual closed targets,
distinguish kernel-only units from whole candidates, and allocations from polls.

## Outstanding

Budget ladder and scoped cache task277382/birth761789543actually queued after
v2retirement. Computation/math joint comparison and original-kernel replay
qualification are still pending.

Lab comparison is NOT completed. Read-only SSH found onlyLean4.30in the standard
user toolchains; command-v lean, /opt/lean, /usr/local/bin/lean and host
/workspaces were absent. This does not prove4.34.1is absent everywhere.
Needed: matching4.34.1SDK, matching compiled Mathlib closure and an authorized
test environment. No host install, Workspace move, or other Pod modification.
