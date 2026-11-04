# ProofServe closure plan

We are delivering a usable open-source Lean verification tool and a six-page empirical + system paper. The latest direct decision replaces sampling as the final answer to total-library cost with a complete build of the pinned corpus. The coordinator's 17 November target is not a user-imposed deadline; the venue remains undecided.

## Full-corpus measurement is now the priority

W is preparing and running the full **163,097-module** build at OpenAI math revision **4eaee875**, on **phobos-vt** in the existing **yunwei356/gpu-smt-dev** Workspace. The user authorized expanding the existing work volume and using as much available host capacity as possible for parallel compilation. The work PVC is now **384 GiB**. The quoted **1–2 days** is a rough estimate, not a completion result or deadline.

The deliverable is each module's observed compiler CPU and outcome, together with the actual build wall clock and execution configuration. Completed module work, operational failures, missing modules, reused artifacts and dependency preparation remain identifiable. The 42 original probability draws and the fixed independent precision panel are retained separately for calibration; they do not replace the census or silently acquire new weights.

W owns the implementation and resource choices for this authorized run. Root records actual progress without starting a second collector, restarting work, or changing infrastructure. Source acquisition, readiness tests and a finite pilot are preparation, not completed full-corpus measurements.

## What changes when complete data returns

| Current manuscript evidence | Replacement or retained role |
|---|---|
| Section 3.2: original42 estimate and variance derivation | Observed full-corpus total and distribution; sampling becomes calibration and the section becomes shorter |
| Marked-file compiler share | Observed compiler work in the source-marker class, still distinct from dynamic kernel phase work |
| Default graph inside/outside coverage | Add measured compiler work for both sets to the existing source/module counts |
| M's current scaling and ablation matrix | Preview only; excluded from final paper performance and Table 1 |
| Installed external cases and package/container CI | Preserve functional evidence and dated cost observations; final performance claims follow the quiet-machine measurements |

Final system timings run **after the census has finished, with the machine otherwise idle**. A committed executable alone does not qualify a concurrent preview as final performance evidence. Root keeps Table 1 pending and does not fill it when the current matrix returns. M may explore full-library original-kernel checking independently; feasibility is unknown and the paper makes no promise or result claim about that attempt.

Until the census returns, the current paper's **279.12 CPU-hour** estimate and nominal **95.18–463.06** interval remain unchanged and explicitly traceable to the original sample. No census total, marked share, default-graph cost or speedup is prefilled.

## Tool delivery and ownership

| Owner | Paths | Delivery |
|---|---|---|
| M | checker/ | Original-kernel checker, receipt v1, parallel/resume implementation and correctly labeled preview/final results |
| W | tools/audit/, data/openai-math-4eaee875/ | Audit tool, complete corpus build data, preserved calibration samples |
| O | crates/, CLI, README, Docker, CI, release workflow, data/external-projects/ | Portable packaging and external-project acceptance |
| Root | docs/paper/, docs records/status, research/README.md | Six-page manuscript and evidence integration |

ProofServe checks compiled dependency closures, audits source/default-target coverage and reported evidence, and maintains the existing Kimina-compatible service without new serving features. Unsupported versions fail clearly or choose an explicit official path. The released-form evaluation separates CPU and wall time and records tool, input and protocol revisions.

The planned selected-closure evaluation retains Mathlib Nat.Basic, Grid and Barrier at 1/2/4/8 workers with three repeats; the Mathlib label denotes the selected closure. Persistence and split-fallback ablations, official default/fresh ledger comparisons and timed interruption/resumption retain their declared scopes. Final scheduling follows completion of the census, not completion of the preview. Root adds no new workload, repeat count or experiment.

## Manuscript and evidence

The title and four current RQs remain in place for now; RQ3 has no cluster claim. Keep 10pt, two columns, six pages including references and at most four displays. Keep technical appendices, the conclusion-to-evidence map and the census handoff in [evidence.md](paper/evidence.md), rather than creating another long paper or adding an appendix to the six-page count.

The earlier nealmcb report measures a complete cloud **wall time** of 13.8 hours on 32 vCPUs. Its roughly **330 compilation CPU-hours** are extrapolated from 26 modules, with estimated ±30% uncertainty; roughly 410 CPU-hours includes Comparator work. Preserve that distinction. The new measurement targets the complete per-module CPU ledger absent from that report; no unmeasured result or universal priority claim is inserted now.

Measurement data comes from the public W package; final system performance comes from committed released-form tools after the quiet-machine run. Prototype interventions explain engineering causes only. The current sample is calibration evidence, not a census result. Existing raw, failed, partial and historical records stay intact.

## Operations and publication

Use the same Workspace, volume and Cloudflare CLI connection. The all-core authorization applies to W's census; quiet system benchmarks retain their recorded timing conditions. Omit -M, preserve disk headroom and foreign work, and do not restart existing collectors. A later host outage still requires preserving the scene and waiting for the user, without recovery or scheduling changes.

No new agent, session, replacement queue, scheduler, prediction, certificate repair, GPU direction, service feature or deeper attribution. M's explicitly relayed full-library check exploration is not an authorization for root to launch a duplicate. No tag, registry publication, upstream issue/PR or announcement; validated main commits and pushes remain authorized.

Root now maintains the records and evidence map. Once W publishes complete census data, replace Section 3.2 and its derived shares; once final quiet-machine system measurements return, replace the preview placeholders. No per-edit step directories or outer-audit files are created.

[Latest direct words](user-instruction.md) · [Status](research-status.md) · [Evidence map](paper/evidence.md) · [Result index](../research/README.md)
