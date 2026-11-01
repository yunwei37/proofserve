# Grid: matched computational component observation

Self-review. The stock4.34.1 compiler successfully reconstructed the entire
3,793-module Grid closure. The exact emitted artifacts then completed streaming
kernel replay with exit0 and the complete3,793-member acceptance graph.

| Quantity | Observation |
|---|---:|
| Sum of closure native compiler subprocess wall |3,878.706740s|
| Matched whole-closure stream wall |563.082232s|
| Whole-closure stream peak RSS |2,328,540KiB(2.221GiB)|
| Grid target compiler wall, including its imports and standard outputs |318.230852s|
| Grid target replay component, in the shared process |255.486529s|
| Target replay component / target compiler wall |80.2834%|
| Grid target module read / map components |0.0000557 /0.0021473s|

The target ratio is a **component** comparison, not two standalone application
wall clocks. It omits shared-process startup and dependency checking from the
target replay component and includes target imports/artifact production in its
compiler cell. The compiler uses -j8; replay uses the original kernel and its
actual execution behavior. These facts bound the interpretation.

This computational target has a much larger checking fraction than the
ordinary Mathlib namespace component(0.848916s kernel /49.606740s compiler,
1.7113%). A whole-closure ratio can be much smaller than80% because expensive
source construction of shared mathematical dependencies is also in its
denominator. Do not use the whole-closure ratio as evidence that this
computational certificate alone is cheap to validate.

At this observation the per-module oracle had finalized1,746/3,793 modules;
the target's matched module-local result and full parity were still pending.
Therefore the whole-closure ratio remains **unfinalized**, despite the stream
and construction both completing. Amplitudes remains a distinct pending
cohort; no expected ratio is inserted.

Input entries382,707 include3,554 upstream-unsafe/partial exclusions.
This is not382,707 individually checked safe proof bodies. Mapped regions are
retained throughout the process; peak RSS is wait4 RSS, distinct from cgroup
charged-page counters. No OOM occurred. All timing used P0–7 and the existing
shared flock, with outer cgroup memory protection and no -M.

Original commands, outputs, timings and memory.events:
`/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031`,
cells build-03792 and timed-constructed-stream-compute-grid. The small CSV
retains the explicit observed oracle coverage rather than silently advancing
it from later measurements.
