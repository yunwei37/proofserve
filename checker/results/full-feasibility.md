# Full-source feasibility and retained-closure qualification

This report separates static planning, completed development qualification, and
future final performance evaluation. No full-corpus or final-matrix run was
started. Initial controls used CPUs 8–9 and a 16 GiB limit. The authorized
continuation used E cores 17–23, two kernel workers, at most 40 GiB, an 8 GiB
node reserve, and no P-core lease. Its native source exactly matches commit
2df1d9d70259d2630edda2aa1a4a8663753e5f9d.

## 1. Complete request frame and grouping

The pinned request contains 163,097 unique source module names: 162,840 ordinary
source-root mappings and 257 nested Hodge mappings. Both share one pinned
toolchain/options/search-path environment. They are not two independent Lake
toolchains. The retained requested-root lists identify every source unit.

The known static graph has 174,537 nodes and 660,205 edges. External imports
come from 11,264 source modules and 135 retained .ilean headers; 41 external
edge sets remain unresolved. At lookup time, three of those 41 had compiled
artifacts in the frozen path and 38 did not. Subsequent W builds are not
inferred from that snapshot. Closure counts are planning lower bounds for the
known graph, not artifact readiness or completed native verification.

| Grouping | Batches | Maximum loaded proof closure | Sum of module entries | Sum / 163,097 |
|---|---:|---:|---:|---:|
| Lexical 500, no umbrella expansion | 69 | 142,124 | 924,870 | 5.67 |
| Lexical 500, assumed empty umbrellas expanded | 208 | 44,660 | 2,518,486 | 15.44 |
| Lexical 1, same expansion | 8,911 | 43,914 | 87,149,170 | 534.34 |
| Largest terminal closure first, 1 | 1,714 | 43,914 | 17,061,109 | 104.61 |
| Dependency-first 500, replay imports | 327 | 44,051 | 4,047,413 | 24.82 |
| Dependency-first 500, completed-module reuse | 327 | 44,051 | 174,537 first checks | 1.07 |

The last row still reconstructs 4,047,413 imported module entries; it does not
turn those loads into one load. Its maximum first-time batch is 11,244 modules.
Static expansion assumes 52 lexically import-only namespace modules. Execution
instead inspects actual compiled private constants and names, including Main
leaves. Source text alone never establishes emptiness.

Existing closure calibrations span 0.0625–0.2309 CPU seconds per module.
Lexical 500-root replay gives a scenario range of 43.7–161.5 CPU hours:
20.2 hours at ideal 8-way speedup, or 80.8 hours at an illustrative effective
2-way speedup. The latter exceeds three days. These are scenarios, not bounds.
The legacy count-only peak estimate is also above 53 GiB.

Unique replay gives 3.03–11.20 CPU hours before imports, hashing, planning,
checkpointing, and fallback. An imperfect retained default-check import/leaf
proxy adds about 1.98 CPU hours, giving a high scenario of 13.17 CPU hours,
or 6.59 hours at effective 2-way speedup. Expensive computation-heavy modules
are not represented adequately by these mean rates. This is not a wall-clock
guarantee or an observed whole-corpus speedup. The CSV retains every assumption.

## 2. Design decision and largest-context limit

The original repeated-replay procedure is not an adequate whole-corpus plan.
The implementation now orders roots by dependencies and reuses a module only
after a completed original-kernel receipt and matching local artifact bytes.
The original importer reconstructs its real context; new proof bodies still
reach the original kernel. Incompatible combined contexts use module-local
checking. Local receipts and ordinary hashes are trusted checkpoint state,
not cryptographic proofs.

Input identity scanning finishes in a separate child before replay starts.
Cached provenance reads the importer's resident ModuleData instead of loading
a second compacted copy. A real 11,478-module / 32,966-part identity control
matched the previous identity exactly and verified equal import-name lists
across all artifact parts. Source layout mismatches fail explicitly.

None of this eliminates an oversized original import context. Original-importer
controls had wait4 maximum RSS of 5.954 GiB for Mathlib's 10,744-module context
and 7.283 GiB for SubexponentialSAT.Main's 13,835-module context. A two-point
affine extrapolation to the static 142,124-module OAI context is 62.415 GiB,
above the 53 GiB planning threshold. It remains an extrapolation, not an actual
OAI measurement or proof that it cannot fit.

Whole-corpus capacity is therefore unqualified. The static graph has no
incoming edge to OAI. If produced artifacts confirm that property and zero own
declarations, the maximum planned scope can check the other 163,096 source
units and leave OAI context compatibility explicitly incomplete. It must not
be relabeled as complete module acceptance. The exact conditions, root-file
command, and conditional coverage-sidecar example are in
../docs/large-library-checking.md. No new kernel mechanism is proposed.

## 3. Actual 14,721-module retained case

The resumed public checker completed all 14,721 SubexponentialSAT-frame modules:
9 batches, 14,720 original-kernel module entries, and one remaining zero-own-
declaration context check. It loaded 86,150 certified import entries across
batches. Those imported proof bodies were not replayed again.

The selected 3,977 source roots reach exactly the original 14,721-module frame
in the retained compiled import graph. Acceptance equals O's full stream set,
recomputed from its 30 raw segments. O's partial module-local original-kernel
reference union was also recomputed from raw outputs: 13,208 legacy plus 1,193
later references, with the retained artifact hardlinks checked.

| Reference | Available modules | Compared | Acceptance differences | Unreferenced |
|---|---:|---:|---:|---:|
| O retained complete stream | 14,721 | 14,721 | 0 | 0 |
| O module-local original-kernel references | 14,401 | 14,401 | 0 | 320 |

This is not a completed 14,721-module official CLI ledger. The 320 missing
module-local references remain unknown; they are not rejections or matches.

| Observation | wait4 maximum single-process RSS | Sampled process-tree RSS | Charged cgroup peak |
|---|---:|---:|---:|
| Historical O stream, 14,721 modules | 14.731 GiB | unavailable | 10.229 GiB |
| Completed 40 GiB continuation | 25.864 GiB | 26.062 GiB | 21.415 GiB |

The new case has a higher observed peak. This is not evidence of a memory
saving on this workload, nor an isolated causal comparison: implementations,
concurrency, process layout and resource points differ. The completed run fits
the authorized 40 GiB point; it did not fit the earlier 16 GiB point.
Earlier stops at about 16 GiB, the root-order binding failure, and the known
missing-import false rejection are preserved separately. All completed
certificates survived. No failed attempt was imputed as a complete sample.

The last continuation's 3,575.54 seconds and 3,853.14 cgroup CPU seconds describe
that resumed invocation only. They exclude earlier attempts and must not be
presented as one continuous fresh-run cost or a final paper benchmark.
The original reference clocks and failed/partial clocks are not added into a
fictional end-to-end duration. The final axiom report contains 15 declared names,
including sorryAx and Lean.trustCompiler; acceptance is not an axiom-free claim.

Native correctness controls cover three malformed proof classes, bad hidden
dependencies before certification, changed certified files on resume and
between live batches, a changed completed but unused input, scope violations,
canonical root binding, and cached imports across segment restoration.
The portable native suite passes. Three Python planning/matrix tests use
explicit stubs and are not native proof or performance evidence.

## 4. Frozen one-command workflow

After W's actual completed census, retired controller, and quiet-machine
handoff, the prepared launch is:

~~~sh
taskset -c 17-23 python3 checker/bench/release.py /workspaces/.agent-state/gpu-smt-captures/checker-full-feasibility-20261104/final-release.json
~~~

Confirm actual W artifact, terminal and launch paths first; the saved config
currently names planned paths. If the CPU allocation changes, inherit the
new authorized preparation affinity. The workflow freezes a clean source
commit, executable and SDK record; binds the complete source manifest to the
actual Lake-selected artifacts; tests import-context capacity; then performs
whole-corpus checking, the fixed final matrix and official controls, followed
by PlanarPacking. It stops on failed capacity and does not silently reduce
the denominator or fabricate the conditional incomplete sidecar.

The real portable workflow control completed on a three-module fixture:
clean commit 2df1d9d7, binary freeze, one controlled launch failure returning
126, preserved failed row, explicit successful retry, native checking,
official default/fresh calls, and result export. Nine actual workflow rows
are retained in workflow-qualification/. Its matrix and Planar labels refer
to the fixture routes, not real Grid or PlanarPacking data. Every row is
qualification-only. The real CLI also rejected container /tmp before directory
creation or Native launch. All native guards and both controllers retired.

## Remaining work

W has not passed its gate or produced the full artifacts. The 41 external
edge sets and actual OAI capacity remain unresolved. No full-corpus checking,
quiet final matrix, matched interruption-overhead experiment, or real
PlanarPacking comparison was started. O's independent checker review remains
separate. The conditional largest available declaration scope is documented
but is not a completed corpus result.

Raw captures, exact binaries, source snapshots, failed attempts, identities,
reference ID lists, and the reduction script remain under
/workspaces/.agent-state/gpu-smt-captures/checker-full-feasibility-20261104.
Only small tables and records are committed.

To reproduce the static plan without a native build:

~~~sh
taskset -c 17-23 python3 checker/bench/plan_full.py --manifest /workspaces/.agent-state/gpu-smt-captures/workloads/census-163097-20261104/manifest.json --out /workspaces/.agent-state/gpu-smt-captures/OWN-PLAN
~~~

Use a new owned directory. The runtime checker independently reads actual
compiled imports; the static graph never substitutes for kernel checking.
