# Kernel-grain distribution and declaration-level parallelism

M lane, 2026-11-01 UTC, same-thread 自审. Edits only in this directory.
Current RQs: RQ1 “Cost locations and runtime-weighted regime prevalence”;
RQ3 “Original-kernel computation across cores/cluster”. User directs measuring
actual goal grain before splitting and requires the original kernel and exact
acceptance-set parity.

The previous single Grid target is not representative of whole-module grain.
The prior component-preserving small-target point acquired its lock and
completed before withdrawal could occur; all original/failed data remain.
No new small-target splitting is scheduled under the latest instruction.

## Hypothesis and paper decision

Independent computations may be mostly many short kernel obligations, rather
than a few long goals. A heavy tail supports within-goal chunking; mostly short
calls redirects the experiment to parallel checking of independent declarations.
Both outcomes alter the RQ3 design. Logical decomposition counts alone cannot
settle the claim. This is decisive characterization, with reader/clock setup
folded into it rather than presented as a contribution.

The source pin and actual identities are checked. UMoments9 contains1164
lexical sites and1164native helper types, not40. The quoted146s cost is from
an old-M point; W's complete no-M attempt is90.2835s wall.40belongs to the
retained EnvelopePsiB case. No estimate is made by dividing those compiler
clocks by site counts.

## First finite capture

The direct three cases are UMoments9, BarrierData41 and Grid. Use their exact
successful no-M W artifacts (including any present parts), read target data
without importing the target, import only its declared dependencies and replay
its local declarations with stock Lean4.34.1 APIs.

For each, compare the original Kernel.Environment.replay against a namespace-
adapted copy of exactly that upstream algorithm. The only checker-path change
is a timer around the same Kernel.Environment.addDeclCore call. Native wall
and worker-thread CPU clocks stop before JSON/goal printing. Ordering, duplicate
theorem rules, unsafe/partial exclusions and generated constructor/recursor
checks remain upstream behavior. No Lean trace.profiler or -M is enabled.

Clock callbacks are the same C clock_gettime functions as the qualified prior
prototype; they do not allocate inside the checking callback. Metadata/logger
cost outside the kernel is still observer cost. The three stock/timed controls
compare complete eligible-name sets and report replay/whole-native overhead.
One pass locates grain; it is not a precise overhead confidence interval.
No source compiler denominator is rescaled from these different replay clocks.

The same single finite capture then profiles the remaining retained W31
artifacts:29original probability-sample modules and2purposeful modules.
It does not rebuild source or duplicate W's compilation work. Plain input paths,
sampling probabilities and original source-capture provenance are retained.
If the window cannot finish, preserve the completed units and mark missing
ones; do not count stdout prefixes as completed acceptance or zeros.

Before real targets, the timed copy must agree with stock replay on a small
original module and both must reject an in-memory loose-bound-variable proof.
The existing O reader/source-equivalent checker controls are reused as
background evidence; O code is read-only, copied adaptations stay here.
These are necessary qualifications, not positive performance results.

## Metrics and global estimate

Per actual C++ declaration call retain full name, whether its proof is headed
by of_decide_eq_true, target expression, wall and thread CPU, and acceptance.
Report native helpers versus source sites without assuming one-to-one identity.
Threshold≥1s is reported for both threadCPU and native-call wall; prototype
selection prioritizes calls with≥1s CPU, then remeasures the selected target.

Report bins, quantiles and top goals. Fractions use (1) decision-helper CPU
and (2) all timed C++ declaration CPU as separate own-run denominators.
Replay/import/logger/process costs remain separate. These are independent
kernel-recheck costs of fixed artifacts, not measured source elaboration time.

For wider scope, compute an inverse-inclusion-probability weighted ratio using
the actually available random modules, excluding purposeful roots from that
population calculation. This is an available-case/model estimate: missing
original draws and censored units prevent an unconditional unbiased whole-
library claim. Relate it to the full source-shape census and report unsupported
shape/coverage gaps; counts do not become CPU by assumption. No global Amdahl
limit or cross-run denominator replacement follows.

## Resource and scheduling protocol

One submitted capture, one native process at a time, P0–7/common existing flock.
The active window is1680s with1740s external timeout *after* lock acquisition.
A cell starts only with its predeclared full cap available; no silent cap
shortening. Per-cell caps are frozen from prior source CPU scheduling estimates,
minimum90s, maximum600s, not scientific runtime denominators.

Own child cgroups under this Workspace Pod cap charged memory at14GiB; an
independent parent samples their entire process RSS at1s and stops above14GiB,
reserving2GiB within M16GiB. Charged memory and RSS differ; sampling is not a
hard RSS quota. Signal cleanup kills only the owned child group/cgroup.
All source/logs/modules/partial/failure data are on the existing PVC. Preparation
uses E8–15. No host setting, other Pod, permission, schedule or O file changes.

## After distribution: two mechanisms

Only observed≥1s goals enter within-goal partition curves at1/2/4/8, preserving
shared computation. CBox has only4primitive fields;8useful subcomputations may
require a proved computation checkpoint rather than duplicate/trivial goals.

For many small goals, inspect BarrierData41's actual local dependency graph.
Batch independent declarations over an already checked prefix, invoke the
original kernel concurrently, and combine through a stock checked-artifact
path. An unchecked environment union is not an acceptable substitute.
Compare against original serial replay as well as1/2/4/8worker versions;
include graph, serialization, import and ordered-commit costs. Exact eligible
acceptance sets and invalid-proof rejection must agree. SCCs/inductive blocks
need native atomic handling or an explicit serial fallback.

No speedup is asserted before the real full comparison. A slow but valid
implementation bounds that implementation, not a proof of impossibility for
all kernel parallelism. No generic novelty claim is made for DAG scheduling,
certificate splitting, futures or parallel proof checking.
