# Built-artifact checking: bounded incomplete prefix

The frozen release checker certified **968 of 162,170 requested source modules** in 15 complete batches. Those batches accepted **12,756 distinct closure modules**, including dependencies. No module rejection was reported. This is an incomplete, dependency-order-dependent prefix, not a representative sample or a whole-library verdict.

New batch admission stopped at 17:00 UTC on 6 November 2026. The last batch did not finish within the allowed drain. GNU timeout returned 124 at 17:15 UTC; result.json was written at 17:15:00.041 UTC. The controller, native processes and native cgroup were absent at 17:15:23 UTC, and the P-core lock was available. No batch was created after admission stopped.

## Exact coverage

| Requested source status | Modules |
| --- | ---: |
| Accepted in certified complete batches | 968 |
| Successful segment accept; batch not certified | 271 |
| Accept event in interrupted segment; not committed | 217 |
| Module header reached; no final verdict | 1 |
| No observed module verdict | 160,713 |
| Total requested built source modules | 162,170 |

Thus **161,202 requested source modules lack complete batch certification**. The additional 488 accept events are retained as provisional observations; they are not added to certified acceptance. The final interrupted segment reached OAI.Algebra.Finitistic.Rectification.ColumnFinite but produced no verdict for it. A header without a verdict is not a rejection.

All 146 returned segment records have exit 0 and empty stderr. There are no reported kernel rejection events, no returned nonzero segment, and no completed receipt for batch-15. That batch has 10 successful segment records and one interrupted event stream. The 15 certified batches remain valid checkpoints; the incomplete batch and all its raw records are preserved.

W completed 162,170 of 163,096 source modules. The separate **926 user-deferred, unbuilt sources** and **one lakefile configuration unit** were excluded. OAI is among the deferred sources and has no compiled artifact. Its capacity precheck is unavailable because of missing input, not an OOM or kernel rejection. No whole-source cost is extrapolated.

## Observed native cost

| Metric | Value |
| --- | ---: |
| Native guard wall time | 16530.349 s |
| Entire own native cgroup CPU | 16194.749 s |
| User CPU | 10359.608 s |
| System CPU | 5835.141 s |
| Sampled own process-tree RSS peak | 8.878 GiB |
| Cgroup charged-memory peak, including cache | 45.512 GiB |
| Native return code | 124, operational deadline |
| Reported kernel-rejected modules | 0 |

The raw guard flag wait4_usage_complete refers to wait4 bookkeeping, not to completion of checking. Cgroup CPU is the cost authority; phase completion remains false.

These costs include completed work, dependency loads, planning and interrupted work within the native cgroup. They exclude Python setup and offline reduction. They are not a per-module cost, a completed-tool benchmark, or a worker-scaling point. Twenty-two workers were allowed on CPUs 0–7 and 10–23, a mixture of P and E cores; CPUs 8–9 were reserved for preparation and the main thread. Protected background workloads were left unchanged. No exclusively idle-host claim is made.

There was no Lean -M. The external charged-memory ceiling was 48.020 GiB, with the existing 8 GiB node-available-memory stop. The cgroup memory max/oom/oom_kill counters are all zero, and no disk, RSS or node-available-memory stop was recorded. GNU timeout won the deadline race before the sampler appended a drain-expired reason; the raw stop_reasons list is empty. Exit 124, the configured deadline and the actual 17:00 coordinator-stop event establish the operational cutoff. It is not a proof rejection.

## Version, policy and trust

The native checker is unchanged from **e000ed62bbf4b9c420bd99d0273a5d21829b4edc**, Lean 4.34.1, binary identity 14707787067517532260. All seven frozen native source blobs still matched after the run. Acquisition driver **616adf8590909d8f5186617b0e4cc225f262b6fc** added the approved built-subset frame and admission/drain handoff; it did not change the checker.

Inputs use source 4eaee87548250b2682affda7d05d947c05554bae, Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612 and W result commit cc5bcc18c87d7bf85afc5e71a6738f06da52c03d. The run reads W's folded artifact view and retained compatibility changes through the prepared dependency environment. Full paths and the exact native command are in provenance.json, native-result.json and the raw workflow-config/artifact-binding files.

This is the default shared-checked theorem-body policy, with the [documented context difference](../../theorem-body-policy/README.md). The checkpoint directory was fresh; within-run certified dependencies were reused under the checker's existing local-certificate contract. Those certificates are editable trusted local state, not cryptographic proofs. Their 64-bit noncryptographic file identities detect ordinary changes but do not resist deliberately constructed collisions. See [large-library checking](../../../docs/large-library-checking.md).

The union contains 15 declared axiom names, including sorryAx and compiler/runtime axioms. This is a declared inventory, not a minimal used-axiom closure or evidence that every proof is sorry-free. No official leanchecker comparison was run over this incomplete prefix, so it establishes no whole-corpus acceptance parity. The final matrix's smaller-scope controls remain [separate](../matrix/README.md).

## Files and reproduction

- coverage.json and source-status-counts.csv give disjoint source counts.
- accepted-requested-sources.csv lists the 968 certified requested sources.
- batches.csv retains each certified batch's closure and requested-source counts.
- native-cost.csv and native-result.json preserve cost, affinity, retirement and memory evidence.
- provenance.json, capacity-precheck.json and retirement-observation.json record pins and boundaries.
- The per-module status list and all raw segment events, receipts, certificates, memory samples, launch output and failed/partial data remain on the PVC at /workspaces/.agent-state/gpu-smt-captures/checker-final-e000ed62-20261106T050828/corpus. The detailed list is module-status-detailed.csv.gz.

The executed acquisition command was the prepared release.py final.json --phase corpus invocation. To reproduce the reduction from the retained raw directory:

    taskset -c 8-9 python3 checker/bench/summarize_corpus.py <raw-corpus-directory> <export-directory>

The reducer checks retirement, native receipt identity and the disjoint source partition. Its first local run expected the short version string; the actual public receipt contains Lean's full version banner. The offline decoder was corrected to match that banner's 4.34.1 version. No native result or input was changed, and the original prepared reducer is retained on the PVC.

Final offline validation passed all 12 existing acquisition unit tests. The detailed source partition has 163,097 unique entries, including the 926 deferred sources and one configuration unit; its requested-source classes sum to 162,170. These checks validate collection bookkeeping, not whole-library correctness.

This report is **self-review (自审)**. The repaired frozen checker has not received an independent runtime review. The supplementary collection is stopped and has not been resumed; the unchecked scope remains unfinished.
