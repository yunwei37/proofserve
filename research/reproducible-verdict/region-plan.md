# Computation versus mathematics, admitted comparison

M/B,2026-11-01UTC; preparation only; self-review.
Math side: actual16-source frontend matrix and raw allocation counter vectors
in the synchronous executing context, at fixed observer/budget.
Compute side:8actual stored decide-kernel proof objects from Grid and8from
EnvelopePsiB, lexicographically selected within the real defining module.
Replay each under a fresh name and original C++ checker against its imported
environment. Explicitly force proof inputs before measured unit; do not charge
shared preparation to whichever worker happens to arrive first.
Use1/2/4/8eager gated workers,2opposite-order repeats; record per-unit tid,
start/stop, raw allocation deltas, verdict. No unchecked insertion or newaxiom.
Counters bracket a noinline IO checkOutcome, forcing the pure kernel result
before reading the stop counter, to avoid lazy/hoisted timing artifacts.

This measures the verification stage, not source elaboration or a new independent
whole-candidate throughput baseline. It excludes imported-environment setup from
the unit counter; whole native resource/time includes it. Raw allocations are
not the separate native kernel poll counter, which remains null.
Matching counts would show conditional stability for prepared closed objects,
not that every computational source is inherently stable. Math stability has
also been observed in this selected sample, so math-only determinism cannot be
inferred even if the compute curve is stable.

Native source compile qualified. Runtime not yet launched; only v3task queued.
One bounded future task: all16cells,180s/native,1690scontroller/1740souter,
M14GiB sampled/charged limits plus reserve within16, no -M, commonP0-7lock.

The mathematical side also needs actual co-execution, not merely changing the
available thread pool while submitting one candidate at a time. The same future
finite task now includes MathBatchProbe:16sources x2budgets,1/2/4/8gated worker
loops,2reversed orders, shared imported base with fixed main module.
It preserves per-request result order and records actual TIDs. These are new
matched batch conditions, not pooled with v2sequential inputs. Source compilation
is first inside the future task; no extra Lean process started while v6queued.

Envelope selection explicitly includes the previously measured6.16s original
envelopeExpB16_calc._proof_1_1 target, plus7lexicographic decide-kernel objects.
Missing that exact stored name aborts instead of silently substituting tiny goals.
The kernel source has therefore changed before first execution; the future task
compile-checks it again before native runs. It remains prepared, not measured.
