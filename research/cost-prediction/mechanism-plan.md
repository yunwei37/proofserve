# Mixed-request regime routing: frozen trace-driven feasibility protocol

2026-11-01UTC, O line, self-review. This supports current RQ2/RQ3:
does selecting a checking operation by a source regime help under CPU budgets?
Positive evidence would support a limited mechanism; negative evidence favors
streaming alone. No regression, new checker, production engine or paper rewrite.

## Scope and measured operations
Use only completed closures with all three actual costs available: Mathlib
Data.Nat.Basic and OAI PlanarPacking.Grid. Barrier lacks complete source-build
CPU; NearPin and Amplitudes lack a qualified matching parallel-closure pair.
Do not impute their costs. Successful original-kernel accept sets are already
qualified on these inputs. Source build sums all actual per-module compiler
user+system CPU, not summed wall, and requests normal olean/ilean/C outputs.
Streams consume the same constructed proof artifacts; parallel is qualified
M v14 uniform4 replay, no proof rewrite. Store all cost sources and input IDs.

This is a trace-driven mixed-request systems feasibility experiment, not new
native batch throughput. The user's permission to use measured costs does not
make replays native repetitions. No new Lean process or timing/profile is run:
untimed analysis uses E8, below12GiB, and leaves the P-core lock to active owners.
All original measured costs are no-M/P0–7 points. Old memory caps and measured
peaks remain disclosed; no new12GiB native qualification is invented.

Requests provide source AND already-produced artifacts, and ask for validation.
Build is current-practice redundant construction with additional outputs;
stream/parallel only validate the artifacts. It is not a source-only replacement
that avoids generating proofs for free. No cache hit, shared-prefix saving,
production of artifacts, queue overhead or zero-cost cancellation is invented.

## Fixed matrix
20 independent fresh-root requests/batch; no exact-result cache, despite repeated
templates. Certificate proportions0/0.1/0.5/0.9/1; request CPU budgets100/800/
10000seconds and total budgets1000/5000/20000seconds. The top request tier
allows BOTH checker modes AND construction on both templates; lower tiers
intentionally expose admission tradeoffs. Three fixed seeds20261101..03.
Use each seed's matching actual Mathlib reference/parallel4 repeat; computational
checking/build costs have only one qualified measured pair/source construction.
Report variation across arrival/noise/Mathlib observations, not a population CI.

Four main policies keep the SAME FIFO order:
1. all_build: stock source construction for every request;
2. all_stream: serial original-kernel stream for every request;
3. classified: predicted ordinary->stream, predicted certificate->parallel4;
4. classified_upper: same actual mode choice plus class-level upper admission.
An explicitly separate all_stream_upper component control tests whether any
benefit needs checker selection rather than admission alone.

The fixed source classifier correctly labels these two selected templates.
That is NOT the earlier29-module93.1% validation. Uniformly flip exactly0/2/4
of20 labels (0/10/20%) using the same seeded batches for every policy; preserve
positions and which true class was flipped. Do not infer robustness from the
earlier0.48% weighted exposure. No incorrect classification changes proof truth.

Upper bounds are frozen maxima of prior observed CPU within each predicted
class/selected route (ordinary stream or certificate parallel4). For the
all_stream_upper control, use the serial-stream class maxima. These are
same-template historical envelopes, not certified new-module bounds. Noise
can make a bound wrong. No upper estimate is supplied to all_build/all_stream.

For each request, allowed work=min(remaining total CPU, request CPU budget).
A completed actual-cost cell counts as a passed validation. Otherwise charge
the entire allowed work, count an operational interruption and discarded CPU,
then continue FIFO if total budget remains. Admission skips/defer before
execution when its upper exceeds allowed work; never calls the proof false.
At zero total budget, remaining requests are unattempted, not zero-CPU failures.
Continuous CPU replay has no integer-RLIMIT artifacts; previous native cuts
stay unchanged. Interrupted wall is unknown, never scaled from completed wall.

Metrics: completed/passed count, pass decisions/presented and pass decisions/
attempted, operational interruptions, discarded CPU, unused CPU and actual CPU.
Report mean/min/max over the3 batches at every setting, plus paired changes
under noise and versus all_stream. No candidate pass@k from unrelated roots.
Keep partial/deferred/unattempted outcomes separate. Completed service wall
may be summed; a full batch wall/makespan exists only with zero interruptions.
No source timestamps or old phase fractions are borrowed.

## Interpretation
Classification may identify work but not make parallel checking CPU efficient.
A false negative can even improve CPU-limited completion when streaming costs
less CPU. Report that rather than calling every flip a loss. The component
control must prevent assigning all admission gains to mode selection.
SATzilla2012 already has cost-sensitive classification; this is Lean-specific
mechanism feasibility, not novelty of routing or a deployable product.
Raw data on existing PVC; only authored code/small summary CSVs in this directory.
Falconer and other healthy native captures remain unchanged.
