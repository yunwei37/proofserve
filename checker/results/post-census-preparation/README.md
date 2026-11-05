# Post-census preparation (not final performance)

The native checker remains frozen at e000ed62. Only the evaluation scripts,
their tests and workflow documentation changed. The two launch commands and
phase boundaries are in ../../docs/release-evaluation.md. No formal matrix,
whole-corpus check or P-core lease was started in this preparation step.

## Matrix budget

The planned matrix has 71 attempts. Nat.Basic and Grid retain their full
1/2/4/8-worker three-repeat matrices, both 8-worker ablations and new
8-worker strict-policy three-repeat points. Barrier retains 1 and 8 workers
with three repeats; only its 2 and 4 points were cut. Official controls,
three bad proofs and actual interruption/resume are retained.

matrix-plan.csv gives every planning component. The selected plan estimates
4.78 hours, or 5.74 hours with 20% reserve. The uncut plan would be 6.38 hours
with reserve. Hardware/load conversion and official-cost proxies are stated
in each row. None of those estimates substitutes for a measured release point.

## Corpus planning

corpus-cost-plan.json is a read-only snapshot taken while W continued:
59,335 completed sources out of 163,097. Its lexical computational stratum
has 4,110 completed sources, with 169,203 seconds of compiler user CPU.
The frame contains 5,848 such sources. Applying the selected-module
75–94% kernel-user fraction to that stratum gives a conditional 50.2–62.9
CPU-hour kernel component. Adding the static repeated-loading envelope gives
a very broad 119.9–322.6 CPU-hour planning range.

This is deliberately not an observed checker total. The source order is
biased; compiler CPU differs from checker CPU; P/E costs differ; the loading
envelope may double-count proof work. Refresh the model after W finishes.
No all-core wall-time claim is derived from these CPU sums.

OAI is a separate compiled-empty capacity test. If its actual original import
context cannot complete, it stays pending while other source-backed requests
run. The original 163,097 denominator is preserved, including unavailable
build artifacts and any further incomplete checks. Only the corpus-check
phase may end partially; W's source traversal must finish.

## Actual small-root qualification

qualification.json records actual CPU 8–9, no lease, <=12 GiB controls.
The three-module fixture uses Base/Fixture/All and 3,000 tiny theorem bodies.
The matrix's dataset labels select workflow routes; they are not real
Nat.Basic, Grid or Barrier measurements. Current-driver matrix and corpus
commands both returned. The actual signal-interrupted corpus exposed one
checked checkpoint source, no currently validated whole-run verdict, and
resumed to all three sources with identical accepted and axiom sets.

A real launch failure (126) is retained in qualification1 and explicit retry
completed. The final native matrix rejects all three kernel mutation controls;
its killed-prefix resume reuses a certified segment. Seven offline driver
tests passed. No independent execution review was requested or performed.

The SIGTERM control first exposed a guard bookkeeping defect: the old finally
path reaped the child without recording its exit/retirement fields.
qualification2 preserves that failure. The corrected guard records the
signal-time wait result, and qualification3/4 completed the real interruption
and resume. Original failed runs remain on the PVC.

Raw path:

    /workspaces/.agent-state/gpu-smt-captures/checker-post-census-preparation-20261105

Qualification ran before the driver commit; its exact source snapshots remain
in each phase's frozen/bench directory. Native provenance is e000ed62.
Final execution refuses uncommitted driver sources and records its separate
driver commit. This is implementation-lane self-review, not independent
runtime qualification of the release.

## Retry-directory follow-up

A focused harness control first failed because an interrupted-leg retry wrote
a fresh state directory but the resume leg still selected its original path.
The driver now reads the actual interrupted row's state_directory. The
red/green control retains both failed attempts and checks the resume target.
Both portable driver-control suites run from the existing native CI contract.
This changes no native checker input or proof verdict. The normal-flow native
qualification above is retained; the follow-up is a harness regression,
not a repeated timing or new native measurement.
