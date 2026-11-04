# Checker evaluation

Final paper performance data are pending. The user reclassified all existing
ba316991 matrix cells as nonfinal previews because the workload build census
now controls the machine. The final frozen tool will be measured after that
census finishes and the machine is quiet.

loaded-preview-cells.csv retains the returned observations with an explicit
paper_eligible=false field. loaded-preview-qualification.json and
loaded-preview.md describe their functional scope. Do not use these timings
as the paper's final system evaluation.

The fixed final matrix remains Mathlib.Data.Nat.Basic, Grid, and Barrier
dependency closures at 1, 2, 4, and 8 workers, three fresh-checkpoint repeats
each. Grid and Nat.Basic also have three 8-worker repeats for each ablation.
Official default and fresh procedures have different proof ledgers and require
an explicit scope discussion. A real interruption/resume comparison is separate.

Full Mathlib means all 8,529 Mathlib directory modules plus the umbrella module.
Its loaded scale preview accepted 10,744 modules including dependencies; it is
distinct from the 1,330-module Nat.Basic closure.

The next capacity target is every module in the 163,097-source workload, after
the build gate and census. Independent closure batches bound retained kernel
state by one batch. Whole-corpus acceptance and capacity remain unverified.
The final performance matrix, official controls, and the single PlanarPacking
comparison wait until after that whole-library verification.

All timing uses no Lean -M. Current non-W preparation uses CPUs 8-9 only and
takes no P-core lease. Raw binaries and large artifacts remain outside Git.
