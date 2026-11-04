# ProofServe evidence index

The active deliverables are the open-source tool and a six-page empirical + system paper.

| Evidence | Location | Current use |
|---|---|---|
| Probability sample and selected closure costs | [Public measurement package](../data/openai-math-4eaee875/README.md) | 42/42 original costs; 279.12 CPU-hours with nominal 95% interval 95.18–463.06 |
| Committed release checker | [checker/results](../checker/results/README.md) | Final scaling, ablations, official comparison and timed resumption remain pending; portable rejection CI has passed |
| External public projects | [External results](../data/external-projects/README.md) | Three installed check/audit cases complete; common-root parity, separate CPU/wall and retained failures published; package/container CI passed |

The [paper](../docs/paper/main.tex) separates CPU pairs from target wall windows, compares the earlier same-corpus report, and reports lexical density, default coverage and historical verdict stability. **33.30% refers to omitted decision sites; omitted modules are 19.78%.** Prototype results explain causes and never fill release-performance tables.

[Checker](../checker/README.md) · [Audit](../tools/audit/README.md) · [Evidence map](../docs/paper/evidence.md) · [Plan](../docs/research-plan.md) · [Status](../docs/research-status.md)

Historical research remains for provenance. Scheduling, prediction, certificate repair, GPU, service additions and further attribution are closed directions. Existing owners complete their authorized work; this index starts no collection.
