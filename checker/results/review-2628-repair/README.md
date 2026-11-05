# Repair of the second code-only review (2628d727)

The supplied [review](../../../packaging/checker-review-2628d727.md) is preserved
unchanged. It read code only. The executions and source inspection here are
implementation self-review (自审), not independent execution review.

All local runs used E cores 8–9, a 12 GiB own-tree budget and the node's 8 GiB
reserve. They used no Lean -M and no P-core lock. W's full build was untouched.
These are correctness controls under background load, not paper performance
measurements. No 14,721-module replay, full-library check or final matrix was run.

## IR validation lifetime follow-up

Post-push self-inspection found a resource defect in our newly added IR
validation path: dropping the return value from readModuleDataParts does not
free its compacted regions. A short control left two file mappings after
16 discarded reads. The repair uses the public CompactedRegion.free operation
in reverse dependency order. A non-inlined reader first drops all ModuleData
references and returns only owned region handles.

The short regression now covers both ownership states: validation alone returns
from zero file mappings to zero after each read; a different owner's live data
retains its two mappings and remains readable while validation allocates and
releases separate regions. It does not alter kernel checking, receipt shape or
artifact acceptance policy. Its evidence concerns region lifetime, not a
measured whole-library memory saving or speedup.

The first combined wiring of this new regression chose a non-module Base
fixture, which has no IR signature, and failed during setup. The regression
now runs on the existing module-system IRBase fixture that actually emits both
parts. That setup failure remains retained as final-contract7.

The initial 981d544d commit's automatic engine and benchmark-smoke CI both
completed successfully, including the combined 90/108-command contract.
That success did not exercise this new lifetime property. The follow-up's
[qualification record](ir-lifetime-followup.json) binds its fixed build5 binary
to the source blobs. The complete final-contract8 entry returned 0: the core
contract, all earlier 90 command records and all new 109 command records passed.
All 198 common command outcomes retain equal exits, status, accepted/rejected
module sets and declared axiom sets. The added record is the ownership control.
See [final-records.csv](final-records.csv) and [ir-lifetime.csv](ir-lifetime.csv).
The counts are commands, not distinct bugs or proofs. The measured mapping
prefix includes both .ir.sig and .ir.

The complete local entry sampled about 2.40 GiB peak own-tree RSS, had no
resource stop and retired its processes and cgroup. It ran under the same
12 GiB / CPU 8–9 correctness constraints. Follow-up automatic CI is pending
at this commit. Earlier build4 evidence below remains historical.

## What was confirmed and changed

| Finding | Actual confirmation | Repair and result |
|---|---|---|
| 1 | Unsafe PrivateConflictC passed old native but failed both stock modes. Partial C already failed. | Track skipped unsafe/partial names across live, restored and certified contexts. All five roots and batched checks now match stock acceptance. |
| 2 | Honest SDK WellFounded/Acc computation failed old native; swapping the two theorem bodies produced old native acceptance despite both stock modes rejecting. | Isolate different theorem bodies and validate shared failures in the original module context. Honest D passes; swapped D rejects. Cached-context control accepts D and rejects ZBroken. |
| 3 | Open bridge mention and unrelated same-named helper roots were wrongly refused. Actual primitive evaluation passes stock default but fails fresh. | Scope labels to actual imports and permit direct open mentions. Closed/higher-order evaluation remains unsupported. The official path now exposes the actual fresh result and exit status. |
| 4 | Missing/corrupt dependency IR passed old native and failed both stock modes. | Read IR through the original artifact reader and bind its presence/bytes. Both inputs now fail operationally with 2, never complete. |
| 5 | Incompatible empty context returned 1 or 2 depending on grouping. | Both groupings now return rejected/1, matching stock. No failed empty context receives acceptance evidence. |
| 6 | Old M occurred in both accepted and rejected. | Accept only after successful path handling; failed combined insertion cannot revoke successful local replay. M now passes like stock and the sets are disjoint. |
| 7 | Default state output made a clean repository report dirty. | Exclude only active untracked checkpoint output. Clean is false; a real source edit remains true. |
| 8 | Axiom-tagged Quot records failed stock and plain old native but passed after old checkpoint restore. | Require primitive quotient tags and matching names. Both malformed native paths now refuse with 2; the genuine quotient control still passes. |
| 9 | Escaped explicit root passed, default discovery failed. | Construct Lean names from path components. Both selections now pass. |
| 10 | Repeated segment allowance made no progress; an empty Leaf lacked context evidence. | Count new segments per invocation and inspect every batch root. Repetition progresses to complete and Leaf receives actual context evidence. |

[findings.csv](findings.csv) records each confirmation, repair and remaining limit.
[official-comparison.csv](official-comparison.csv) gives the 26 explicit oracle
rows, including unsafe and partial PrivateConflict, proof-body contexts, native
evaluation and both empty-context groupings.

The old cached-body control itself rejected D; it is not another confirmed
complete false acceptance. The swapped-body control is the confirmed false
acceptance for finding 2. The current cached-body assertion additionally requires
honest D to be accepted and the bad ZBroken root to be rejected.

## Initial build4 qualification and retained failures

The native binary is a fixed build4 copy. Its three modified Lean sources match
the saved build source byte for byte. [qualification.json](qualification.json)
records the actual receipt binary identity, toolchain, source Git blobs and
individual run boundaries. Child ABI 5 and independent-closures v7 invalidate
earlier state.

Local qualification is composed from the following actual executions:

- The core correctness contract and the earlier review's 90 command records
  passed in final-contract5. That whole invocation nevertheless exited 1 because
  the next fixture failed to compile; it is not labelled a complete suite pass.
- After adding the explicit Init.WFComputable compiler dependency,
  final-review6 returned 0 with all 108 command records and assertions complete.
- Original-binary context comparison returned 0 in observation mode with 15
  command records. It reproduced the honest false rejection, swapped-body false
  acceptance and accepted/rejected overlap. The two-command old empty-leaf
  comparison also completed.

Command records include builds, artifact mutations and official invocations;
90 and 108 are not counts of independent bugs or distinct mathematical proofs.
The CI entry is python3 checker/tests/contract.py. The initial local
qualification was explicitly partitioned above. The terminal 981d544d CI
snapshot is [ci-981d544d.json](ci-981d544d.json); it subsequently passed the
combined entry. The current lifetime follow-up has its own complete local run.

The initial combined attempt reached the earlier IR control's 600-second
self-limit while replaying an unnecessary implicit import of the whole Lean
library. It did not reach that control's final semantic assertion. The fixture
now explicitly imports only Init.Core / Init.System.IO and retains its original
printing implementation, proof mutation and non-acceptance assertion. The
earlier runner's success summary also now executes only after a successful run;
a finally-block count printed before an exception is not success.

A repair intermediate (build3, final-remainder3) wrongly accepted the closed
primitive-evaluation control. The check had used ConstantInfo.value? without
allowOpaque, so the theorem proof body was absent. The fixed check explicitly
includes theorem/opaque values. The final closed and higher-order controls
return unsupported/2. That failed intermediate is retained and never qualifies
the final source.

The first reduced WF fixture lacked its compiler support and failed to build.
Earlier custom accessibility-recursion proxies either failed to build or did
not reproduce body sensitivity; they do not replace the genuine SDK
WellFounded/Acc controls. An earlier source-only private-import attempt did not
create an import conflict. The actual empty-context control uses the existing
metadata-import mutation. These setup/negative outcomes remain separate from
semantic rejections.

Raw sources, binaries, generated artifacts, stdout/stderr, partial segments,
guard records and failed attempts remain on the PVC:

/workspaces/.agent-state/gpu-smt-captures/checker-review-2628-fix-20261104

[attempts.csv](attempts.csv) indexes the guarded attempts.
[baseline.csv](baseline.csv), [legacy.csv](legacy.csv) and
[repair.csv](repair.csv) index actual command outcomes. The final core/legacy,
new review and focused baseline runs retired their processes and cgroups, had
no memory/reserve stop, and sampled peaks below 2 GiB. Diagnostic run durations
are not performance comparisons.

To reproduce the combined contract with a matching Lean toolchain on Linux:

~~~sh
cd checker
lake build
python3 tests/contract.py
~~~

## Known limits and next boundary

Native IR refusal remains conservative: direct open mentions are supported,
but some passive higher-order uses can still be refused. Stock --fresh can
lack IR available to stock default, so --official is not a guaranteed escape.
Missing/corrupt inputs and malformed reserved quotient records use operational
2 while stock may use 1; no such row is accepted. See the explicit oracle table.

The quotient guard addresses the demonstrated declaration-tag/name mismatch,
not every possible forged quotInfo payload. Upstream may itself skip a redundant
imported theorem body with an equal interface. These controls do not establish
byte-for-byte checking of every redundant serialized proof or equivalence on
arbitrary malformed metadata.

Local certificates and partial checkpoints remain trusted editable state.
Manual certificate forgery and deliberately constructed 64-bit hash collisions
are outside their ordinary-change guarantee. A Git revision does not bind
source to built artifacts. This repair is qualified locally only on 4.34.1;
other version rows in the package README describe earlier source.

This source can be submitted as a freeze candidate after its automatic CI
contract passes. No freeze or release is performed here. The old 14,721-module
result belongs to source 3fe83c5a / ABI 4 and is not reused as ABI 5 qualification.
Its acceptance and 15 reported axioms must be rechecked after W retires, followed
by the already agreed full-library and final quiet-machine evaluation.
