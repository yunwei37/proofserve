# Binary regime classification: validation and cost of choosing a checker

2026-11-01UTC, O line; self-review. No regression was fitted or retuned.
Native repeated policy cells remain pending at this checkpoint; below are
completed static/trace analyses, not a finished scheduling experiment.

## Classification versus a runtime forecast

The fixed source rule is explicit computation-marker density>0. It returns a
label only. It is neither a numeric cost estimate nor a failure/validity verdict.
Goal-shape and file-structure features remain available; the existing simple rule
is evaluated without fitting a classifier to this very small dynamic panel.
A learned class model is not required to test this source-level hypothesis.

It would be incorrect to distinguish this from all SATzilla variants by saying
SATzilla predicts exact runtimes.
[SATzilla2012](https://www.cs.ubc.ca/~kevinlb/papers/2012-SATzilla2012-Solver-Description.pdf)
already selects solvers with cost-sensitive classification without runtime
regression. Here the label concerns Lean proof-checking work rather than a
winning SAT solver. That domain/target distinction does not establish novelty
for classification or portfolio routing. See[prior-art.md](prior-art.md).

## Independent operational labels and confusion matrix

W uses the same explicit-marker rule. All142 overlapping OAI source rows agree,
including all42 original draws. This is rule/scanner consistency, not142
independent dynamic validations.

For independent evidence we use M's retained no-M original-kernel per-declaration
CPU traces. Operational reference class: decision-shaped helper declarations
consume >=50% of that module's own kernel-call CPU. No source CPU denominator
or historical-M profile share is substituted. A helper's structural kind is
identified from its actual proof head; its cost is dynamically measured.
This definition is narrower than all possible large reductions: an expensive
rfl without a recognized decision proof head could escape it. It is not a
classification of producer elaboration/search/import cost dominance.

29 of the original42 draws have this dynamic observation;13 remain unknown.
The two additional purposeful hot modules(Grid,Amplitudes) stay separate.
Only this completed, selected panel is evaluated.

| Actual kernel-replay class | Predicted certificate | Predicted ordinary |
|---|---:|---:|
| Decision-helper CPU majority |14|1|
| Other |1|13|

Accuracy27/29=93.10%. A2000-resample project-block bootstrap over20 observed
source projects gives[77.78%,100%]. This conditional interval does not account
for the13 missing draws, whole-library label error, or observer perturbation;
it does not establish a population guarantee. No new model training occurred.

The two mistakes:
- ManuscriptNormLogPGroup006 has explicit markers, but helpers consume43.79%
  of original kernel-call CPU: a false positive under the >=50% definition.
- FixedCompactRow48 has no explicit marker, but its ordinary decide elaborates
  to decision helpers consuming61.67%: a false negative.

Their combined measured kernel-call CPU is1.028414s out of213.362303s,
a time-weighted error of0.4820%(conditional bootstrap[0%,3.4800%]).
Their corresponding source-compilation costs sum8.204648s out of602.627562s,
or1.3615% exposed source CPU. These denominators belong to distinct operations.
Neither is a measured extra cost caused by a wrong checker choice; obtaining
that causal penalty would require both checker routes on the misclassified
inputs. Do not describe all exposed work as removable wasted CPU.

Grid and Amplitudes both match the operational label. Adding them gives29/31
correct, but they dominate kernel CPU and were selected because they are hot.
They do not strengthen a random-sample prevalence or accuracy claim.
Sensitivity at25%/75% reference CPU thresholds is in
[classification-summary.csv](classification-summary.csv); the source rule is
unchanged rather than tuned to the dynamic outcomes. The single-project
purposeful subset has no meaningful project-bootstrap CI and its CI fields
are blank.

## Completed trace-based policy comparison

We have matched whole-closure serial/parallel cost pairs only for three
selected roots: Mathlib.Data.Nat.Basic(1330 modules), Barrier(4449) and
Grid(3793). They are whole checked artifact closures, not31 individual
source-compilation requests, and not alternative proofs of one theorem.
No speedup factor is imputed onto unmeasured module rows.

FIFO uses O's original serial kernel stream for every root. Type-route preserves
arrival order, checking the ordinary root serially and certificate roots through
M's qualified v14 four-worker original-kernel declaration waves. It does not
change proof terms or use chunk rewrites. Upper-admission adds a type-level
envelope: maximum previously observed whole-process CPU in that type/route.
It is a historical-workload limit on these same roots, not a calibrated unseen-
module bound. Prior compiler regression intervals are not reused.

All six root arrival orders and the three real Mathlib reference repetitions
give18 replay cases per budget/policy. The computational pairs each have only
one prior observation;18 cases are not18 native repetitions. The exact replay
table is[routing-replay.csv](routing-replay.csv).
Completed means a whole root request, not a partially accepted dependency.

| CPU budget | FIFO mean completed | Type-route | Upper-admission |
|---|---:|---:|---:|
|120s|0.333|0.333|1.000|
|600s|1.333|0.667|1.000|
|900s|1.667|1.667|2.000|
|1200s|3.000|1.667|2.000|

At120s, FIFO/type each interrupt one root, spending97.08CPU seconds on average
on the incomplete root. Upper admission interrupts none, finishes the ordinary
root and leaves51.24CPU seconds unused. At1200s, FIFO completes all three
without interruption, whereas type-route still interrupts one root on every
arrival and upper admission defers one. Parallel checking reduces wall on the
measured computational roots but raises aggregate CPU; under a fixed CPU-work
budget this can worsen completion count. A correct regime label is not a
sufficient algorithm-selection policy.

Replay wall for an interrupted root is unknown: we do not linearly scale a
completed whole-run wall by a CPU fraction. All replay ranges describe the
enumerated arrivals/Mathlib observations, not confidence about repeated native
computational runs. No semantic rejection is inferred from a budget cut.

## What the class label does not guarantee

The finite42-draw frame has27known correct labels,2known errors and13unknown
dynamic outcomes. Without assumptions about those missing outcomes, its
unweighted accuracy can range from27/42=64.29% to40/42=95.24%.
Missing runtime weights prevent a corresponding nontrivial whole-frame CPU
error bound. The93.10% is conditional accuracy, not filled-in population truth.

| Root closure | Serial CPU / wall s | Selected type-route CPU / wall s |
|---|---:|---:|
|math|68.756 / 68.800|68.756 / 68.800|
|barrier|474.582 / 474.851|591.467 / 304.862|
|grid|557.350 / 557.568|744.406 / 296.293|

These completed-process cost sums are 1100.688CPU seconds for all-serial
versus1404.629 for type-route(+27.61%).
Summed process wall falls39.16%
(1101.218->669.955s), but this is a sum of prior completed cells,
not an additional measured continuous batch or service makespan.
The observed wall/CPU tradeoff explains why the fixed-CPU replay can be worse
despite faster computational checking. It cannot be described as CPU saved.

Nor is the ordinary class a proof that parallel checking is useless:
the existing Mathlib parallel4 matrix has a47.60s median wall versus68.61s
serial, while using84.64s versus68.57s median CPU. A regime label does not by
itself identify the wall-optimal or CPU-optimal checker; the policy objective
and actual dependency graph still matter. No firstness claim for such routing
follows from high classification accuracy.

## Upper admission's transfer limit

The type-level upper envelope is deliberately calibrated from previous
observations of the same roots. It is an availability control for recurrent
known work, not evidence that class membership alone bounds unseen work.
A leave-one-cohort-out calculation exposes the gap: using only Barrier's
591.47CPU seconds underestimates Grid's744.41s; using Grid covers Barrier.
There is no other ordinary cohort to calibrate a held-out Mathlib upper limit.
Thus the only two computational transfer cases have1/2coverage, and the
ordinary case has no finite bound. These tiny counts are diagnostic, not a
coverage estimate.[Exact transfer table](class-envelope-transfer.csv).
No numerical regression is fitted to repair this. In particular, avoiding
interruptions in the coming known-root experiment cannot be advertised as
a certified unseen-module admission bound.

## Native matrix currently collecting

[classification-plan.md](classification-plan.md) fixes three cyclic arrivals,
rotated policy execution order,120CPU seconds per policy, and three repetitions.
P0–7/flock/no-M, external11.5GiB child memory plus512MiB driver reserve.
It consumes the same actual artifacts with original-kernel serial or qualified
four-worker checking. Upper envelopes are frozen before execution.
Queue wait, source production, and offline feature computation are outside
this artifact-checking budget and stay explicit.

The120s point deliberately allows the ordinary closure but not either whole
computational closure in the retained completed pairs. It is an availability
diagnostic for rejecting work that does not fit, not a representative mixed
service or a general speedup. Native per-root interruption work, actual budget
excess, unused budget, completed IDs and partial dependency acceptances are
separate. Pass@k>1 remains unidentifiable from these distinct reference roots.

Raw input/features/traces and the finite native matrix are on the existing PVC:
/workspaces/.agent-state/gpu-smt-captures/cost-classification-20261101.
Falconer remains active and unchanged; the new bounded matrix joins the shared
P-core FIFO lock behind the existing holder. Its completion is not assumed here.
