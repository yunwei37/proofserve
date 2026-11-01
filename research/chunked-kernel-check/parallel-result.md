# BarrierData41: declaration-level original-kernel curve

The original task actually ran and finished. Its absence at03:32UTC was
retirement, not evidence of failed/nonblocking lock admission. The launch used
blocking flock without -n. Raw first-command file time is02:53:11UTC and
terminal file time03:01:30UTC on2026-11-01. File timestamps are provenance,
not additional performance clocks. No second Barrier task was started.

## Complete observed curve
Three repetitions per setting, exact same original compiled artifact and trusted
imports, original Lean4.34.1 C++ kernel. All timing P0–7 under pcore.lock,
no-M, native memory scope14GiB within M16GiB.

| Setting | Whole pipeline wall median [min,max],s | Native CPU median,s |
|---|---:|---:|
| Direct official serial replay |46.992 [46.813,47.151]|46.956|
| Wave1worker |53.321 [53.159,53.939]|53.205|
| Wave2workers |31.072 [30.884,32.892]|54.556|
| Wave4workers |20.233 [20.158,20.342]|58.335|
| Wave8workers |14.127 [13.989,14.359]|60.016|

Eight-worker wall speedup versus the **direct stock baseline** is3.326x by
ratio of medians (paired ratios3.284–3.359x). Native CPU increases27.8%.
Wave-k1 is13.5%slower than direct stock; comparing only wave1with wave8would
overstate gain. All import, process, graph, standard export/reimport and final
audit costs are included in whole-wall clocks. Native CPU excludes the small
Python driver's CPU; interstage wall is separately tabulated.

The dominant ready frontier contains1099declarations and had44.646s of
independently measured serial checker-call CPU. In this new8worker curve its
whole stage costs7.361s wall and51.190s CPU (medians). Other waves, planning
and final audit contribute substantial fixed work; per-stage medians need
not sum exactly to whole-cell medians. See parallel-stage-summary.csv.

## Correctness and limits
15/15cells accept. Each compares all3425original typed ConstantInfo values,
including3313theorem types and proof bodies plus112definitions, and the
original name-array order.99actual native stage receipts returned0, no
resource stop; all native children/cgroups and the old controller retired.
Maximum sampled own-tree RSS3,131,117,568bytes; maximum charged child
peak526,700,544bytes. These accounting measures differ and are not hard RSS
quota claims.

Only stock kernel replay adds declarations. Checked worker environments export
ordinary Lean modules; successor waves import them normally. No unchecked
environment union, temporary proof axioms, replacement kernel or changed
original proof terms. The complete target is never imported before its checks.
Imported dependencies remain trusted as in stock single-module leanchecker.
The first-wave prototype supports ordinary acyclic declarations only.
Within-wave physical insertion and fragment layout differ; final typed/name
audit is exact. Artifact byte equality across worker counts is not claimed.

This establishes a positive **single-module independent replay** result.
It does not measure source elaboration, a whole library, a warm verification
service, an aggregate heartbeat-transparent request, or novelty of parallel
proof checking. No1swithin-goal split was applied to Barrier's subsecond goals.

Raw point:
 /workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check/parallel-barrier-v1

Next: the separately measured6.163s Envelope Fin31 helper is eligible for
within-goal range splitting. Its sole next task was submitted with blocking
flock at03:35:08UTC; /proc/locks explicitly shows PID216219 as a -> waiter.
No Envelope acceptance or speed result follows from queue admission.
