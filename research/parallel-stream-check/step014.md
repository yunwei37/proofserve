# Step014 — preserve completed Grid reference and repair controller paths

## EXPERIMENT
The generalized paired controller failed after the original O Grid arm completed:
557.567719s,3,793accepted IDs equal to the completed same-input curve, native/group
retired. It then attempted ROOT/label+'-full-pair-results.json', whose Python
precedence tries PosixPath+str. Its finalizer had the same bug, masking the first
metadata write error. No parallel arm was started; actual lock is free. Native
mathematical checking and the preserved reference summary/stdout are unaffected.

## WRITE
Corrected derived paths with explicit f-string filenames. Retained failing raw
full_grid_pair.py/log without alteration. Two E-core controller integration
controls execute both grid/barrier result/complete/terminal path branches with
stubbed expensive runner; no Lean, timer or scientific gain inferred from tests.
Added finish_grid_pair.py to validate and reuse only the completed native Grid
reference, then run the missing uniform4arm with the same800s budget.

## REVIEW — 自审
Syntax-only checking had missed this runtime path operation: acknowledged as an
implementation mistake. Regression now executes the actual path-writing branches.
The original baseline is not restarted. Resume will disclose the controller-
repair gap; the two native arm times remain separate actual full-process clocks,
not one uninterrupted end-to-end session. No whole-Grid gain yet published.
Next submit only the missing arm after checking no live old capture/lock owner.
