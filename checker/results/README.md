# Release-form evaluation

Only measurements from the committed proofserve-check and audit tools belong in
the paper's system evaluation. qualification.json is functional evidence, not a
performance result.

The fixed matrix contains Mathlib.Data.Nat.Basic, Grid, and Barrier at 1, 2, 4,
and 8 workers, with three fresh-checkpoint repeats at each point. Grid and
Mathlib.Data.Nat.Basic also have three 8-worker repeats with persistence disabled
and three with split fallback disabled. Official default and fresh comparisons
must disclose their exact scopes. A real interrupted-resume pair reports its
overhead separately.

A separate default-worker run covers every module in the fixed Mathlib source
tree. This is distinct from the 1,330-module Mathlib.Data.Nat.Basic closure.

Each timed cell records the executable commit, artifact roots, command, CPU,
wall time, peak RSS, accepted modules, shared P-core lease, and absence of -M.
Raw binaries and large snapshots stay outside Git.
