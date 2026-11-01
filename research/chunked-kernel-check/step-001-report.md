# Step001 — real-goal decomposition, native kernel checks, and an initial negative curve

M lane, 2026-11-01 UTC; same-thread 自审. Only this directory is edited.

## EXPERIMENT

The user's two-cost-regime characterization is the accepted direction. This
step asks whether a genuine computational obligation can be decomposed without
changing the trusted proof checker, and measures complete costs rather than
only the parallel section.

An automatic source generator extracts Grid's actual p0_0 definition and
PointBox.calc p0_0.t = p0_0 obligation from pinned OpenAI/math4eaee875. It reads
the source record schemas and recursively makes18 Int-field equalities, groups
them into k=1/2/4/8 conjunctions, and generates constructor-based extensionality
and merge lemmas. No witness numbers are supplied manually. A separate native
TargetEquivalence.lean check relates the extracted input and proposition back
to the imported original Grid definitions.

A single Lean process runs k concurrent IO tasks with immutable imported
environments. Each child calls the unmodified C++ Environment.addDeclCore
with checking enabled and a finite raw-heartbeat allowance, then writes an
ordinary module. The final stage uses standard module import and a further
original-kernel check of the assembled theorem. There is no unchecked union,
debug.skipKernelTC, native_decide, new axiom declaration or custom logical
evaluator. The original and final proof dependencies are both [propext].
The generator helpers and final statement are kernel checked, not trusted.

The original monolithic target and k=1/2/4/8 have3repetitions each (15 completed
native processes). Every original and transformed target accepts. A false-first-
chunk negative control is rejected by the original kernel and creates no final
combined artifact. All timed cells use no-M/P0–7/common pcore.lock, same SDK and
data; one native process,180s self alarm, finite heartbeats,14GiB sampled own-
tree stop (2GiB headroom within M16GiB for analysis). CPU time for phases uses
a small clock_gettime(CLOCK_PROCESS_CPUTIME_ID) FFI, not trace.profiler.
Whole-process CPU/RSS come from wait4. No source is modified during the matrix.
Cumulative whole-request heartbeats have not been made equivalent to an
untransformed budget-limited request: the measured passing examples must not
be generalized into timeout/outcome transparency for arbitrary requests.

The v1 curve is **negative end-to-end**: whole-process medians ~1.85s original,
~5.5s transformed. The child-check/write stage is0.192/0.143/0.149/0.194s for
k1/2/4/8; CPU increases0.220→0.593s. Ordinary module reimport/audit/export takes
~3.44s. Splitting also loses reduction sharing. No8x or old hand-written grid
speedup is transferred to this real target. The original arm does not serialize
a final .olean whereas the split pipeline does; v1 retains that exact output
boundary and is not an artifact-matched service comparison. A corrected
original-output control is needed before a matched pipeline ratio.

Failed qualification points are retained: missing psutil prevented any native
start; wrong writeModule namespace caused a frontend failure; missing FFI
interpreter alias caused an abort; requiring zero axioms instead of equality
with the original caused an overly strict rejection. The alias and axiom
comparison were corrected before the frozen15-cell run.

## Static and native coverage

The available build-source cache contains13,952files/148,021sites, not the whole
163,097-file corpus. That initial cache-only pass was retained under PVC
partial-build-cache-scan and is not published as the global ratio.
The full pinned public source archive is being acquired on PVC, checked against
the existing exact file-list/byte-count frame (not an added digest gate).

Native types for Grid,UMoments9,BarrierData41 were extracted from actual
mkDecideProof-headed auxiliary declarations: Grid has1536RBox equalities,
1536PointBox equalities and1536conjunctions; UMoments9 has1164CBox equalities;
BarrierData41 has1246Box equalities and74atomic comparisons. This explains why
looking only for surface quantifiers misses these particular hotspots.
Auxiliary counts are not blindly equated with source executions.

A separate E-core metadata panel reads W's completed no-M data, with no timed
rerun. Its first24metadata targets returned; the next4-target batch hit its90s self limit before output. Those types remain unknown, raw logs preserved; the global scan is pending. No full-corpus
splittable-time share is claimed.

## WRITE and REVIEW

Source, generator, explicit phase/whole-process CSVs, validation and literature
position are persisted here. Root owns paper integration; no paper edit.
Review is same-thread, with native positive/negative controls and preserved
failures. Broad parallel proof checking and certificate splitting are established
prior work; no novelty is claimed from their names alone.

Next: complete the fixed-frame census and cost-weighted scope analysis, preserve
unresolved types as unknown, and account for standard artifact output before
claiming a matched complete pipeline ratio.
