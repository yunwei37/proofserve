# Step038: P4/P8 PMUcounts support a coherence-cost hypothesis, not yet RCcausality
EXPERIMENT_GATE: both complete fullstat runs, identical4,449reference accepted
IDs and ordinary checks/allocations, allseven events100%running.
Whole-command usercycles+8.3107%;instructions+0.03961%;lockedloads+0.11710%;
L3miss loads+11.9794%;L3modified-line-response loads+46.4111%;
RFOmodified-line requests+49.7555%. IPC1.833725→1.693693.
Cycles/reference-cycles0.885624→0.874085(-1.3029%); referencecycles+9.7406%.
Frequency change alone cannot explain the extra observed cycles/instruction.
Near-identical whole-command instructions and locked-access counts, with
higher CPI/coherence traffic, support a cache/coherence cost explanation;
they do not establish which object/operation produced it. Serial phases are
included in these totals, so do not relabel them kernel-only counters.
P8record still pending and required for category attribution.

WRITE_GATE: actual same-closurestat comparison saved. Added small offline
offset bins within the known lean_dec_ref_coldsymbol using verified frozen
binary disassembly, before looking at any P8sample. P4anchored helper weights:
17.654billion cycles-periods at0x11immediately after the outerLOCKincl;
4.565billion at0x91after the childLOCKincl;
61.716billion in the other destruction-loop region;
3.483billion at other header-fastpathIPs.
The loop also contains RCheader loads and further child-reference work,
so it is not a pure allocator bucket. Cycle events can skid: these adjacency
weights are not exact atomic stall time, retired-lock instruction samples,
or a shared-versus-private object classification.

REVIEW_GATE 自审: work and countercoverage verified from actualstat, no mixed
record/stat clocks or rescaled historical denominator. Current data undermine
a frequency-only/large extra-instruction explanation at whole-command scope,
but shared atomics, task/heap migration, allocator/cache effects remain
alternatives. No Leanchange. Fullmatrix6/16returned; continue blocking wait.
