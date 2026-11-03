# Step029: real native PMU control and explicit failed record qualification
EXPERIMENT: retained ComputeControl, fixed fd1e9be native binary and C observer,
P8/taskset0-7/blocking lock/no-M. q1 failed before Lean: GNU time absent.
Installed Workspace Debian time1.9-0.2, .deb cached on PVC for restart. No
host settings changed. q2 plain/stat both complete650 reference accepted IDs,
native/cgroups retired. Raw whole-command stat seven events all100%running:
211793745860cycles,332175553747instructions,IPC1.568392;
9108073retired L3miss loads,683461088locked loads,92331273L3HITM and
54811816RFOHITM. This is a short native control, not complete Barrier closure
or a worker-count comparison. Counter scopes are whole command; no causal
RC/cache-contention result is inferred.

q2record failed before Lean: optional -z argument was passed as a separate1,
which perf treated as workload. Saved stderr/terminal, changed to
--compression-level=1. q3record alone really queued under blocking flock,
PID504330/birth772216809, arrow verified. No duplicate native started.
The q2 qualification remains partial; parser acceptance had not proved runtime
CLI behavior. Initial q1/no-time failure is retained on PVC.

WRITE: small control counters/native terminals and explicit failure retained
here; raw PERF/PVC remains outside Git. Plain wall32.137s/user76.302s/sys0.838s,
stat32.269s/77.074s/1.219s are distinct instrumented arms, not a speedup or
overhead estimate with replication. Native stack/per-thread qualification is
still pending. Source inspection corrects an alternative: sharecommon tables
are local helper state, not evidence of a global hash-consing mutex.

REVIEW 自审: main and owned paths only; no foreign changes stashed.
Seven counters have real values, but record counters and sample anchoring do
not yet qualify. No Lean modification; original full finite series already
completed and archived. Continue new perf study after actual qualifier results;
the project remains active.
