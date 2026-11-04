# Preview closeout and independent closure checking

Status: completed development step; full-corpus verification and final system evaluation remain pending.
Review: 自审, performed by the implementing M lane. No independent review is claimed.
Recorded UTC: 2026-11-04T04:51:25.513887+00:00

Only checker/ is changed. The latest direct instruction supersedes the older
continuous-research plan: productize the original-kernel checker, preserve the
loaded previews, release the P-core lease, and prepare full-corpus verification
while W owns the gate and census. Preparation runs use CPUs 8-9 only, no Lean -M,
and no new P-core task. The root-owned paper and other lanes' paths are unchanged.

## EXPERIMENT gate

Entry: the current direct user instruction, checker qualification and evaluation
plans, and the orchestrator's evidence requirements were checked. This gate
closes the already authorized finite preview and qualifies the necessary
large-library coordinator. It does not add another research experiment.

### E1. Close the finite preview

Question: did the shortened preview finish, and what can it support?
The frozen native executable is ba316991653155daedc9769c3058c166e83d79ce.
Raw evidence is at
/workspaces/.agent-state/gpu-smt-captures/checker-release-ba316991.

The terminal record contains 56 returned attempts. All 44 complete native
preview cells preserve their workload's input identities, ordered accepted
modules, declared axioms, and module-set hash. Three real-prefix malformed
proofs reach original-kernel rejection. Actual abrupt interruption and resume
preserve acceptance, axioms, and module hash, reusing one certified segment.
The controller and all native cgroups retired. The M P-core lease is released.

The once-only complete Mathlib scale attempt requested 8,529 directory modules
and the Mathlib umbrella. It accepted a 10,744-module dependency closure in
22 segments at 4 workers. Loaded wall time is 1,113.094 seconds; whole-cgroup
CPU is 1,860.421 seconds. Aggregate sampled RSS peaks at 7.575 GiB; charged
memory high water is 6.939 GiB. These different memory measurements are not
interchanged. No resource stop occurred.

Four Grid/Barrier official attempts failed before checking: the official
module-name enumeration resolves symlinks outside registered roots. Two
Nat.Basic official controls succeeded. A later metadata-only E-core control
confirms that appending the canonical root after the existing overlay exposes
the intended modules without changing artifact precedence. Corrected official
kernel replays remain pending.

The earlier controller boundary stops, failed launch without SDK configuration,
the abrupt interruption, and every partial record remain preserved. No new
Mathlib scale run is scheduled. All preview timings are ineligible for final
paper performance claims. The small reducer outputs are
[loaded-preview.md](../../loaded-preview.md),
[loaded-preview-cells.csv](../../loaded-preview-cells.csv), and
[loaded-preview-qualification.json](../../loaded-preview-qualification.json).
Whole-cgroup CPU, rather than incomplete wait4 accounting after abrupt death,
is used for retained costs.

### E2. Bound the live checked frontier

Question: can the checker stop retaining the union of every previous proof?
Independent batches invoke the same public native executable and recheck each
batch's complete actual import closure from an empty kernel environment. The
coordinator retains names, input identities, and completed receipts. It skips
later roots already covered. Only after an atomic complete-batch certificate
are that batch's generated snapshots retired. Interrupted batches retain their
partial checkpoints. Shared dependencies can be checked repeatedly: extra CPU
is an explicit cost, not an avoided or hidden check.

A root file avoids command-line length limits. Empty files are explicit errors.
The batch limit defaults to 500 requested roots; zero retains the old single
frontier. Local certificate identities are checked again on resume. A completed
global receipt requires every requested root in the accepted set.

The first real Nat.Basic / Int.Basic comparison yields the same 1,360 accepted
modules, axioms, and module hash as the single-frontier path. Resume reuses the
completed real certificate and skips the covered later root. A fresh current
coordinator control confirms parity after that optimization. These are untimed
CPU 8-9 correctness preparations, not final performance or full-corpus capacity.

Raw evidence:
 /workspaces/.agent-state/gpu-smt-captures/checker-closure-batches-20261104.
See [closure-batch-qualification.json](../../closure-batch-qualification.json)
and [large-library-checking.md](../../../docs/large-library-checking.md).
Earlier source and binary snapshots remain alongside their results.

### E3. Do not let an empty umbrella recreate the whole proof frontier

The pinned corpus has lean/OAI.lean. A module name only selects candidates for
inspection; actual most-private ModuleData must contain zero constants and
zero constant names before it can expand into imports. All imported proof
closures are checked first. The original upstream importer and empty replay
then validate the combined declared context.

Self-review found an essential boundary: separately valid imports can contain
conflicting definitions. Zero own declarations alone is insufficient. The
implementation now refuses an empty parent when its original combined import
context cannot load. This prevents an acceptance obtained solely by stitching
together independently valid but incompatible dependency receipts.

Portable controls cover three actual malformed serialized theorem bodies under
an empty parent, default namespace detection, stale-plan rejection, and an
empty parent importing incompatible definitions. Plain and expanded paths both
refuse the malformed inputs. Metadata inspection of the already checked
Mathlib umbrella finds zero own declarations and 8,533 actual imports; its input
hashes match the completed scale preview and every import appears in that
accepted closure. This is not another whole-Mathlib kernel run.

Build attempts 4 and 5 failed on Lean syntax/API issues and remain intact.
The final build-8 and contract-8 return zero, without resource stops. Both
native trees and temporary cgroups retired; their affinity is CPUs 8-9 and
measured is false. Their terminal paths are runs/build-8/result.json and
runs/contract-8/result.json. The latter includes correctness, official parity,
three bad proofs, axiom reporting, ordinary and batch resume, changed inputs,
root files, covered roots, empty umbrellas, imported bad proofs, and incompatible
import-context rejection.

This removes the global checked-proof frontier, not every large allocation.
The largest single dependency closure or combined original import context can
still exceed memory. Whole-corpus feasibility is not established.

Transition: functional qualification is sufficient to publish this development
step. W's full artifacts and build-context identities remain prerequisites for
the full run; no unbuilt or missing source unit is counted as verified.

## WRITE gate

Updated the public README, CLI integration notes, receipt schema, qualification
history, preview closeout, and final evaluation plan. The README separates
reader-facing behavior and trust from development chronology. Independent
closure and import-only receipt fields are additive schema-version-1 fields.

The corpus total counts source units. Full checking must join W's source
manifest to actual toolchain, manifest, search path, and artifacts; distinct
build contexts cannot be merged merely by bare module names. The future run
order is full-corpus checking, then a frozen quiet final matrix, official
controls, and the single PlanarPacking comparison.

The PlanarPacking plan identifies OAI.Analysis.PlanarPacking.Main and the
sharp_fourier_certificate proof. ComparatorChallenges.PlanarPacking is a
specification containing sorry and is not substituted for the proof. The
255,199 source occurrences are lexical sites, not executed checks or a measured
closure size. No new target timing was launched.

No paper text, scientific framing, research direction, external project record,
or other lane-owned path is changed. No new novelty or performance claim follows
from this preparation.

## REVIEW gate and disposition

The review is a same-thread self-review, not an independent audit. The required
second report records the checked evidence and limits. No extra agent or
external action was initiated.

The code path preserves original-kernel decisions; private FFI, the artifact
reader, and trusted local checkpoint state remain extra trust. Hashes detect
ordinary stale inputs rather than malicious tampering. Empty-context import
compatibility is checked by the upstream importer, not inferred by the planner.

Live observation during closeout confirms W's gate controller PID 149346 still
has birth 4507860 and state S. This does not establish gate success or a
completed census. There are no live M checker/contract processes. Disk use is
31%, below the user threshold. Preparation does not take W's CPUs or lock.

Ranked open items:
1. Join the full produced source/build-context manifest and check every intended
   unit after W's gate and census; record failures and actual memory.
2. Freeze the release executable and run the approved quiet matrix and corrected
   official controls, keeping proof-ledger scope differences explicit.
3. Run the single PlanarPacking pair and reference controls on that frozen tool.
4. O owns packaging, CI wiring, and external project acceptance; these are not
   established by this lane's local contract.

The implementation question is resolved enough to commit this coherent step.
The overall delivery remains in progress. No global completion or blocked state
is inferred from these development results.
