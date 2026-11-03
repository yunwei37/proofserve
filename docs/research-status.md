# ProofServe: current status

We are closing two deliverables: an independent Lean project verification tool and a six-page empirical + system paper. The coordinator's working target is 17 November, not a user-imposed deadline. Publication still needs user confirmation.

## Established evidence

- [Measurement package](../data/openai-math-4eaee875/README.md): **42/42 original costs**, all 21 strata complete. Estimated native compiler work is **279.12 CPU-hours**, with a fragile nominal 95% interval of **95.18–463.06**. The fixed independent precision panel remains separate.
- [Six-page paper](paper/main.tex): a data figure shows module CPU pairs and matched target wall windows. Computational certificates retain 80.28–82.35% of source wall time in two selected cases; ordinary controls retain 0.46–6.54%. Different clocks and scopes stay explicit.
- Default coverage omits **19.78% of source modules** and **33.30% of kernel-decision sites**. The latter is not a module percentage. Historical 2,524-target testing records 30,288 accepted checks without verdict differences.
- [External static audits](../data/external-projects/audit-before-build.csv): installed-tool results cover CrocSwap 64/64, Newspeak 105/105 and Solar 12/32 default-import modules. These are static coverage findings, not native checking acceptance.

## Remaining delivery

The final [release matrix](../checker/results/README.md), official comparisons, bad-proof CI, timed interruption pair and full external package/container acceptance await owner returns. Their pending paper tables contain no prototype performance substitutions.

[Checker](../checker/README.md) and [audit](../tools/audit/README.md) implement the workflow. The paper now compares the earlier same-corpus report directly: its roughly 410 CPU-hours include about 330 compilation hours and 80 Comparator hours; its complete cloud build is a separate wall-time result. [Evidence map](paper/evidence.md) records pins and measurement boundaries.

## Boundaries

Root integrates paper/docs only. No new collection, replacement agent, scheduling, prediction, certificate repair, GPU, serving features or deeper attribution. Preserve existing collectors and results. No tag, package publication, upstream issue/PR or announcement.

[Plan](research-plan.md) · [Evidence index](../research/README.md) · [Historical evidence](evaluation.md)
