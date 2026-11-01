# Private-inode cold/warm runtime experiment
Prepared2026-11-01UTC,self-review. v3evicts only request JSON; that does NOT
answer SDK/Mathlib page-cache sensitivity. v6copies runtime input types
(.olean variants/.ir/.so) plus identical Lean executable into private inodes
on the existing PVC. Actual estimate8.237GiB,~72500files;35GiBfree.
No download/rebuild/global drop_caches/sysctl/source-inode eviction.
Same copied paths in both conditions; mincore measures residency after
DONTNEED or pread. System libc/loader/page tables remain outside treatment.
512observations,256cold-warm pairs:16sources x2frontends x2budgets x2threads
x2repetitions x2cacheconditions. Copy/advice is preparation outside native
timing but inside the finite shared-lock task. Whole1690s/outer1740s,
pernative180s/no-M/P0-7/14GiBguard plus reserve within M16.
Runtime copies stay outsideGit; remove only these copies after preserved
results and an own-directory cleanup record. Prepared, not launched.
