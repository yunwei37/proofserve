# Rebuilding and reading the ProofServe paper artifact

The manuscript is a six-page empirical + system paper. Its current revision
uses the named author line and separates background, measurement, findings,
ProofServe, limitations and related work. Detailed run bookkeeping belongs here.

All work in the shared research Workspace enters through taskset -c 8,9.
No command below is needed to launch a new measurement for the paper.

## Current manuscript

Title: "AI Now Writes Lean Proofs Faster Than Lean Can Check Them". Claude
rewrote main.tex on 2026-11-07 around the storyline the user fixed that day
(see docs/user-instruction.md): as AI improves, can checking keep up with
what it writes? Figure 1 compares, for every file, the time a model needs to
write it at 100 / 1,000 / 10,000 tokens per second with Lean's first-check CPU
time from the census and, for 200 sampled files, the re-check CPU time from
data/generation-vs-checking (commit 1c84dd21). The text is written without
negation expressions, at the user's request.

    python3 docs/paper/figures/plot-gen-vs-check.py data/openai-math-4eaee875/census/modules.csv.gz data/generation-vs-checking/tokens.csv.gz docs/paper/figures/gen-vs-check.pdf data/generation-vs-checking/sample.csv
    python3 docs/paper/figures/plot-cost-regimes.py docs/paper/figures docs/paper/figures/check-vs-compile.pdf
    python3 docs/paper/figures/plot-census-concentration.py data/openai-math-4eaee875/census/modules.csv.gz docs/paper/figures/census-concentration.pdf

The Grid excerpt is abridged from lean/OAI/Analysis/PlanarPacking/Grid.lean at
openai/math 4eaee875 (590 lemmas, 1,664 decide +kernel calls). Build with
latexmk -pdf from docs/paper. generated/observations/ and figures/cost-regimes.*
belong to earlier revisions.

## Rebuild from committed measurements

From the repository root, with Tectonic available:

    python3 docs/paper/generate_observations.py --root . --tectonic /path/to/tectonic

This performs offline reductions only. It reads the committed module ledger,
profile summaries and release-tool summaries, and produces:
- generated/observations/observation-summary.json: unrounded statistics and input commits;
- cost-share-P.csv and cost-share-E.csv: cumulative CPU shares, sorted by cost within each pool;
- cpu-concentration.tex/pdf: the cumulative-share plot;
- memory-guard-table.tex: three-repeat plain-run guard controls;
- release-evaluation-table.tex: installed-tool scaling and external costs.

It also compiles figures/cost-regimes.tex from the retained pair/target CSVs.
No Lean compiler, checker, profiler, collector, queue or agent is started.
Figure-only engine notices about reading /dev/null are recorded in the summary;
they are not suppressed or represented as main-manuscript layout warnings.

Compile main.tex with Tectonic --keep-logs from docs/paper, or copy its source,
references.bib, figures/ and generated/ into an external build directory first.
Inspect the complete compiler stdout/stderr and main.log, not only overfull
boxes. Use pdfinfo to check six pages, then render and inspect every page.
The paper uses 10pt Times, two columns, ragged-right text/captions and ragged-bottom
pages. No warning/badness threshold is raised.

## Finding-to-evidence map

| Paper observation | Committed input | Interpretation |
|---|---|---|
| Target checking retains 80–82% versus 0.5–7% of compilation wall time | figures/cost-regimes-target-wall.csv; data/openai-math-4eaee875/ and evidence.md retain raw provenance | Target read/map/replay after dependency preparation, divided by that module's compiler-process wall |
| 31 whole-process checker/compiler CPU pairs | figures/cost-regimes-cpu.csv | A distinct process-level clock, not target-only or logical-kernel phase CPU |
| Cost concentration, medians, examples, source-size association | data/openai-math-4eaee875/census/modules.csv.gz and top20-cpu.csv | Completed rows only, P/E separately; no extrapolation |
| Default targets omit files/call sites | data/openai-math-4eaee875/ source inventory and generated/census summaries | Full static source frame, separate from completed-cost frame |
| Import-only controls and short-module checker costs | research/profile-2026-10-31/startup-replay/startup-analysis.md, repaired-replay-analysis.md and CSVs | 13 modules selected by historical build time; material observer cost; build/checker runs not contemporaneous randomized pairs |
| Import hotspots and resident memory | startup-replay/perf-hotspots.csv, import-memory.csv | 9.29%/5.69% are the separate perf-all-mathlib profile; file-backed PSS is not mutable heap or hard RSS |
| Native memory guard | research/profile-2026-10-31/systime/final/README.md, native-summary.csv, operations-summary.csv, syscalls-summary.csv, artifacts.csv | Plain timing, sampled cycles, syscall traces and artifact equality have distinct clocks/denominators |
| Module discovery and official-mode examples | data/lean-observations/README.md, timings.csv, discovery.csv, cases.csv, examples/ | Single large/small path contrast; controlled compiled/altered artifacts, not a false theorem from normal source |
| Installed ProofServe evaluation | checker/results/release-e000ed62bbf4/matrix/; data/external-projects/e000ed62-final/ | Original release-tool data, not historical profiles or prototype timings |

Every number newly selected for the manuscript already existed in these committed
inputs. The new CPU shares, Spearman ranks and curves are reductions of those
measurements, not new experiments. The script records input-publication commits.

## Compilation population, clocks and selection

Publication cc5bcc18 contains 162170 completed executable modules of163096.
The926 deferred modules have no successful cost; one configuration unit is
outside the executable frame. Completed rows in a family remain even when its
unfinished remainder was deferred. There were no final native failures or
failed-dependency blocks;66 unsuccessful/interrupted attempts are separate.

Successful P/E CPU is168.955932305/302.399244343h, unconverted.
The chronological execution intervals are:
1. fixed22-slot admission plus draining/exclusive retry,128331 completed,
   134.651176009P /256.667855090E CPUh,24.624732950wallh;
2. memory/headroom admission plus family deferral,33788 completed,
   32.717748677P /45.731389253E CPUh,6.178604211wallh;
3. continuation of the second admission rule,51 completed,
   1.587007619P /0E CPUh,.725697047wallh.

Measured execution walls sum to31.529034208h. Calendar span33.085971073h includes
5604.972714s of pauses. Execution wall includes preparation, all attempts,
hashing, publication and cleanup; successful CPU excludes failed attempts.
Per-module wall sums are not makespan. No old withdrawn deadline clips successes.
Source/measurement commits9389daff/05c91979/b5035842 and all UTC boundaries remain
in the source README/segments registry, not in the manuscript narrative.

The top1% means ceil(.01 * completed pool population):823 P /800 E modules,
25.1063%/25.6892% CPU. P/E medians are3.959777/7.541694s.
The source-size/CPU Spearman coefficients are0.615179/0.604140, with tied ranks
averaged. File size is therefore associated with cost; it is not accurate to
say the two are unrelated. The extreme examples are:
- OAI.Analysis.FreeWords.UltraExpectationFull:15860bytes, no decide+kernel,
  E CPU9313.899945s;
- OAI.Combinatorics.Ramsey.CycleClique.Construction.CertificatesK17Part012:
  5287058bytes,11114 call sites, E CPU2241.232406s.

The5848 marked completed modules use17.8897% P /18.3453% E CPU.
The full static frame has163097 source/configuration units,32263 outside the
default graph; executable-only outside is32262. Omitted sites are451008/1354379.
These are separate denominators. The observed outside-graph cost is
30.881815210P /56.237268054E CPUh. No original42 calibration or model fills the tail.

## Counter selection and profile interpretation

The four-condition,20-module qualification compared P/E and quiet/loaded runs,
three repeats each. Total-instruction spreads had median1.331198%/P953.149811%,
above the original1%/3% criteria. That criterion failed and was not changed.
User-only spreads were selected after observing the difference:
median.017559%/P95.144424%. OS-kernel counts had median8.616206% spread.
This is post-hoc metric selection, not a substitute passing gate or universal
invariance proof. Process user-mode counts do not attribute Lean-kernel work.
Full counters and failed-gate decisions remain in measurement/census-gate/.

The startup cohort used historical short-build times for selection, with three
build/import pairs per module. Import-only per-module wall medians have median
1.355s; their wait4 peak-RSS median is3.113GiB, and PSS file fraction92.89%.
The stock checker ratio1.2805 includes discovery/import/replay/cleanup.
Historical startup options and sampling differ from the main no-M campaign;
they must not be relabelled new no-M measurements.
The separate Mathlib profile, not a pooled short-cohort profile, supplies the
9.29% lean_mark_persistent /5.69% lean_name_eq observations.

Memory-guard controls retain an outer15GiB cgroup in every arm; baseline native
guards are-M8192 for Grid and-M9216 for the others. Ninety passing outcomes
and all produced baseline-comparable artifacts agree, as detailed in artifacts.csv.
The baseline kernel-cycle percentages and syscall elapsed times are not
fractions of plain wall time. There is no no-M perf-record arm.
Grid no-M system CPU spans101.35–213.35s despite wall303.20–320.61s.
Observer overhead is material: its stat control adds7.25%wall /126.98%systemCPU.
Do not pool plain/stat/record/trace clocks or turn these three cases into a
library-wide correction factor.

The large/small search paths resolve the same unchanged Nat.Basic artifacts
using same-inode hardlinks. The full checks take322.853078947/.394341134s.
The discovery probes are separate runs, not additive phases of that full check.
The missing-private and mutated-proof tests are intentionally altered artifacts.
The explicit ofReduceBool example uses a special native-evaluation bridge;
its fresh-mode limitation is not a result about ordinary decide+kernel.

## Release-tool versions and incomplete configurations

The frozen checker is e000ed62; original matrix drivercc5bcc18 and publication818f7422.
Receipt v1, child ABI6 and independent-closure statev8 bind compatible checkpoint
state. Earlier e155 isolation costs do not replace current strict costs.
The two read-only review reports (e0c92d51/2628d727), implementer regression
results and absence of independent repaired-binary runtime review remain in
packaging/checker-review-*.md and checker/results/theorem-body-policy/.
The historical SubexponentialSAT repaired replays e0c92d51/3fe83c5a agree;
module-local reference coverage is14401/14721, with320 unreferenced.
These development records are not the main empirical narrative.

The matrix's71 planned cells yielded61 returned attempts and10 unrun cells.
Barrier two/four-worker configurations were in the initial plan and were
removed to fit the six-hour collection budget.
Unrun: Grid strict r2/r3; Grid/Barrier official default/fresh r2/r3.
Nat.Basic official-fresh r3 was attempted and stopped by the overall window
after77.703905s. It is not one of those10 unrun cells.
Grid strict r1 timed out after1800.010274s; its CPU is not a completed strict cost,
and no three-repeat Grid strict median exists.
Only complete three-repeat points receive matrix medians.
Official samples with fewer repeats retain their counts/ranges in the CSV.
The one deliberate interrupt/resume includes killed work and gives16.94%extra
wall /10.68%CPU, not a repeated population estimate.

For exact matrix/external tables, retained failures, controls and reproduction:

    python3 docs/paper/generate_system.py --help

Use the final matrix and e000ed62-final measurements/status paths described by
their READMEs. Existing generated/system/ holds the full original tables,
strict bound, ablations, failed-attempt ledger and unattempted-cell list;
the readable paper table only selects their main installed-tool results.
External publication0516279d uses tool818f7422, nativee000ed62 and Lean4.34.1,
one uninterrupted fresh-checkpoint run per arm, one worker.
Inputs Newspeak/Solar/AI are e2232d8f/f4f5c9a1/3042904c.
Native closure versus official local-root duties differ, so no equal-obligation
speedup is calculated. The AI corpus is an upstream collection-level attribution,
with model/AI/human proportions undisclosed. The AI cgroup has888 memory.max
events, zero OOM kills/resource stops; its cost is memory-bounded.
The installed archive is Debian13/glibc2.41-qualified, not the separate Ubuntu
workflow artifact. Fixed order, warm caches and observed background work remain
part of the reported conditions.

## Supplementary library checking, not a whole-library verdict

Publication5f491682 reports15 complete batch certificates:12756 distinct
closure modules, including968/162170 requested compiled sources.
161202 requests lack complete certification:271 accepted in completed segments
pending a whole batch,217 in-flight uncommitted accepts,1 attempted without final
verdict and160713 without an observed verdict. The488 uncertified accepts are
not added to the certified set. The926 deferred sources and1 configuration unit
are separate. OAI lacks a compiled artifact, so capacity is unmeasured.

Admission stopped17:00 and the authorized drain ended17:15; exit124 is an
operational deadline, with no reported kernel rejection or OOM.
Closed-native-cgroup wall16530.349473379s /CPU16194.74918s includes interrupted work.
Sampled own-tree RSS9532841984B (8.878GiB) is not a hard RSS bound or cgroup charge.
No official-reference comparison on this prefix or whole-source verdict exists.
Root's earlier independent identity/partition/certificate-union arithmetic is
generated/system/library-check-validation.json, not an independent proof replay.

For the older compilation-derived CDFs and full interval/group summaries:

    python3 docs/paper/generate_census.py --retired --data data/openai-math-4eaee875/census --out docs/paper/generated/census --tectonic /path/to/tectonic

This also launches no Lean measurement. The new manuscript uses the CPU-share
plot instead of the old CDF. Old data and qualified derivations are retained.
