# Falconer: decoupled native checking

Self-review.

## Source denominator

All 13,205 source nodes compiled successfully: 8,128 new +5,077 exact same-capture reused nodes, charged once per closure. Successful compiler wall sum **22077.770248s**, CPU sum 32292.603807s. Of these, the 2,461 Falconer AI modules account for 6,476.297931s wall; 10,744 dependencies account for15,601.472317s. The source census has7,312 theorem/lemma sites and zero explicit decide+kernel, native_decide or bv_decide sites in Falconer. That is a source classification, not a claim that its dependencies contain no kernel computation.

This is summed per-module compilation (including repeated imports and normal olean/ilean/C output), not parallel Lake makespan, warm-service throughput or source-only verification without artifacts. The old0.053097s recovered source fault remains separately recorded.

## Native result

No complete new native full-check result yet. The interrupted old prefix is not a numerator and no ratio is finalized.

The same-adapter Mathlib1330 comparison is pending; the historic65.692644s/622.379412s=10.5551% used the unindexed audit. Treating a difference against that number as purely an AI workload effect would confound adapter overhead.

## Acceptance and interruption boundaries

Module-local reference qualification: {'verified': 5077, 'expected': 13205, 'remaining': 8128, 'reused_exact_common': 5077, 'chunks': 0, 'complete': False}. Exact common nodes reuse their previous original-checker qualification; each remaining module is checked by the frozen measurement-v1 original checker in independently saved <=512-module chunks. Full differential parity is complete only when all13,205 belong to that union. Until then the whole-closure comparison is pending; do not label it accepted-set equality.

The ten indexed/native module-local boundary controls agree, including explicit rejection of a corrupt duplicate theorem and an unimported sibling proof. These are controls, not a substitute for full input parity. The source/compiled artifacts are unchanged; corruptions are in-memory experimental proof replacements.

Every timed task uses taskset0–7 and the shared FIFO flock, no-M, a child cgroup of11.75GiB plus a small parent, and a finite wall timeout. The separate memory pass, if present, is excluded from primary wall time. A timed-out/malformed record is operationally incomplete, never a mathematical rejection. Raw old and new stdout/stderr/commands, including the JSON-truncated failed attempt and initial failed compiler invocation, remain on PVC at the paths documented in falconer-recovery-plan.md.

See admission-control-reconciliation.md: all-stream+upper admits by the same type-conditioned bound and serial Grid CPU557.350s, whereas class-selected parallel Grid CPU744.406s. Under CPU-work budgets the latter cannot imply a completion advantage;17 vs14.33 is a negative routing result, not a paradox or native-throughput claim.
