# Initial backend qualification — 自审,2026-11-03
Original-kernel parallel stream and copied O checkpoint reader are built as a
new portable Lean package. Default persistence and split fallback are enabled;
both explicit release ablations available. New CLI and receipt1 are implemented.
Raw: existing PVC captures/checker-package-20261103,not committed binaries.

lake-build1 failed(missing C headers/ambiguous Options/JSON UInt32),build2 failed
(host fscanf symbol unavailable in matched SDK linker); both retained. Build3
and help completed. Build4 and5 completed. Initial import-heavy test reached
its90s finite limit on E cores; no cost or semantic success inferred. Tiny
portable tests avoid that expensive dependency; they do not establish real-library
performance. First tiny contract failed because Base was not a Lake library,
second exposed missing mutation enum support,both retained and corrected.
Build6 and portable-contract4 completed: correct2-module closure,workers1/2/4
same accepts and axioms,stock leanchecker parity,loose-var/unknown-constant/
wrong-sort rejection,one-module bounded checkpoint/resume parity,unknown declared
toolchain explicit error. These are functional development controls,not P-core
timing cells. Final checkpoint-lock build7 and portable-contract5 also pass,with all native\nprocesses and cgroups retired. Axioms include accepted segregated modules.
All native controls used finite external timeout and14GiB own-tree guard on E8–15.
No formal release matrix or external-project acceptance is complete.
Remaining: release Mathlib/Grid/Barrier1/2/4/8x3;8worker ablations;official scope
comparison; actual interrupted-process resume overhead;O release CI and external
projects. Segmentation does not remove cumulative prefix memory growth.
