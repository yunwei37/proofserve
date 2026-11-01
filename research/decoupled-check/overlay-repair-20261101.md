# Falconer exact-artifact overlay repair

2026-11-01UTC, self-review. The first actual source window retained two
successful new source nodes, then failed Std.Data.DHashMap in0.053097s.
This was an operational dependency lookup failure, not a proof rejection.

Lean resolved the Std namespace in the new output root and did not fall
through to the older root for its missing Basic child. Reused artifacts must
therefore appear in the same namespace overlay as newly generated ones.

Preparation on E8 hardlinked the exact immutable successful shared artifacts
into the new output root:5,077 modules,25,377 typed/IR files,4,097,492,120 logical
referenced bytes,2.658s untimed setup. This does not copy those bytes or rebuild
the common modules. The original inodes and source measurements are unchanged.
Generated C/editor outputs deleted during cleanup are not needed by imports.

The failed cell, old progress, old controller terminal and source version are
retained. A new window resumes with the namespace overlay. The next invocation
gets a fresh attempt suffix; no command or stderr is overwritten. The reducer
reports successful source work and retained failed native work separately,
and includes both in the complete source-work denominator.

This repair is not a new performance or correctness result. Complete
construction, exact-artifact checking, memory profiling and native module
parity remain required before the Falconer ratio is finalized.
