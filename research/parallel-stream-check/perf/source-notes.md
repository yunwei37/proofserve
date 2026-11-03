# Static source observations for the RC hypothesis — not a profile result

The measured4.34.1header makes persistent/compacted objects bypass RCupdates;
its shared-count increment is inline. Static disassembly of the exact binary
also contains inline atomic sites in type-checker/instantiation functions.
Absent lean_inc_ref symbols cannot establish absent RCtraffic. Conversely,
static LOCKinstructions do not establish that the measured workload executes
them. No RCstate distribution or sampled cycle attribution is measured yet.

The compiled local declarationOf conversion allocates a fresh outer declaration
when it cannot reuse the incoming object. C++constant_info construction from a
declaration reuses that declaration object, while kernel addition stores the
result in the environment. Thus a validated result can be structurally identical
to a persistent input yet have different physical lifetime/RCstate. Replayed
metadata, not every original proof expression, is a specific candidate for
shared counters. Whether the actual retained objects become MTand dominate
cycles remains an inference to test, not a conclusion.

- [ConstantInfo construction](https://raw.githubusercontent.com/leanprover/lean4/v4.34.1/src/kernel/declaration.cpp)
- [Environment insertion and lookup](https://raw.githubusercontent.com/leanprover/lean4/v4.34.1/src/kernel/environment.cpp)

Constant inference obtains an environment entry before instantiating its type;
normalization/definitional equality also performs repeated constant access.
Those paths provide concrete places for RCand lookup costs to appear.
The theorem insertion path additionally canonicalizes persistent terms before
checking, so hash-consing/canonicalization must be considered separately from
semantic whnf/defeq. The matched sharecommon header/source was subsequently
read directly: its tables belong to each helper instance, and the theorem
path constructs a local helper. A hypothetical global hash-consing-table lock
is therefore not supported by that path; local hash/allocation/cache costs
still need measured samples. This is a source observation, not measured time.
- https://raw.githubusercontent.com/leanprover/lean4/v4.34.1/src/runtime/sharecommon.h
- https://raw.githubusercontent.com/leanprover/lean4/v4.34.1/src/runtime/sharecommon.cpp

- [Type checker](https://raw.githubusercontent.com/leanprover/lean4/v4.34.1/src/kernel/type_checker.cpp)
- The local frozen ParallelCore.c / SDKinclude/lean/lean.h and static-sites
  outputs are retained on the PVCperf point.

P1already uses task dispatch, so a one-to-two-worker ST->MTtransition is not
assumed. Even fixed atomic instruction counts can cost more cycles under
contention. IPC, reference cycles, HITM/locked-load counts and sampled
instruction locations are needed to distinguish contention, extra work,
frequency and placement/migration effects. Do not optimize Lean in this step.
