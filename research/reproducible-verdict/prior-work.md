# Prior art and claim boundary

2026-11-01 UTC, B/M lane; self-review (自审). Primary sources read online
and pinned implementation sources inspected in the retained Workspace.
This is a claim audit, not a claim of venue acceptance or exhaustive absence.

## Candidate claims and direct decision

1. Replace wall time with deterministic proof work: **not new**. Lean
   heartbeats and ACL2 prover-step limits already do this.
2. Identical budgeted outcomes across threads/observers/hardware:
   **not established; the unrestricted statement is false** for programs that
   inspect time, options, available budget, external state, or experience OOM.
   Lean itself already fixes nondeterministic budget accounting. Its
   shared-thunk fix is directly overlapping prior engineering.
3. Re-run evidence for a budgeted verifier outcome: record/replay is established.
   A possible increment is a measured contract covering actual RL verifier
   budget/observation boundaries plus independently rerunnable receipts.
   No new mechanism or complete cross-machine guarantee is established yet.

These are findings against the requested hypothesis, not an unapproved change
to the paper thesis. The main thread owns synthesis.

## Verified sources

| Primary source | What it already establishes | Implication |
|---|---|---|
| [Lean IO timing manual](https://lean-lang.org/doc/reference/latest/IO/Timing/) and [v4.34.1 allocation runtime](https://github.com/leanprover/lean4/blob/v4.34.1/src/runtime/alloc.cpp) | Heartbeats track small allocations on the current thread; counter adjustment is public. | Not a process-wide allocation total or new deterministic-clock proposal. |
| [v4.34.1 CoreM](https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/CoreM.lean), checkMaxHeartbeatsCore and wrapAsync | User units multiply by1000. Async wrapper carries work already spent into a child context. | The premise that all threads simply share one global heartbeat counter is incorrect. Child totals and inherited prefix work cannot just be summed. |
| [Lean shared-thunk fix 51c2c9e116cecfffb3c8f9f3bf650857d1b55f44](https://github.com/leanprover/lean4/commit/51c2c9e116cecfffb3c8f9f3bf650857d1b55f44) / PR15890 | Scheduling decided which thread paid for shared thunk evaluation. The fix excludes shared/persistent thunk work, while local thunk work still counts. | Direct same-problem/same-mechanism risk. Do not rebrand this fix as ours. Official GitHub API resolved the full commit/message; distribution backport status still needs checking. |
| [Lean PR13956](https://github.com/leanprover/lean4/pull/13956), [4.33 release](https://lean-lang.org/doc/reference/latest/releases/v4.33.0/) | Kernel recursion is limited by maxRecDepth instead of native stack size, addressing platform/build dependent failures. | Cross-platform resource-verdict stability is already an explicit upstream concern. |
| [ACL2 with-prover-step-limit](https://acl2.org/doc/index-seo.php?path=5540%2F7933%2F3532%2F476&xkey=ACL2____WITH-PROVER-STEP-LIMIT), [release4.3](https://www.cs.utexas.edu/~moore/acl2/v6-3/NOTE-4-3.html) | Proof-step budgets, counters, nested charging/exemption; units may change across versions. | Direct prior art for work budgets and replay accounting; version identity is necessary. |
| [Rocq Ltac manual, timeout](https://rocq-prover.org/doc/master/refman/proof-engine/ltac.html#timeout) | Elapsed-time interruption is machine dependent; interaction with tacticals can reverse expected behavior. | Resource failure is operational, not a negative mathematical certificate. |
| [Isabelle system manual](https://isabelle.in.tum.de/doc/system.pdf), session options; [2026 NEWS](https://isabelle.in.tum.de/website-Isabelle2026-RC3/dist/Isabelle2026-RC3/doc/NEWS.html) | Parallel checking threads; external wall-clock session timeout; timeout_scale compensates for slow hardware and now affects ML tools too. | Existing policy is explicit hardware-sensitive timing, not universal budget determinism. |
| [Kimina repl.py](https://github.com/project-numina/kimina-lean-server/blob/fb2393de3461db35eda4c714e3fd21187e92ec90/server/repl.py), [server README](https://github.com/project-numina/kimina-lean-server/tree/fb2393de3461db35eda4c714e3fd21187e92ec90) | Async waiting/timeouts and REPL lifetime/memory controls; client-facing outcomes depend on service policy. | A heartbeat-only wrapper does not reproduce queue/OS/memory timeout policy. |
| [DeepSeek-ProverV1.5 verifier](https://github.com/deepseek-ai/DeepSeek-Prover-V1.5/blob/2c4ba9119eef74d0d611f494261b2c5bae98c69a/prover/lean/verifier.py) | Default300s subprocess timeout; optional address-space bound; pass vs complete distinguishes errors and sorries. | These exact checks must be preserved in any service parity claim; a frontend error flag is insufficient. |
| [O'Callahan et al., USENIX ATC2017, rr](https://www.usenix.org/system/files/conference/atc17/atc17-o_callahan.pdf) | Deterministic replay records nondeterministic events; hardware progress counters have caveats. | Generic receipts/replay and instruction counting are not novelty, and PMU instructions are not an architecture-independent work unit. |
| [Auditing Failed Lean Proof-Agent Searches with Exact Replay, OpenReview manuscript](https://openreview.net/pdf/263b5c096aadff7657ca3a4560b28a20cdc0dd8b.pdf) | Search-index primary abstract describes exhaustive finite saved tactic support under fixed Lean/depth/timeout, distinguishing timeout-limited transcripts from closed certificates. | Related failure replay, not evidence of budget invariance across hardware. Direct PDF open hit an access challenge; full text and publication status unverified. Search abstract only is used; no secondary venue attribution adopted. |

## Search record and coverage

Queries, same session 2026-11-01 (UTC); sources selected above, generic agent
journals and vendor replay marketing excluded as unrelated:

- Lean maxHeartbeats deterministic profiler threads allocations
- site.github.com/leanprover/lean4 heartbeats nondeterministic profiler
- site.github.com/leanprover/lean4 heartbeat shared thunk
- proof assistant deterministic replay timeout reproducibility Isabelle Coq
- site.rocq-prover.org timeout tactic machine dependent
- site.isabelle.in.tum.de timeout parallel proof checking
- site.isabelle.in.tum.de reproducible timeout
- ACL2 with-prover-step-limit deterministic time limit steps
- site.usenix.org rr deterministic replay counters retired conditional branches
- Kimina lean server timeout maxHeartbeats
- site.github.com deepseek-ai DeepSeek-Prover-V1.5 prover lean timeout
- Auditing Failed Lean Proof-Agent Searches with Exact Replay

The shared-thunk fix first appeared as a secondary changelog lead; only the
official commit API payload is used for its technical conclusion. The raw API
payload and resolved Kimina/DeepSeek heads are retained outside Git in v1.
The exact-replay manuscript remains a partial primary read, not verified as an
accepted conference paper. Searches do not prove that no closer work exists.

## Decisive experiments

Retained profiler flag changes already refute transparent instrumentation at
one diagnostic point. Fresh native tests must establish their own denominator,
source/toolchain/options and complete acceptance checks. Thread-local counters
must be measured in the actual executing context, not around a blocked parent.
Compare stock async and synchronous accounting explicitly. Preserve ordinary
errors, exhausted work, timeout, OOM and missing process outcomes separately.

A larger B may change a budget-aware tactic's search path; therefore monotonicity
is an experiment and a contract condition, not a theorem about arbitrary Lean.
A receipt supplies input and configuration for rerunning the original kernel.
It does not turn a measured allocation count or failed tactic into a proof of
nonprovability, nor make native IO deterministic.
