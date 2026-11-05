# Checker evaluation

## Current native freeze

Native source e1557c77 is frozen under the correctness-first exception.
[Real-closure qualification](pre-freeze-e1557c77/README.md) completed both the
1,330-module Nat.Basic and 3,793-module Grid closures with unchanged acceptance
and the same 15 reported axioms as the corrected 3fe reference. Extensive
module-local replay means the performance-growth threshold failed. The release
speed comparison remains unqualified; the results are background-load previews.

> **Superseded correctness qualification:** O's review of 2df1d9d7 found false
> acceptance in certificate reuse without modifying certificate contents.
> The historical 14,721-module result used that logic. Its qualification is
> superseded by the [fresh e0c92d51 replay](certificate-reuse-fix/subexp-fresh-e0c92d51/README.md).
> Old raw results and memory observations remain preserved; they do not qualify
> the repaired checker or establish final performance.


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
The final performance matrix and official controls wait for W's census to
retire and the machine to become quiet. The latest closeout order is M's matrix
(at most six hours), O's external timings (at most two hours), then resumable
corpus checking, ending by 2026-11-06 14:00 UTC. The separate PlanarPacking
comparison is cancelled. Report an unfinished census or checking run as partial;
a completed subset is not the full 163,097-module source frame.

All timing uses no Lean -M. Current non-W preparation uses CPUs 8-9 only and
takes no P-core lease. Raw binaries and large artifacts remain outside Git.

See full-feasibility.md for the whole-source import graph, grouping/replay model,
local-certificate correctness controls, and the actual largest-closure capacity
attempts. full-feasibility-plan.csv separates repeated loads from first kernel
checks. The whole-corpus capacity decision remains open. The prepared frozen
workflow first tests the actual largest empty import context; its small native
workflow qualification exports separately to workflow-qualification/.

The completed development result is now in full-feasibility.md,
full-feasibility-memory.csv and full-feasibility-acceptance.csv: 14,721 modules,
26.062 GiB sampled tree peak, and no differences on 14,401 available module-local
references. This E-core resumed qualification is ineligible for final paper
performance claims. workflow-qualification/ contains the real three-module
workflow test, including a preserved failed launch and successful retry.
