# Research status

Updated2026-11-01UTC. The user-selected paper mainline is **two verification
cost regimes**: computation replay versus checking mathematical witnesses.
It replaces the old prepared-state/accelerator mainline.
[Paper](paper/main.tex) · [Plan](research-plan.md) · [Result index](../research/README.md).

## Current contract
Computational certificates can require the kernel to redo encoded computation.
Mathematical proofs may have a cheaper checking boundary, while imports and
elaboration coupling can obstruct cheap independent verification.
The old75–94%/~2% user-cycle panel and1.28build/replay ratio were measured
under-M. They motivate questions, not current noMphase shares or cost bounds.
No-M population phase weights, AI-closure checking ratios and matched-output
parallel speedups remain missing. One complete Mathlib checking control is below.
All current native measurements omit-M; memory protection is external cgroup.
Old-Mcosts/profiles remain historical methodology, never corrected by Grid's
ratio. [Withdrawal](tmp/build-and-evaluate/step-0229-20261031T235441+0000/step-report.md).

## Lines and paths
| Line | Responsibility | Paths |
|---|---|---|
| W | Public outputs, census, original-frame noMcosts and regime prevalence | [workloads/](../workloads/W-status.md) |
| M | Automatic chunking and original-kernel parallel checking | [chunked-kernel-check](../research/chunked-kernel-check/README.md) |
| O | Decoupled single-process streaming checker, engine and open-source delivery | [decoupled-check](../research/decoupled-check/README.md), crates/ and service docs |
| Root | Paper, source/count verification, evidence and user-record integration | docs/paper/, research index, status and plan |

Earlier work:
[mechanisms-2026-10-30](../research/mechanisms-2026-10-30/README.md),
[system profiles](../research/profile-2026-10-31/systime/final/README.md),
[startup/replay](../research/profile-2026-10-31/startup-replay/README.md).
Same phobos-vt Workspace/PVC,40GiB shares W16/M16/O4/root4;<=8cores per line.
Shared P0–7 timing lock; root E22–23. No new agent or infrastructure change.

## Evidence and limitations
- [Static census](../workloads/openai-math/README.md):
  163097files; default root omits451008/1354379=33.30%lexical decide+kernel,
  not runtime. Same-scanner Mathlib masked7sites/4files versus openai1354379/5848;
  density10668.32x, positivegeneratedfiles3.5856%, not CPUweights.
- [Fresh noM31](../workloads/openai-math/noM-standard-artifacts-a/README.md):
  W reports31successful native calls:29/42random costs/12complete strata,
  plus2purposeful modules.13draws remain missing; no fullCPU/globalCI.
- [NoM26dependency prefix](../workloads/openai-math/noM-original-c-prefix26/README.md):
  no new random endpoint; lock deferral is not proof/resource failure.
- [Replay scopes](../research/profile-2026-10-31/startup-replay/repaired-replay-analysis.md):
  15stockchecker targets pass,13short median3.510s without-M. Separate
  process/trust boundary, not pure kernel or matched noMbuild/replay gain.
- [Chunking status](../research/chunked-kernel-check/README.md):
  realGrid equality,18scalar leaves, k0/1/2/4/8. Initial15cells have an
  output-boundary mismatch; correctedV3 remains partial, no matched scaling
  claim. Earlier lexical target-header borrowing is corrected; superseded
  shape ratios are not certified split coverage.
- [Matched Mathlib closure](../research/decoupled-check/math-closed-result.md):
  all1330 reconstructed modules, matched stream65.692644s / serial source
  work622.379412s=10.55508%;42 complete oracle chunks match1330acceptances.
  Stream132484entries/2269upstream unsafe-partial exclusions; three bad proofs
  rejected by both paths. One Mathlib control/warm pass, not AI-population,
  serving speedup, parallel Lake makespan or full axiom/soundness audit.
  [Root reanalysis](tmp/build-and-evaluate/step-0232-20261101T011130+0000/step-report.md).

## Retained negative or limited results
- [Warm comparison](../artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z/result-review.md):
  7808same statuses/3014accepted IDs,19.28%less elapsed at one point;
  retry/order/CPU eligibility differ, not isolatedCOW or general superiority.
- [GPU screening](../artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/result-review.md):
  8.86%slower/no timeout removed, not a universal GPU impossibility result.
- [Source-cost scheduling](../artifacts/candidate-scheduling-2026-10-25/source-cost-crossfit-20261026/README.md):
  held-out predictor did not beatFIFO; don't repeat.
- [Seven row certificates](../research/mechanisms-2026-10-30/openai-kernel-sample/README.md):
  all7+7sources accepted; old-M timing ranking isn't a current noMtransfer result.
- [Evaluation](evaluation.md) preserves42resource failures, failed判死prototypes,
  interrupted state-reuse capture, and all partial/failed results.
  CPU oracle stays frozen; no new oracle contribution/experiment.

Draft/CI/native completion/axiom-clean acceptance are different.
All root reviews are **自审**, not independent or venue acceptance.
The supplied word supplement is preserved and deduplicated; unavailable
complete cross-chat conversation history is not claimed recovered.
