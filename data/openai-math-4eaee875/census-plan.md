# Native compilation census: qualification first

**Gate completed and failed; the full census remains unstarted.** The result
is below; the gate never starts a census automatically.
The 2026-11-04 instruction replaces the proposed E-first/P-later launch and all
E/P conversion. All 163,097 source files are present. Precision sampling is
permanently superseded (7/12 returned); all partial/original records are retained.

## Frozen candidate protocol

openai/math 4eaee87548250b2682affda7d05d947c05554bae,
Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612, Lean 4.34.1.
Per module: lean --root=<source-root> -j8 -DautoImplicit=false
-o <module.olean> -i <module.ilean> -c <module.c> <source.lean>;
LEAN_NUM_THREADS=8, no -M, unchanged authored heartbeats.
These are the original 42 samples' compiler settings and three output kinds.
Gate sources are pinned originals; outputs have fresh per-attempt paths.
CPU includes imports and Lean-generated C, excludes separate C compilation,
linking, Lake and cache acquisition. It is not independent kernel verification.

If later authorized, both pools start together: eight P workers on CPUs 0–7,
fourteen E workers on CPUs 10–23. Each compiler/thread remains in its pool;
CPU 8–9 is for the other chats. Unrelated Workspaces stay unrestricted.
-j8 stays for comparability; 22 compilers can oversubscribe OS threads.
CPU seconds are reported by pool with no conversion or extrapolation.
The pcore lease covers the whole qualification and is then released.

Every second the guard samples cgroup actual charge and node MemAvailable,
with a response margin above the required 8-GiB available reserve. A breach
kills the largest own charged compiler, records it, and stops the gate.
RSS is recorded but never summed for admission. Sampling is not a hard global
free-memory guarantee. PVC output only; 85% disk usage stops new work.
A future census must keep unsuccessful attempts and blocked modules separate;
failed/preempted CPU cannot silently become successful-module cost.

## Qualification (self-review / 自审)

Twenty original samples, ten ordinary and ten explicit-kernel-marker modules,
362–625,596 source bytes. Historical P wall sum 135.49 s, each selected module
under 25 s. Cached prerequisite closures are present. This purposeful protocol
check is not a new probability sample. Exact IDs/hashes are frozen in CSV.

Three repetitions of P quiet, P loaded, E quiet and E loaded give 240
foreground compilations. Loaded conditions maintain 22 real Lean jobs (8 P,
14 E, including foreground), replacing completed background jobs while
foreground runs. They use identical settings and bounded measured inputs.
Background jobs finish naturally at condition boundaries. Retain per-core
busy time, actual concurrency, charge, available memory, and background
outcomes; saturation is measured, not inferred. A 180-s gate deadline never
becomes a successful cost. Any failure/preemption stops the gate.

Separate counter-on/off quiet controls alternate treatment order, three
repetitions on each pool and each module (240 more calls). Pre-exec
perf_event_open counters inherit into threads; separate sysfs cpu_core and
cpu_atom retired-instruction events count user/kernel mode. Record
enabled/running time; an inactive PMU's zero is expected. No silent multiplex
scaling. A pthread control checks both PMUs and exited-thread inheritance;
it is instrumentation setup, not a Lean measurement.

Requested thresholds stay unchanged: median cross-condition instruction
deviation <=1%, P95 <=3%, byte-identical outputs, no failures/kills, overhead
<=1%. Report per-module condition medians and max/min spread, deviations
relative to P quiet, CPU and wall overhead, and P/E loaded/quiet CPU inflation.
Inflation never corrects census totals. Noise or missing conditions yields
an inconclusive result, not a pass.

Each attempt binds measurement Git commit, source revision/content hash
(provenance only), toolchain, argv, attempt, start/end UTC, pool, wait4
user/system CPU, wall/RSS, cgroup peak/events, and instruction coverage.
Raw data stays on PVC; small summaries enter Git.
census_full.py is an unexecuted obsolete draft, not a qualified launch path.
This gate has no code path that launches a full census.

## Retained earlier methodology

The six-module E-only pilot is not a census conversion. In its two-worker arm
the old summed-RSS guard killed one compiler at 16.06 GiB mapped RSS although
recorded own cgroup charge was only 2.06 GiB. It was not a node OOM.
The new protocol drops that RSS cap. All failures/setup errors remain.
The nealmcb report concerns a different revision and module set; its ~330 CPU
hours extrapolate 26 modules rather than measuring pinned per-module CPU.

## Actual qualification result — 2026-11-04

**FAIL under the frozen cross-condition spread metric. Do not start the full
census.** Measurement source commit:
`2c901ec4f0bbf73b75b534bbc255fcc973aebe6f`.
The controller ran 03:19:19–05:15:28 UTC (6,969.00 s), returned normally,
retired all native children, removed its own cgroup, and released pcore.lock.
No full-census process was launched. The initial E-first/j1 controller draft
was never executed and is not this protocol.

| Check | Observed | Interpretation |
|---|---:|---|
| Four conditions × 20 modules × 3 repeats | 240/240 successful | Complete foreground matrix |
| Counter-on/off controls | 240/240 successful | Three paired controls/module/pool |
| Real background compiles | 1,413/1,413 successful | Not census module costs |
| Native/resource failures or kills | 0 | No failed-attempt cost imputed |
| Four-condition instruction spread, median | 1.3312% | Exceeds 1% |
| Four-condition instruction spread, P95 | 3.1498% | Exceeds 3% |
| Active PMU running/enabled coverage | 100% in every measured row | No multiplex scaling |
| Current olean/ilean/C bytes | All 1,893 attempts identical per module/kind | Direct byte comparison, not only hashes |
| Historical original-sample bytes available | 17/20 modules, all three kinds equal | Three historical sets unavailable; not claimed checked |
| Node minimum MemAvailable | 28.350 GiB | Above 8-GiB reserve |
| Maximum own cgroup actual charge | 22.463 GiB | No RSS-sum admission; all memory event counters zero |
| 22-concurrent-job samples | 3,057 | Median mean busy: P 98.90%, E 99.93% |

For each module, first take the median total retired instructions in each of
the four conditions, then compute max/min minus one. The reported median and
P95 are across the 20 module spreads; P95 linearly interpolates index
(n−1)×0.95. Twelve module spreads exceed 1%; one exceeds 3%. This is a
descriptive purposeful subset, not a population confidence interval.

Metric sensitivity is material: pooling absolute deviations of the other
three condition medians relative only to P-quiet gives median 0.3988%, P95
2.2380%. Those values meet the numerical thresholds under that different
statistic. We retain both, rather than choosing the reference/statistic after
seeing the result. Max/min tests invariance among all four conditions and is
the conservative frozen-plan interpretation. The failed primary comparison
is not changed into a pass.

The largest exception is Transonic.Certificates.Barrier50: total instruction
condition-median spread is 20.0772%, even though its three products match.
Its user-mode spread is 0.4755%, kernel-mode spread 68.8188%. Across all
20 modules the median user-mode spread is 0.01756%, versus 8.6162% for
kernel-mode counts. Thus the split identifies variable kernel-mode work in
the recorded totals; it does not identify a particular syscall/page-fault/
scheduler path, nor imply a proof inconsistency. No new attribution run was
added. Counter PMU types/events came from live sysfs (cpu_core type 4 and
cpu_atom type 10, event 0xc0); raw counts and coverage are published.

### CPU inflation and counter overhead

| Descriptive statistic | P pool | E pool |
|---|---:|---:|
| Loaded/quiet CPU, median module ratio | 1.12821× | 1.25420× |
| Loaded/quiet CPU, ratio of all foreground CPU sums | 1.10969× | 1.20515× |
| Quiet foreground CPU sum (60 calls) | 724.713524 s | 1,367.001935 s |
| Loaded foreground CPU sum (60 calls) | 804.206239 s | 1,647.444966 s |
| Counter CPU overhead, median module paired median | 0.5274% | 0.2804% |
| Counter wall overhead, same statistic | 0.1276% | 0.2497% |
| P95 of module CPU-overhead medians | 1.9696% | 2.2190% |
| Maximum module CPU-overhead median | 4.4679% | 15.2805% |

CPU inflation is observed, not a correction factor. Some modules consume less
CPU loaded (Barrier50: P 0.88139×, E 0.78804×); no guarantee of uniform inflation.
P and E CPU are never converted. Overhead medians satisfy 1%, but these data
do not establish a uniform <=1% bound for every module. They measure native
wait4 CPU and launch-to-reap wall (including counter setup), not a separately
isolated accounting of the controller's own CPU. Quiet means no additional
W load; other explicitly permitted Workspaces were not paused or restricted.

### Scope, departures and next choices

The compiled definition is the original samples' -j8/LEAN_NUM_THREADS=8,
no-M, olean/ilean/C definition. Only 20 original modules were rerun, not all
42. Historical products missing for DihedralIntervals, OriginalBlock81 and
KeySound82 cannot be certified by their past scalar costs; all current
conditions/controls for those modules do agree directly with one another.
A tiny pthread PMU ABI/inheritance setup control preceded the lease; its
P-core portion used approximately 0.0418 CPU seconds without the gate lock.
This was a preparation deviation, is retained, and is excluded from all Lean
timing/overhead comparisons. The 480 Lean foreground/control calls and 1,413
load calls were all inside the one exclusive pcore lease.

The live post-run kernel is 7.0.0-42-generic, boot
585778d2-4fc1-48f5-aa9d-01cb7301e944. Post-run environment observations are
labelled as such, not backdated. This gate does not silently equate historical
sample hardware/kernel conditions with current timing. All 20 pinned source
content hashes still match, and retained historical bytes match where present.

The full source archive is acquired, but source availability is not complete
dependency readiness. The preserved initial readiness audit found 38 missing
external import names affecting 7,754 modules; this gate uses 20 cached
closures and does not resolve or misclassify those missing inputs as native
failures. The initial readiness CSV predates acquisition; the separately
published source-acquisition record confirms 163,097 source files present.

No threshold, thread setting or admission rule was changed during this run.
The default action is to stop here. Options for a later explicit decision:
(1) keep the fixed -j8 protocol and report actual machine/condition-specific
CPU, wall and raw instructions without claiming instruction invariance;
(2) approve a different thread/compiler protocol and a separate qualification,
preserving this failed gate; or (3) retain existing sample evidence and do not
run a census. None is launched by this report.

Small tables, immutable protocol, terminal record, environment and the byte
comparison are under [measurement/census-gate/](measurement/census-gate/).
All source hashes are provenance, not a download/install acceptance gate.
Raw logs and compiler bytes remain on the existing PVC under
/workspaces/.agent-state/gpu-smt-captures/workloads/census-gate-20261104/run-1.
The analysis is self-review (自审), not an independent system-acceptance claim.

The untracked obsolete full-controller source was preserved byte-for-byte at
/workspaces/.agent-state/gpu-smt-captures/workloads/census-gate-20261104/obsolete-full-controller-draft-never-executed.py
and removed from executable repository entry points. No historical tracked
source, raw result or other author file was deleted.

## Post-gate descriptive reanalysis (not a gate or a replacement decision)

Computed after the failed gate, from the published 240 foreground rows. No
new native run, cost observation, threshold or gate decision was introduced.
Per module, use max/min minus one across the four condition medians, and the
same linearly interpolated P95 as above:

| Mode | Median spread | P95 spread | Maximum spread |
|---|---:|---:|---:|
| User instructions | 0.01756% | 0.14442% | 0.47548% |
| Kernel instructions | 8.61621% | 43.53525% | 68.81880% |

The total kernel fraction is **8.95569%** when summing kernel instructions and
dividing by summed total foreground instructions. The median of the 240
individual kernel/total fractions is **14.89905%**. The proposed approximate
14% must therefore not be labelled a share of the summed workload; the
aggregation basis changes the answer.

For repeat variability, compute max(CPU)/min(CPU)-1 over each module's three
repetitions within a condition, then P95 across modules: **P loaded 19.72789%,
E loaded 8.30414%**, confirming the suggested 19.73% / 8.30%. Dividing the
range by the median instead gives 19.66439% / 7.99437%, a different statistic.
Exact fractions/formulas are retained in postgate-descriptive.json.
None of these descriptions changes the failed total-instruction gate.

## Earlier static preparation after the failed gate

At that earlier static step, the dependency audit and controller were prepared
on CPU 8–9 only.
See dependency-audit/README.md and controller-readiness.md. The 38 missing
external artifacts / 7,754 affected source units are unchanged after full
source acquisition; all 38 have pinned source or compatibility-patch evidence.
Native buildability remains unverified. The declared one-root Lake context,
two source roots and configuration-unit distinction are exported for M.
No guessed actual Lake environment is promoted to a verified context.

The replacement controller defaults to preparation only and has not run a
full collection. Its functional fixture uses five tiny modules, no PMU
counters or published native costs, no P-core lock. It exercised native
rejection/retry, dependent blocking, independent progress, clean resume,
orphan output directory recovery, and preserved malformed-tail handling.
Resource/disk fault injection and an actual interrupted native job were not
added this round; those paths are implementation, not newly qualified evidence.
The gate failure and requirement for a separate user decision still hold.

## Earlier actual-root preparation snapshot — 24fea9be

Started on CPU 8–9, then moved existing threads/controllers to CPU 10–16
without restarting them, as instructed. No pcore lease or --execute. The
official root Lake environment
has now been exported and its 42 package commits and 23 declared patches
verified. The earlier 24-entry patch count included a README. The old captured
12-path context is preserved separately from the 44-path actual export.
This is dependency preparation and functional evidence, not a cost run.

All 38 original requested artifacts were built successfully. All 38 functional
checks returned: 9 successful compiler calls covering 7 distinct source modules,
and 29 calls blocked by unbuilt internal OAI imports. No source rejection,
timeout, resource failure or native panic was observed.

The actual root context still lacks the external Rellich module identified in
dependency-audit/remaining-import-provenance.json. Its fixed-pin source is
available, but it is outside the original 38-target closure and was not built.
It blocks 3,768 source units. There are 159,329 source units without a known
external/source-rejection blocker, including the one configuration unit:
159,328 ordinary source modules, of which 9,223 form the static initial DAG
frontier and 150,105 await internal prerequisites. These are static/functional
categories, not successful builds. The whole-corpus build success count remains
unknown. No source pin was changed; no new cost data were collected.

census_controller.py defaults to the actual verified export and checks
context/compiler identity, package/manifest identity and external artifact
availability before execution. Functional compilation budgets and the
preparation thread setting are not substituted for the frozen census protocol.
The failed gate is unchanged; no full census was started or authorized here.

## Final dependency completion and remaining technical evidence — 2026-11-04

The final Rellich target and its prerequisites built at the unchanged pin.
Its smallest direct importer stopped at an unbuilt internal OAI parent.
All 3,528 enumerated external import artifacts are now present in the real
root environment. The previous 3,768-unit external-input block is cleared:
163,096 source modules have no known enumerated external/source-rejection
blocker, plus one separate configuration unit. This is not native acceptance.

The requested byte comparison considered the seven distinct successful
functional sources and their 21 olean/ilean/C products. No usable historical
counterpart was found in the retained locations searched; zero pairs were
compared. Parity between the old twelve-path environment and the real
forty-four-path environment is therefore unestablished, not passed. The seven
sources are not among the original42. Preparation also used the two-thread
environment setting rather than the frozen explicit -j8 cost command.

User decisions are excluded from this technical-state list:
(1) input availability is complete for the enumerated graph;
(2) same-source retained-reference parity under the finalized full recipe is
still missing;
(3) the full driver builds a first-hit symlink import-view instead of passing
the 44 paths through unchanged, and that real-corpus adapter path was not
executed here;
(4) earlier native-interruption/resource/disk-stop qualification limits remain
as disclosed, not new gates. Internal prerequisites will be ordinary DAG build
work, and untested corpus sources may still fail.

See [dependency-audit/final-preparation.md](dependency-audit/final-preparation.md)
and its small CSV/JSON records. No --execute, P-core lease, full-census launch,
new cost observation, pin change or protocol adjustment occurred.

## Real-corpus subset qualification — 2026-11-04

The explicitly authorized bounded controller attempt has returned. Three gate
targets with retained references had a five-module internal closure. Using the
unchanged 44-path export/folded-view recipe, three dependency-ready modules
failed at import time (six calls including retries), and two were blocked.
No current target products were produced: nine references are available but
zero artifact pairs could be compared. Equality remains unknown.

The folded view omits .ir/.ir.sig siblings that are present beside the original
Batteries and SDK olean files; pinned Lean source resolves IR beside its selected
olean. This is a confirmed view coverage defect consistent with the diagnostics,
without a changed-recipe repair comparison. No recipe or threshold was changed.
See [the bounded native report](dependency-audit/controller-real-subset/README.md).
This is functional evidence only, not costs or a passed census gate.
Full census was not launched; all W-owned validation processes have retired.

## Corrected adapter and selected-product parity — 2026-11-04

The previously unresolved folded-view defect is repaired by preserving the
complete first-hit file manifest, including IR and arbitrary companion
products. --execute now refuses a differing view before native launch.
The explicit E-core-only five-module closure rerun completed all five modules.
The initial complete file comparison passed for 139,944 external files; after
publication it passed for those files plus 15 new internal products. Nine
actual historical/current olean/ilean/C pairs were compared, all byte-identical.

The compilation command, -j8, LEAN_NUM_THREADS=8, options and pins were
unchanged. This selected functionality/parity prerequisite is established,
not full-corpus buildability, P8/22-core concurrency or a performance result.
The original instruction-invariance gate remains failed and its thresholds
unchanged. No costs were collected or added to census tables; no full census
was started. See dependency-audit/controller-real-subset-fixed/README.md.
All W validation processes have retired. Await the user's decision.

## Authorized full census: fixed 22-core protocol — 2026-11-04

门槛按总指令未通过（中位 1.33%、P95 3.15%），阈值没有改；决定运行是 Claude 按用户要求推进做的；跨模块比较用用户态指令（四条件中位 0.018%、P95 0.14%），这个判据是看到门槛结果之后才选的，论文要写明；内核态指令照常记录，但不用于比较；CPU 秒按 P 和 E 分开报告，不换算；墙钟是这台机器这个配置下的实测。

This supersedes the earlier wait-for-decision/no-full-launch direction.
The user requested autonomous continuation; Claude selected plan A. No failed
gate was relabelled passed and no threshold changed. The post-result choice
of user-only instructions is descriptive and must be disclosed in the paper.

Freeze from first to last source module: Lean 4.34.1, corpus 4eaee875,
Mathlib d13f23b7, the verified actual 44 search roots and complete folded view,
-j8, LEAN_NUM_THREADS=8, -DautoImplicit=false, no -M. P workers use 0–7,
E workers use 10–23, with capacities eight and fourteen; memory-dependent
admission may reduce actual concurrency. The whole execution holds pcore.lock.
Other project lanes use 8–9; no change is made to other Workspaces.

The universe is 163,096 source modules plus one configuration unit. New
native execution has an empty corpus-product view. Dependency-ready ordering
is lexicographic via a heap, without rescanning the entire pending frame
on each return. Compiler failures get one retry; dependent modules are
reported blocked and unrelated ready work continues. Resource-preempted
attempts are recorded separately, drained to exclusive retry and excluded
from successful module costs. The sampler uses node available memory and
actual cgroup charge, never summed RSS. The existing eight-GiB reserve and
one-GiB response slack remain; other Workspaces are not limited. Sampling
and unrelated allocations can transiently change headroom.

### Storage determined before launch

census-storage-plan.json retains actual filesystem headroom and artifact-size
inputs. Grouping twenty gate targets by the lexical decide+kernel marker,
and applying group artifact/source-byte ratios to this complete source frame,
predicts about 79.0 GiB olean and 5.85 GiB ilean, plus about 9.85 GiB C.
This is a sizing model, not a sampling estimate/CI. The five fresh closure
products corroborate available product types and selected target bytes.
A further 16 GiB allowance covers directories, logs, metadata and transient
products. This sizing fits below the 85% line at the observed starting use.
The different-commit nealmcb 116 GB / 122,458 modules reference extrapolates
to about 154.5 GB olean alone and gives a substantially higher disk scenario;
unobserved large products may still exhaust headroom. No fit guarantee is
claimed and no other lane's files or PVC capacity are changed.

From the first module, successful generated .c files have bytes/hash recorded
in the fsynced result before unlinking. The compiler still writes -c with the
same command, so compilation CPU/instructions include that work. .olean and
all required companions remain for M's full checker; .ilean remains.
Failed/partial native outputs and raw diagnostics remain. A crash between
durable record and C deletion is cleaned on resume only within this owned
output tree. Every deletion is appended to storage.jsonl. No Lake build or
--setup is invoked, so no per-module Lake .setup.json is generated.
Disk usage at 85% stops admission and preserves interruption records.

### Counters, record audit and continuation

The full --execute call supplies neither --functional nor --validate-subset.
Gate.launch opens cpu_core and cpu_atom user/kernel PMUs before releasing
the native exec pipe, with inherited task/thread counting. Every row retains
all four counter results, time-enabled/running and coverage. Only the active
pool's user/kernel coverage is interpreted; the inactive PMU may have zero
enabled time and null coverage. CPU and instruction comparisons never
convert E seconds into P seconds.

After the first 100 successful returns, the controller writes first100-audit.json
and stops on any missing required counter/provenance/cost field. A failed
contract requires a corrected new run directory, with old data preserved.
Gate launch identity correctly marks a full run. The standalone Workspace
supervisor has no SSH-session lifetime dependency. Fsynced records and native
start/exit identities support explicit same-protocol resume; interruptions
are unknown-cost events, not completed modules. Host/container interruptions
must remain distinct from continuous machine wall time.

Eleven preparation regressions passed, including a tiny non-Lean executable
flow that checks ready ordering, one failure retry, dependent blocking,
durable-C pruning and no-new-native resume. These are not cost results.
Final publication occurs only after execution ends, under census/. No
progress commits are planned. First-100 verification, 10% and 50% milestones
are runtime evidence/messages; the latter include resource headroom.


## 2026-11-05 operational continuation: segment 2, bounded by UTC

The first segment retired at 20:29:39.647 UTC with **128,331 completed
source modules**, 34,765 incomplete source modules and one configuration unit.
Two sources completed after the earlier 128,329 observation. There were 65
resource-interrupted attempts and one transition-interrupted attempt. They
are retained separately. The 20:33 cancellation was superseded by the direct
request to attempt most of the remaining work within six hours.

This is an explicitly different admission segment, not the original frozen
concurrency protocol. The original total-instruction gate remains failed.
Lean command, -j8, LEAN_NUM_THREADS=8, no-M, pool membership P0-7/E10-23,
source pins, actual 44-entry environment and canonical import view stay
unchanged. Completed source modules are never rerun. Every new lifecycle and
result record includes segment=2, active_at_launch and admission state.
Segment 1 is assigned segment=1 only in the exported table, without editing
its raw records.

Admission uses actual native cgroup charge and node MemAvailable, also
respecting finite ancestor cgroup headroom. It reserves max(1 GiB, 1.25 times
observed parent-namespace peak) per candidate, deducts each running job's
remaining predicted growth, and retains a 12 GiB soft node-available margin.
Risk roots are the first three module namespace components with an observed
resource interruption. Their concurrent cap uses the measured root peak
times 1.25 and the available actual native budget. A censored failed peak
increases the parent-family estimate by 1.5. If only an over-predicted source
remains, an otherwise idle machine with at least 16 GiB available may make a
guarded standalone attempt, explicitly recorded in admission metadata.

Ready queues retain lexical dependency-ready ordering; only candidates
ineligible for memory admission are deferred. There is no cheapness or
source-cost sorting. First resource interruptions requeue normally, without
draining the machine; a second resource failure requests an exclusive retry.
A failure of that exclusive retry is recorded as a terminal resource outcome.
Ordinary native compilation failures retain their existing retry policy.

The existing parent-controller guard is retained; its proactive kill
threshold is 10 GiB available in segment 2. Sampling is nominally once per
second and can be delayed by artifact handling; this is not an independent
hard-memory guarantee. The original owned-cgroup ceiling and 85% disk stop
remain. No Workspace quota or other Workspace is changed.

**2026-11-06 03:00 UTC** stops admission of new modules. In-flight jobs may
finish until **03:30 UTC**, when remaining attempts are forcibly interrupted
and separately recorded. The controller then releases pcore.lock. Both
segments' CPU and wall are reported separately, along with their observed
sum and the transition gap. All cost summaries describe completed modules
only; this dependency-ordered subset is not a random sample. Unfinished costs
are blank and are not extrapolated from the original 42 samples. Whole-corpus
cost is reported only as an observed lower bound. All olean companions stay
available for M's checking of the built subset.

Reference correction: nealmcb's 116 GB describes the whole finished build,
including packages; its Lean lib artifacts are about 68 GB. The earlier
olean-only description above was incorrect. This changes no native recipe.
