# Installed original checker controls, with explicit verification scopes
Unchanged installed SDK4.34.1 commit5045d005, no-M, P0-7 blocking lock,
same14GiB guards inside16GiB lane. All three native controls return0 and their
applications/groups/controllers retire. One observation per stock setting,
not a replicated performance comparison. M rows are3-repeat plain medians.

| Program / setting | Verification scope | Wall s | CPU s | wait4 peak RSS GiB |
|---|---|---:|---:|---:|
| stock default8 | one root leaf;imports trusted | 65.423 | 64.985 | 2.925735 |
| stock --fresh1 | one final imported environment replayed from empty;SDK duplicate policy | 534.698 | 534.532 | 3.340912 |
| stock --fresh8 | one final imported environment replayed from empty;SDK duplicate policy | 580.090 | 579.906 | 3.353504 |
| M full closure unmarked8P | independent module stream;exact4,449-ID/work ledger | 314.839 | 722.297 | 3.268742 |
| M full closure marked8P | independent module stream;exact4,449-ID/work ledger | 298.675 | 620.240 | 3.281971 |

Do not divide these mismatched scope clocks into a claimed speedup over stock.
Default verifies one leaf after trusting imports. --fresh checks one final
imported map with its own duplicate policy; it does not emit our module-level
check/HB vectors. Exact full-workload ledger equivalence was not measured.
The32-cell on/off causal contrast is within one M binary/protocol, not a
new strong-service throughput result.

The configured thread count is not actual declaration parallelism here.
All three SDK controls use about1CPU core on average. Matched SDK main's
normal path creates one IO.asTask per selected module; only one root was
selected. --fresh loops its target replay sequentially. The8configured fresh
observation is slower than1(580.090 vs534.698s); preserve this outcome, but
one observation/order/frequency/placement were not isolated, so do not call it
intrinsic negative scaling of Lean.

## Persistence premise and effect
The supplied premise 'stock parallel import is already leaked' is false for
this exact SDK: replayFromImports calls importModulesCore/finalizeImport false,
false; importModules defaults leakEnv=false. The native probe finds the kernel
base ST and imported Nat.add/Nat.mul CIs already persistent. These are different
object layers. A module-local root constructed inside its own task also differs
from M's reconstructed root shared across declaration workers. Enabling leakEnv
in the direct probe marks the base. See source-and-scope.md for header evidence.
The M intervention uses that existing runtime primitive at a quiescent frontier,
not a new kernel rule or novel technique.

## What happens to the old3.33x/1.88x claims?
Keep every old result as measurement of its unmarked prototype/version/scope.
The causal matrix demonstrates that much of the old4-to-8 extra CPU was an
avoidable prototype object-state choice. Those clocks cannot establish an
intrinsic native-kernel/workload scaling limit. Their exact leaf/Grid serial-
parallel pairs need retiming with the corrected implementation before being
reported as corrected gains. Do not multiply an old gain by the5.134% full-
Barrier wall reduction, switch denominators, or substitute a different scope.
The old8P+E result also remains unmarked-only; no corrected heterogeneous-core
result was measured here.
