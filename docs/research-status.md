# ProofServe: current status

The two deliverables are the open-source Lean checking/audit tool and a six-page empirical + system paper. The latest decision prioritizes a full build of all **163,097 modules** at the pinned OpenAI revision; sampling will serve as calibration.

## In progress

W owns the full-corpus build on phobos-vt in the existing gpu-smt-dev Workspace. The work PVC is verified at **384 GiB**. Available host resources may be used for parallel compilation under the new direct instruction. The 1–2 day estimate is provisional. The latest source-acquisition terminal is complete; a full build result has not returned.

M's current matrix is a **preview**, excluded from final paper performance and Table 1. Final system timings wait until the census ends and the machine is otherwise idle. A possible full-library original-kernel attempt has unknown feasibility and is not a paper result.

## Evidence already available

- [Sample package](../data/openai-math-4eaee875/README.md): 42/42 original costs, estimated compiler work **279.12 CPU-hours**, fragile nominal interval **95.18–463.06**. These existing numbers remain unchanged until complete census data replaces Section 3.2. The fixed precision panel stays separate.
- [External installed checks](../data/external-projects/results.md): three cases, exact common-local-root acceptance, separate CPU/wall observations, and retained official resource failures. Package and network-disabled container CI passed finite functional controls. These establish functionality, not equal-obligation speedups.
- [Current six-page paper](paper/main.tex): matched cost windows, lexical density, default coverage and stored-proof repeatability. The PDF remains at the 4e63272a revision; no census numbers have been inserted.

The nealmcb comparison remains explicit: 13.8 hours on 32 vCPUs is measured cloud wall time; about 330 compilation CPU-hours is a 26-module extrapolation, and about 410 includes Comparator work.

[Plan](research-plan.md) owns the new execution and manuscript transition. [Evidence map and protocol appendix](paper/evidence.md) distinguish completed evidence, previews and pending census results. Root maintains documentation without starting another collection or changing owner implementations.

No tag, registry publication, upstream issue/PR or announcement. Preserve existing data and active work; a later host outage still means preserve the scene and wait for the user.
