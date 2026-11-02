# Missing11draw impact: source versus stream (W076,2026-11-02)

**Decisive answer:** the11missing original draws can materially change both
total CPU and regime prevalence. Under the declared observed-class-range
assumption, the eventual complete-sample source HT point spans
**178.226–627.348CPU h**, rather than a tight neighborhood of W074's215.924h
class-mean projection. A10xclass-maximum stress gives **4786.791CPU h**.
These are scenario endpoints, **not confidence intervals or data-guaranteed
population bounds**. Without additional cost assumptions there is no finite
pessimistic completion-cost upper bound.

## Final source / serial-stream table

All values CPU hours. For each missing draw assume its original native cost
lies between the observed minimum and maximum **of its source proxy class**:
ordinary[1.204525,40.791652]s, marked[1.069679,163.845944]s.
Preserve all31observed costs and their original inclusion weights; fill only
the11missing draw values for this sensitivity calculation.

| Source proxy | Constructed-cost scenario range | Serial stream, O-ratio-transfer range | Stream if missing maximum-cost draws get **no savings** |
|---|---:|---:|---:|
| Ordinary mathematical |150.348–573.155|5.969–36.967|444.539|
| Marked computational |27.877–54.193|2.353–4.589|28.834|
| **All163097source modules** |**178.226–627.348**|**8.322–41.555**|**473.373**|

This is the requested whole-frame **conditional table**, not a full-frame
measurement or95%interval. Its finite ends are conditional on missing-draw cost
ranges and checker-transfer assumptions. The last column is a separate
unfavorable verification hypothesis, not a proven upper bound.

For streaming transfer use O's measured complete-closure CPU fractions:
ordinary0.039699–0.064497(NearPin/Nat.Basic), marked0.084421–0.084671
(Amplitudes/Grid). These are CPU ratios, not reciprocal elapsed speedups.
Known31stream contributions are also modeled using these anchors; they are
not31measured stream costs. Both small CSV columns and actual raw references
are preserved in ../cost_staircase/calibration.csv.

The selected closure ratios mix shared base/ordinary dependencies with
computational roots. O's elapsed target-only components show a much sharper
0.46%NearPin versus80.28/82.35%Grid/Amplitudes contrast; these are not CPU
and are not used to create fictitious CPU values. External once-only
SDK/Mathlib checking, global scheduling, memory scaling and generation costs
remain unmeasured.

### What “most optimistic / pessimistic” can mean

| Missing-cost assumption | SourceCPU h | StreamCPU h, fixed O anchors | StreamCPU h if missing draws get no savings |
|---|---:|---:|---:|
| Artificial zero missing work |165.188|7.797–11.213|11.213|
| Each at its observed class minimum |178.226|8.322–12.057|24.251|
| Each at its observed class median |216.476|9.908–14.555|62.501|
| Each at its observed class maximum |627.348|27.329–41.555|473.373|
| Each at10xclass maximum |4786.791|203.115–314.635|4632.816|

Zero is an algebraic sensitivity floor for the **future complete observed HT
point**, not a lower confidence bound on population work or a plausible
prediction that the missing sources cost nothing. Original partial known
terms already sum165.187936h, more than the complete14-cell subtotal140.851561h,
because three incomplete cells have one known draw. Hence this table is not
obtained by simply adding assumptions to140.85h.

There is **no finite pessimistic upper bound for successful completion**.
An additional nominal9600CPU-second/draw budget illustration(8eligible cores
x1200native seconds) yields104249.188weighted CPU h. That changes the estimand
to budgeted consumed work and says nothing about completing every build.
It is not a hard timing/CPU ceiling: deadline response can overshoot. The
actual capture's cgroup/RSS safeguards are independent of this illustration.

## Does the gap change the conclusion?

1. **Total size:** the observed-class-min/max range alone differs by3.52x;
   missing high-weight draws can swamp a140.85hcomplete-cell estimate.
   +1CPU second on *each* missing draw changes the eventual HT point
   +10.842083h; Hodge alone contributes+5.54625h.
2. **Regime prevalence:** assuming ordinary missing draws cost10xordinary
   maximum but marked missing draws cost their observed minimum gives
   computational source share **0.6165%**. Reversing the hard tail gives
   **66.0565%**. These are deliberately contrasting stress assumptions,
   not a confidence interval. The marked proxy and complete14cell17.14%
   share are unchanged in the underlying data.
3. **Streaming robustness:** forcing every unknown module to inherit the
   same subunit stream/build ratio guarantees a favorable answer by model
   construction. It cannot validate a general speedup. With class-maximum
   missing source costs, giving their checks no savings changes stream work
   from27.33–41.56h to473.37h versus627.35hsource. If their checking CPU is
   **1.3332xsource CPU**, total modeled stream and source are equal;2xgives
   **935.53hstream**, reversing the comparison. With10xsource tails the
   break-even is only **1.0333x**. No such checking overhead is claimed
   observed; the threshold states exactly what the missing data can change.
4. **Chunking focus:** W074's0.47%covered elapsed marginal is still a
   conditional model, not a universal small-benefit theorem. Missing marked
   work could raise its relevance, but source markers do not establish
   >=1sgoal grain, source-qualified splitting or actual savings. Neither
   17% nor66%sourceCPU share can be substituted for eligible stage-c checking
   elapsed share. The current evidence supports a local example while the
   missing costs remain a genuine decision uncertainty.

## Bounds versus confidence intervals

W074 retains nominal sampling-only intervals for the **covered14cells**
(build140.852h,[0,455.504]); its full-class-mean extrapolation interval further
conditions on an unverified nonresponse model. The ranges here are **gap
sensitivity bounds under explicitly assumed cost support**, not confidence
intervals. No t approximation repairs missing heavy-tail data. Combining
these finite stress ends with nominal CI endpoints would fabricate an overall
coverage guarantee, so the two forms of uncertainty remain separate.

The whole-frame current empirical cost/confidence fields therefore remain
unknown. The lower algebraic point165.188 and unbounded upper pertain only to
completing the same42observed draws with nonnegative finite costs, not to
inference on the population total.

## Reproduction, files and review

```sh
taskset -c 8-15 python3 workloads/openai-math/missing_draw_stress.py
```

Small outputs only; no Lean, profile, cgroup or lock submission. Inputs are
the fixed original42frame and31qualified no-M native cost rows from
../noM-original-c-suffix48/sample-costs.csv plus W074's Ocalibrations.
The actual31fresh target replays are separately finalized in
../native-replay31/README.md and are **not** the empty-environment stream.

- source-vs-stream-scenarios.csv:27domain/scenario totals, adverse missing
  checker alternatives and exact break-even k.
- missing-draw-scenarios.csv:all11specific missing IDs/inclusion weights and
  assumed costs for every scenario; no primary-data imputation adopted.
- assumed-cost-levels.csv:observed source class ranges/medians, covered means
  and unknown inclusion-weight sums.
- receipt.json:formal unknown/unbounded fields and checks.

Nine class sums independently reconcile, and known HT terms/+1second slope
match W073. All31original values unchanged; no sample replacement or
discarded hard draw. Statistical method is standard HT/sensitivity analysis,
not novelty. Review is this thread's **自审**.
