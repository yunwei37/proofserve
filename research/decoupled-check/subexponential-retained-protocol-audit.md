# Retained dependency compiler-record audit

Review: 自审. All10744retained dependency command/result files were read
directly, not assumed from current runner settings. See adjacent JSON for
literal counts, including missing records if any, Lean memory flags, affinity,
source rc, measured flags, timeout limits, cgroup caps and memory events.

The old records use180/300s per-call deadlines; new target calls use1400s.
Both measure successful original compiler work rather than equating deadlines.
The original small dependency point reserves128MiB for the parent
(cgroup11.875GiB); later/current point reserves256MiB(cgroup11.75GiB).
Do not describe them as identical external caps. Both fit the user's total
12GiBallocation, use P0–7/-j8/no Lean-M and original authored package options.
These records supply already-paid source costs, not a new from-scratch
continuous wall run or proof that resource/caching differences have zero effect.
The incremental denominator explicitly excludes this historical source work.
