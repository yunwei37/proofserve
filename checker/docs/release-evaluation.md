# Frozen post-census evaluation

> **The 2026-11-05 complete-census decision supersedes the historical driver
> below.** W must finish all requested build modules, with no admission deadline
> or partial-build closeout. Its configuration is unchanged. Keep W's P-core
> lease and CPU allocation until its actual controller and native jobs retire.
> M and other preparation use CPU 8–9 during that run.
>
> The next quiet-machine order is M's final matrix (at most six hours), O's
> external-project timings (at most two hours), then resumable corpus checking.
> To meet the 2026-11-06 20:00 UTC overall target, corpus checking alone may
> report partial coverage. Do not truncate W's census to meet that target.
> There is no separate PlanarPacking comparison.
>
> The old capacity-first all-in-one command is not the current launch procedure.
> Bind the completed W artifacts and the replacement frozen checker binary
> before final measurements. The e1557c77 freeze is superseded by the replacement freeze in
> results/theorem-body-policy/freeze.json; its historical preview timings
> cannot be reused as the new tool's final evaluation.

## 2026-11-05 operator stop

The user stopped W at 20:33 UTC: "别跑了, 现在的数据够吗".
The next final matrix may run after actual controller/cgroup retirement and
P-core lease release. The prepared configuration now names W's user-stop.json
and supervisor terminal. That explicit handoff permits a partial source frame;
it does not turn the stopped build into a complete census. Matrix roots still
use their actually available source-qualified artifacts. No missing corpus
cost is extrapolated, and there is no automatic build restart or corpus check.
The earlier complete-census requirement below is superseded by this decision.

## Current launch procedure

The native executable remains frozen at e000ed62. The driver checks the seven
native/build blobs in results/theorem-body-policy/freeze.json and copies the
already-qualified executable. It does not rebuild at the current HEAD.
Results record native and driver commits separately; each phase also freezes
its driver source on the PVC.

The prepared configuration is:

    /workspaces/.agent-state/gpu-smt-captures/checker-post-census-preparation-20261105/final.json

It selects W's actual 22-core census manifest, run/import-view, original Lake
project and run-config environment. The complete source traversal and retired
controller/cgroup are required. Explicit build failures and blocked dependents
are accounted for; unattempted work and a stopped census are refused. Missing
artifacts remain named in corpus coverage.

After W retires and the coordinator confirms the machine is quiet:

~~~sh
taskset -c 8-9 python3 checker/bench/release.py /workspaces/.agent-state/gpu-smt-captures/checker-post-census-preparation-20261105/final.json --phase matrix
~~~

The matrix takes the blocking P-core lease per native cell, binds it to CPUs
0–7, and returns at the end. O's external-project timings run next.
There is no automatic corpus queue. After O returns and releases its lease:

~~~sh
taskset -c 8-9 python3 checker/bench/release.py /workspaces/.agent-state/gpu-smt-captures/checker-post-census-preparation-20261105/final.json --phase corpus
~~~

Corpus checking takes the same lease and enables all 24 cores. It preserves
8 GiB of node-available memory and uses no Lean -M. It binds actual file
selection to W's source-qualified import view. It first checks capacity of
the compiled-empty OAI context. A nonempty umbrella cannot be excluded.
If the original empty-context check does not complete, OAI remains pending
while other source-backed roots run. Every other missing or rejected source
remains in the original denominator; subset success is not whole-frame success.

## Finite matrix and estimate

Nat.Basic and Grid keep 1, 2, 4 and 8 workers, three repetitions, both
8-worker ablations, and three 8-worker strict-policy runs. Barrier keeps
1 and 8 workers, three repetitions; only its 2- and 4-worker points are
omitted. All roots keep official default/fresh controls, followed by three
original-kernel bad proofs and real interruption/resume. The 71 planned
attempts have an accumulated six-hour budget, including archived failed
attempts. Failed attempts never enter successful-point medians.

The planning model in results/post-census-preparation/matrix-plan.csv predicts
17,225 seconds (4.78 hours), or 20,670 seconds (5.74 hours) with 20% reserve.
Keeping Barrier's middle points would give about 6.38 hours with that reserve.
These are planning values, not release measurements. Strict costs convert
historical E-core attempts using the observed default P2/E2 wall ratio, with
no further 8-worker gain assumed. Grid and Barrier official fresh costs use
native 1-worker proxies. All final points will use the frozen executable.

Nat.Basic is a 1,330-module dependency closure, not all of Mathlib. Grid has
3,793 retained modules and Barrier has 4,449. Acceptance, axioms, module hashes
and input identities are compared within each scope. Official default checks
a leaf with trusted imports; fresh replays a final imported map. The reducer
does not invent a whole-ledger speedup across these different scopes.

## Stop, retry and exports

Raw data and checkpoints remain on the configured PVC. Small exports go to
checker/results/release-e000ed62bbf4/matrix/ and corpus/. The driver never
commits, publishes or tags.

After inspecting a failure, use the same phase command with --retry-failed.
Matrix retries use fresh state and retain failed rows. Its intentional
interruption leg keeps the real certified prefix. Corpus retry preserves
batch certificates and native segment checkpoints and recovers the durable
result of a signal-interrupted attempt.

SIGTERM stops only the owned native cgroup. The corpus finally path writes
coverage even on interruption. checkpoint_accepted_source_units records
provisional trusted local progress; verified_source_units stays null until
this invocation revalidates the native result. A stale complete receipt
cannot make a failed invocation complete. Editable checkpoint metadata
remains trusted local state. Resume revalidates current artifact bytes.

The planning-only corpus estimate uses W's observed computational-stratum
CPU as well as ordinary-module and repeated-import costs. Its unfinished,
order-biased snapshot and assumptions are explicit in
results/post-census-preparation/corpus-cost-plan.json. Compiler CPU is not
checker CPU; refresh the estimate after W finishes.

Qualification uses CPUs 8–9, at most 12 GiB, no lease, and a three-module
portable fixture. It exercises both phase commands, strict/default routes,
official calls, failed-launch retry, bad proofs and actual signal/resume.
Its data are ineligible for final performance tables.

## Historical preparation driver (removed interface, retained provenance)

The following paragraphs describe the earlier qualified workflow. They are
retained for interpreting its records, not as the current launch instruction.

Run this historical workflow only after W has completed its gate and full build census,
released the P-core lease, and the machine is quiet. It is not a background
collector and never starts automatically. While a census is active, only qualification
mode is allowed, on its inherited E-core affinity without the P-core lease.

The workspace configuration at that preparation boundary was:

    /workspaces/.agent-state/gpu-smt-captures/checker-full-feasibility-20261104/final-release.json

This configuration points to the planned W output directory. Confirm the
actual terminal, launch and artifact paths from W's completed run before use;
the full census has not started at preparation time. The workflow requires
W's real complete terminal, retired controller identity and empty native
cgroup before it can start P-core work. It does not manufacture those records.

From the repository, the complete launch command is:

~~~sh
taskset -c 17-23 python3 checker/bench/release.py /workspaces/.agent-state/gpu-smt-captures/checker-full-feasibility-20261104/final-release.json
~~~

The command builds and freezes proofserve-check, records its commit, checker
source tree, toolchain and source snapshot, then checks capacity of the configured compiled-empty umbrella import context
before checking the full pinned source manifest. It next runs the fixed three-repeat matrix, official default/fresh
controls, bad proofs and interruption/resume. Finally it runs the real
PlanarPacking proof at default and 8 workers, with its official controls.

The full request comes from the 163,097-source manifest. It is not whatever
artifacts happen to exist. Every requested artifact must be present before
the whole check starts. The evaluated Lake search path must select those same
artifact files; a stale project-local build cannot silently replace a census
output. Missing or differently selected artifacts stop before whole checking.

The prepared run uses the existing matching Mathlib Lake environment with an
explicit overlay of W's pinned corpus artifacts and an explicit corpus root
file. It does not select Mathlib's default targets or pretend that its Git
revision is the corpus revision. Whole-coverage output keeps the source-frame
revision, Mathlib pin, original source root and actual execution project
separate. Distinct environments or colliding module names must be split into
separate explicit configurations.

## Resume and failure handling

Successful native segment and batch checkpoints remain reusable. A workflow
restart keeps the same frozen binary, even if other lanes have advanced HEAD.
It revalidates whole-check input identities before consuming an earlier whole
success. It never rebuilds a frozen binary in place.

A failed native attempt stops the workflow. Review the retained stderr,
receipt and resource observations, correct the real fault, then use:

~~~sh
python3 checker/bench/release.py CONFIG.json --retry-failed
~~~

Each retry gets a separate native result directory. Failed attempts remain in
the raw workflow and matrix ledgers, and are excluded explicitly from the
successful-point medians. The fixed matrix retains failed-cells.json and
exports a separate failure table. It does not silently turn an unsuccessful
attempt into a measurement. Native matrix performance retries use fresh state;
the actual interruption/resume leg retains its certified prefix.

Changing frozen tool inputs is not an operational retry. Use a new raw
directory for a changed toolchain, binary, manifest or configuration. A stale
artifact identity is an explicit failure. An unsupported official comparison
remains a failure with its scope visible, rather than an imputed speedup.

## Outputs and scope

Large raw records, native receipts and snapshots stay in the configured PVC
directory. Small tables go to checker/results/release-COMMIT/. CPU comes from
closed native cgroups, not incomplete wait4 accounting after killed parents.
The fixed matrix reduces its own guarded native cells; the outer matrix
coordinator is not treated as the timing of those cells.

The native full-check receipt identifies accepted modules and axioms. Official
default checks a leaf with trusted imports; official fresh replays a final
imported map. They are not an identical per-module proof ledger. No ratio is
invented across those scopes. The source census measures compiler production,
not independent checking.

--freeze-only prepares the exact binary and source record without starting the
workflow's checks. It reports workflow_complete=false.

For end-to-end interface qualification, mode=qualification uses a small portable
fixture, workers confined to the caller’s E-core affinity, no P-core lease, an explicit qualification memory budget and
an 8-GiB node-available stop. It runs reduced phase controls and exports only to
checker/results/workflow-qualification/. Its matrix/Planar phase names describe
workflow routes on the fixture; they are not Grid or PlanarPacking measurements.
No qualification value is eligible for the paper's final performance tables.

The configured OAI capacity preflight performs only original import and an
empty own-declaration replay. It cannot certify the imported proofs. Failure or
a memory stop prevents the whole-library phase and remains a recorded failure.
The current full-corpus capacity decision is open, even though the proof-replay
plan now avoids repeated shared proof checks.

The capacity helper receives the actual evaluated Lake search path, including
project dependency paths; it does not rely on the source manifest alone to
reconstruct those paths. Its successful output must identify the configured
compiled-empty module.

Current development qualification: the real portable end-to-end workflow
completed on a three-module fixture. Its frozen native and bench source is the
clean commit 2df1d9d7. One actual launch failure returned 126; its row remains
beside the successful explicit retry. Native checking, stock default/fresh calls,
and the fixture's final worker-route comparison returned. The nine rows and
terminal are in results/workflow-qualification/. No fixture value is a real
Grid, PlanarPacking or final system measurement.

The current preparation allocation is E17–23, with a maximum 40 GiB budget and
an 8 GiB node reserve. The driver inherits the taskset affinity and restores it
after future measured cells. Earlier CPU 8–9 / 16 GiB results retain their own
identity. If W is approved to start the full census, obey the updated allocation
before launching preparation. The capacity-first driver stops on failure; it
does not silently generate the conditional sidecar in large-library-checking.md.
