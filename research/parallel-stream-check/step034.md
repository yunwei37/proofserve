# Step034: P4 original-kernel samples actually decoded
EXPERIMENT_GATE: fullP4record accepted identical4,449IDs and identical ordinary
work. Wall349.724s/user649.140s/system7.983s, kept separate from normal times.
35,145cycles samples, allpositiveperiods, reportedzero losses. Per-thread
READtable covers5/5historical observed check-worker TIDs. Decoder complete,
sampled own tree peak856,678,400bytes, actual decode214.960s on E8-15;
this is offline CPU, not measured verifier overhead.

Period-weighted primary anchored sample cycles653,429,387,673:
RC/destruction88,559,751,583;hash/lookup266,394,725,102;
allocation68,476,621,753;whnf/defeq140,837,028,642;
otherinference87,944,848,153;other1,216,412,440.
These are estimates within covered stacks, not exact hardware event counts.
Another388,739,494,060periods have an observed worker TIDand C++kernel frame
but lack checkOne ancestry. Serial/otherkernel249,496,955,999;
workerother/truncated10,709,988,150;outside91,610,104,332.
Total1,393,985,930,214. Primary anchored scope is62.7%of anchored+unanchored
worker kernel samples, not full coverage. Do not silently combine scopes or
attribute a4→8difference caused by depth/coverage to a semantic category.

WRITE_GATE: complete P4small per-thread counter/IPC/L3miss and categorical
tables saved, native and observation clocks separate. Matching Intel family6/
model183Pcore metadata verifies the XSNP_FWD/HITMalias0xd2/umask4. Record raw
remains PVCuntil this derived analysis is committed. Address/offset weights,
native logs, resources and static disassembly retained. Actual RCcold+0x11
sample hotspot is immediately afterLOCKincl, a candidate, not a causal
contention measurement; compare same full-work4/8before interpreting.

REVIEW_GATE 自审: actual decoder/parent/native retirement and actual worker
coverage verified. Five historicalTIDs are not active5worker concurrency.
No P8samples yet, no negative/perf-overhead conclusion before aftercontrol.
Full study3/16native returned; P4after already genuinely queued, controller
collect/decode policy stays active. No Lean/event/affinity change.

Offline resource correction before the next record decode: now that the latest
user explicitly requires serial per-cell decode, reuse the existing native
14GiBguard for analysis instead of the earlier1GiBconcurrent-decode guard.
P4actual1GiBconfiguration remains in its rawmetadata. Later offline decode
may use14GiBwithin16GiBlane with no own native alive; this is not a native
resource/config change or perf-overhead point. Avoid making an unnecessary
analysis-only limit an artificial failure. Decoder algorithms unchanged.
