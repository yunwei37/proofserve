# Durable segmented kernel checking (self-review)

The second unsegmented attempt also timed out:1500.204755s,9040 complete
accept events,rc124. The reachability cache did not solve scale. Its raw
output is retained; do not report a speedup or complete checking ratio.

CheckpointAudit exports only constants already in the original kernel's
checked environment, using Lean4.34.1 saveModuleData. A delta imports only
the successful preceding certified delta. Pure visibility/origin/quarantine
metadata is serialized as a private experiment extension; it is not an
untrusted public input format. On restart the original Lean importer loads
that checked prefix, and the unchanged original kernel checks new declarations.

A segment stops after500 newly accepted modules, saving the prefix before
exiting. The next process starts from that prefix; there is no long-lived
Lean process, and the optional queue can die without losing completed state.
The run is one validation of frozen source/compiled inputs. It cannot reuse
a snapshot after changing its certified input prefix. It is not production
failure caching or a change to the kernel. Serialization/import and the audit
adapter remain part of the experimental correctness obligations.

Five native qualification cases completed across18 separate processes with
a forced checkpoint every module: ordinary duplicates, corrupted duplicate
proof, unimported sibling proof, conflicting definitions and private names.
Both bad-proof cases reject after successful restore. These are untimed
preparation on E8, not P-core performance evidence. Full commands, outputs,
snapshots and completion records remain at checkpoint-recheck-v2.
Two earlier compiler errors and the unused full-snapshot preparation remain
recorded; its waiting control was canceled before it had any child process.

Each timed segment uses the shared P0–7 FIFO lock, external11.75GiB child
cgroup plus a small parent, no-M,1400s child and1740s outer wall bounds.
Every complete segment is independently reduced and committed/pushed; the
queue re-enters behind current waiters after each segment. Snapshot attempts
never overwrite an existing snapshot. Raw delta objects stay on PVC;
only small cost CSVs/results enter Git. Disk free before preparation:23.52GB.

Aggregate all segment wall/CPU, including startup/import/export/normal exit.
Keep the two failed full-check attempts and any failed segment work visible.
Compare the complete segmented sum against the successful source compiler
sum22,077.770248s. Do not relabel a segmented sum as a single uninterrupted
check. Full native graph and13,205 accept events, plus the independently
running original module-local oracle union, are required for whole-set parity.
