# Checker evaluation

## Current native freeze

The introducing commit of
[the replacement policy freeze](theorem-body-policy/freeze.json) supersedes
e1557c77. Default shared-checked and the explicit strict option have distinct
artifact-context semantics, recorded in receipts and certificate identity.
[The report](theorem-body-policy/README.md) documents the reasoning,
26-row official comparison and real default-mode closures: 1,330 / 3,793
accepted modules, 15 axioms each, and exactly 49 / 157 module-local replays.
The gate is restored. The [frozen release evaluation](release-e000ed62bbf4/matrix/README.md) now provides three-repeat native scaling and ablations, with timeout, background-load and official-scope limitations.
Earlier e155 metrics remain historical strict-context strategy data.

> **Superseded correctness qualification:** O's review of 2df1d9d7 found false
> acceptance in certificate reuse without modifying certificate contents.
> The historical 14,721-module result used that logic. Its qualification is
> superseded by the [fresh e0c92d51 replay](certificate-reuse-fix/subexp-fresh-e0c92d51/README.md).
> Old raw results and memory observations remain preserved; they do not qualify
> the repaired checker or establish final performance.


The [final frozen-tool collection](release-e000ed62bbf4/matrix/README.md) ended at its original six-hour budget on 2026-11-06. Its 30 primary runs, 12 persistence/split ablations and three Nat.Basic strict runs completed; strict Grid and some official repeats remain incomplete. Per-attempt data, medians/ranges, correctness controls and actual resume comparison are exported there. Protected zettai-dev background remained, so the report does not claim an exclusively idle host.

Earlier ba316991 cells remain nonfinal previews and are not mixed with these results.

loaded-preview-cells.csv retains the returned observations with an explicit
paper_eligible=false field. loaded-preview-qualification.json and
loaded-preview.md describe their functional scope. Do not use these timings
as the paper's final system evaluation.

The executed primary matrix uses Mathlib.Data.Nat.Basic and Grid at 1, 2, 4 and 8 workers, and Barrier at 1 and 8 workers, with three fresh-checkpoint repeats each. Grid and Nat.Basic also have three 8-worker repeats for each persistence/split ablation. Nat.Basic strict repeats completed; strict Grid has one timeout and two unattempted repeats.
Official default and fresh procedures have different proof ledgers and require
an explicit scope discussion. A real interruption/resume comparison is separate.

Full Mathlib means all 8,529 Mathlib directory modules plus the umbrella module.
Its loaded scale preview accepted 10,744 modules including dependencies; it is
distinct from the 1,330-module Nat.Basic closure.

The [bounded built-artifact check](release-e000ed62bbf4/corpus/README.md) ended at the authorized 17:15 UTC drain limit on 6 November. Fifteen complete batches certified 12,756 distinct closure modules, including 968 of W's 162,170 requested built sources. Another 488 source accept events remain provisional; 161,202 requested sources lack complete batch certification. No module rejection was reported. The 926 deferred sources and one lakefile configuration unit are separate. OAI has no compiled artifact, so its capacity is unmeasured. All processes retired and the lock was released. This is an incomplete prefix, with no whole-corpus parity or cost extrapolation. Earlier unexecuted corpus commands are historical preparation; the current report records the actual driver and terminal evidence. The separate PlanarPacking comparison remains cancelled.

Final native timing uses no Lean -M, P cores 0-7 and the P-core lease. Preparation and analysis use CPUs 8-9. Raw binaries and large artifacts remain outside Git.

See full-feasibility.md for the whole-source import graph, grouping/replay model,
local-certificate correctness controls, and the actual largest-closure capacity
attempts. full-feasibility-plan.csv separates repeated loads from first kernel
checks. The whole-corpus capacity decision remains open. The older prepared workflow tested an empty-import-context stage; its small native qualification remains in workflow-qualification/. The current built-subset command excludes the unbuilt OAI umbrella and makes no combined-context capacity claim for it.

The completed development result is now in full-feasibility.md,
full-feasibility-memory.csv and full-feasibility-acceptance.csv: 14,721 modules,
26.062 GiB sampled tree peak, and no differences on 14,401 available module-local
references. This E-core resumed qualification is ineligible for final paper
performance claims. workflow-qualification/ contains the real three-module
workflow test, including a preserved failed launch and successful retry.
