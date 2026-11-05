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

## Historical preparation driver (superseded for closeout)

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
