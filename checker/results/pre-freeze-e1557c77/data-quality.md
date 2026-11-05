# Qualification data boundaries

These E-core runs occur during W's census and are not final paper timings.

The first Grid invocation reached its 1,800-second finite window and retired.
Its guarded command, memory samples, exit and complete segment checkpoints are
retained. Continuation uses the same binary and state, not a fresh speed run.
The native resume path truncates an uncommitted segment's .events file before
replaying that segment. The operator of this M run did not archive that partial
event file before the first continuation. That intermediate event sequence is
therefore not separately retained; the complete checkpoint records and timeout
attempt remain. Do not claim every partial event was preserved or use partial
accept events as a final acceptance set. Subsequent complete segment events and
the final receipt establish the reported final set.

Any additional continuation must archive the state directory's small log/event
files before starting. Sum guarded attempts only as actual operational CPU
including interrupted/repeated work. Report complete-segment CPU separately;
do not splice the split clocks into one uninterrupted benchmark.

The first extended theorem-body diagnostic had a Lean token-spacing parse
error. Its failed source/output remain beside the successful corrected copy.
No production native source is changed by that diagnostic.

The command-line transport disconnected while waiting for the retained 3fe Grid
reference. On reconnection at 2026-11-05 03:46 UTC, the PVC already contained its
successful terminal and receipt. Its process and cgroup had retired, and W's
controller birth identity was unchanged. No native task was restarted for the
transport failure. The observation gap is not part of the reference's native
1,062.80-second interval.
