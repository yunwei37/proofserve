# Real-corpus controller subset: failed import adapter qualification

This is functional preparation, not a cost run or a passed census gate.
The original total-instruction gate remains failed. No full census was
started. No compilation recipe, source pin, import-view rule or threshold
was adjusted after observing this failure.

## Selection and execution

The gate has 20 targets; 17 retain all three historical products.
Sort those 17 by complete internal closure size, then module name, and
take the first three:

| Selected target | Regime proxy | Internal closure, target included |
|---|---|---:|
| OAI.Probability.TraceReconstruction.Binomial | ordinary mathematics | 1 |
| OAI.Analysis.Conductivity.Variational.VariationalDN | ordinary mathematics | 2 |
| OAI.Analysis.Laughlin.FiniteFlux.ComputeRow1115Batch17 | computation certificate | 2 |

The union has five modules. selection.csv records all twenty candidates,
including the three without complete retained references. plan.json preserves
the deterministic selection and the nine reference identities.

The frozen census_controller.py executed the five-module manifest through its
real export validation, package-pin checks, first-hit folded import view,
dependency scheduler, native Gate.launch and result ledger. An explicit
--validate-subset --execute opt-in bounded this exception. The normal default
still only prepares, and the full entrance still requires --execute.

Compiler argv used the same absolute Lean binary, original source/root,
-j8, -DautoImplicit=false and olean/ilean/C outputs as the prepared full
driver. LEAN_NUM_THREADS=8; no -M. The actual 44-path Lake export was folded
by the unchanged view code into one runtime LEAN_PATH. External libraries
were reused; no prior OAI/ComparatorChallenges/HodgeConjecture corpus outputs
were admitted to the fresh view. The five internal modules started with no
completed ledger and no existing internal products.

Allowed nonmeasurement differences: E-core affinity 10–16, one active native
worker, no pcore lock, no PMU counters, suppression of CPU/wall/RSS cost
fields, a six-hour/2,000-module maximum and cgroup memory bounds. The native
scope was bounded at 11 GiB, the supervisor/controller scope at 1 GiB;
only these owned scopes were touched. This does not validate the full
22-core or P8 concurrency/resource behavior. The run identity retains the
core-pool capacities; validation_limits.workers=1 is the actual admission
override. All six attempts actually recorded affinity 10–16 and eight threads.

The raw result's legacy measurement_commit field identifies the base
661a7c5c, not an assertion that its code was already committed there.
summary.json binds all four frozen implementation files by provenance hashes;
this result commit publishes those exact controller/adapter bytes. They were
not edited during or after execution. The new dry tests do not launch Lean.

## Actual outcomes

| Module | Outcome | Calls |
|---|---|---:|
| OAI.Analysis.Conductivity.Model | import-time native implementation unavailable | 2 |
| OAI.Analysis.Laughlin.FourBody.RowCompute | interpreter declaration unavailable | 2 |
| OAI.Probability.TraceReconstruction.Binomial | import-time native implementation unavailable | 2 |
| OAI.Analysis.Conductivity.Variational.VariationalDN | blocked by Model | 0 |
| OAI.Analysis.Laughlin.FiniteFlux.ComputeRow1115Batch17 | blocked by RowCompute | 0 |

All three attempted modules failed twice under the existing one-retry policy:
six native calls, no successful current products, two dependent modules
blocked. These are environment/adapter failures during imports, not evidence
that the source propositions are false or that the fixed pins themselves
cannot build. There was no timeout, resource kill, native panic or controller
failure. The controller returned zero while outcomes.complete=false: its
exit status alone is not a successful build. All five inputs have an outcome.

The two distinct messages are preserved verbatim in native-diagnostics.json:
missing Lean.registerTagAttributeExtra (Batteries lp_batteries symbols), and
an unknown Lean.Option.register specialization under SimpTheorems.
static-validation.json rechecks all 42 package commits, the three selected
source hashes, and the absence of reused internal outputs.

## Folded-view defect: static evidence, no repair A/B

The unchanged view builder only links glob('*.olean*'). Its selected
Batteries.Lean.AttributeExtra and Lean.Meta.Tactic.Simp.SimpTheorems
.olean/.olean.private/.olean.server files are present, but their .ir and
.ir.sig siblings are absent, although the original package/SDK directories
contain them. The entire folded view contains zero .ir and zero .ir.sig files.
sidecar-coverage.json records both concrete examples.

In the pinned SDK source, Lean/Environment.lean readIRPartsOfMod
(lines 2093–2106) calls findOLean and derives .ir.sig/.ir from the selected
olean path. If .ir.sig is absent it returns an empty IR array. Lean/Util/Path.lean
findOLean (lines 116 onward) resolves through the search path. Thus moving
only olean-family files into a view can select imports without their IR;
ordinary SDK fallback does not supply siblings beside that selected path.

This is a confirmed coverage defect consistent with the observed failures.
No altered-view run or causal repair comparison was performed, so the report
does not claim the defect is the only cause or that adding siblings would
complete this closure. Newly built module publication uses an olean-family
glob too; module-mode products may require the same consideration. No such
publication occurred here.

## Byte comparison: no comparable current pair

Nine historical products are retained and were checked unchanged. None of
the three selected targets produced a successful current olean/ilean/C set.
Therefore **zero pairs were compared, zero pairs established equal, and
the number of differing pairs is unknown**. artifact-byte-comparison.csv
contains nine explicit not_compared_current_product_unavailable rows, with
blank byte_equal cells. This is neither byte mismatch nor byte parity.

The previous seven-source/21-unpaired-products report is historical and
unchanged. This attempt resolved reference selection and exercised the real
adapter, but failed to establish the requested parity. No replacement
historical baseline or different recipe was created.

## Reproduction and current technical state

The PVC raw point is
/workspaces/.agent-state/gpu-smt-captures/workloads/controller-real-subset-20261104.
It retains the five-module manifest, exact frozen sources, launch identity,
full argv, actual environment export identity, run configuration, fsynced
lifecycle/results, native logs, memory records and returned outcome.
Read plan.json, attempts.json, outcomes.json and summary.json for the small
public evidence. No cost fields are published from this preparation.
The original 163,097-unit manifest was not executed.

The explicit exception command was:

    python source/census_controller.py --manifest manifest.json --out run       --validate-subset --environment-export PATH_TO_VERIFIED_EXPORT       --commit 661a7c5c9ac09482d78b0f5780237b48a7ba244c --execute

Do not run that command as a full-census authorization. A new output directory
is required for any changed recipe. Dry regression command:

    cd data/openai-math-4eaee875
    python3 -m unittest test_census_controller_subset -v

Four dry regressions passed: unchanged full default remains preparation-only,
subset preparation stays E-core/nonmeasurement, an unclosed subset is refused,
and more than 2,000 modules is refused. These do not qualify native success,
six-hour fault handling, full concurrency, resume or resource/disk injection.

External artifact availability remains complete for the enumerated import
graph; this run now establishes that the prepared folded environment is not
yet functionally usable for the selected real sources. The adapter and
same-source artifact parity are unresolved technical prerequisites, separate
from the unchanged failed instruction gate and user decision. No protocol
repair or rerun is silently authorized by this report.

自审: checked all six raw native records, five outcomes, selected source and
reference identities, absent cost fields, actual affinity/threads, unchanged
pins and frozen implementation bytes. Supervisor, controller and all native
PIDs retired; owned empty scopes were removed. No background W collection
remains. This round ends here as requested.
