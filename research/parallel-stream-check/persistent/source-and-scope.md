# Persistence layers and the matched upstream checker
Matched SDK4.34.1 commit5045d0056413266e57c625dcd7c365b10e377c52;
installed source and small native probe are retained on PVC. This corrects
the premise that all environments loaded by the stock checker are leaked.

| Object / stage | Observed state | Evidence scope |
|---|---|---|
| Original compacted input ConstantInfo | persistent | ComputeControl imported parts;462,919 repeated observations, not distinct constants |
| Stock finalizeImport false kernel base | single-thread | native official-import probe |
| Stock imported Nat.add/Nat.mul CIs | persistent | actual header probe; does not imply all environment layers persistent |
| Stock finalizeImport true kernel base | persistent | native official-import probe |
| Outer Environment wrapper after either finalize mode | single-thread | final record update constructs a new wrapper |
| Replay base before task enqueue, unmarked | single-thread | all18,990 primary frontiers per full cell |
| Same replay base after task enqueue, unmarked | active MT | actual post-enqueue header counts |
| Replay-created/stored Nat.add/Nat.mul wrappers | active MT after sharing | diagnostic ComputeControl probe, distinct from compacted input |
| Marked replay base before and after enqueue | persistent | every primary frontier; diagnostic CI probes disabled during primary timing |

Installed LeanChecker.lean replayFromImports calls importModulesCore then
finalizeImport(...false,false), rather than leakEnv=true. Its default parallelism
is one IO.asTask per module, followed by sequential replay within each task.
A task-local ST root is different from our root shared among declaration workers.
Environment.lean documents leakEnv=false by default and leakEnv=true as avoiding
RC updates when an environment already lives until process end.
The stock default therefore is not evidence of a marked shared replay base.
Compacted payloads being persistent does not mark newly built hashmap/CI wrappers.

The original Runtime.markPersistent primitive recursively sets RC0 and skips
already persistent subgraphs. Source task publication consumes its closure and
finishes mark_mt before publishing its value; all previous wave tasks are joined.
Our call is before enqueuing the next wave. This supports the stated quiescent
site, not arbitrary user extension tasks. Runtime/source safety remains an
explicit implementation precondition, not a formal whole-system proof.

Stock one-root default checks the leaf with trusted imports; --fresh replays one
final imported environment. Neither is identical to independently rechecking
all4,449 modules with our exact per-module check/allocation vectors. Planned
native stock timing controls are labeled by their actual scope. The original
kernel is unchanged; unsafe coordinator/FFI correctness is still trusted glue.
No new mathematical axiom or skipped proof check is introduced.


Read-only ready-snapshot detail: waves with multiple workers hold the common
gate until the root read; the single-worker path has no gate and may already
be checking at that read. The marker itself is always before enqueue in both
paths. This wording does not move the marker or mutate running code.

Stock import-header observations are at the importer return, not a census
inside Replay.lean. Matched Replay uses StateRefT state and serial replayConstant/
replayConstants calls; intermediate newly reconstructed SDK objects were not
header-probed. Do not infer that the stock replay retains ST headers forever,
has no atomic RC, or persistently marks every new CI. Those were not measured.
The stock 'already persistent' premise is corrected by distinct importer/base/
CI layers, not replaced by a different unobserved whole-runtime assertion.
