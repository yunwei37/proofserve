# Closest work and novelty boundary

Search session2026-11-01UTC, bounded to this task(well under half a day).
Self-review. Exact queries are in search-queries.csv. This report is literature
analysis only; no competitor system is installed or reproduced.

|Primary source inspected|What overlaps|Decision|
|---|---|---|
|[Hutter et al., Algorithm Runtime Prediction](https://www.cs.ubc.ca/labs/algorithms/Projects/EPMs/)|Instance/configuration features predict empirical runtime; published models/data span multiple benchmark families.|Feature-based regression is established, not our contribution.|
|[SATzilla](https://arxiv.org/abs/1111.2249)|Per-instance empirical hardness models and hierarchical models support portfolio selection.|A two-domain mixture is not algorithmically new merely because domains are Lean tactics.|
|[MachSMT, author institution record](https://uwspace.uwaterloo.ca/items/f73cf195-823d-4613-92b2-fdf3484cb2fb)|Learned SMT hardness models rank solvers across SMT-LIB logics.|Verification-runtime-based selection already exists; SMT search is not the same target as Lean kernel replay.|
|[Efficient Solver Scheduling and Selection,2024](https://www.scitepress.org/Link.aspx?doi=10.5220%2F0012393600003654)|Publisher search metadata describes runtime-interval-driven solver scheduling.|Direct same-mechanism threat. PDF requests returned403; technical guarantees remain unverified, not invented.|
|[openai-math-lean-tooling, section3c](https://github.com/nealmcb/openai-math-lean-tooling/blob/main/REPORT.md#3c-what-makes-a-check-expensive)|On the same public library family, log checking time is fitted to closure source size, decide+kernel and certificate-module counts; the report discusses computational outliers.|Strongest same-setting overlap. Different revision, uncontrolled/paused loaded-machine observations and no inspected heldout calibration mean our controlled validation can add evidence, not priority for the idea.|
|[Kimina Lean Server report](https://arxiv.org/html/2504.21230v2)|Idle-process routing, multicore workers and import-header LRU already address verifier throughput.|The inspected report does not claim a calibrated static runtime estimator; its established resource/cache substrate is not our novelty.|
|[DeepSeek-Prover-V1.5 verifier source](https://github.com/deepseek-ai/DeepSeek-Prover-V1.5/blob/main/prover/lean/verifier.py)|Configurable worker count, timeout and optional address-space limits, plus resource-error retry.|Static limits are already used. This inspected implementation does not establish our proposed predictive admission, and is not a claim about every DeepSeek version.|
|[Mathlib build benchmark](https://raw.githubusercontent.com/leanprover-community/mathlib4/master/scripts/bench/build/README.md)|Whole-build/per-module counters and build/rebuild critical paths already exist.|Measurement and historical costs are established. Measuring time is not predicting unseen source cost.|
|[Mathlib cache](https://raw.githubusercontent.com/leanprover-community/mathlib4/master/Cache/README.md)|Selective prebuilt dependency artifacts avoid repeated compilation.|Dependency-aware reuse is prior art; the inspected docs do not provide an unseen-proof error bound.|
|[Resource Aware ML](https://www.cs.cmu.edu/~janh/assets/pdf/HoffmannAH12a.pdf)|Static type-based analysis derives resource bounds for a supported functional language.|A proved cost bound is a different claim from empirical regression on source text. We have not built such a sound analysis for Lean tactics/normalization.|
|[Angelopoulos and Bates, conformal prediction](https://arxiv.org/html/2107.07511v6)|Prediction intervals can obtain marginal coverage under suitable sampling assumptions.|Statistical intervals are standard and are not deterministic per-instance guarantees; incomplete/nonexchangeable samples matter.|

Compiler static-feature performance models and ML-guided optimization are also
established([Wang/O'Boyle survey](https://arxiv.org/abs/1805.03441)).
That is adjacent technique precedent, not evidence of a Lean-specific theorem
checking model with certified errors. Searches also returned proofs *of*
algorithmic complexity in Lean; those are excluded from checking-cost prediction.

## Explicit claim disposition

1. **Source features predict cost with bounded error:** unestablished here.
   Regression is mature, direct same-library overlap exists, and our incomplete
   sample cannot certify a deterministic bound. Measure out-of-sample error
   and interval coverage; leave the universal version unsupported.
2. **Two source-defined regimes help prediction:** a testable empirical
   increment, not an assumed novelty. It needs a regime-agnostic ablation,
   heldout projects and per-domain errors, including heavy/censored inputs.
3. **Predictions improve admission/scheduling:** shortest-job/cost-aware
   scheduling and runtime intervals are established mechanisms. An increment
   would need measured resource/quality outcomes, uncertainty failures and
   comparison with competent prior-information baselines. No free-cancellation
   assumption or pass@k claim from unrelated module proofs.
4. **Import-only/incremental construction supplies a cost model:** dependency
   availability and cache reuse are established; inspected official docs show
   these mechanisms and measurement, not a proved unseen-source runtime bound.
   This is a limited search conclusion, not proof that no such work exists.

The root paper and RQs are not rewritten by this O-line literature finding.
The requested experiments proceed; their outcomes decide whether the useful
result is regime-conditioned predictability or a measured limit on it.
