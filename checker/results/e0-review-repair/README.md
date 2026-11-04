# Repair of the code-only e0c92d51 review

This is untimed correctness qualification on E cores 10–23, not a frozen release,
a final performance matrix, or an independent execution review. The supplied
independent report is preserved unchanged in packaging/checker-review-e0c92d51.md.

## Confirmation before repair

The immutable e0 executable was run on small local fixtures. baseline.csv lists
the resulting observations; all raw outputs, failed development controls and
fixture projects are retained on the PVC at
/workspaces/.agent-state/gpu-smt-captures/checker-review-e0-fix-20261104.

| Finding | Actual pre-repair evidence |
|---|---|
| 1 | Plain segregated module accepted, but cheat missing from axioms. |
| 2 | State-directory good module hid the bad real artifact; project module named ProofServeSegment0 was hidden by a generated snapshot. Both completed incorrectly. |
| 3 | Identical imported axioms and the upstream PrivateConflict identical-definition variant were incorrectly accepted. Both official modes reject the combined module. |
| 4 | Bad non-module exported part was hidden by stale good private parts. Native and official default accepted; official --fresh rejected. |
| 5 | A saved complete segment with a nonzero exit was incorrectly accepted. The supplied printing-native-code fixture did NOT print a worker event and was rejected by e0; that IR route is not an empirically confirmed false acceptance. |
| 6 | An already-visited empty module was listed as context-checked without its actual empty-context invocation. |
| 7 | Safe proof borrowed an unsafe same-named constant from an unrelated sibling; official modes rejected while native completed. |
| 8 | Removing an accepted root event from saved trusted segment metadata still produced complete. The roots pending-write failure control tests checked publication; it is not a reproduction of real tmpfs truncation of the old roots writer. |
| 9 | Git dirty state was not reported. Entry counts lacked per-module fresh/reuse evidence and did not count kernel calls. |
| 10 | Prelude-only Quot checkpoint control agreed with both official modes. This proposed Quot counterexample was not confirmed. A malformed non-Prop theorem control and conservative duplicate handling are recorded separately. |

The metadata editing controls above isolate coordinator logic; they do not
change the declared assumption that local checkpoint metadata is trusted.
They must not be presented as tamper resistance.

## Historical SubexponentialSAT scope

The requested reason categories different_constant, unimported_reference and
segregated_dependency are absent from the retained original e0 segment output.
Its 60 fallbacks all have duplicate_proof_requires_native reasons. O's stream
has 64 such fallbacks and none of the requested three categories. The prior_2df
scan includes multiple retained development attempts and is not one clean run.
These observations do not establish that the historical 15-name axiom list
was incomplete. The fresh repair run below still reports exactly those 15 names.

## Qualification status

The complete local contract passed using build10. Its review fixture runner
returned 87 command records, including builds, mutations and official commands;
these are not 87 independent defect classes. There were no fixture timeouts.
All ten PrivateConflict rows agree with both official modes, including the
identical-definition variant. The malformed non-Prop theorem and Quot controls
are recorded without claiming the proposed low-severity counterexamples were
reproduced. The native IR fixture is explicitly refused with an operational
diagnostic, not accepted or silently executed.

The contract's sampled process-tree peak was 3.063 GiB, without a resource stop.
Its raw stdout and guard result are included. The regression runner is invoked
by checker/tests/contract.py, the existing CI entry point.

The original O base and edge modes completed. The original extended mode
stopped at its assumption that an isModule input without required server/private
parts can obtain a good certificate. Native now explicitly refuses that
incomplete input, as official --fresh does. Official default accepts its
exported-only input; default and fresh are not interchangeable oracles here.
The transparent adapter records that precondition change and then executes the
unchanged filesystem and private-axiom controls. O-cases.csv includes every
observation, including the original stopped mode. It is not an assertion that
the previous 42 required rows passed unchanged.

The explicit old-e0 native-reduction fixture also refused: its original
interpreter reports unknown declaration printBool. It did not print a fake
worker event. This remains an unconfirmed route, unlike the reproduced
complete/nonzero dominance bug. The new native refusal is an explicit boundary
on project IR evaluation, not proof that an old IR false acceptance occurred.

No repaired full-closure result or independent review is claimed at this
checkpoint. The fresh repair replay is active; final result files will identify
its actual terminal outcome. Original e0 and earlier qualification are retained
as historical evidence; they cannot establish the repaired binary's behavior.

## Development failures retained

Build4–6 contain syntax failures; build7–10 logs identify the subsequent source
boundaries. The first contract attempts exposed fixture assumptions about
incomplete module-system parts and about which write was reached. These were
corrected by using complete good parts before changing the private proof, and
an independent ordinary input for final-receipt ENOSPC. Expected refusal was
not weakened to accept incomplete or invalid artifacts.

Contract4 was explicitly stopped after its event log established excessive
quarantine of normal SDK theorem interfaces. It is partial, not a complete
sample. The later build checks repeated proof bodies in their original context
while retaining split fallback for new declarations; definition/axiom conflicts
remain isolated. All raw guard and event records are on the PVC.

Contract1 and contract2 used the old test harness's automatic temporary-fixture
cleanup. Their stdout, stderr and guard records remain, but those generated
fixture directories do not. From contract3 onward explicit PVC work directories
preserve the fixtures too. No formal corpus or final timing data were generated
in these attempts. This qualification and result inspection are 自审.

## Original O replay interpretation

Thirty base observations, four edge observations, the original extended mode's
stopped precondition, and seven transparent-adapter observations are retained.
Some names repeat and two deliberate local-certificate edits remain observations
outside the guarantee; they must not be counted as independent passing tests.
In particular, forged-missing-axioms still demonstrates trusted editable state.

Actual ENOSPC and read-only private mount-namespace controls each have native
exit 2, no complete stdout and a parseable prior receipt. Their outer namespace
control exits 0; that outer code is not the native verification verdict.
The private-axiom replay and reuse sets match each other and the original
axiom oracle. Wrong Lean identity, receipt version, child ABI, authentic foreign
state, changed dependencies and partial publication are still refused.

The four original added-part observations after the incomplete seed could not
execute unchanged, because no certificate is issued for that seed now. The CI
contract instead starts from complete good module parts, changes the private
proof, and checks refusal and original-kernel rejection. A focused added-part
presence-inventory regression now passes as well: a valid ordinary seed gains
an optional bad private part without changing its exported artifact or certificate.
Resume returns 2, emits no complete stdout, reports the changed inventory, and
leaves the certificate unchanged. It ran only after the full replay retired.
The three new command records join the existing CI entry point; the previously
completed 87-command CI did not yet contain this additional control.

CI run 41860036796 at cdf86d68 includes unchanged checker source from 3fe83c5a.
Its checker-contract job actually completed successfully and its log contains
the 87-command review runner. Rust and native-repl jobs also succeeded. This is
mechanical execution evidence, not independent review or a scientific result.

## Completed retained-frame replay

The new fresh point is
/workspaces/.agent-state/gpu-smt-captures/checker-subexp-review-repair-3fe83c5a-20261104.
It uses unchanged build10 / source 3fe83c5a, two workers, E cores 10–23,
a fresh checkpoint directory and the same 3,977-root / 14,721-module input
frame. launch.json records exact controller PID/birth; verify live identity,
not an old running flag. The guard retains the 40 GiB maximum and node reserve.
It completed at 2026-11-04T19:03:16Z: 14,721 accepted, zero rejected,
15 unchanged axioms, sampled tree peak 29.810 GiB, no resource stop.
The 36,209 input-path/hash pairs match the old frame. Acceptance agrees with
O\'s full stream and all 14,401 available module-local references; 320 remain
unavailable. See the linked fresh result for exact reference scopes and preview
CPU/wall values. No final timing, whole-corpus completion or freeze is implied.
