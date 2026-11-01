# Measurement protocol (M lane, 自审)

The primary library task is the exact constructed 1330-module
Mathlib.Data.Nat.Basic closure used by O. O's unchanged stream-check binary is
the reference. Our audited serial mode isolates context-validation overhead;
parallel 1/2/4/8 isolates checked-frontier execution. Three full cold-process
cells of each variant, same artifacts and LEAN_PATH, no Lean -M. Persistent
filesystem page caches are not flushed; native ordering is sequential and
reported. Every completed cell must have all 1330 accepted module IDs equal
to the reference. Native errors, timeout and resource stops remain failures,
never zero-cost observations. The finite lock window may yield a partial
matrix, in which case no complete median/scalability claim is made.

## Computational leaves

A separate finite lock window handles one module and one repeat. The process
streams and checks its actual import prefix once. It snapshots the verified
prefix and checks the leaf with serial replay and parallel 1/2/4/8. Each parallel
trial must reproduce all serial typed constants exactly. The selected result is
then committed into the stream. Per-trial wall and process CPU are recorded;
whole-process wall/CPU/peak memory include the prefix, startup and all trials.
Thus an incremental leaf curve is not mislabeled an independent complete
module invocation or a whole-library speedup. File reading and graph planning
inside each trial are included when they occur; source compilation is excluded.

Grid and Barrier helpers were all <1s in the earlier native profile, so this
prototype uses declaration parallelism only there. The Envelope generator nominates all ten measured >=1s Fin31 helpers from the
complete large-goal CSV, rather than the top-five summary. All their chunks in
one ready frontier share a single bounded worker pool. It is a pinned,
artifact-specific certificate experiment, not a generic arbitrary-proposition
optimizer. Generated/schema coverage and actual native matched coverage are
reported separately.

Prepared support/chunk terms are read as untrusted ModuleData, not imported as
trusted facts or executed as metaprograms. The current stream's original kernel
checks support declarations, each chunk, and the final merge theorem. A chunk is
enabled only for an incoming ConstantInfo fully equal to the pinned original.
A mutated original proof falls back to ordinary checking. Bad chunks must be
rejected. No added axioms or sorry in payload; final root's transitive axioms must
be a subset of the original qualified [propext] set. Generic equivalence of
acceptance for all malformed future artifacts is not proved; real fixed input
and negative controls are the evaluation scope.

Source-to-certificate generation was performed before measurement, using the
earlier validated guard partition; its cost is excluded and disclosed. In the
new stream, payload read/check/commit and ordered merge are included. It removes
the previous second process, repeated import and file-export round trips.

## Limits and ownership

P0-7, the existing blocking pcore.lock, one timing task at a time. Preparation
uses E8-15, never a concurrent second Lean process. Each native run <=1680s,
outer window <=1740s, 14GiB external charged-memory cap and 1s own-RSS sampler
within the lane's 16GiB allocation. External time/resource interruption is not
a mathematical rejection. Raw data and large compiled files remain on PVC.
Only research/parallel-stream-check/ is edited. O's code is read-only.

The original mathematical kernel is retained. The scheduler/graph walker,
checked-token ledger and internal-ABI C insertion adapter are additional trusted
coordination code and are audited as such. Positive/negative tests do not prove
that code universally correct. Unsafe/partial source exclusions, complex-module
serial fallbacks, module-local context fallbacks and duplicate handling are
reported separately.

## Cost staircase

Label source build (serial summed compiler wall, same artifacts), original serial
stream (one full closure invocation), parallel stream (one full closure invocation),
and incremental computational-leaf trials as different rows. Do not reuse the
old 65.7s number as a fresh paired denominator. Do not equate stream acceptance
with source elaboration, dependency integrity/authenticity or full olean-extension
validation. Stock LeanChecker already parallelizes modules; this prototype tests
within a single persistent stream, not the invention of proof parallelism.
