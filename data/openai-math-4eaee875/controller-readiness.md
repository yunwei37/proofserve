# Prepared census controller (not authorized to execute a census)

census_controller.py is a preparation tool for the frozen -j8, no-M protocol,
not a ProofServe product command and not a successful gate result. Default
invocation only prints the plan; it does not take pcore.lock, create cgroups,
or compile any module. --execute is necessary to run. No full execution was
performed this round; the instruction-invariance gate remains failed.

Prepared choices are 22 cores (P 0–7, E 10–23) and P8 (P 0–7 only).
Both pools are configured before any compilation, under one P-core lease.
Per-process affinity/threads, admission rule and context remain fixed in the
run identity. A changed identity requires a separate output directory.
Run distinct Lake contexts separately; a mixed-context manifest is rejected.

Implementation includes dependency-order scheduling, a shared import view of
qualified external and newly completed internal artifacts, actual compiler
version verification, fsynced native results/lifecycle records, original source
hash/commit/argv/toolchain/attempt binding, separate inherited user/kernel PMU
counts and coverage, and native wait4 CPU/wall/RSS. Failure records are retained
separately. One native retry is allowed; dependent modules get explicit blocked
reasons while unrelated modules progress. A resource-preempted job drains to
an exclusive retry; a failure at current standalone headroom is operational
resource failure, not proof rejection. Interrupted attempts are never imputed
as successful cost. Completed artifacts/sources are checked before resume;
orphan directories and malformed tails are preserved, never overwritten.

The shared native adapter's new options are opt-in; the measured gate source
remains available at 2c901ec4 and in its frozen raw snapshot. No old measurements
are rerun or reclassified. The functional flag uses CPUs 8 and 9, no pcore lock,
no PMU counters, and suppresses native cost fields. Its cgroup is bounded.
The full path uses node available memory plus cgroup actual charge, not RSS
sums; a one-second sampled response has one GiB of margin above the required
eight-GiB reserve. It cannot guarantee global headroom against other workloads'
instantaneous allocations. It never limits other Workspaces. Disk 85% stops
new admissions; the shared guard may terminate active attempts, preserving
their interruption records, and all unattempted units receive a reason.
The root lakefile.lean configuration is accounted separately from proof modules.

The five-module functional fixture returned three successful modules, one
deliberate native type error (two attempts), and one dependent blocked module.
Independent progress, clean no-new-native resume, orphan-directory handling
and malformed-tail preservation were exercised. Initial flat-module-directory
and orphan-numbering defects were found and fixed; raw development failures
remain on PVC. This is status/flow evidence only. Resource/disk fault injection,
live native interruption and whole-corpus throughput were not claimed tested.
Later guard refinements were syntax/recovery checked, not performance-qualified.

Default preparation examples (do not add --execute while the gate is failed):

    python census_controller.py --manifest MANIFEST --out PVC_POINT --pool 22 --commit GIT_COMMIT
    python census_controller.py --manifest MANIFEST --out PVC_POINT --pool P8 --commit GIT_COMMIT

controller-prepared-protocols.json records the earlier pre-export preparation;
controller-functional.json captures the earlier fixture statuses. The current
actual-context preflight is dependency-audit/controller-context-preflight.json.
None enters a cost table.
The functional raw point is retained at
/workspaces/.agent-state/gpu-smt-captures/workloads/controller-functional-20261104.
Planning estimates live separately in dependency-audit/planning.json and are
not publication measurements. The default preparation path now reads
dependency-audit/lake-environment.json.
It refuses a missing or unverified export, wrong corpus/compiler/toolchain, or
a context belonging to another project rather than silently using the old
captured search path. Before native execution it also rechecks the manifest
identity and actual package commits, and refuses missing external artifacts.
A verified environment alone is not readiness for all source modules:
dependency-audit/summary.json distinguishes missing inputs, observed functional
rejections, and the still-unbuilt remainder. The failed gate and separate user
decision remain independent prerequisites. No --execute invocation was made
during the actual root-context dependency preparation.
