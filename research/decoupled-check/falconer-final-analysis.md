# Falconer complete-closure recovery: final reduction

Self-review.

Successful source build:13,205 modules,8,128 newly constructed plus5,077 exact same-capture common nodes, **22077.770248265006s** summed compiler wall. One prior source-overlay fault0.053097s is retained separately. Source construction is complete; no source gap remains.

- {"check_over_build": 0.09256303751776258, "cohort": "Falconer", "complete": true, "cpu_s": 2038.443942, "modules": 13205, "peak_rss_gib": 10.36832046508789, "segments": 27, "source_wall_sum_s": 22077.770248265006, "wall_s": 2043.5854757986963}
- {"check_over_build": 0.14666154599527065, "cohort": "Mathlib", "complete": true, "cpu_s": 91.145172, "modules": 1330, "peak_rss_gib": 1.32440185546875, "segments": 3, "source_wall_sum_s": 622.3794121909887, "wall_s": 91.2791267875582}

Original module-local parity status: {"chunks": 16, "complete": true, "expected": 13205, "remaining": 0, "reused_exact_common": 5077, "verified": 13205}.

**Falconer segmented check/build: 9.2563%; matched segmented Mathlib: 14.6662%.** Falconer is lower by5.4099percentage points. These are measured aggregate native process costs including startup, verified-prefix import, snapshot writes and normal exits; no unfinished prefix is extrapolated. The historical unsegmented Mathlib10.5551% used another adapter and is not the causal workload control.

The AI subtree contains2,461 Falconer modules and7,312 source theorem/lemma sites with zero explicit decide+kernel/native_decide/bv_decide. Its source compiler wall sum is6476.297931s, versus15601.472317s for10,744 dependencies. This is not a declaration-level CPU attribution: the full numerator checks dependencies too. Shared original-kernel terms avoid rerunning tactics and repeated per-module frontend imports; wide dependency graphs, context fallbacks, prefix import and serialization still cost work. Source composition and these overheads, rather than AI authorship alone, can change the ratio. We have not causally isolated those factors.

The original full checker timed out at1500.210998s with8942 surviving accepts and a JSON-truncated final line; a reachability-cached full attempt timed out at1500.204755s with9040 accepts. Both remain operational failures, with no complete ratio or demonstrated optimization benefit. Their3000.415754s are diagnostic recovery overhead, excluded from the successful segmented protocol but never hidden. Queue wait, reference qualification and controls are likewise separate from service cost.

A segment exports only already original-kernel-checked constants and pure audit metadata; the next imports that certified delta and checks new terms. All inputs are frozen. This is not a standalone verifier of arbitrary snapshots, a public failure cache, a modified kernel or production implementation. Five native cases across18 fresh processes qualified checkpoint/restore, including bad-proof rejection after restore. Whole-input parity requires the independent original module-local union to cover all13,205 plus segmented native import-graph equality. See falconer-segmented-result.md and falconer-parity-progress.md for those conditions; do not infer equality from a partial status.

Finally, the17-vs14.33 admission comparison is resolved in admission-control-reconciliation.md: both policies use predicted-type upper bounds and FIFO, but serial Grid costs557.350 CPU s while the class-selected parallel method costs744.406. The all-serial control completes17/20, versus13/15/15 for the classified method; both interrupt zero. It shows no incremental CPU-budget benefit from changing checker mode, not a paradox or a native throughput result.
