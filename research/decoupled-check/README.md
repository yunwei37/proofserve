# Decoupling native kernel verification from proof construction

This O-line experiment tests the user's two-cost-regime characterization:
ordinary mathematical proof production versus computational certificates.
It does not assume that a 2% sampled C++ share implies a 50x realizable speedup.

## Complete Falconer mathematical closure (2026-11-02)

[Paper-ready Falconer result](falconer-paper-result.md): **13,205 modules,
27 checkpointed processes, 2,043.59 / 22,077.77 s = 9.26%**. Snapshot export
and certified-prefix import are included; acceptance set and import graph
match the complete original module-local reference. Matched checkpointed
Mathlib is14.67%; historical unsegmented Mathlib is10.56%. These are serial
native process work ratios, not service throughput or parallel Lake latency.
[Recomputed evidence](falconer-paper-evidence.json) · [comparison CSV](falconer-paper-table.csv).

## Whole-library direct measurement (started 2026-11-02)

[Plan](whole-library-plan.md) · [actual progress](whole-library-progress.md) ·
[coverage](whole-library-coverage.csv) · [initial typed-input availability](whole-library-input-availability.csv).
All163097pinned source files are restored on PVC. Only2469have initial matching
compiled terms; missing terms require separately recorded source production.
The resumable500-new-module checker uses the qualified original kernel and
bounded P-core tasks. No full-library CPU cost or validation of extrapolation
is claimed before actual complete coverage. The source and dependency coverage,
failed launches, source errors/censors, kernel outcomes and memory failures
remain explicit. Snapshots enable restart but do not shrink imported state.

## Implementation and trust
StreamCheck.lean reads original Lean 4.34.1 olean parts, recursively visits
imports in dependency order, and calls the stock Kernel.Environment.replay.
There is one initially empty checked environment for the entire process.
No imported environment is finalized in stream mode; no tactics, persistent
tactic extensions or external checker are executed. Raw module data contain
extension entries, but stream mode ignores those entries and reads declarations.
Mapped regions remain alive while their kernel terms are referenced.

The upstream replay policy skips unsafe and partial constants; the adapter
counts and reports these. Constructors/recursors receive upstream generated-form
checks, and axioms retain Lean's normal meaning. This is kernel eligibility,
not a new no-sorry/axiom policy or a parser-hardening claim. Only the original
Lean kernel accepts mathematical declarations; nanoda/lean4lean are not in TCB.
The artifact reader has the same well-formed olean assumption as leanchecker.

The one mode mirrors bundled leanchecker: create the target's imported
environment and replay target declarations. It is a correctness oracle,
not the implementation of streaming. Stock leanchecker itself additionally
qualifies the thirteen-module preflight acceptance set.

## Real functional qualification (no timing data)
E-core controls already completed:
- Entire Init.Data.Nat.Basic closure: 13/13 module acceptances equal stock
  leanchecker, 5,317 declaration entries, 58 upstream-ineligible entries.
- Three distinct real theorems receive deliberately invalid proof terms
  (loose variable, nonexistent constant, wrong sort). Stream and per-module
  oracle both reject all three. These are in-memory copies, not edits to originals.
- Entire Mathlib.Data.Nat.Basic closure: 1,330 modules, 132,484 entries,
  2,269 upstream-ineligible entries, native process exit0.
These are interface/correctness qualifications, not measured speed results.
All controls use an outer 12GiB cgroup and timeout; no Lean -M option.

## Comparison plan and self-review
Primary control: same source dependency closure produced by the stock 4.34.1
compiler, one native compiler invocation per module in dependency order,
including that invocation's imports, elaboration/tactics, kernel checks and
standard olean/ilean/C artifacts. The fixed compiler/toolchain is reused; this
does not rebuild the C++ compiler executable. It is a serial native compiler
work comparison, not default parallel Lake project wall time.
Every closure node must have a successful measured source build before a
complete-closure ratio is reported. No multiplication of a leaf time or
borrowed historical denominator fills a missing dependency.

Report whole-closure total wall, user/system CPU and memory; additionally report
module replay/read/map times and production work for predeclared ordinary
targets versus computational targets. Shared dependency work remains explicit.
Use one process per streamed closure/union so all its dependencies are checked
once; do not relabel target-only replay as complete verification.
Source/compiler flags and cache/artifact state are retained in native command logs.
Incomplete build windows, timeouts, OOMs, rejection and missing sources remain
separate; no cost ratio is imputed for incomplete closures.

The experimental role is decisive for whether validation can be substantially
cheaper than production. A small ratio supports the cost separation; a large
ratio or rejection of valid modules challenges that interpretation. Both remain
reportable. The source and initial qualification receive self-review only.

## Resources and queue
All timed/profiling runs require taskset 0-7 plus the existing shared
/workspaces/.agent-state/gpu-smt-captures/pcore.lock. Observe /proc/locks before
submission and join behind existing waiters. Preparation stays on E cores.
No timing invocation uses -M. Native processes enter a temporary cgroup under
this Workspace's existing Pod; memory.max and memory.events are recorded.
No host sysctl, modules, other pods or parent limits change.
Each native process and each locked window has a finite timeout. Outputs,
failed compilation attempts and original raw data stay on the existing PVC:
 /workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031 .
Only adapters, small CSVs and analysis enter this directory.

## Source references
- [4.34.1 kernel replay](https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Replay.lean)
- [Bundled checker](https://github.com/leanprover/lean4/blob/v4.34.1/src/LeanChecker.lean)
- [Module regions and environment](https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Environment.lean)

## First actual P-core stream observation
Mathlib.Data.Nat.Basic complete closure: 1330 modules,
132484 declaration entries; native exit0.
Wall 65.964395s, user 65.736833s,
system 0.200969s; wait4 maximum RSS
0.698GiB. Cgroup peak charged memory is separately
79.055GiB; shared file pages can be charged to
another preexisting group, so cgroup memory.peak is not a physical RSS estimate.
Read/map/replay module timer sums are 0.089605/
0.055303/65.688288s.
There is no complete source-build denominator yet. No stream/build ratio is
claimed at this checkpoint. Standard compiler reconstruction of the exact
dependency graph is active, with output artifacts isolated from original data.
Cgroup child memory.max is 11.875GiB, reserving128MiB for the small O parent
inside the12GiB allocation. No Lean -M flag is present.

## Matched artifact requirement
The first 65.964s stream run reads the retained original compiled inputs and is
an observed control. Primary stream/build ratios will instead replay the exact
new artifacts emitted by the measured source reconstruction. This avoids
assuming regenerated proof terms are identical to a distributed cache.
A matched-stream acceptance graph must equal the planned complete closure.
Every module of that newly produced closure is also checked by the
source-equivalent single-module oracle. Bounded chunks retain per-module
acceptances and never reuse a checked kernel environment across modules.
The stock CLI 13-module preflight separately qualifies that oracle. A timeout
or missing acceptance is not a native rejection or parity success.
Large target compiler invocations begin only in a window with their full
declared per-module budget available; partial windows do not silently shrink
the Grid/Amplitudes bounds.

## Source construction completed for the first cohort
All1,330 Mathlib.Data.Nat.Basic closure members have successful measured standard
compiler artifacts, with 622.379412s summed native subprocess wall. This is a
complete source-closure denominator; the original-cache 65.964395s check is
still a separate input control until regenerated artifacts are rechecked.
The union frame comprises5,085 source modules (no missing source), including
both PlanarPacking computational roots and the ordinary NearPinDeletion root.
Later cohorts include their actually measured member costs; shared dependencies
are measured once, not replaced by a guessed average or a leaf-only denominator.

## Bounded continuation
Each locked window is internally1,680s and externally1,740s; every native child
has a timeout and its own temporary cgroup. The finite coordinator waits for
actual exit, reduces/publishes small result tables, checks /proc/locks, then
joins the back of any existing queue for the next window. It stops on a real
cell error or its eight-hour continuation bound, preserving partials. That is
a capture bound, not a research deadline. It creates no schedule, service,
new agent or alternative Workspace. Successful already-built artifacts are
never overwritten; matched oracle records may cover the same immutable module
in multiple enclosing closures. Old cached-input oracle data are retained
separately and do not fill the matched-input acceptance set.

Oracle chunks contribute acceptance parity only when the whole native chunk
exits0 and its accepted module set exactly matches its requested set.
Any stdout prefix from a timeout, OOM or crash stays raw evidence and never
counts toward parity. The completed first mathematical cohort contains no
such records, so this qualification clarification changes none of its results.
Current native capture code stays loaded; the next bounded window uses this rule.

Resume writes preserve old stdout/stderr and commands by allocating an attempt
suffix; incomplete compiler artifacts are moved to an owned raw backup before
retry. Successful constructed modules remain immutable. Progress updates use
fsync plus atomic replacement, so a container interruption cannot truncate the
only checkpoint. Original native attempts and their elapsed costs stay recorded.
The active window keeps its loaded code; later windows use these resume rules.

## Falconer recovery, 2026-11-02

All 13,205 source nodes are built. Full checker attempts at 1,500s did not
complete. [Diagnosis](falconer-interruption-20261102.md),
[recovery cost records](falconer-recovery-costs.csv),
[checkpoint protocol and native controls](falconer-checkpoint-plan.md),
[segmented current result](falconer-segmented-result.md),
[original module-local parity](falconer-parity-progress.md).
Both complete segmented checking and the original module-local reference are
now observed. The [paper-ready result](falconer-paper-result.md) supersedes
the earlier incomplete status. The final reducer is falconer-finalize.py
--reduce-only; no unfinished prefix is extrapolated.
[The 17 vs14.33 admission control explanation](admission-control-reconciliation.md)
is a separate completed reconciliation.


## 2026-11-02 cleanup and producer correction

[Cleanup record](cleanup-20261102.md) retires regenerable certified snapshot
intermediates and duplicate extracted sources; all native commands/results/logs
and original typed proof inputs remain. Old snapshot-restoration audits require
regenerating the retired deltas; their historical measured costs remain valid.
[Whole-library source diagnosis](whole-library-source-errors.md) identifies
a producer/SDK configuration defect. Its9124errors and151485blocked modules
are not proof-rejection counts. The whole-library point is partial coverage.
