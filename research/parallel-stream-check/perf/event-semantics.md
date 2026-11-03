# Counter scope and model-specific event naming
Actual CPU read during the matrix: GenuineIntel family6model183(0xB7),
i9-14900Kstepping1. Intel's current mapfile assigns the Pcore to ADLGoldenCove
events; selected vendor records/version are saved beside this note.
- [Intel family/model mapping](https://raw.githubusercontent.com/intel/perfmon/main/mapfile.csv)
- [Matched Pcore events](https://raw.githubusercontent.com/intel/perfmon/main/ADL/events/alderlake_goldencove_core.json)

The native record attrs resolve the selected legacy XSNP_HITMname to
XSNP_FWD(config0xd2/umask0x04). The matched Intel entry also describes this
event as retired loads receiving modified-line responses, so this is an alias
in the actual selected encoding, not an unsupported counter or a new0value.
Locked-load events count retired instructions, not stalled cycles. L3miss is
retired load-instruction misses, not every LLCrequest from every agent.
Counter totals refer to whole command or recorded thread lifetimes; only
period-weighted, checkOne+C++-anchored samples concern the ordinary original
kernel calls. Never infer an exact RCstall fraction from HITMcounts.

Aggregate coherence counts cannot distinguish shared reference counters from
other shared metadata or private allocator data migrating between cores.
Cycles sampling can skid; static nearbyLOCKinstructions are not precise
retired-lock samples. Inline RCsymbols are partly unavailable. Use the exact
same work/thread comparisons first; retain unresolved inline costs and sample
coverage rather than assign all environment/hash/typechecker cycles to RC.
No event selection, native code, affinity or sysctl changed for this lookup.
