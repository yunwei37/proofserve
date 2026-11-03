# The coarse lookup bucket contains ownership bookkeeping
This is post-hoc source/instruction localization of the same captured samples,
not a new native experiment, a precise stall measurement or a runtime change.

In the strict checkOne+C++kernel-anchored scope, the largest growing leaf is
the generated lookup wrapper lean_environment_find:26.751→60.129billion
sampledcycle-periods(+33.378). The C++environment::find bridge grows
7.760→15.082(+7.322);lean_dec_ref_cold87.418→103.667(+16.249).
The complete strictscope increase is84.764billion. Source-labeled positions
at/immediately after RCheaderloads or atomic RCupdates within these three
functions grow83.159→135.735(+52.576), about62.0%of that observed increase.
This is a diagnostic localization, not a lower bound on removable CPUtime or
a claim that removing RCwould remove62%of the execution cost.

The frozen actual disassembly is retained beside the data. The C++const lookup
increments the environment/name argument references before calling the Lean
lookup. The generated Lean helper acquires/releases an inner object and the
environment argument. Its hot positions0xe,0x1c,0x74are adjacent to RCheader
loads;0xd2is immediately after its MTatomic update. In the C++bridge0xfis
after the receiver RCheaderload and0x49after its MTupdate. Thus a bucket named
hash/lookup is not purely hash arithmetic. This directly addresses the user
hypothesis without relabeling all that bucket as RC.

[Matched Lean4.34.1lookup bridge](https://raw.githubusercontent.com/leanprover/lean4/v4.34.1/src/kernel/environment.cpp)
calls the owning-argument conversion before the generated lookup, consistent
with the actual increment paths in the frozen binary. Shared input environment
metadata is a concrete candidate for cross-core ownership traffic. Runtime data
addresses weren't sampled, so same-counter contention versus false sharing,
task/private-heap migration and other cache effects are not independently
identified. Pool threads start checks on all allowed cores across waves.
Cycle sampling can skid; incomplete C++inline debug persists. Do not treat
adjacent-PCperiods as retired-lock instruction samples or exact atomic latency.

The coarse table still correctly says lookup-path growth is largest. Finer
instruction evidence supports RCmetadata/coherence participating within that
path, while the completed stat pair shows almost unchanged instructions/
locked-access counts and greater modified-line traffic. This is evidence
supporting the proposed mechanism, not an intervention proving its exact
causal fraction. No Leanoptimization is part of this study.

Reproduce with perf/ip_localization.py on the retained compressed address/
offset aggregates. Its role labels are specific to this exact fd1e9bemeasured
fixture and must be rechecked against assembly for any other binary.
