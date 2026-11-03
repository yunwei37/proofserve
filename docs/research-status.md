# ProofServe: current status

The project is closing around two deliverables: an independent Lean project verification tool and a six-page empirical + system paper. The paper keeps its title and four RQs. The coordinator's working target is 17 November; publication still needs user confirmation.

## Ready to use as evidence

- [Public measurement package](../data/openai-math-4eaee875/README.md): 41 of 42 original costs, with missingness preserved. Twenty complete strata estimate 278.09 CPU-hours, with a fragile nominal 95% interval of 94.15–462.04 hours. This is not a full-library confidence bound.
- [Native checker](../checker/README.md): original-kernel checking, parallel declarations, checkpoint/resume, receipt v1 and explicit version fallback. Development controls exist.
- [Audit tool](../tools/audit/README.md): portable source/default-target inventory, lexical computation counts, receipt/axiom reporting and explicit cost logs.

## Still required

The final [release matrix](../checker/results/README.md), official scope-matched comparisons, CI rejection evidence and timed interruption pair are incomplete. The old one-point executable record is excluded from the frozen matrix. Three unseen public projects, including a published AI project, and clean package/container acceptance are also pending. Development success is not release acceptance.

The [six-page paper](paper/main.tex) has been rewritten, compiled and visually checked on all six pages; the [evidence map](paper/evidence.md) identifies admitted numbers and empty system-result slots. Research prototype results explain causes only. No release speedup is claimed yet.

## Boundaries

No new scheduling, prediction, certificate-repair, GPU, serving-feature or attribution work. Do not restart existing collectors. Root changes paper/docs only; implementation remains with M/W/O. No tag, package publication, upstream issue/PR or announcement.

[Plan and ownership](research-plan.md) · [Data](../data/openai-math-4eaee875/README.md) · [Result index](../research/README.md) · [Historical evidence](evaluation.md)
