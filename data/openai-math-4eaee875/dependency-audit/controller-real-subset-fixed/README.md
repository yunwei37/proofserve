# Corrected folded import view: bounded native qualification

This is a functional result, not a measurement or a passed census gate.
The original instruction-invariance gate remains failed; no full census was
started. The earlier failed attempt is retained unchanged in
[controller-real-subset](../controller-real-subset/README.md).

## Adapter fix and mandatory pre-native comparison

The previous suffix filter copied only olean-family artifacts. The adapter
now inventories **all regular files** visible through the actual 44 ordered
search roots. It follows directory aliases with cycle detection, preserves
first-hit resolution, and retains the previous exclusion of old OAI,
ComparatorChallenges and HodgeConjecture corpus outputs.

The resulting view includes .olean/private/server parts, .ir, .ir.sig,
ilean/C, libraries, metadata and otherwise unlisted sibling extensions.
There is no replacement suffix allowlist. For a selected olean, companions
must come from that selected module directory: partial module-family shadowing
is refused instead of silently combining an earlier olean with a later IR.
Unresolved source aliases are refused. Newly built module publication now
includes all same-module siblings rather than obj.name+'*', so future IR or
other products are not dropped at publication either.

Before creating the native compiler scope or launching any build, the real
--execute path writes and checks the complete manifest. Missing, extra,
wrong-target or unresolved files prevent native launch. Symlink targets are
compared to the original first-hit files, so the view names refer to the same
underlying files; this is not merely a count or suffix-existence comparison.
The dry default still performs no native execution or view creation. No pin,
compiler option, command recipe, threshold or automatic full entrance changed.

The real preflight compared **139,944 external files**:
**zero missing, zero extra, zero different targets**. The compressed
[complete manifest](import-view-files.csv.gz) is included, with relative view
path and resolved original file path per row. These absolute paths record the
preparation environment, not a requirement on downstream ProofServe users.
The preflight file predates the native launch record. After publishing the
new internal products, a second complete check passed for **139,959 files**:
the same 139,944 external files plus 15 newly generated internal products.

## Fresh same-closure execution

The target selection is unchanged from the previous attempt: sort the 17 gate
modules with retained historical triplets by internal closure size and name;
take Binomial (1), VariationalDN (2), ComputeRow1115Batch17 (2).
The union is five real source modules. Its input manifest was copied without
modification, and the output directory started empty: no internal products,
completed ledger or old corpus outputs were reused.

| Module | Native calls | Result |
|---|---:|---|
| OAI.Analysis.Conductivity.Model | 1 | completed |
| OAI.Analysis.Conductivity.Variational.VariationalDN | 1 | completed |
| OAI.Analysis.Laughlin.FourBody.RowCompute | 1 | completed |
| OAI.Analysis.Laughlin.FiniteFlux.ComputeRow1115Batch17 | 1 | completed |
| OAI.Probability.TraceReconstruction.Binomial | 1 | completed |

All five completed with exit zero. There were no failures, retries, blocked
modules, interruptions or resource kills. No additional import/path repair
or second corrected run was needed. The previous failure ledger was not
overwritten, resumed into success or included as successful work.

The same census_controller.py execution path supplied the verified export,
folded view, dependency scheduling and shared native adapter. Native argv
retained the original compiler/source/root, **-j8**, **LEAN_NUM_THREADS=8**,
**-DautoImplicit=false**, and olean/ilean/C output recipe. There was no -M.
The adapter fix changes availability of import files, not those parameters.

This explicitly bounded exception used CPUs **10–16**, one active native
process, no P-core lease and no PMU measurement. Its native cgroup was bounded
at 11 GiB and supervisor/controller cgroup at 1 GiB; only these owned scopes
were controlled. No compilation CPU/wall/RSS cost fields were emitted.
The 2,000-module/six-hour maximum was not enlarged. It does not qualify
full 22-core/P8 concurrency, end-to-end performance or the failed gate.

## Direct byte comparison

The historical references remain unchanged. Read both files and compare their
actual bytes; the recorded hashes are provenance, not a substitute for that
comparison or a download/acceptance gate.

| Target | olean | ilean | C |
|---|---|---|---|
| OAI.Probability.TraceReconstruction.Binomial | identical | identical | identical |
| OAI.Analysis.Conductivity.Variational.VariationalDN | identical | identical | identical |
| OAI.Analysis.Laughlin.FiniteFlux.ComputeRow1115Batch17 | identical | identical | identical |

**Nine pairs compared, nine byte-identical, zero different.**
[artifact-byte-comparison.csv](artifact-byte-comparison.csv) gives sizes,
paths and equality for every pair; first_difference_offset is blank because
no difference exists. No recipe was changed to force equality. This establishes
the requested selected-target parity between the retained historical products
and this real 44-path/folded-view run. It does not establish parity for all
42 historical samples or all 163,097 source units.

The before/after native results are consistent with the diagnosed missing-IR
adapter defect: the unchanged five-module source closure now completes after
the full-file view fix. This is not an additional performance or novelty claim.

## Evidence and reproduction

The complete PVC raw point is:

    /workspaces/.agent-state/gpu-smt-captures/workloads/controller-real-subset-fixed-20261104

It retains the unchanged five-module manifest, four frozen implementation
files, exact run configuration, supervisor and native identities, fsynced
lifecycle/results, preflight file list, memory guard records and terminal
record. [plan.json](plan.json) records the base commit and frozen source
hashes; the legacy raw measurement_commit field is the base 94875d6b, while
this result commit publishes the exact changed adapter source identified
by those hashes. The compiler adapter census_gate.py was unchanged this round.

[attempts.json](attempts.json), [outcomes.json](outcomes.json) and
[native-diagnostics.json](native-diagnostics.json) contain the five returns.
summary.json records the narrow qualification and unchanged failed gate.
No old costs or source successes were silently reclassified.

The bounded call was the prior explicit --validate-subset --execute invocation,
with its new empty output directory and this frozen fixed adapter. The full
163,097-unit manifest was not executed. To run only dry regressions:

    cd data/openai-math-4eaee875
    python3 -m unittest test_census_controller_subset -v

Ten passed: four existing dry/default/closure-bound checks and six focused
file-view checks covering arbitrary extensions, first-hit precedence and
old-corpus exclusion, partial family shadowing, missing/extra/wrong-target
detection, all-sibling publication and directory aliases/cycles. These are
functional checks, not measurements or native full-run qualification.
Resource/disk/deadline fault injection and interrupted-resume qualification
were not newly claimed here.

自审: checked all five native returns and outputs, direct nine-pair bytes,
frozen source identities, actual thread/affinity settings, absence of cost
fields, 42 unchanged package pins, both complete view comparisons and process
retirement. Supervisor, controller and all native processes have retired;
their empty owned cgroups were removed. External inputs and this selected
real-adapter closure are ready. The original failed gate and the user decision
remain separate; no full launch is implied. This round stops here.
