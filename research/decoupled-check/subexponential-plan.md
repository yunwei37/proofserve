# SubexponentialSAT complete-directory cost plan

Review: 自审. Pinned openai/math4eaee87548250b2682affda7d05d947c05554bae,
Lean4.34.1/5045d005, Mathlibd13f23b7. Exactly3977 source files under
OAI/Algorithms/SubexponentialSAT (35,509,858bytes); a similarly named
ComparatorChallenges.SubexponentialSAT file is outside this directory and
is not included. Full native-header closure14721nodes:3977new target inputs,
10744exact retained common typed artifacts. No external OAI subtree.

## Before-run estimate and the user's12h decision

Matching Falconer production has2461targets/6918.855422CPU-s, mean
2.811400s/target. Applying this **planning scenario**, not a
prediction bound, gives3.106CPUh for the3977new source files.
Falconer's2038.443942checkerCPU-s/13205closure modules transfers to
0.631CPUh for14721nodes, including startup/checkpoint work.
The complete comparison's source-plus-check CPU estimate is
**10.785h**, including the actual
**7.048263h** retained common source work, which remains charged to the
denominator and is not executed again.

**Remaining native work now** is about
**3.737CPUh** for production
and stream, plus a separate**2CPUh** module-local reference qualification
reserve: **5.737CPUh**
from this point. Both the full comparison scenario and remaining work are
below12h, so a finite pilot is justified. Lock waiting is additional elapsed
time, not charged Lean CPU. The reference reserve is not included in the
production/check ratio. These are fallible transfers: file size and absence of
+kernel do not guarantee inexpensive proofs (Ramsey K10 is a counterexample).

After the first25-source window, reestimate using actual new CPU; after
larger prefixes, retain heavy-tail uncertainty and stop rather than press
on if the remaining-work estimate exceeds12h. No claim of completed
SubexponentialSAT validation follows from this preparation.

## Protocol

Reuse the repaired producer's complete original SDK/Mathlib/package runtime
providers; only new OAI artifacts enter the producer overlay. Recompiled core
terms never replace executable SDK modules. Every original source/options is
unchanged (-DautoImplicit=false), emits olean/ilean/C, with user+system CPU
and wall inside its own external cgroup (11.75GiB +256MiB parent reserve).
No Lean-M. P0–7/shared flock, join after waiters, one O native task at a time.
Per-call1400s, outer1740s; at most25 source calls per window, with new calls
started only in the first200s. First real failure or disk>=85% stops.
No second O task is queued before the Ramsey sampled-reference episode retires.

A fresh original kernel streams the complete dependency closure in500-node
certified-checkpoint segments. Every retained source cost is counted once.
Acceptance must equal the exact measured-source closure and original
module-local reference set. Only then report a complete ratio alongside
Falconer6.31% and matched-protocol Mathlib8.95%. Startup/import/export are
included; reference qualification is separate. A bounded unsuccessful or
partial episode is reported as such, never as full-directory cost.


## Static risk check before the pilot

All3977source files were read without Lean. There are0explicit decide+kernel
or native_decide/decide+native tokens, but **26593plain by-decide sites across
1932files**, so marker absence is not evidence of a purely noncomputational
regime. The largest file is147641bytes, versus multi-MB Ramsey certificate
samples. These lexical counts include comments/strings and are not a
cost predictor or semantic interval classifier. All six sorry/admit matches
were read: they are English 'admit' words in comments, zero 'sorry' tokens;
this is not a dependency-axiom audit. See subexponential-input-census.json.
The empirical pilot and per-window12h reassessment remain necessary.
