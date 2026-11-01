# Post-math native continuation

Self-review, planned native qualification. Existing captures and binaries are
unchanged; new source is AuditedStream.lean. boundary-controls.py is a finite
control run queued through the existing P-core lock after observed waiters.
It uses an outer11.75GiB native cgroup, leaving256MiB for O-line parents, and a
1,500s outer timeout. Every child has its own timeout; no -M is used.

Five sibling-module cases compare module-local replay, naive union and the
audited/context-separating adapter:
1. Same-name, same typed proof: accept in all modes.
2. Corrupt second proof under an existing theorem name: local/audited reject;
   naive replay's theorem-skip behavior is expected to accept.
3. A proof referring to a preceding but unimported sibling constant:
   local/audited reject, naive union is expected to accept.
4. Two individually valid different definitions under one public full name:
   local/audited accept; naive union is expected to reject the second.
5. Same private surface helper names in separate modules: accept.

These are **predictions**, not observed results until native compilation and
the raw qualified.json exist. Compilation failure, timeout, crash or absent
reject event is not a successful negative control. The driver checks native
events and statuses, not only expected nonzero exit codes.

The adapter compares actual typed declaration fields, audits used constant
references against transitive source-module visibility, and sends a conflicting
module and its dependents to module-local replay. It never changes a context
conflict into mathematical rejection. A run with fallback is explicitly
**segmented**, not a single shared environment. This implementation needs
native controls and real-library differential qualification; no proof of
universal context equivalence or performance is claimed by this design note.

Optional DECOUPLED_MEMORY_PROFILE checkpoints report smaps_rollup every100
modules(default; configurable). These must be a separately identified
profiling run. Primary timing leaves checkpoints disabled.

plan-falconer.py consumes a stock external-artifact manifest and the pinned
complete Falconer source graph. It adds implicit Init for the AI source
modules, requires unique existing source paths for every closure member and
writes a dependency-ordered source frame. Final compiled imports must equal
that plan; an absent source, failed construction or typed-context fallback is
reported, not hidden. The script is currently source-prepared; the external
native graph and full-project timing have not run.

At preparation the shared PVC had12.77GB free. A second full Mathlib/source
reconstruction may not fit alongside all lines' active artifacts. No foreign
files were cleaned and no storage setting changed. The next native manifest
will determine the exact closure; artifact-size estimates and available space
must be recorded before starting that construction. Existing small compiled
Falconer/NearPin artifacts are not substituted for the full2,461-module test.

The complete Grid source build has now actually exited0: target-only compiler
wall318.230852s, user385.855286s, system105.437298s, peak RSS7,940,196KiB,
no cgroup OOM. This is a **target production component**, not a complete
closure ratio; its matched-artifact stream and module-local parity must still
finish. Shared Mathlib dependency construction is reported separately in the
existing cohort tables. A target near-one ratio and a smaller whole-closure
ratio can coexist because the latter amortizes mathematical dependencies.
No expected Grid or Amplitudes ratio is filled in.
