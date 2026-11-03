# Ramsey CertificatesK10: one required original-kernel reference

Review: 自审. Pinned openai/math4eaee87548250b2682affda7d05d947c05554bae,
Lean4.34.1/5045d0056413266e57c625dcd7c365b10e377c52, Mathlibd13f23b7.
This is a single-file preflight, not the unfinished directory result.

| Quantity | Source compiler | Original-kernel module-local reference |
|---|---:|---:|
| CPU seconds | 1725.133882 | 356.442522 |
| Wall seconds | 674.563076 | 357.111161 |
| Peak RSS GiB | 11.527206 | 3.083138 |
| Native return code | 0 | 0 |

Reference/source CPU = **20.661731%**, wall = **52.939625%**.
Each side includes its own startup/import. The source call emits typed artifacts
and C source. The reference checks the same typed file using the original
kernel replay API with its imports trusted, exactly the module-local reference
path used by the primary experiment. This accepted ID has been added to that
point's reference cursor and is skipped later; it is not counted as a fresh
whole-closure stream acceptance. Reference CPU is kept separate from the main
streaming numerator.

The source has no +kernel marker but12872ordinary by-decide proof tactics.
The full text also includes decide in expressions. This file is finite
certificate data, not a marker-free mathematical control. It nevertheless
requires only a fraction of source-production CPU in this measured reference.
No cost for the remaining targets or native full-closure checking is inferred.
[Exact source and reference cells](ramsey-k10-reference.json) preserve commands,
faults, cgroup events and limits. Both used the shared P0–7lock, no-M, external
cgroups inside12GiB and the same1400s native task timeout.

## Native observation-adapter qualification

Lean code generation succeeded in the first preparation attempt. SDK leanc
then failed to compile the tiny C clock helper because its include set lacks
time.h. That attempt and source remain unchanged onPVC. The repair compiles
only this helper to an object with system cc and SDK Lean headers, then links
it with the successful version-matched generated C using leanc.
Buildv2 and all4native controls actually succeeded: base and clock binaries
accept Init.Prelude; both reject the injected loose-bound-variable proof at
Nat.set_induction with the same original-kernel diagnostic.
The clock emits a positive process-CPU interval. These controls establish
basic observation and verdict compatibility only. Cross-binary checkpoint
restoration and full-corpus acceptance equality remain to be tested.
[Qualification cells](ramsey-cpu-clock-qualification.json) retain that boundary.
No primary source, compiled input, kernel implementation or measurement clock
was replaced by the observation copy.
