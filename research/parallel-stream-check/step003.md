# Step 003 — complete exact-closure matrix (自审)

## EXPERIMENT
Frozen v4 completes all 18 cells: O reference, audited serial, parallel1/2/4/8,
three repetitions each. Actual controller/native processes and P lock retired.
Every cell accepts identical 1330 IDs, 132484 entries, 2269 upstream exclusions.
All memory groups retired with no timeout/guard/OOM/native error.

Fresh median wall: 65.9399/74.5306/78.4043/75.2648/59.0900/57.0523 seconds.
8-worker/reference ratio of medians 1.15578x; 13.48% less wall, 17.24% more CPU.
Ranges and all paired ratios are in math-results.md and CSV; do not suppress the
large spread or slow 1/2-worker results. 858 modules /55255 jobs /3616 waves run
in parallel;472 modules use original complex/cycle serial replay.

## WRITE
math-results.md, 18-row cell CSV, six-row summary, completeness and labeled cost
staircase are generated from complete real files. O source build622.379s is its
recorded serial compiler work, not a new build measurement or identical task.
Missing O internal stage timers are unknown, not zero. Kernel-only admission is
not source elaboration or module-extension integrity.

## REVIEW — 自审
No whole-library/novelty/strongest-checker claim. Trusted coordinator/C adapter
remain explicit. Positive fixed-input acceptance equality is measured, not a
universal malformed-input equivalence proof. An indirect local-cycle interaction
with compatible duplicate theorems was identified during source audit; construct
a negative native control and strengthen this boundary before calling the
combined prototype qualified. Chunk source preparation is not yet a result.
The pending build waiter saw a transient proc entry after pidfd exit readiness
and stopped before any compiler; actual matrix retirement subsequently verified.
