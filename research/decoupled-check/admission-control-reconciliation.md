# Why all-stream admission completes 17 rather than 14.33

Self-review; this reconciles the frozen 5e2a73a replay, not a new native experiment.

Both controls retain FIFO arrival order. For each request:
`allowed = min(request CPU cap, remaining batch CPU)`.
An upper-admission policy defers when its calibrated
`upper[predicted_type, selected_mode] > allowed`. Deferral consumes zero CPU
in this ideal replay and is not rejection. Calibration is the maximum observed
CPU cost for that type/mode among the SAME two templates, not an unseen-input
guarantee. All-stream + admission still uses predicted type for the bound; it
is not a classification-free admission control.

- All-stream + admission selects serial replay for both types. Its math upper
  is 71.744430 CPU s; Grid upper is 557.349965 CPU s.
- Classification + admission selects serial for math, parallel4 for Grid.
  Its math upper is identical, but Grid upper is 744.406169 CPU s.
- Costs charged at completion are the actual input/mode measurement, not the
  upper. All modes use the same original kernel; no validity is guessed.

At 50% computation, per-request cap 10,000 CPU s and total 5,000 CPU s,
serial math costs 65.954551–71.744430 CPU s and serial Grid 557.349965;
parallel math costs 83.756762–85.665428 and parallel Grid 744.406169.
Parallel is cheaper in neither input's CPU-work objective. The classifier is
perfect in this zero-noise cell, so classification error cannot explain the loss.

Across the three paired batches the classified upper completes 13,15,15
(mean 14.3333), while the serial upper completes 17,17,17. Both have zero
interruptions and discarded CPU. Serial completes all 10 math plus 7 Grid in
each batch. Classified runs admit 7 math + 6 Grid, then 10 math + 5 Grid in
each of the other two. The higher Grid charge leaves less budget for the remaining requests;
no erroneous label or different FIFO order is needed to produce the loss.

The small CSV records exact per-batch work and deferrals. The frozen full
request traces remain on PVC at cost-mechanism-mixed-20261101-v2/requests.jsonl.
Repeated source closures represent synthetic independent requests with source
and existing artifacts provided; they are not 20 distinct observed candidates.
No wall-throughput, native cancellation or pass@k claim follows from this CPU
replay. Parallelism may reduce wall latency yet increase CPU work.

**Paper implication:** the measured CPU-budget benefit is serial verification
plus known-template admission. Selecting parallel recomputation by type has no
incremental completion benefit here; do not use 17 vs 14.33 as evidence for
class-selected checking, general admission guarantees or a shipped mechanism.
