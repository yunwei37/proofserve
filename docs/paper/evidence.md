# Six-page paper: evidence and completion map

This is the paper's claim-to-evidence map, not a second long paper or an independent audit. The six-page reconstruction is directly authorized by the 3 November closure instruction. Previous sources/PDFs and detailed raw qualifications remain in Git history and the retained PVC. No new native measurement is run by root.

## Current snapshot

The paper uses data-package commit **31a57411e528c203c8ae7d5e20f29b249c145ab1**, with 41/42 original costs and 20 complete strata. The last original and fixed independent precision panels are not imputed or pooled. The paper must be updated only when W publishes their complete, appropriately scoped return.

| Paper conclusion | Evidence | Allowed interpretation |
|---|---|---|
| Source cost is heterogeneous and population precision remains weak (RQ1) | [sample-costs.csv](../../data/openai-math-4eaee875/sample-costs.csv), [strata.csv](../../data/openai-math-4eaee875/strata.csv), [sampling-intervals.csv](../../data/openai-math-4eaee875/sampling-intervals.csv) | 20 complete strata / 163,057 modules; 278.091768 CPUh, nominal 94.148040–462.035496, df 2.608579. Conditional, n=2, not a full-frame bound |
| Marked-file compiler share differs from file share (RQ1) | Same package; reproducible summarize.py | 57.546404/278.091768 = 20.6933%. Marker is lexical, not dynamic kernel CPU |
| Completing the fixed sample is a different uncertainty | [scenario-ranges.csv](../../data/openai-math-4eaee875/scenario-ranges.csv) | Source 278.535705–279.012225 CPUh under observed-class extremes; paper rounds outward to 278.5–279.1. Not CI or guaranteed bounds |
| Selected complete checking is cheaper than source compilation (RQ2) | [closure-ratios.csv](../../data/openai-math-4eaee875/closure-ratios.csv) | Falconer CPU 6.3124%, wall 9.2563%; matched segmented Mathlib CPU 8.9514%, wall 14.6662%. Grid/Amplitudes CPU 8.4671/8.4421%, wall 14.5173/14.5473%. Different protocols; overlapping selected cases |
| Persistence was our prototype method correction | [root0279 qualification](../tmp/build-and-evaluate/step-0279-20261103T122418+0000/step-report.md) | Same-executable eight-worker CPU −14.13%, wall −5.13%; causal explanation only |
| Whole-module fallback was an avoidable prototype policy | [root0285 qualification](../tmp/build-and-evaluate/step-0285-20261103T182451+0000/step-report.md) | Plain medians 257.658745→196.669275 s, wall −23.6706%, CPU +0.10565%; no release result or intrinsic serial lower bound |
| Official checker scope differs | [baseline scope](../../checker/results/baseline-scope.md), pinned LeanChecker/Replay source | Default module tasks and final-map --fresh are different ledgers; unmatched clocks have no speedup ratio |
| Original-kernel workflow adds trusted implementation code (RQ3) | [checker README](../../checker/README.md), [receipt schema](../../checker/docs/receipt-schema.md) | Reader, token adapter, prefix/quiescence and local snapshots trusted; no unchanged implementation TCB or cluster claim |
| Audit distinguishes acceptance from coverage (RQ4) | [audit contract](../../tools/audit/README.md) | Lexical/configuration limits, partial receipt axioms and source binding gaps stay explicit |

## Reserved release results

Only committed proofserve-check and proofserve audit results enter system evaluation. Record executable and project commits for every admitted result. Do not use research/ prototype tables or the superseded checker 51769793 one-point record to fill the final matrix.

- M: Mathlib Nat.Basic, Grid and Barrier, workers 1/2/4/8, three fresh-checkpoint repeats per point; separate CPU and wall medians/ranges. Mathlib Nat.Basic is not all Mathlib.
- M: eight-worker no-persistence and no-split-fallback ablations on Grid and Mathlib, three repeats each.
- M: official default and --fresh comparisons with explicit actual ledgers, acceptance parity, three bad-proof classes in CI, and timed interrupted/resumed versus uninterrupted operation plus overhead.
- O: three unseen public Lean projects, at least one with published AI-generated source; immutable commits, counts, CPU/wall, official parity, audit findings, problems and package/container clean-start acceptance.
- W: integrate only authorized sample/panel returns in the public package. Broad intervals are a result, not grounds to add samples.

Current blocker for a submission-ready paper: the final release matrix, external acceptance and completed data return have not all arrived. Placeholder tables visibly say Pending; there are zero missing/evidence-grade macros. Before submission, replace those cells with admitted results or state the unavailable conclusion in limitations. No fabricated speedup or acceptance verdict is allowed.

## Position and primary sources

The mechanisms have precedents; the contribution is empirical characterization, a usable tool, and its evaluation. No new scheduling, prediction, certificate-repair, GPU or serving mechanism is proposed.

The [FRO roadmap](https://lean-lang.org/fro/roadmap/y4-1/) motivates routine checking. The [official 4.35 release notes](https://lean-lang.org/doc/reference/latest/releases/v4.35.0/) already ship lake check, comparator and independent-kernel integration. Both were opened on 3 November. The manuscript reflects this current state and does not claim that lake check is merely future work. No new competitor experiment is added.

## Reconstruction and verification

The existing 10pt double-column source is retained. The title and four RQ texts are unchanged; the obsolete 20-table/body freeze is released by the author. Measurements occupy the first half; check/audit/receipts/trust and the fixed evaluation occupy the second half. At most four figures/tables, including references in the six-page total. No long alternative is created.

Generated untracked historical data/log/binary outputs are ignored in place using artifact-scoped .gitignore patterns. Implementation source and Markdown remain visible; tracked evidence is unaffected. No result, raw file, foreign dirty path or live collector is deleted or moved. This does not reclaim disk space.

Root read the current owner identities before editing: old M controller 23773 and Packet prerequisite 29873 were absent; W master 8141/birth 169629 and its later prerequisite controller remained active. These are observations, not permission to resume retired work.


Final check on 3 November: the PDF is **6 pages including references, 87,549 bytes**, with 4 figures/tables and 13 resolved references. The 10pt two-column layout, title and exact four RQ texts are preserved. There are no missing/evidence-grade macros and no overfull boxes. All six final pages were visually inspected; this is self-review, not independent acceptance. The final build took 2.022 seconds on E cores 22–23. Early layout and two literal-newline compilation failures remain outside Git with their logs; they changed no measurement.

No new step directory or audit report was created. The current snapshot still has only the superseded release one-point record; the complete release matrix and external-project results are the remaining integration dependency.
