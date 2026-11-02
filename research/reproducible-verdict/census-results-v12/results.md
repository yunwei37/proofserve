# All 2,524 computation helpers: completed heartbeat census

The three-module census completed on 2026-11-02 UTC: **2,524/2,524 targets
(100%) have zero allocation-heartbeat variation** across 1/2/4/8 actual worker
threads, each repeated three times. There are 30,288 checked target observations
and 22,716 within-repeat j1-versus-j2/4/8 comparisons: zero allocation-count,
verdict or diagnostic differences. All observations are accepted by the
original Lean 4.34.1 kernel.

| Module | Complete eligible helpers | Observations | Matched pairs | Zero-variation targets | P95 / maximum variation |
|---|---:|---:|---:|---:|---:|
| UMoments9 | 1,164 | 13,968 | 10,476 | 100% | 0% / 0% |
| BarrierData41 | 1,320 | 15,840 | 11,880 | 100% | 0% / 0% |
| EnvelopePsiB | 40 | 480 | 360 | 100% | 0% / 0% |
| Total | 2,524 | 30,288 | 22,716 | 100% | 0% / 0% |

Per-target variation is 100*(maximum-minimum)/minimum over its 12 observations.
P95 is the nearest-rank percentile across targets, not across raw work costs.
[target-heartbeats.csv](target-heartbeats.csv) gives every target's count range
at each thread count; all three repeats at each count are identical.
[distribution.csv](distribution.csv) is the compact distribution.
No nonzero cases exist to stratify by existential quantifiers, search dependencies,
or size. Costs do span 984 to 51,563,153 raw allocation heartbeats across targets;
even the largest observed target has zero range. This does not establish
stability for unmeasured syntactic shapes.

## Scope and validity

This is a census of all target-module theorem helpers whose cleaned proof head
is `of_decide_eq_true`: 1,164/1,320/40, as extracted from the matching compiled
modules. It is not a census of all openai/math computations, source-level
`decide +kernel` occurrences, definitions, or full-source elaboration.
The original stored proof and type are rechecked under a fresh theorem name
with `Kernel.Environment.addDeclCore`, in the original imported environment.
No sorry/free/meta-variable proof is admitted by input preparation. No new
axiom or unchecked declaration insertion is introduced. Imported dependency
trust is the ordinary original-kernel trust boundary. Prepared imported terms
and any shared realization they contain remain part of this measurement
setting; it is not cold elaboration or a from-scratch build.

Allocation deltas are read on each executing worker around the original kernel
call; CPU uses CLOCK_THREAD_CPUTIME_ID. Every j1/j2/j4/j8 process produced
1/2/4/8 distinct worker TIDs, respectively. This is actual worker coexecution,
not merely available-pool-size changes. Counter measurement adds common wrapper
work; its counter perturbation has not been independently subtracted.
The kernel's distinct native heartbeat-poll counter remains unobserved.
Its generous 2,000,000,000-poll limit is not the reported allocation count.
All 36 native processes returned0 and retired; cgroups retired, no sampled
memory stop or cgroup memory event. Largest sampled own-tree RSS was12.134GiB.
No Lean -M; shared P0-7 lock, at most one native process at a time. The controller
took1284.000s after lock acquisition; waiting time is not added to this run cost.

Raw sources, executable, stdout, stderr, memory and native terminals remain on
the existing PVC at
`/workspaces/.agent-state/gpu-smt-captures/reproducible-verdict-v12`.
Only compact data are in Git. Reproduce the full paired analysis on the PVC:

```sh
python3 research/reproducible-verdict/analyze_modules.py   /workspaces/.agent-state/gpu-smt-captures/reproducible-verdict-v12   /workspaces/.agent-state/gpu-smt-captures/reproducible-verdict-v12/analysis
```

The original terminal and raw JSON were also read independently to check all
target identities, 12 distinct repeat/worker combinations per target, accepted
verdicts, zero range, process retirement, resource events and affinity. The
retained local foreground handle no longer exists; authoritative complete
terminal and raw native retirement records establish completion.

## Budget implication and two-regime boundary

A paper-safe sentence is: **Across all2,524 prepared computation helpers in
three real modules, allocation-heartbeat variation across1/2/4/8workers and
three repeats has P95=0% and maximum=0%; no extra allocation-count headroom was
needed to cover these observed runs.** This is an empirical envelope, not a
guarantee that a future run at zero padding will accept. No near-limit native
kernel-poll ladder was run, and raw allocation counts are not directly an
authoritative whole-candidate maxHeartbeats budget.

The earlier fresh three-repeat mathematical full-source experiment
[rechecked two source modules](../module-results-v11/results.md):
InteriorH1Derivative92,995,454..93,029,620raw counts, observed headroom
0.0367394303%; ReindexSingle8,090,121..8,101,322, 0.1384528118%.
Those ranges pool96executions per identical source, and cover measured
command-count sums. Source counters vary in40/72and38/72thread comparisons,
while judgments agree. Another16-source coexecution sample reached2.333868%;
do not substitute the smaller two-module envelope as a guarantee for it.
The prepared mathematical theorem kernel checks were stable too, although
each module had only one eligible theorem and thus no8-way proof coexecution.

The supported distinction is therefore **stable prepared kernel recomputation
versus variable source elaboration under coexecution**, not a proof that all
mathematical search is nondeterministic or that every computational program is
deterministic under any observer. Shared realization/caches/task accounting are
still alternative explanations to changed search branches. Deterministic
budgeting, if pursued, should first target the observed variable elaboration
stage; a subject-matter-only classifier is not justified by these data.

## Cold/warm comparison: already complete, not rerun

[The private-runtime cache experiment](../cache-and-coexecution-results.md)
already completed512observations/256pairs: zero verdict/diagnostic/axiom
differences, and zero synchronous command-count differences in128pairs.
The second mincore pass checked2,238,400private pages: all absent for cold
and all resident for warm. Parent-only asynchronous counts differ in42pairs
and cannot stand in for total asynchronous work. These16miniF2Fsources are
a separate point, not a cold/warm census of these2,524helpers. System libraries
and global host caches were not evicted. Existing failed/partial predecessors
remain preserved; no need to duplicate this completed cache experiment.
