# ProofServe closure plan

The deliverables remain an open-source Lean checking/audit tool and a six-page empirical + system paper. **Proceed with option A: W launches the frozen 22-core census protocol. Do not wait for another user decision.** This latest instruction supersedes the earlier stop-and-wait disposition; the failed gate remains part of the evidence.

## Full-run usability gate

W's [qualification report](../data/openai-math-4eaee875/measurement/census-gate/README.md) is committed as f97e6fbd, with measurement source 2c901ec4. The complete 20-module, four-condition, three-repeat matrix gives a cross-condition instruction spread of 1.3312% median and 3.1498% P95, exceeding the frozen 1%/3% criteria. All 480 foreground/control and 1,413 background attempts returned successfully; aggregate counter-overhead medians passed. Root independently recomputed these statistics from the raw records. This does not establish that every possible census protocol would fail.

The target is all 163,097 modules at OpenAI math revision 4eaee875 in the existing phobos-vt / yunwei356/gpu-smt-dev Workspace. W owns launch and execution of the frozen eight-P-core plus fourteen-E-core protocol. Root verifies the actual launch and subsequent terminal rather than treating this authorization as completed measurement, and starts no duplicate collector. Preserve the failed gate, preparation and all native outcomes.

The earlier 1–2 day estimate is a planning estimate, not a running campaign duration or a start commitment. The original42 and independent precision samples remain separate and preserved. W has superseded the independent precision continuation with 7/12 returned; root does not resume it. Preparation and pilots are not complete corpus measurements.

## Current manuscript and data handoff

**Do not add full-corpus numerical results before they return.** The existing original42 estimate remains 279.12 compiler CPU-hours with nominal interval 95.18–463.06, at its recorded sample revision. The manuscript now discloses the census measurement decision without inventing its outcome.

Section 3.2 keeps the existing sample estimate until complete usable census records return. Report that the total-instruction gate failed without changing its thresholds. Cross-module comparisons use user-mode instructions, explicitly identified as a criterion selected after observing the gate results. Report P-core and E-core CPU seconds separately, without conversion, and wall time as an observation of this machine and configuration. This is not a passing replacement gate or hardware-independent cost scale.

M's current scaling matrix is preview-only, even if it completes. It cannot fill Table 1 or serve as final paper performance. Final timing requires an otherwise idle machine and follows the resolved gate/full-run path; it must not overlap an admitted census. M's possible full-library original-kernel attempt has unknown feasibility and is not mentioned as a paper result.

Existing installed external check/audit cases and package/container CI remain versioned functional evidence and dated cost observations. Different proof obligations do not support a speedup ratio. Final system results must identify committed tool and input revisions and keep CPU/wall clocks separate.

## Owners and tool delivery

| Owner | Paths | Delivery |
|---|---|---|
| M | checker/ | Original-kernel checker, receipt v1, parallel/resume implementation, labeled preview/final evidence |
| W | tools/audit/, data/openai-math-4eaee875/ | Audit tool, frozen census execution, gate history and preserved samples |
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
