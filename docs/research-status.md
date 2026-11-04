# ProofServe: current status

We are delivering the open-source tool and a six-page empirical + system paper.

## Current decision

**The usability gate failed; the full run was not started.** W's [completed qualification](../data/openai-math-4eaee875/measurement/census-gate/README.md), committed as f97e6fbd, reports instruction spreads of 1.3312% median and 3.1498% P95, above the frozen 1% and 3% thresholds. All 480 foreground/control and 1,413 background calls completed successfully. Under the user's instruction, no census is launched. This is a failure of the proposed measurement protocol's invariance check, not a proof rejection.

All root work inside the Workspace now uses **CPUs 8–9**, including PDF compilation. The former CPU 22–23 setting is retired for future work; historical records remain unchanged.

M's current matrix is preview-only and cannot fill Table 1. Final system timing requires an otherwise idle machine and follows the resolved gate/full-run path. No full-library original-kernel result is promised.

## Evidence retained

- [Sample package](../data/openai-math-4eaee875/README.md): 42/42 original costs, estimated compiler work 279.12 CPU-hours, fragile nominal interval 95.18–463.06. The independent precision panel remains separate.
- [External installed checks](../data/external-projects/results.md): three cases with common-local-root parity, separate costs and retained official resource failures. Package/container CI passed finite controls; proof obligations differ.
- [Current six-page paper](paper/main.tex): unchanged from 4e63272a, with no full-corpus measurement content inserted. Its numbers and PDF remain unchanged.

The nealmcb report's 13.8-hour cloud wall measurement and 26-module CPU extrapolation remain distinct.

[Plan](research-plan.md) · [Evidence and protocol](paper/evidence.md) · [Result index](../research/README.md)

Root maintains documentation without another collector or owner implementation changes. No external publication is authorized; a later host outage still means preserve the scene and wait for the user.
