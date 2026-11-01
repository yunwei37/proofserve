# Decoupling native kernel verification from proof construction

This O-line experiment tests the user's two-cost-regime characterization:
ordinary mathematical proof production versus computational certificates.
It does not assume that a 2% sampled C++ share implies a 50x realizable speedup.

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
