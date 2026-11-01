# Cost prediction: useful estimates, no bounded-error claim

2026-11-01 UTC, O line. Self-review. The protocol and prior-art judgment were
committed in58ab893 before fitting. No new predictor, corpus, validation split
or feature threshold was selected after seeing held-out errors.

## Conclusion and novelty

The proposed strong claim is unsupported: we cannot predict an arbitrary
AI-generated module's cost with a demonstrated per-instance error bound.
Source-only models give rough estimates on the observed completed subset.
The two source-defined regimes do not consistently improve held-out prediction,
and native budgeted ordering did not improve the number completed in this run.
Conservative upper admission traded completions for avoiding interruptions.

Generic log-runtime prediction, solver selection, uncertainty-based scheduling,
and cost ordering have substantial prior art. Most directly, the independent
[openai/math tooling report](https://github.com/nealmcb/openai-math-lean-tooling/blob/main/REPORT.md#3c-what-makes-a-check-expensive)
already models checking cost using closure size and computation markers on the
same library. It also discusses outliers; this defeats a claim that merely using
these features is new. Different revisions and measurement protocols prevent
comparing its fit score to our held-out errors. See[prior-art.md](prior-art.md)
and[search-queries.csv](search-queries.csv) for searches, primary sources, and
which technical details were not independently accessible.

The increment here is controlled measurement of predictability limits:
source-only versus post-production features; compiler versus kernel-component
targets; project leakage; missing/censored heavy jobs; domain ablation; and the
native completion/interruption tradeoff. This is characterization evidence,
not a novel scheduler or a certified static bound. We do not install a learned
policy in the production engine based on this result.

## Data, censoring, and features

The original42-target frame has31 qualified completed no-M source builds.
All42 static rows remain in[primary42-features.csv](primary42-features.csv);
the11 unavailable primary costs remain missing, not zero or a successful
subset silently relabeled as the frame. No inference about all163,000 modules
follows from these31 observations. No sampling-design population CI is claimed.

The frozen expanded set has6,214 compiler-cost modules, including131 OAI
modules, plus5,085 conditional kernel-replay component labels; there are6,225
distinct feature rows overall. SDK/Mathlib modules dominate this auxiliary set.
Repeated measurements of the same module are retained in raw tables but not
counted as independent training examples. A further observed noncompletion,
TableDensity1Panel0, was clipped by its owning run's wall budget after33.20CPU
seconds: it is censored and excluded from completed regression, not a known
33.20-second service cost. Missing and censored tails could make every quoted
accuracy optimistic. Dataset sources/exclusions are in[dataset-receipt.json](dataset-receipt.json).

Static extraction parses the pinned source and import DAG without executing
Lean: source bytes, direct/closure file counts and bytes, import depth, lexical
declaration counts, explicit computation markers and density, largest numeral
and literal range, and statement equality/quantifier/arithmetic/logic fractions.
No dependency cycles or unresolved source imports were found in this input.
These are lexical proxies, not elaborated goals or a proof of computational
size. Macros, imported definitions and typeclass inference can hide work.
The extracted large-decidable-risk flag is descriptive; the fixed regression
uses its constituent numeral/range/marker features rather than tuning a new
risk classifier. Source path resolution for three patched Rellich inputs was
corrected before the final fit; initial incomplete extraction remains on PVC
and is documented in[revision-reason.json](revision-reason.json).

## Prediction results

Costs are natural-log ridge targets: native compiler CPU(user+system) and,
separately, conditional kernel replay wall components. The former includes
imports, search, checking and output. The latter excludes environment import,
contains tiny/empty modules and only a few AI roots. They must not be treated
as interchangeable verification costs.

Ridge penalty1, transforms, seeds, lexical regimes and all model comparisons
were fixed in advance. Errors below are absolute relative error, not R-squared.
Exact leave-one-module-out PRESS was cross-checked with explicit refits of
three actual rows per model/cohort:20 checks passed at relative difference
below1e-5. Five-fold grouping holds complete source projects out; ordinary
module folds can leak project-specific structure.

| Model | LOO median / P90 | Module 5-fold median / P90 | Project 5-fold median / P90 |
|---|---:|---:|---:|
| constant | 85.79% / 343.50% | 87.68% / 378.94% | 86.50% / 366.74% |
| bytes | 41.54% / 110.72% | 43.09% / 114.77% | 34.03% / 100.55% |
| imports | 49.34% / 85.67% | 53.88% / 105.16% | 48.08% / 77.62% |
| static | 38.67% / 106.60% | 48.66% / 120.03% | 34.95% / 77.38% |
| regime | 44.11% / 83.49% | 48.13% / 98.53% | 50.07% / 93.02% |

For project-grouped static prediction, the95% project-block bootstrap CI is
24.24–58.97% for median error and66.44–165.37% for P90. With the regime features
it is24.92–66.63% and66.08–170.99%. Paired bootstrap differences(regime minus
static) include zero: median[-8.72,+23.81]percentage points,
P90[-14.16,+48.06]points. Thus the observed overall deterioration is not
a statistically established negative effect of regime features.
CIs resample fixed out-of-fold errors, not the full training procedure;
they are not per-request or corpus-wide error bounds.

By source regime, project-grouped primary static errors are29.65%/77.09%
for14 ordinary-marker-absent modules, and53.91%/109.50% for17 computation-
marker-positive modules. With regime features these are24.14%/70.59% and
62.26%/126.57%, respectively. The desired claim that separating two regimes
makes their costs reliably predictable is not supported.

Auxiliary131AI modules give24.50%/84.01% static error and15.21%/86.15% with
regime features; the bytes-only model gives13.46%/89.03%. Project imbalance
and unrepresentative extra roots preclude a broad AI-library claim.
Across6,214 mixed compiler modules, static26.44%/70.37% becomes
26.16%/69.56%, a small change dominated by non-AI dependencies.
For5,085 kernel-component labels, static63.61%/291.36% becomes
63.86%/291.29%; only14 component labels are marker-positive.
See[errors.csv](errors.csv) for all splits, domains and CIs.

Wall-clock sensitivity keeps the same design and31 completed primary inputs:
project-grouped static median/P90 error42.45%/100.84%, regime41.01%/89.82%.
Full LOO/5-fold/domain tables are in[wall-errors.csv](wall-errors.csv).
This sensitivity was evaluated after the CPU analysis without changing the
model, choosing a winner, or using it to retune the native scheduling plan.

## Upper estimates and offline replay

Outer project folds reserve separate fitting and calibration projects. A
one-sided90% residual quantile gives28/31 observed coverage for both the
imports and regime models. Rank overflow yields infinity, not a fabricated
finite bound. Stratified incomplete selection, dependent projects and small
calibration sets prevent treating this as guaranteed90% future coverage,
let alone a deterministic bound. See[intervals.csv](intervals.csv).
The point and upper policies share these calibration-fit point predictions.

The offline replay uses actual frozen CPU costs,100 fixed arrival
permutations, five predeclared budget fractions, and FIFO/predicted/upper/oracle
policies. At25% total observed CPU(158.15s), mean completions are FIFO7.83,
regime sorting22, regime upper admission21 and oracle24. FIFO/sorting/oracle
have one budget interruption; upper admission has none and defers10 jobs.
This counterfactual result is not native throughput. See[simulation.csv](simulation.csv).
It overstates the gain actually observed below, so it cannot substitute for
execution evidence.

## Actual bounded native experiment

One matched new point executes the31 reference modules with Lean4.34.1,
P0–7 shared lock, j8, no-M, normal olean/ilean/C outputs, one child at a time,
11.5GiB child cgroup plus512MiB parent reserve, and a60CPU-second budget per
policy. The same regime forecasts were frozen before the run; actual old
service costs were not passed to the policy. Feature extraction/forecasting
were precomputed; their online cost is not included. Wait4 child CPU and driver
CPU are charged. OS CPU limits are approximate quantum-based operational
limits, not Lean heartbeat semantics. Children/driver retired,45 calls returned.

| Policy | Completed | CPU used / allocated | Wall | Budget interruptions | Deferred |
|---|---:|---:|---:|---:|---:|
| FIFO |15|59.44 /60s|53.55s|1|15|
| Predicted cost |15|59.46 /60s|51.60s|1|15|
| Upper admission |13|41.85 /60s|38.81s|0|18|

All43 completed calls exit0. Two others exit with SIGXCPU; neither is a Lean
semantic rejection or a false theorem. No OOM or wall-time interruption was
observed; maximum child cgroup peak was0.873GiB. Sorting does not increase
completion count. Upper admission avoids budget cuts by leaving18.15CPU
seconds unused, with fewer completions. Each policy has two definite upper-
estimate misses among its observed calls: these are a descriptive lower count,
not coverage computed by assuming interrupted/deferred costs.

Accepted sets differ under this fixed budget because different work is
selected; this is not a claim of identical full-batch rewards.
There is one reference proof per distinct module. Completion fractions
15/31,15/31,13/31 can be reported as this subset's budgeted pass@1 only;
pass@k for k>1 is not identifiable. They are not miniF2F candidate pass@32.
A single sequential policy order, warm filesystem effects, changed fresh-
compile environment, and absent failed/heavy primary cases limit causal
throughput claims. No claim of beating a warm service or replicated native
speedup is made. Native evidence contradicts a simple reading of the much
larger offline gain, rather than being omitted in favor of that gain.

Raw commands, outputs, cgroup memory events and exact IDs are on PVC at
/workspaces/.agent-state/gpu-smt-captures/cost-prediction-20261101-v2/native-policy-v1.
Small outputs:[native-summary.csv](native-summary.csv),
[native-results.csv](native-results.csv),[native-terminal.json](native-terminal.json).

## Reproduction and next action

extract.py freezes eligible labels and source features; fit.py evaluates fixed
models/calibration; wall_sensitivity.py adds the wall target; simulate.py replays
CPU service costs; native_policy.py executes a plan in its own output directory.
Absolute PVC paths intentionally identify this research snapshot and matching
toolchain; these scripts are not portable production APIs. Full feature,
prediction, repeat, failed and source records remain on PVC(v1 and correctedv2).
Only small tables and authored scripts enter Git.

No data support a novel bounded-error predictor or production admission
mechanism here. Keep this as characterization evidence and resume the existing
Falconer full-closure build/check experiment; do not replace it with further
post-hoc predictor tuning.
