# W059: exact import-name sets have low top100coverage

## EXPERIMENT
Complete untimed E8–15 graph analysis at pinned4eaee875.163,097module partition:
143,637direct-name sets;141,573internal-transitive-plus-external-frontier
classes;143,745ordered-direct sequences. Top100cover8,061/8,074/8,061modules
(4.94246%/4.95043%/4.94246%). Unlimited exact direct-name classes have19,460
potential repeated loads,11.93155%of unweighted requests, before native-state
correctness/first-load/cache-capacity costs. No timing claim.

Independent class/membership census reconciles all163,097counts for each
partition; ordinary set/BFS checks200closureclasses/310members,all pass.
Rawall-class/membershipgzip stays PVC; smallsummary/top100/histograms published.
Leader peakRSS2,260,116KiB, not a whole-W synchronized peak. No native process
started by the analysis; concurrent noM timing group remains preserved.

## WRITE
Explain closure's3,529unexpanded external frontier nodes, implicit/prelude/
options/import-order limitations, and membership vs true cache-hit/CPU share.
Whole-set warming is limited by observed population concentration; common
subsets/Mathlib prefixes are separate unmeasured policies, not ruled out.
No partial-graph key is called a semantically sound environment cache.

## REVIEW — self-review
User requested existing-graph, no-generation, untimedEanalysis; exact counts
and independent BFS supply it. No approximate hashes, all-source scan scope
unchanged, ordered alternative checks one known source of overmerging.
No root paper or M/O source edited. New noM sample is not prematurely counted
as complete and no old-Mdenominator returns to the estimator.
