# e0c92d51 review repair: qualified source checkpoint

Scope: M lane, checker/ plus the unchanged supplied packaging review. This is a
correctness repair, not a release freeze or final performance measurement.

## EXPERIMENT

The immutable e0 binary reproduced the input-shadowing, segregated-axiom,
identical-definition, unsafe-reference, nonzero-exit and coverage defects listed
in results/e0-review-repair/README.md. Negative and unconfirmed controls are
kept distinct. build10 passed the full local contract and the review fixture
runner, with no fixture timeout or resource stop. Exact commands and guard
results are retained on the capture PVC.

The original O replay and the old-binary explicit native-evaluation control
remain pending at this checkpoint. The 14,721-module repair replay has not
started. No corpus or final matrix was launched.

## WRITE

README, current version qualification, large-library trust documentation and
receipt schema now explain explicit snapshot resolution, complete input-part
binding, executable identity, event/exit validation, per-module evidence,
revision provenance, editable local certificates and native-evaluation refusal.
Historical e0 and earlier results remain historical.

## REVIEW

Implementation review and native result inspection are 自审. The supplied
independent review read e0 source only; it did not execute this repair.
PrivateConflict actual and identical variants agree with both official modes.
The native route deliberately refuses terms requiring project IR and does not
silently execute them through the official path. General malformed-artifact
equivalence and the low-severity Quot/body hypotheses are not claimed proved.

## Next required boundary

Finish original O controls; inspect any expectation changes explicitly. Then
commit-bound fresh SubexponentialSAT replay, comparing acceptance and axioms to
historical and available O references. Coordinator review and release freeze
remain outside this checkpoint.

## Engineering reflection

Calling the original kernel is insufficient if the importer selects different
bytes from the receipt's input scan, or if the coordinator trusts the wrong
terminal signal. This repair therefore qualified input selection, publication
and scope before the large replay. Fixture assumptions about artifact parts
were checked against both official modes instead of silently weakening the
expectation. Preserve failed fixtures on the PVC and distinguish module-entry
counts from actual kernel calls. Final performance must use a later agreed
binary after correctness qualification; these E-core controls do not supply it.


## Completed qualification boundary

The original O controls have been replayed with explicit disclosure of the
incomplete-module-part precondition change. The old explicit-IR control still
refuses unknown printBool and did not print a forged worker event. The fresh
3fe83c5a / build10 replay returned 0 at 19:03:16 UTC, accepted all 14,721
retained modules, reported the same 15 axioms, and retired without resource
stops. All 36,209 input-path/hash pairs match the retained frame. O's full
stream and 14,401 available module-local references match; 320 references are
unavailable. Exact comparison and preview resources are in
results/e0-review-repair/subexp-fresh-3fe83c5a/. The focused added-part inventory
control then passed, with no concurrent native replay.

PrivateConflict's ten rows agree with both official modes. Actual full/read-only
mount-namespace controls refuse publication, retain a parseable old receipt and
emit no complete stdout. CI 41860036796 actually passed the existing full
contract; its 87 review command records predate the three focused added-part
records now added to the same CI entry point. All failures and controls remain
separate from successful native samples. No final timing or full corpus was run.

The repair is not frozen. Independent execution review remains pending.
Kernel invocation alone is not an end-to-end guarantee: selected bytes, the
declared importer context, a nonzero child exit, publication success and root
coverage must all agree before accepting. The now-complete real replay
confirms this retained input frame; it does not prove every malformed-artifact
edge or make editable local certificates untrusted proofs.

Final CI at 1f80c14a completed successfully: engine 41894137393,
benchmark-smoke 41894137395, and all 90 review-runner command records.
Native core source remains 3fe83c5a. This is mechanical execution, not
independent review or release freeze.
