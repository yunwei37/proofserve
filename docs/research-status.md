# ProofServe: current status

We are closing two deliverables: an independent Lean project verification tool and a six-page empirical + system paper. The coordinator's working target is 17 November, not a user-imposed deadline. Publication still needs user confirmation.

## Established evidence

- [Measurement package](../data/openai-math-4eaee875/README.md): **42/42 original costs**, all 21 strata complete. Estimated native compiler work is **279.12 CPU-hours**, with a fragile nominal 95% interval of **95.18–463.06**. The fixed independent precision panel remains separate.
- [Six-page paper](paper/main.tex): a data figure shows module CPU pairs and matched target wall windows. Computational certificates retain 80.28–82.35% of source wall time in two selected cases; ordinary controls retain 0.46–6.54%. Different clocks and scopes stay explicit.
- Default coverage omits **19.78% of source modules** and **33.30% of kernel-decision sites**. The latter is not a module percentage. Historical 2,524-target testing records 30,288 accepted checks without verdict differences.
- [External installed checks](../data/external-projects/results.md): Newspeak, Solar and CrocSwap checked closures of 754, 2,368 and 3,166 modules; common local acceptance sets of 105, 12 and 64 match official replay. Proof obligations differ, so no speed ratio is claimed. Solar audit leaves 20/32 files outside the default graph; CrocSwap has disclosed AI assistance and a setup repair.

## Remaining delivery

The final [release matrix](../checker/results/README.md), matched official comparisons and timed interruption pair await M. External CPU/wall results and retained official resource failures now appear in the paper. Portable-package CI rejects three malformed-proof classes; the container passes installed-project and version checks with networking disabled. These finite qualifications do not complete the performance evaluation.

[Checker](../checker/README.md) and [audit](../tools/audit/README.md) implement the workflow. The paper now compares the earlier same-corpus report directly: its roughly 410 CPU-hours include about 330 compilation hours and 80 Comparator hours; its complete cloud build is a separate wall-time result. [Evidence map](paper/evidence.md) records pins and measurement boundaries.

## Boundaries

Root integrates paper/docs only. No new collection, replacement agent, scheduling, prediction, certificate repair, GPU, serving features or deeper attribution. Preserve existing collectors and results. No tag, package publication, upstream issue/PR or announcement.

[Plan](research-plan.md) · [Evidence index](../research/README.md) · [Historical evidence](evaluation.md)
