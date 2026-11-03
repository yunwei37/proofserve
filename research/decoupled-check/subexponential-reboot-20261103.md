# SubexponentialSAT: host-reboot interruption and continuation

Review: 自审.

The user reports a14:48UTC host reboot of unknown cause, Ready around14:50UTC. At14:39UTC our control-plane read had Ready=Unknown and last heartbeat14:35:01; existing SSH paths failed. No O recovery mutation, reschedule or replacement capture was performed. The old primary and post-run processes did not survive.

**Completed prefix retained:2425/3977targets +10744dependencies =13169/14721source nodes.** All2425ledger rows parse, end in newline, report rc0 and match their command/result JSON. State coverage equals successful module IDs plus the retained dependency set. All13169source-produced oleans are present, nonempty and have the Lean artifact header; all2425new target C/ilean outputs are nonempty and producer hardlinks match. This is structural/provenance checking, not a substitute for the planned complete original-kernel stream and module-local reference.

The pending task-7769261375147801 has a0-byte log and no unmatched native source-command record. The next uncompleted module is OAI.Algorithms.SubexponentialSAT.SqrtLog.RingProgramTableBridge (frame13169); no output for it was found. Thus the dispatch is labelled **host_reboot_interrupted**, with unknown time excluded from costs and not treated as censoring, native proof rejection, or a completed timing sample. There is no observed native start to assign a false failure to this module; it will be built normally. No completed source module is rerun.

Existing original compiler/Lean/C/kernel-checker sources and capture ledger are unchanged. Continuation uses the same finite worker: P0–7/shared FIFO flock, no-M,1400s native/1740s outer limits, native11.75GiB cgroup plus256MiB parent reserve. Only native child intervals are summed across the reboot; no continuous episode wall clock is formed. The self-owned short TERM control returned-15 after recovery. Current future-work scenario is5.063474CPUh (prefix mean, stream scenario and reference reserve), not a bound.

Raw interruption evidence remains under the existing capture subexponential-20261103/reboot-20261103T1448/. If the node drops again, preserve state and wait for the operator; perform no host recovery or scheduling mutation.
