# ProofServe closure plan

The deliverables remain an open-source Lean checking/audit tool and a six-page empirical + system paper. **W's usability gate completed and failed; the full run was not started.** The user's instruction applies: a failed gate means do not run. **Await the user's decision before any full-run restart, alternative protocol or new qualification.**

## Full-run usability gate

W's [qualification report](../data/openai-math-4eaee875/measurement/census-gate/README.md) is committed as f97e6fbd, with measurement source 2c901ec4. The complete 20-module, four-condition, three-repeat matrix gives a cross-condition instruction spread of 1.3312% median and 3.1498% P95, exceeding the frozen 1%/3% criteria. All 480 foreground/control and 1,413 background attempts returned successfully; aggregate counter-overhead medians passed. Root independently recomputed these statistics from the raw records. This does not establish that every possible census protocol would fail.

The proposed target was all 163,097 modules at OpenAI math revision 4eaee875 in the existing phobos-vt / yunwei356/gpu-smt-dev Workspace. No full workload, alternative protocol, threshold change or retry is launched after this failure. Source availability and the 384 GiB expansion do not qualify the measurement. Preserve the completed gate, preparation and failure records; W owns its technical report.

The earlier 1–2 day estimate is a planning estimate, not a running campaign duration or a start commitment. The original42 and independent precision samples remain separate and preserved. W has superseded the independent precision continuation with 7/12 returned; root does not resume it. Preparation and pilots are not complete corpus measurements.

## Current manuscript and conditional handoff

**Do not add full-corpus measurement content to the paper now.** Keep its numbers, source and PDF unchanged. The existing original42 estimate remains 279.12 compiler CPU-hours with nominal interval 95.18–463.06, at its recorded sample revision.

Section 3.2 keeps the existing sample estimate. The failed gate supplies no full-corpus total, marked-file cost or default-graph cost to substitute into the paper. A different census protocol would need a later explicit decision; this plan starts none.

M's current scaling matrix is preview-only, even if it completes. It cannot fill Table 1 or serve as final paper performance. Final timing requires an otherwise idle machine and follows the resolved gate/full-run path; it must not overlap an admitted census. M's possible full-library original-kernel attempt has unknown feasibility and is not mentioned as a paper result.

Existing installed external check/audit cases and package/container CI remain versioned functional evidence and dated cost observations. Different proof obligations do not support a speedup ratio. Final system results must identify committed tool and input revisions and keep CPU/wall clocks separate.

## Owners and tool delivery

| Owner | Paths | Delivery |
|---|---|---|
| M | checker/ | Original-kernel checker, receipt v1, parallel/resume implementation, labeled preview/final evidence |
| W | tools/audit/, data/openai-math-4eaee875/ | Audit tool, usability-gate validation, conditional full-run data and preserved samples |
| O | crates/, CLI, README, Docker, CI, release workflow, data/external-projects/ | Portable package and external-project acceptance |
| Root | docs/paper/, docs records/status, research/README.md | Six-page paper and evidence integration |

ProofServe checks compiled dependency closures, audits source/default-target coverage and reported evidence, and maintains the existing Kimina-compatible service. Unsupported versions fail clearly or select an explicit official path. No new service feature is added.

The selected-closure performance design retains Mathlib Nat.Basic, Grid and Barrier at 1/2/4/8 workers, three repeats; its Mathlib label is the selected closure. Persistence/split-fallback ablations, official default/fresh comparisons and interruption/resumption retain their scopes. Scheduling final runs follows the gate/full-run outcome and quiet-machine condition, not preview completion.

## Paper and evidence

Keep the title, current four RQs, 10pt double-column format, six pages including references and at most four displays. Keep the technical protocol and conclusion-to-evidence map in [evidence.md](paper/evidence.md); do not create a second long paper.

Preserve the nealmcb distinction: 13.8 hours on 32 vCPUs is measured cloud wall time; approximately 330 compilation CPU-hours is extrapolated from 26 modules with estimated ±30% uncertainty, and approximately 410 includes Comparator work. No unmeasured full-run result or universal priority claim is added now.

## Root execution, operations and publication

**Every root operation inside the Workspace uses CPUs 8–9, including reading, analysis, Git and PDF compilation.** Prefix remote work with `taskset -c 8,9` and preserve that affinity in child processes. Do not reuse the former CPU 22–23 setting. Historical records of earlier compilations retain the CPUs actually used.

Use the same Workspace, volume and Cloudflare CLI path. Omit -M, preserve disk headroom and foreign work, and do not restart active collectors. A later host outage still means preserve the scene and wait for the user, without recovery or scheduling changes.

No new root agent, session, replacement queue, scheduler, prediction, certificate repair, GPU direction, service feature or deeper attribution. No tag, registry upload, upstream issue/PR or announcement. Validated owned-path commits and pushes on main remain authorized. The coordinator's 17 November target is not a user-imposed deadline; the venue is undecided.

[Latest direct words](user-instruction.md) · [Status](research-status.md) · [Evidence map](paper/evidence.md) · [Result index](../research/README.md)
