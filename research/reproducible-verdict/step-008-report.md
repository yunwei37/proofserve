# Step008: preserve private-runtime failure; correct input closure and residency
2026-11-01UTC; EXPERIMENTv6actual partial; WRITEfailure+method correction; REVIEW自审.
v6actually acquired the lock and retired between observations. The attempted
unstarted-waiter cancellation asserted before any signal; no process was killed
or source modified. First cold native exits1at12.079s, peak1458552KiB,
no resource event and zero candidate rows. Cause: copied .ir files but omitted
.ir.sig files; Probe itself fails IR compilation at CollectAxioms. This is not
a Lean-candidate rejection, monotonicity counterexample, or completed cache pair.
All v6source/input/runtime/raw failure records remain unchanged.

v8forward correction copies .ir.sig too, checks a private-runtime6-case
qualification before candidate cells, and verifies residency only after ALL
files are treated (immediate per-file checks overstate final warm residency).
Runtime copying runs bounded on E8-15; native verification remains P0-7/flock,
no-M/14GiBguard withinM16. Space is checked against copy payload/metadata.
Own retired v6private data may be hardlinked into v8to avoid another8GiBcopy;
original live SDK/Mathlib input inodes must remain different. Old file bytes and
raw outcomes are preserved; no live other-lane inputs evicted or deleted.
v8controller292324/birth762016923 is a real -> waiter behind O290929/W290953
at launch. It is the sole own queued task; no actual new verdict claimed.

New matched math/kernel batch source and analysis are prepared; no runtime
qualification yet. Regionselection includes the retained6.16s Envelope kernel
target explicitly, avoiding only tiny lexicographic targets.
A re-analysis of v2gives184B1000-pass→B3000pairs over all tested observers/
frontends/thread settings, zero acceptance violations; separate from v3's
100five-step comparisons. These are configuration observations, not284unique
independent candidate pairs and not a universal monotonicity proof.
