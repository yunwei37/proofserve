# Mixed-request regime-aware checking: feasibility result

2026-11-01UTC, O line; self-review. Protocol393841a. This is an executable
policy prototype evaluated by **trace-driven replay of actual native operation
costs**, not a production implementation or a new native batch throughput run.
No regression is fitted. All four main policies preserve identical FIFO order.
The classifier changes the chosen checking implementation, not just order.

## Verdict

On these measured inputs, **classification-driven mode selection does not
improve completed work under a fixed aggregate CPU budget**. Using streaming
for every request is as good or better in every tested setting. The useful
component is selective admission; it does not require switching computational
requests to the more CPU-expensive parallel checker. A separate all-stream
admission control confirms this distinction in the representative mixed case.

Misclassification robustness cannot be inferred from the earlier93.1% accuracy
or0.48% CPU exposure. Injected errors can reduce admission completion and cause
cuts, or can accidentally improve completion by selecting the cheaper serial
checker for computation. Label accuracy and policy utility are different targets.

## Inputs, budget and operation boundaries

Only two closures currently have complete measured costs for all operations:
Mathlib.Data.Nat.Basic(1330 modules) and PlanarPacking.Grid(3793).
Barrier lacks a matched complete construction cost; NearPin and Amplitudes lack
a matching qualified parallel-closure pair. No ratio fills those missing cells.
These two templates do not represent all AI mathematical/computational traffic.

| Root | Source build CPU | Serial stream CPU | Parallel4 CPU |
|---|---:|---:|---:|
| Mathlib.Data.Nat.Basic |1018.219s|65.955–71.744s,3 repeats|83.757–85.665s,3 repeats|
| Grid |6593.253s|557.350s,1 observation|744.406s,1 observation|

Construction CPU is the sum of native compiler user+system time over the exact
dependency closure, including imports and normal olean/ilean/C output. It is
NOT622.379/3878.707s summed compiler wall, and not parallel Lake makespan.
Compiler commands/exit0/three artifacts/no sorry/no-M were checked against raw.
Serial/parallel costs are complete native checked-closure process CPU, including
startup/read/context work, not isolated leaf timers or scaled kernel shares.
The same typed artifact paths and accepted IDs were qualified in the original
native experiments. Grid's repaired pair gap and single observation remain;
no new randomized/repeated Grid timing is claimed.

Requests provide source AND already-produced artifacts and ask for validation.
Full source reconstruction is the requested build baseline, with extra outputs.
It is not an optimized warm candidate compiler. Proof generation, artifact
production for the checking paths, network/queue work, online feature extraction,
process replacement and real cancellation costs are not magically eliminated:
they are OUTSIDE this narrowly defined artifact-validation replay.
Consequently, the build/check difference is an operation-cost comparison,
not a source-only end-to-end service speedup.

The prior native points used P0–7, no-M and external memory guards; all recorded
operation RSS peaks are below12GiB(max7.57GiB source process). Some original M
checker caps were14GiB; reusing their observed costs is not a new12GiB execution
qualification. This analysis uses E8, launches no Lean and does not acquire or
interfere with the active native P-core lock.

## Mixed-request matrix and actual policy decisions

Each synthetic batch has20 independent fresh-root requests, with no result
cache or shared preparation across requests. Repeated templates are intentional
stress inputs, not20different measured mathematical proofs.
Certificate fraction:0/10/50/90/100%. Per-request CPU cap:100/800/10000s.
Total batch CPU budget:1000/5000/20000s. All combinations use3 fixed seeds.
The800s request tier permits both checking implementations on both templates;
10000s permits building as well. Low tiers deliberately expose budget failures.

Source labels are fixed from explicit-marker counts (ordinary versus certificate);
both selected templates are correctly labeled. This is NOT an experiment with
93.1%-accurate labels sampled from the previous29-module population. Exactly
0,2,4 randomly chosen request labels are flipped per batch (0/10/20%).
The same actual requests/order/noise positions/budget apply to all policies.

- **all_build:** source compiler reconstruction, irrespective of label.
- **all_stream:** original serial kernel streaming, irrespective of label.
- **classified:** predicted ordinary -> serial streaming; predicted certificate
  -> qualified original-kernel parallel4 rechecking, no chunk proof rewrite.
- **classified_upper:** identical mode choice plus pre-dispatch admission.
- **all_stream_upper:** separately identified component control, always stream,
  to separate the value of admission from the value of choosing a checker.

Every cost lookup is indexed by ACTUAL input and SELECTED mode, not predicted
input. A falsely ordinary Grid request therefore still costs557.350CPU seconds
in streaming, not the68-second mathematical-template cost. Route engagement
is explicit: the main classified policy actually dispatches2280 computation
requests to parallel checking and3111 mathematical requests to streaming over
the entire matrix, plus335mathematical->parallel and287computation->stream
dispatches under noise. These are counterfactual operation selections, not new
native invocations.[Full engagement](mechanism-route-engagement.csv).

Class upper envelopes are maxima of previous measured cost within the predicted
class and selected checker. They are same-template historical bounds, not
certified unseen-module intervals. All-stream admission uses its corresponding
serial envelopes. The previous NearPin transfer counterexample remains valid.
No runtime regression predicts individual requests here.

Each attempted job receives min(request cap, remaining batch CPU). A cost that
does not fit consumes that allowance, becomes an operational interruption,
and its work is discarded; later requests can run if batch budget remains.
Admission defers rather than labels a proof false. At zero remaining budget,
other requests are unattempted, not zero-CPU interruptions.
This continuous-work model idealizes instantaneous cancellation and omits real
cleanup; it does not overwrite the previous native RLIMIT-quantization findings.
An interrupted job's wall/makespan is unknown, never linearly inferred from CPU.

There are1620 main-policy batch replays plus405control replays:2025batch cells,
40500request cells and675three-seed summary rows. Only the original8full checker
native cells and two compiler-work aggregates supply cost observations; these
are not2025new native runs. Tables give observed three-seed ranges, not a
population confidence interval or repeated-native uncertainty for Grid.

## Representative mixed case: all modes feasible per request

50% computation;10000CPU seconds/request;5000CPU seconds total; no label noise.
Each mean below comes from3paired batches:

| Main policy | Completed [min,max] | Interruptions mean | Discarded CPU mean | Passed/presented |
|---|---:|---:|---:|---:|
| all_build |3.00 [1,4]|1|1945.34s|15.00%|
| all_stream |16.00 [15,17]|1|481.67s|80.00%|
| classified |13.33 [13,14]|1|480.66s|66.67%|
| classified_upper |14.33 [13,15]|0|0s|71.67%|

CPU-budget goodput is respectively2.16/11.52/9.60/10.32 completed requests per
allocated CPU hour, not wall TPS. The all-stream-upper component control gives
17[17,17]completions, no interruption/waste,85%passed/presented and12.24/CPUhour.
Thus admission has value here, but switching to parallel computation is not
needed for that value and reduces the CPU-budgeted completion count.

Across all45mix/request-budget/total-budget settings, classified versus
all_stream at0noise wins0, ties35 and loses10. At10%noise it wins0/ties32/
loses13; at20% wins0/ties31/loses14. On these inputs every serial CPU cost is
lower than its paired parallel cost, so a FIFO CPU-work objective cannot benefit
from that mode switch. This is specific to this cost table, not a theorem that
parallel checking never helps wall latency or other proof families.

With10000s/request and20000s total in the50/50mix, all checking policies
complete20/20 with no interruption; building completes6.67[6,7].
This does not create extra value for the classifier at generous checking budgets.
With100s/request and1000s total, build completes0, all_stream and classified
both6.33[6,7], and classified_upper10[10,10].
The complete675-row table includes pure-class and all intermediate cases;
these examples do not replace the full matrix.[Summary](mechanism-summary.csv).

## Misclassification sensitivity: no presumed robustness

At50/50mix,100s/request,1000s total, classified_upper yields:

| Injected wrong labels | Completed [min,max] | Interruptions mean | Discarded CPU mean |
|---|---:|---:|---:|
|0%|10.00 [10,10]|0|0s|
|10%|9.67 [9,10]|1.67|166.67s|
|20%|8.67 [8,9]|2.67|266.67s|

Completion falls3.33% and13.33% relative to the perfect-label admission case.
The misleading ordinary label can admit an expensive Grid request under a
too-small mathematical upper; every resulting cut is retained. False positives
can instead defer cheap mathematical work that would have fitted.

For the pure mathematical batch with100s/request and5000s total, upper admission
completes20/18/16 under0/10/20%noise: exactly the two/four flipped requests are
incorrectly deferred. There is no interruption/wasted CPU, but availability
falls20% at20%noise. Small measured CPU on a mislabeled module does not bound
its opportunity cost as a skipped request.

The effect is not always deterioration. At50/50mix,800s/request and5000s total,
classified completion increases13.33 ->14.33 ->14.33 under0/10/20%noise;
classified_upper increases14.33 ->15.67 ->15.67. Some wrong ordinary labels
send Grid to the CHEAPER serial checker, accidentally helping CPU-limited
completion. This is not a success of an inaccurate classifier: the chosen
regime-to-method policy is mismatched to its CPU objective.
The full paired-noise deltas and each request's true/predicted kind, mode,
budget and outcome remain on PVC.

All inputs are previously accepted references. Passed/presented measures the
fraction yielding a completed known-valid validation within the budgets;
passed/attempted is also retained in raw batch tables. It is not a false-accept
rate, changed theorem validity, or candidate pass@k. Trace replay does not
test malformed proofs or prove a production adapter sound. Existing kernel
qualifications do not turn a classified/deferred request into a rejection.

## Reproduce, trust and decision

Run inside the owning Workspace:
    python3 research/cost-prediction/mixed_mechanism.py --out /workspaces/.agent-state/gpu-smt-captures/NEW_EMPTY_POINT

The output directory must not already exist. Inputs are retained pinned
native captures and their source/command records; absolute paths intentionally
identify this research snapshot. No dependency installs or Lean invocation.
[Operation costs](mechanism-operation-costs.csv) and full small summaries
are in Git. Raw requests, batch repetitions, paired-noise deltas and both
initial/final calculation snapshots stay on the existing PVC:
cost-mechanism-mixed-20261101 and cost-mechanism-mixed-20261101-v2.
The latter adds a CPU-goodput output column and corrects aggregate-row wording;
inputs/policies/seeds/results did not change.

Conclusion: **classification is feasible on the previously measured panel,
but streaming itself supplies the useful CPU-cost reduction here. Class-based
parallel routing adds no CPU-budgeted completion gain.** Historical class-aware
admission can preserve known-workload availability, but the all-stream control
shows that mode switching is not necessary. Noise robustness is mixed and
cannot be extrapolated from93.1%label accuracy or0.48%kernel-CPU exposure.
SATzilla2012 already uses cost-sensitive classification; this experiment is
systems-mechanism feasibility evidence, not a novelty or product claim.
Keep these negative and conditional results. Do not enable a production policy
from this two-template replay, and do not claim new native throughput.
