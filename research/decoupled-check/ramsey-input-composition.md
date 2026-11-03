# Ramsey input composition and measured-denominator boundary

Review: 自审. Input is the unchanged openai/math commit
4eaee87548250b2682affda7d05d947c05554bae. This is an offline census of the
444 Ramsey sources already extracted for the running comparison; it executes
no Lean process and adds no timed work.

| Textual class | Modules | Source bytes | decide +kernel occurrences |
|---|---:|---:|---:|
| ordinary-proxy | 264 | 36078209 | 0 |
| kernel-marked | 180 | 186536353 | 396958 |

The marker is a static proxy, not a measured kernel-time classification.
The regex \bdecide\s+\+kernel\b is applied to the unmodified text;
comments/strings are not parsed, and marker absence does not establish that
kernel conversion is cheap. The per-file input rows are in
[ramsey-target-census.csv](ramsey-target-census.csv).
Ramsey is therefore not interchangeable with the no-marker Falconer branch.
Its complete-closure result must be reported as a mixed mathematical and
computational workload. No measured marker-class checking ratio is claimed.

The source-work denominator includes all 11,188 closure nodes once: 10,744
common dependency nodes whose exact immutable terms and compiler costs are
retained from the same pinned capture, plus 444 newly produced Ramsey targets.
It measures original Lean elaboration and output of .olean, .ilean and C
source, including each call's imports; it does not include an external C/C++
compiler or linker, and is not a fresh parallel Lake build's elapsed time.
Common source work alone is 25,373.748385 CPU seconds (7.048263 hours).
New target cost is unknown until the source cursor completes.

The checking numerator will recheck all 11,188 modules through the original
kernel in this Ramsey run, including checkpoint export/restore and any local
fallbacks. Independent module-local parity work is reported separately.
A ratio over the whole closure can hide a high target-only compute cost
behind a large common dependency denominator; both source components will be
listed. Without matched per-target checker measurements, subtraction from
an older dependency-only run would be a cross-run estimate and is not done.

The retired global attempt still accepted only 2,488 / 163,097 source IDs and
10,744 dependency IDs, with 0.694505 kernel CPU hours, 9,124 producer errors
and 151,485 blocked nodes. Neither that partial denominator nor the model
forecast is substituted for this full-directory experiment.

## Source-token check relevant to the two cost regions

All444unmodified target source texts were scanned, including comments and
strings. There are zero occurrences of each of these tokens/patterns:
native_decide, sorry, admit, debug.skipKernelTC, and maxHeartbeats followed
by0. The raw per-pattern result is retained onPVC in
source-option-token-census.json. By contrast,396958decide +kernel markers
occur across180target files, as listed in the per-file census.

This is source-level characterization only. It does not establish the absence
of axioms in imported dependencies, prove that any candidate checks, or replace
the planned complete original-kernel and module-local acceptance comparison.
It helps distinguish this selected directory from a workload whose visible
proofs delegate reduction to native_decide or skip the kernel explicitly.
The original successful source cells and their exact typed artifacts remain
the inputs to the primary check.

## Authored project settings checked against the pinned archive

The complete pinned lean/lakefile.lean and lean/lean-toolchain were read from
the retained source archive. The only package/library option-setting line is
leanOptions := #[autoImplicit,false] in the OAI package; there are no further
leanOptions/moreLeanArgs/weakLeanArgs overrides or kernel-skip/heartbeat/depth
settings in that configuration. The measured target flag -DautoImplicit=false
therefore matches the authored package setting. Leanv4.34.1 and the Mathlib
d13f23b723b8a846827a245b89c10fc7d3f11612 pin also match.
See [the extracted settings](ramsey-project-options.json); full raw metadata
remains onPVC. Per-source set_option commands are left unchanged.

The author's Lake file explicitly declares and pins external project
dependencies. The41missing external module artifacts are absent from this
capture's prepared provider paths; the census must not be described as41
dependencies omitted by the upstream corpus. Ramsey and the chosen next
Transonic closure do not require an additional external OAI subtree.
