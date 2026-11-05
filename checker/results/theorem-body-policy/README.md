# Replacement theorem-body policy and native freeze

The introducing commit of freeze.json is the new native freeze, replacing
e1557c77. Resolve its exact revision in any clone with:

    git log --diff-filter=A -1 --format=%H -- checker/results/theorem-body-policy/freeze.json

Git history is the authority for the containing commit. freeze.json binds its
seven native/build input blobs to the tested executable, avoiding an impossible
self-referential commit hash. No native behavior changes after these real runs.

## Reason checked and implementation

The coordinator's reasoning holds relative to the accepted shared closure and
its reported axioms, assuming the original kernel and existing adapter/local
checkpoint trust boundary. Retaining a checked proof of an identical theorem
interface does not add an axiom or disable kernel checking. A later statement
may be kernel-checkable in that shared environment while its serialized proof
fails in the module's original import context. Default checking now explicitly
allows that artifact-context difference.

One premise needed correction: upstream replay skips a duplicate same-interface
theorem body, so module-local replay alone does not ensure every distinct body
is checked. Local replay now explicitly checks skipped bodies under fresh
temporary theorem names, using the original imports and the module's replayed
declarations. The values and statement types are unchanged; temporary names
never enter the shared frontier and add no axiom. The unit control demonstrates
upstream skipping a malformed duplicate body, our direct check rejecting it,
and a valid copied body passing.

Default shared-checked retains the first body without automatically isolating
the whole module. Different interfaces, definition/unsafe/partial conflicts,
IR validation, input binding, receipt publication and certified-cache context
checks are preserved from e1557c77. A shared-path failure is confirmed by
original-context replay before rejection. Insertion failure after successful
local checking still accepts the honest module and isolates that context.

--strict-theorem-bodies preserves distinct-body isolation. Receipts identify
shared-checked, strict, or official-fresh. Policy is bound into single-frontier
and independent-closure identities, certificate identity/receipt consistency,
and the completed-import cache. Child ABI 6 and independent-closures v8 make
older state obsolete. Fresh state is required after the implementation change.

## Real default-mode closures

CPU 8–9, two workers, at most 12 GiB, no P-core lease and no Lean -M.
W's census continued; these are single-point functional/regression previews,
not paper performance data or a claim of an isolated causal CPU effect.

| Closure | Accepted | Axioms | Module-local replay | Segments | Wall s | CPU s | Peak tree GiB | Explicit duplicate body checks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| nat | 1330 | 15 | 49 | 3 | 155.45 | 187.00 | 1.725 | 33 |
| grid | 3793 | 15 | 157 | 8 | 1134.90 | 1507.06 | 3.593 | 34 |

Nat.Basic is the 1,330-module dependency closure, not the entire Mathlib library.
Grid is the 3,793-module dependency closure. Both acceptance and 15-name declared
axiom sets equal the prior 3fe reference and e155 replay. All 3,990 / 11,371
previous input identities still match. Full identities now additionally bind IR.
The module-local counts are exactly the 3fe counts, 49 and 157. Observed CPU is
1.019 and 1.007 times the reference; wall time is 1.040 and 1.068 times.
They remain background-load observations, not general throughput statistics.

closures.csv retains both older references and complete-segment CPU separately.
The e155 isolation strategy's historical cost is not a new strict-mode timing.
In particular, the new strict implementation also explicitly checks duplicate
bodies; it was not rerun on these large roots. The old Grid strict intervals
include an interrupted attempt and must not be called one continuous run.

## Official comparison and regressions

official-comparison.csv adds strict_proofserve to the 26 supplied oracle rows.
All 109 earlier common command exits and result sets were compared with the
new 142-record run. Only 2-crafted-body-native changes from reject to accept
by design; all 33 strict command exits equal their former behavior. There is
no other new default-accept / official-reject row in this supplied fixture set.
This is not a proof of parity for arbitrary malformed metadata.

The honest WellFounded computation still passes both modes; the cached distinct
body case still rejects ZBroken, preserving exact cached-context consistency.
The old 90-record review also passes with identical exit statuses. Both modes
exercise the original three malformed proof classes. Policy switching refuses
both ordinary and batched state. An authentic strict certificate copied into
an unchanged default directory is refused with exit 2; restoring it permits
valid resume.

qualification.json records actual boundaries: contract3 passed the core and
90 / 142 command suites; the subsequently added direct-kernel duplicate test
and authentic cross-policy regression were separately run as focused controls.
The pushed CI entry includes these controls together. All interpretation here
is self-review (自审). No independent execution review is claimed.

## Retained failures and evidence

The first focused attempt copied a binary without its executable mode and did
not reach verification. The next test harness accidentally reused the same
checkpoint directory for both policies and correctly received a configuration
error. The corrected harness uses separate directories. Both failed attempts
and intermediate sources remain on the PVC, not classified as mathematical
rejections. A noinline Unit-returning local helper drops temporary kernel
environments before freeing original import regions.

The first contract invocation did not request the old review's detailed JSON
file, although its owned fixtures and suite stdout were retained. Its 90 cases
were rerun with the existing row-output option for exact archival comparison.
No real closure was rerun for this record-only correction. All native groups
retired with no memory/reserve/OOM stop.

Raw directory:

/workspaces/.agent-state/gpu-smt-captures/checker-body-policy-20261105

Regenerate the closure tables with:

    python3 checker/results/theorem-body-policy/analyze.py RAW_DIRECTORY

## Remaining work

The native freeze supersedes the earlier e155 freeze; after it only real
defects justify native changes and affected results must be rerun. No tag or
release is created. Current qualification is Linux Lean 4.34.1. Existing FFI,
ABI-reader and trusted editable-checkpoint limitations remain; the 64-bit hashes
do not resist deliberate collisions or certificate edits.

W must finish its entire build census without an admission cutoff. After it
retires: final quiet-machine M matrix (at most six hours), O external timings
(at most two hours), then resumable corpus checking. Only the latter may report
partial coverage to meet the overall 2026-11-06 20:00 UTC target. The large ABI 6
recheck, corpus check, final performance and external release acceptance remain
unqualified. There is no separate PlanarPacking comparison.
