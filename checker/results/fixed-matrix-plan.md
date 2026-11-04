# Final release evaluation plan

No final timing is scheduled during the workload gate or census. CPUs 0-7 and
10-23 belong to W during that period; M preparation uses CPUs 8-9 only.
The completed ba316991 observations remain nonfinal previews.

After the census, first verify the whole 163,097-module corpus using the pinned
module manifest and the release checker. Then freeze the final executable and
run the performance matrix on a quiet machine. Record the exact source commit,
input identities, runtime placement, and complete receipts.

The matrix is Mathlib.Data.Nat.Basic, OAI.Analysis.PlanarPacking.Grid, and
OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41. Each dependency
closure receives three fresh-checkpoint runs at 1, 2, 4, and 8 workers.
At 8 workers, Nat.Basic and Grid also receive three repeats without persistence
and three without split fallback. The second repeat reverses worker order.

Official default and fresh controls receive three repeats per root. Append a
canonical artifact root after the original overlay when a symlink's real path
would otherwise be outside every enumerated search root. This preserves lookup
precedence and artifact bytes. Default leaf checking trusts imports; fresh
checking replays a final imported map. They are not an identical per-module
proof ledger, so do not invent a scope-normalized speedup.

Three bad proof terms after a real Mathlib prefix must still reject. One real
interruption and resume is compared with an uninterrupted 4-worker run.
The once-only complete Mathlib scale preview is already finished; it is not
queued again by this final matrix.

Finally, run the real PlanarPacking proof root from bench/planar-target.json
once at default workers and once at 8 workers, with the official procedures
scoped explicitly. The Comparator challenge file is a specification containing
sorry, not the submitted proof. No speed claim may be made by checking only it.

No Lean -M is used. Timed native requests use the shared P-core lease and CPUs
0-7 only after W has finished. The external memory guard reserves 8 GiB of host
available memory and samples its owned tree every second; sampling can react
after a transient crossing and is not a kernel hard RSS quota. The temporary
cgroup's charged-memory limit is distinct from aggregate process RSS.
The caller records finite native limits and all operational failures.

The complete fixed performance matrix has 71 planned attempts: 48 native cells,
18 official controls, 3 bad terms, and 2 interruption/resume legs. Whole-corpus
verification and the later PlanarPacking comparison have separate receipts.
Completed root batches retain their local certificates and input identities;
only their regenerable environment snapshots are retired. Failed and partial
attempts remain visible. Results are committed at complete boundaries, not
once per matrix cell.
