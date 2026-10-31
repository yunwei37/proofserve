# Exact import-set reuse opportunity in pinned openai/math

Untimed E8–15 analysis of all163,097modules at4eaee875, using the existing
source import graph. No native compilation, generated candidate or timing.
Exact tuples/integer bitsets are compared for equality; no approximate digest
can collapse different import-name sets.

|Key|Distinct classes|Largest class|Top100 modules|Top100 coverage|Singleton classes|
|---|---:|---:|---:|---:|---:|
|Unordered direct import names|143,637|4,415|8,061|4.94246%|135,421|
|Internal transitive imports plus external frontier|141,573|4,415|8,074|4.95043%|131,884|
|Ordered direct import-name sequence|143,745|4,415|8,061|4.94246%|135,617|

Top100coverage is membership, assuming those environments are prewarmed.
If each class must pay its first load, those100classes permit at most7,961
subsequent same-direct-class requests,4.88114%of all modules. A pool with
unlimited exact direct-set entries can avoid at most19,460first-load repeats
(11.93155%of requests); closure keys yield at most21,524(13.19705%).
These are unweighted static opportunity counts, not hit rates measured from
a schedule or fractions of import CPU saved.

## What closure means
The graph contains163,097internal modules and3,529external frontier names.
A closure includes every reachable internal dependency plus external names
directly imported anywhere in that reachable subtree. The target itself is
excluded. External Mathlib/third-party dependency graphs are not expanded.
Thus the closure result is exact for the retained source graph, not a census
of every imported constant/native environment in the complete toolchain.

A direct import set is not a safe native state-cache key by itself. Order,
import modifiers/visibility, implicit Init/prelude, options, toolchain and
extension state can matter. Ordered names are also reported, but modifiers
and hidden state were not reconstructed. Equal closure name sets likewise
do not prove equal extension insertion order or safe COW/replay.
Shared Mathlib subsets, partial-prefix reuse and loading a superset are
different policies; these counts do not establish their correctness or cost.

## Audit and retained detail
All class counts and163,097module memberships were independently reconciled.
A separate ordinary set/BFS implementation checked200closureclasses:largest100
and100uniform remaining classes(seed20261101),310memberchecks; all agreed.
BFSchecks cover sampled equivalence/cardinality, not every bitset computation.
All three partitions have exactly163,097members. Analysis leader peakRSS
2,260,116KiB; this is not synchronized whole-W peak or a native memory profile.

Small published tables contain all class-size histogram bins and top100 for
each key. Every class and count, full module-to-class membership and full
independent BFS records remain on the existing PVC at:
workloads/openai4341-import-set-classes-20261031/
  direct_import_set-all-classes.csv.gz
  internal_transitive_closure_plus_external_frontier-all-classes.csv.gz
  ordered_direct_import_names-all-classes.csv.gz
  module-groups.csv.gz
  independent-bfs-checks.json

Reproduce with analyze_import_sets.py --inventory static-4eaee875 --out
a new PVC directory. The program refuses to overwrite an existing capture.
The largest100exact import sets cover only~5%of requests; a whole-import-set
pool is therefore a limited coverage mechanism on this workload. No CPU/wall
speedup or reason to dismiss common-subset warming follows from that alone.
