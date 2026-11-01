# Paired CPU estimation and coverage rules

estimate_paired_replay_costs.py consumes the fixed42original targets/21strata,
qualified source-cost records and actual accepted native replay rows.
Source/target artifact references must match;operation,output scope,no-M,
Pcore lock,threads,exact source and retirement are checked. Repetitions do
not become new original draws. All statuses remain in the result receipt.

For a complete cell,n=2and population N:
    B_hat=N*mean(b_i), Q_hat=N*mean(q_i)
    V_B=N²(1-n/N)*sample_variance(b_i)/n
and analogously for Q. b/q are direct native wait4user+system CPU.
Incomplete cells are excluded from conditional totals,never filled by zero,
source-clock ratios,profiles or a purposeful closure. Missing population is
reported separately for all/certificate/ordinary source proxy domains.

For R=Q_hat/B_hat,the paired delta variance uses q_i-R*b_i residuals and the
same finite-population variance divided by B_hat². This incorporates covariance;
separate unpaired error bars do not. Nominal tcritical values use
Welch–Satterthwaite degrees of freedom. CPUtotals have nonnegative clipped
lower limits;ratio upper limits are not capped at1because replay may be slower.
No simultaneous all-domain coverage or heavy-tail guarantee is claimed.

A domain total can become identifiable before every other domain completes:
for the primary source proxy,all marker-positive strata suffice for its source
CPUtotal. The complete-library total/share still needs all21cells. Source-only
and paired-replay cell coverage are separate. A newly completed source draw
cannot fill its missing verification cost.

Outputs distinguish:
- unweighted observed paired CPU/wall distributions;
- complete-stratum conditional weighted costs/ratio;
- full-domain or full-source-frame estimates only when every required cell
  has its original costs,with nominal pointwise95%intervals;
- missing/rejected/setup/timeout/resource results and unsupported domains.

The replay variable is **fresh target-only native checking with imports trusted
like leanchecker**,including repeated imports/startup. It is not O's shared
empty-environment stream variable or proof-only kernel CPU. Its eventual
population total is a workflow cost over the163,097source-module frame,not
a certificate that all163,097artifacts are valid. Whole project construction,
external library checking/linking,axiom closure and transitive byte-identical
context costs remain outside this estimand. None is imputed from this adapter.

Two-draw heavy-tailed cells,nonresponse/censoring,environment drift,source-proxy
misclassification and missing whole-transitive artifact equality limit the
nominal intervals. HTweights and paired delta arithmetic are standard methods,
not claimed novelty. Five closed-form tests exercise exact-census totals,
covariance cancellation,hand-computed nonproportional variance,unequal
population weights and invalid sampling sizes. They are not native data.
