# Ramsey CPU composition: matched primary result and separate attribution

Review: 自审. The primary Ramsey collector and original-kernel adapter are
unchanged. No new Lean compiler or profiling run has started for this
attribution. The C clock helper passes a syntax-only check; its generated
Lean adapter remains uncompiled and unqualified. The first generator attempt
had overescaped newline selectors and stopped before compilation; the corrected
generator now produces the intended instrumentation. Neither ran a measurement.

The primary complete-closure check/source-compiler comparison is expressed in
CPU seconds. The matched 500-new-module checkpoint baselines are Falconer
2038.443942 / 32292.603807 CPU-s = 6.312417%, and Mathlib Nat.Basic
91.145172 / 1018.219383 CPU-s = 8.951428%.
The older 9.26% and 14.67% numbers are wall-clock ratios, not conflicting
CPU observations. They must not be mixed into the CPU comparison.

The Ramsey static classes are 264 ordinary-proxy files and 180 kernel-marked
files; marker absence is not a measured conversion-time claim. The source
cost CSV can already be joined to the static census once construction ends.
The current primary checkpoint adapter does not record per-module CPU.
Therefore a mathematics-vs-computation checking ratio cannot be recovered by
allocating the process total in proportion to source bytes or marker counts.

After primary completion, the prepared observation-only adapter will repeat
the same exact frame, 500-module quota, original kernel and reference policy.
CLOCK_PROCESS_CPUTIME_ID readings bracket each module, subtracting recursively
visited imports. Exclusive module CPU covers typed-data reading, map/audit
work, kernel replay and local fallback for that node; checkpoint export,
restore and process startup remain in an explicitly unallocated residual.
No descendant is counted again in its importer. The process clock includes
CPU of all native threads.

The full source and checking totals and accepted module sets will be compared
to the primary run before using this diagnostic. Common dependency CPU,
ordinary target CPU, marked target CPU, and unallocated overhead will be
reported separately. Target-class checking/source ratios are diagnostic
exclusive-work fractions; the full-closure primary ratio includes startup and
checkpoints. Any measurement overhead or disagreement remains visible.
The profile copy never replaces the primary clock or proves a speedup.

All native controls and measured profile segments will use the P0–7 shared
flock, no -M, the existing external cgroup and finite per-task timeouts.
Compilation is preparation only; it waits until the current O native sequence
retires, so there are not two O Lean processes. No live collector source or
compiled module is modified.

## Actual source evidence revises the descriptive grouping

CertificatesK10 completed in1725.133882 CPU-s/674.563076 wall-s with no
+kernel marker. Direct inspection shows finite LayoutCertificate and
ForbiddenMatrix data and12872 ordinary by-decide proof tactics.
It is not a marker-free mathematical control.

The original180marked/264unmarked split remains in the CSV. Additional
descriptive groups are180kernel-marked,20unmarked-certificate-family,
24other-unmarked-plain-decide and220other-unmarked files. These groups
are not a validated cost-regime classifier. In particular, trivial decide
subgoals also occur in ordinary mathematics. Component attribution must
join measured per-module CPU to these distinct groups, keep unresolved
interpretations separate and not force every unmarked file into “math”.
No source CPU measurement is labelled kernel replay CPU. The primary
complete-closure protocol and accepted sets remain unchanged.
