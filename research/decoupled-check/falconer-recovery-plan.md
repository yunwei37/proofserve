# Falconer closure recovery (self-review)

The source closure is complete: 13,205 successful nodes = 8,128 newly
constructed + 5,077 exact common nodes from the same experiment. The sole
source failure was an old namespace overlay fault (0.053097 s), subsequently
recovered. Successful compiler invocation wall sum: 22,077.770248 s.

Window 14 completed construction then launched primary checking. It timed out
at 1,500.211 s (rc 124), with 8,942 complete accepts / 8,943 module headers and
one truncated JSON line. The parser raised JSONDecodeError and coordinator
exited rc 1. There is no full stream result, no finalized ratio, and no OOM:
memory.events reports zero oom/oom_kill. Preserve that raw attempt untouched.
The older 11,679-node report was a checkpoint, not the final source prefix.

Recovery retains the original kernel and context/duplicate checks. The adapter
currently recomputes transitive import closure from scratch per module.
IndexedAudit replaces only reachability with memoized ancestry bit masks;
by dependency-order induction this is the same import relation. No declarations
are inserted without kernel replay and no trust level changes. Native boundary
and corruption controls must qualify the change before measuring.

Every new task is finite, P0–7 locked, no -M, <=12 GiB external cgroup, with a
separate output directory and complete terminal result. Source construction is
not repeated. Small root subsets are independent complete-closure checkpoints;
full-check failure stays operational failure, never rejection or acceptance.
If the bounded full check remains too large, directory/root subsets yield
independent complete results with duplicated dependency work charged explicitly.
A native module-local replay comparison is separately resumable in fixed
chunks; its partial prefix cannot finalize whole-set parity.

The final report distinguishes full source build sum, timed complete kernel
checking, diagnostic/memory passes, module-local comparison, interruptions and
adapter qualification. It does not splice an interrupted prefix into a speed.
