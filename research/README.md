# ProofServe evidence index

Active deliverables: open-source ProofServe and the six-page empirical +
system paper. **W's cc5bcc18 campaign retired with 162,170/163,096 modules
completed (99.43%) and 926 user-deferred modules unmeasured.**
Three physical intervals use two admission rules. P/E work is
168.956/302.399 CPUh, unconverted; measured wall totals 31.529 h.
Dependency order and high-memory deferral prevent extrapolation.
The total-instruction gate remains failed and user-mode comparison post hoc.

| Evidence | Location | Current use |
|---|---|---|
| Final observed compilation | [W publication](../data/openai-math-4eaee875/census/README.md), [derived artifacts](../docs/paper/generated/census/) | 162,170 completed; 926 deferred; P/E lower bounds, no extrapolation |
| Original sample | [Public package](../data/openai-math-4eaee875/README.md) | Historical 42/42 data, never filling the missing tail |
| Final checker matrix | [818f7422 results](../checker/results/release-e000ed62bbf4/matrix/README.md), [derived summaries](../docs/paper/generated/system/) | 1.70/2.14/1.73 wall scaling; strict Grid censored, ten cells unrun, background condition explicit |
| External projects | [Final 0516279d results](../data/external-projects/e000ed62-final/README.md), [derived table](../docs/paper/generated/system/external-table.tex) | Three one-worker projects, one observation per arm, 126 common roots pass; unequal checking obligations, no speedup ratio |
| Built-subset checking | [Plan](../docs/research-plan.md) | M checks available artifacts only; partial or unstarted scope is explicit |

The [paper](../docs/paper/main.tex) now uses returned observed distributions,
interval/P-E costs and conditional groups. Root independently reduced the
module CSV against cc5bcc18; product-byte validation remains W's self-review.
Full-frame coverage stays separate: **33.30% omitted sites versus 19.78%
source files**. P/E work is not converted; module wall is not machine wall.

Native e000
shared-checked/strict policy, two read-only review limits and no repaired-source
independent runtime review remain explicit. The matrix and external table now use returned frozen-tool costs; supplementary built-subset checking remains pending.
No preview cost or prototype ratio fills missing results.

All root Workspace work uses **CPU8–9**. Root starts no native collection,
replacement agent/session or infrastructure change, and publishes no release.

[Checker](../checker/README.md) · [Audit](../tools/audit/README.md) · [Evidence](../docs/paper/evidence.md) · [Status](../docs/research-status.md)
