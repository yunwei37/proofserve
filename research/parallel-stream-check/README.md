# Parallel kernel-only stream prototype

M-lane implementation, Lean 4.34.1. The reader is copied from O's
`research/decoupled-check/AuditedStream.lean` without editing that source.

Independent ordinary declarations run against the same immutable frontier, in
dependency waves. Original `Kernel.Environment.addDeclCore 0 0` checks every
job. Tasks are joined before errors propagate. Returned typed constants must
match the input completely, and token indices must cover the wave exactly.
`checked_commit.c` validates frontier identity before committing checked
constants in original input order via the pinned runtime's map-insertion API.

**Trust boundary:** the coordinator and 40-line C commit adapter are additional
trusted implementation code. Mathematical checking uses the original kernel;
this is not a claim of an unchanged implementation TCB. Public environment
replay rechecks constants, so using it for commit would duplicate the work.
This prototype does not execute client metaprograms or imported IR.

Unsafe/partial exclusions match upstream replay. Inductive/constructor/recursor/
quotient modules and cyclic plans currently fall back to upstream replay.
Context conflicts retain O's module-local check. Compatible duplicate theorems
with differing proof bodies are checked under a collision-checked fresh name;
self-reference or different types take the module-local path. They never overwrite
an already checked name. Sibling-context, corrupt duplicate, and conflicting
definition controls are included.

The default has no chunk rewriting yet. Existing large-goal results are in
`research/chunked-kernel-check/`; integrating their certificate is pending,
rather than implied by the declaration implementation.

Raw data live on the PVC, outside Git:
`/workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v3`.
16 minimal-import native controls qualify; no full-closure speedup is claimed yet.
All measured cells use the existing P0-7 lock, no Lean -M, sampled own RSS plus
14GiB external cgroup cap inside the lane's 16GiB budget. Original per-module
source build cost and the serial stream are different operations and are labeled
separately.
