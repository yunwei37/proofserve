# Fresh SubexponentialSAT replay on the repaired checker

The public proofserve-check executable from native source commit
e0c92d51ab0faf24f1c7ac64323d5ea2f2e4575d completed a fresh 14,721-module retained
closure. This is development qualification on E cores, not a final performance
measurement or a release freeze.

## Invocation and scope

The run used Linux on phobos-vt, CPUs 17–23, two kernel workers, Lean 4.34.1,
a 40 GiB maximum for the owned native tree, and an 8 GiB node-available-memory
stop condition. No P-core lease or Lean -M was used. The original 3,977 requested
roots and artifact search path were retained; a new, initially nonexistent
checkpoint directory was used. The input project is the retained Lake wrapper
over O's compiled artifacts, not a newly built public project.

All nine batches and 38 segment records were newly generated. No old successful
checkpoint was reused. Completed dependencies were shared within this fresh
invocation through the repaired ABI 3 / independent-closures-v5 path.

The result has 14,721 accepted module names and zero rejected modules.
module_check_entries is 14,720. The remaining module is the compiled-empty
parent: its imports were checked first and its combined context then passed the
original importer and empty replay. trusted_import_entries is 86,150 across
batches; these are repeated import entries, not extra unique proofs.

## Acceptance and declared axioms

| Reference | Modules compared | Acceptance differences | Modules without that reference | Axiom comparison |
|---|---:|---:|---:|---|
| Previous checker result, now superseded | 14,721 | 0 | 0 | Same 15 names |
| O's complete stream, 30 raw segments | 14,721 | 0 | 0 | Not recorded |
| O's partial module-local original-kernel references | 14,401 | 0 | 320 | Not compared |

The old checker is a historical consistency comparison, not a validity oracle:
its certificate logic was defective. O's module-local references are not a
completed 14,721-invocation official CLI ledger. Their raw outputs, successful
exits, accepted IDs and retained artifact links were revalidated. The 320
unreferenced modules are unknown under that reference, not mismatches or failures.

All 36,209 recorded input paths and their 64-bit hashes equal the old recorded
union, including the empty parent. The repaired checker also validated the
current complete part inventory. This is ordinary file-identity evidence; these
noncryptographic hashes cannot resist deliberately constructed collisions.

The declared axiom names are:

~~~text
Classical.choice
Lean.ofReduceBool
Lean.ofReduceNat
Lean.trustCompiler
Quot.lcInv
Quot.sound
isScalarObj
lcAny
lcCast
lcErased
lcProof
lcUnreachable
lcVoid
propext
sorryAx
~~~

This is a declared-axiom set for the accepted closure, not a minimal dependency
set for each theorem. It includes sorryAx and Lean.trustCompiler, so acceptance
is not an axiom-free claim. O's stream contains no axiom field; its absence was
checked across all 30 raw outputs and is not reported as an empty axiom set.

## Resource observations — preview only

| Metric | Value |
|---|---:|
| Wall time, complete fresh invocation | 5784.790577 s |
| CPU, complete owned cgroup | 6948.353055 s |
| CPU reported by the native receipt | 6948.257081 s |
| Sampled sum of native process RSS | 26.112801 GiB |
| wait4 maximum single-process RSS across descendants | 25.884964 GiB |
| Charged cgroup memory peak | 19.921318 GiB |
| Complete batches | 9 |

RSS was sampled once per second and can miss a transient peak. The metrics are
different accounting methods, not additive memory quantities. No memory,
node-reserve, disk or OOM stop occurred. The prior resumed checker run had a
26.062 GiB sampled tree peak and a 25.864 GiB wait4 peak. O's historical stream
had a 14.731 GiB wait4 peak. These implementations, freshness and resource points
differ; the observations do not establish a memory-saving ratio or an isolated
performance comparison.

An observation channel exited during the run. The original controller's
PID/birth and native group were verified still live, and the original run was
preserved. It subsequently wrote its real complete terminal record. No
derived terminal was needed, no native process was restarted, and no interrupted
clocks were added together. The controller, native processes and cgroup have
all retired.

## Review and remaining work

The coordinator (Claude) read the e0c92d51 Main.lean diff and the repair's case
results, summary and runner adaptations. That reading added no adversarial
tests and is not an independent review. O's session was stopped by the model
provider's content filter; the repaired checker has no completed independent
code review. Result inspection here is 自审.

This fresh run supersedes the old 14,721-module correctness qualification.
The old raw results remain intact and their defective-source status remains
explicit. The checker is not frozen. Independent review, an actual quiet
final evaluation and the rest of the release requirements remain pending.
No full-corpus check or final matrix was started.

Raw receipts, the accepted-set list, all input identities, native outputs,
memory samples, reference reductions, executable and source snapshots remain at:
/workspaces/.agent-state/gpu-smt-captures/checker-subexp-fixed-e0c92d51-20261104.
