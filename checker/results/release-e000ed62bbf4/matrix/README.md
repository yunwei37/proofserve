# Frozen ProofServe release evaluation

Native checker: e000ed62bbf4b9c420bd99d0273a5d21829b4edc. Original driver: cc5bcc18c87d7bf85afc5e71a6738f06da52c03d.

The six-hour native matrix window ended on 2026-11-06 at 11:13 UTC. All 30 primary scaling runs, 12 persistence/split-fallback ablation runs, and three Nat.Basic strict runs completed. The original 71-cell plan is **incomplete**: 61 attempts returned, including one strict Grid timeout and one official sample cut off by the overall window; 10 cells were not run. No incomplete observation is used as a successful timing.

The native checker and its behavior were not changed. Two finite collector continuations retained completed cells and the original deadline. Their exact code and the between-cell handoff record are included here. The current official cell completed before the second collector was replaced while waiting for the lease; no measured native process was interrupted by that change.

## Conditions and scope

These are prebuilt-artifact checks on phobos-vt, an Intel Core i9-14900K. Every measured native cgroup was restricted to P cores 0–7; preparation and decoding used E cores 8–9. All timing used the shared blocking P-core lease and no Lean -M. Every returned native process and cgroup was confirmed retired; M observed the lease free before export. Release preflight began at 05:08:28 UTC, before the native matrix budget began around 05:13 UTC. Terminal bookkeeping finished at 11:13:18.576 UTC. Preflight and final export are outside individual native cell costs.

No heavy compilation remained in the study Workspace. The user-required zettai-dev workload remained running; about one host P-core of background work was observed before launch. These results do **not** establish exclusively idle-host performance. The raw legacy label quiet final release evaluation is qualified by this observation.

Lean is 4.34.1; openai/math is 4eaee87548250b2682affda7d05d947c05554bae, with Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612 and [W's recorded compatibility changes](../../../../data/openai-math-4eaee875/census/README.md). Inputs come from W's completed canonical artifact view. The abandoned 2026-11-05 launch is retained separately and contributes no timings.

| Label | Requested root | Accepted dependency-closure modules |
| --- | --- | ---: |
| Nat.Basic | Mathlib.Data.Nat.Basic | 1,330 |
| Grid | OAI.Analysis.PlanarPacking.Grid | 3,793 |
| Barrier | OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41 | 4,449 |

Nat.Basic is **not all of Mathlib**. These closures overlap, so their module counts must not be added as distinct coverage. Each performance run used a fresh checkpoint directory. Barrier's worker points were reduced to 1 and 8 in the prepared six-hour plan; 2 and 4 were never planned here.

## Native scaling

Each row is three complete repeats. Time is seconds, shown as median [minimum, maximum]. CPU is the closed native cgroup's whole-tree CPU, including descendants. The per-attempt CSV retains wait4 CPU for audit. RSS is the largest sampled own-tree sum among the repeats; it differs from cgroup memory charges and from the single-child ru_maxrss field.

| Closure | Workers | Wall seconds | CPU seconds | Max sampled tree GiB | Wall speedup vs 1 worker |
| --- | ---: | --- | --- | ---: | ---: |
| Nat.Basic | 1 | 110.809 [110.707, 111.171] | 110.246 [110.128, 110.300] | 2.689 | 1.000× |
| Nat.Basic | 2 | 82.725 [82.712, 82.918] | 111.288 [111.283, 111.480] | 1.751 | 1.339× |
| Nat.Basic | 4 | 69.693 [69.630, 69.803] | 112.127 [111.952, 112.263] | 1.755 | 1.590× |
| Nat.Basic | 8 | 65.312 [65.175, 65.526] | 113.455 [113.125, 113.514] | 1.753 | 1.697× |
| Grid | 1 | 753.992 [752.735, 755.379] | 751.162 [750.176, 751.554] | 3.550 | 1.000× |
| Grid | 2 | 517.290 [509.165, 517.913] | 778.643 [765.573, 779.560] | 3.550 | 1.458× |
| Grid | 4 | 398.372 [392.905, 398.828] | 799.129 [791.240, 804.478] | 3.553 | 1.893× |
| Grid | 8 | 352.349 [348.067, 361.103] | 835.761 [827.466, 836.815] | 3.552 | 2.140× |
| Barrier | 1 | 735.591 [734.357, 739.654] | 732.639 [731.514, 735.912] | 3.931 | 1.000× |
| Barrier | 8 | 425.906 [421.291, 426.295] | 766.344 [762.113, 766.690] | 4.522 | 1.727× |

The 1-to-8-worker wall speedups are 1.697×, 2.140×, and 1.727×. These are within-tool comparisons with the same per-input proof ledger, not speedups over the official checker.

## Native 8-worker ablations and strict policy

| Closure | Configuration | Wall seconds | CPU seconds | Wall/default-8 | CPU/default-8 |
| --- | --- | --- | --- | ---: | ---: |
| Nat.Basic | no-persistence | 67.485 [67.460, 67.546] | 127.203 [126.960, 127.509] | 1.033× | 1.121× |
| Nat.Basic | no-split-fallback | 78.367 [78.302, 78.531] | 111.885 [111.704, 111.980] | 1.200× | 0.986× |
| Nat.Basic | strict-theorem-bodies | 276.053 [275.957, 276.236] | 283.782 [283.607, 283.927] | 4.227× | 2.501× |
| Grid | no-persistence | 370.712 [370.284, 374.913] | 976.802 [976.474, 1005.622] | 1.052× | 1.169× |
| Grid | no-split-fallback | 396.080 [395.604, 398.570] | 824.353 [823.531, 828.128] | 1.124× | 0.986× |

Strict Grid repeat 1 returned 124 after 1,800.010 wall seconds, with 1,803.564 closed-cgroup CPU seconds. It was not an original-kernel rejection and produced no complete acceptance receipt. Its two remaining repeats were not run. There is **no strict Grid median or completed-run slowdown estimate**. The successful Nat.Basic strict policy costs 4.227× wall and 2.501× CPU relative to default 8 workers.

Default shared-checked and strict theorem-body policies retain the documented semantic difference for crafted artifacts. See [the native checker trust boundary](../../../README.md) and [the policy qualification](../../theorem-body-policy/README.md). These honest-artifact controls do not establish universal agreement on malformed artifacts.

## Official CLI controls

All nine completed official samples accepted their requested root. The table lists successful samples individually. Only Nat.Basic default completed all three repeats. Blank medians in the official CSV mean the three-repeat requirement was not met; they are not observations to impute.

| Closure | Mode | Complete/planned | Successful wall seconds | Successful CPU seconds |
| --- | --- | ---: | --- | --- |
| Nat.Basic | default | 3/3 | 407.290, 407.817, 409.090 | 407.107, 407.816, 409.035 |
| Nat.Basic | fresh | 2/3 | 477.848, 478.941 | 477.646, 478.852 |
| Grid | default | 1/3 | 667.452 | 667.214 |
| Grid | fresh | 1/3 | 1004.122 | 1003.813 |
| Barrier | default | 1/3 | 458.908 | 458.858 |
| Barrier | fresh | 1/3 | 927.109 | 926.663 |

Nat.Basic default wall median is 407.817 s [407.290, 409.090], and CPU median is 407.816 s [407.107, 409.035]. Its third fresh sample was stopped after 77.704 s by the remaining overall budget, not by its own 1,800 s cell cap. Grid and Barrier each completed one sample per mode; their remaining repeats were not reached.

These are **not equivalent whole-ledger speed baselines**. Lean 4.34.1 LeanChecker.lean first enumerates .olean files over the complete search path. Default mode then replays the target module into trusted imports. Fresh mode replays the final imported constant map into an empty environment; it does not preserve every module-local proof body that the per-input ledger checks. Grid and Barrier also require the already-qualified canonical path alias for the stock CLI's symlink-resolving module discovery; exact roots are in context.json.

The measurements include stock CLI search/discovery, Lake startup, imports and checking. Nat.Basic default repeat 1 charged about 340.6 s in system mode and 66.5 s in user mode. The release harness's one-time artifact-binding preflight is outside per-cell native timings. No ratio between these different ledgers and discovery procedures is presented as ProofServe's independent-checking speedup. Official whole-ledger acceptance equivalence is **not established** by root exit codes.

## Acceptance, bad proofs, and actual interruption

Across all 45 complete fixed native points and the resumed point, the reducer verified exact equality within each dataset of input artifact identities, accepted module lists, reported axiom lists, and module-set hashes. The reported axiom inventory contains 15 declarations in every closure, including sorryAx and compiler/runtime axioms. This is a declaration inventory, **not** a minimal used-axiom closure or a certificate that all theorems are sorry-free; the presence of a declaration does not prove that a theorem uses it.

All three existing real-prefix controls (bvar, unknown, sort) returned 2 with original-kernel rejection messages. Excerpts are in bad-controls.json; full raw streams remain on PVC. These are functional controls, not an independent runtime review.

The deliberate interruption killed the native tree after its first certified segment. Resume accepted the same 1,330 modules with the same input identities, axiom inventory and module hash, and reused one segment. Combined interruption plus resume cost was 81.501 wall seconds and 124.106 CPU seconds. Uninterrupted 4-worker medians were 69.693 wall and 112.127 CPU seconds: this one interruption cost 16.94% additional wall and 10.68% additional CPU. The killed parent's wait4 CPU was only 0.002 s, while its closed cgroup recorded 78.233 s; the latter is included in these totals.

## Incomplete cells and handoff

The planned-status CSV lists all 71 original cells. The two cutoff attempts and charged costs are in fixed-failed-attempts.csv. Strict Grid repeats 2–3 and eight Grid/Barrier official repeats were not run. No old preview, zero, partial prefix or historical strict result fills those cells.

The raw collector records collection_failed when its finite budget is exhausted. The separate verified handoff marks all returned native cgroups retired and the lease returned while keeping original-matrix completion false. The checker was not changed or refrozen. Export verification is self-review (自审), not a new independent review.

After O's external timings, the prepared built-subset command is:

```sh
taskset -c 8-9 python3 /workspaces/.agent-state/gpu-smt-captures/checker-built-subset-cc5bcc18/run-built-subset.py
```

It has **not been launched**. Inputs use W commit cc5bcc18: 162,170 built source modules, 926 deferred source modules excluded, plus one uncharged lakefile configuration unit excluded. The unbuilt OAI umbrella is not requested. The source frame is 163,096 source modules, or 163,097 units including that configuration file. A complete check of the built subset is not a whole-source-corpus check. Invocation remains manual after the coordinator hands back O's timing stage; no automatic corpus job is queued.

## Files and provenance

- fixed-cells.csv: all 61 physical attempts, closed-cgroup CPU, user/system split, wall, memory, result class and exact native commit.
- fixed-native-summary.csv: only the 15 fully repeated native groups, preserving prepared reducer column names. The incomplete-native CSV holds strict Grid with no imputed median.
- fixed-official-summary.csv, official-replayed-modules.json, fixed-resume.json, fixed-acceptance.json and bad-controls.json: scoped summaries, observed stock module names and assertions.
- context.json, frozen-source.json and collection-terminal.json: versions, hardware, background, input frame, finite-window deviations and retirement evidence.
- reduce-returned.py and collector continuations: exact small analysis/collection code. These are historical experiment scripts, not installed checker entry points.
- partial-cells.csv: the original 40-row first-stop export, retained for provenance. Use fixed-cells.csv for the final collection.
- built-subset-plan.json and run-built-subset.py.txt: prepared input selection and an archival runner copy, not a completed corpus result. Execute only the cited original PVC command, not archived scripts from this Git directory.

Original, failed and partial raw logs, receipts, segments and command records remain on PVC:

```text
/workspaces/.agent-state/gpu-smt-captures/checker-final-e000ed62-20261106T050828/matrix
```

Native binary, snapshots and large artifacts are not committed. Context notes qualify raw legacy labels and the last eligible census segment. The source-corpus cost remains a lower bound from W's measured subset; these checker results make no total-cost extrapolation.
