# Cost staircase after the32nd original source draw

2026-11-02UTC; self-review. This updates W074's transferred model with W077's
actual LowBlock15_1 sourcecost. **Only construction is newly measured.**
Source frame32/42/15complete cells,104632coveredmodules;58465ordinarymodules
remain in six incompletecells. Complete-cell estimates are conditional.
Full-frame columns additionally assign unobservedmodules the observed
within-source-class mean. No full-library point/CI has become empirically complete.

## Four stages, CPU hours

Nat.Basic/Grid complete-closure CPU transfer, with M's distinct parallel
CPU factors; ratios of elapsed gains are never applied as CPU savings.

|Scope/domain|Construction|Serial stream model|Parallel stream model|+Qualified chunk model|
|---|---:|---:|---:|---:|
|Covered15 ordinary|116.704826|7.527061|10.255975|10.255975|
|Covered15 explicit computational|57.546404|4.872539|6.596149|6.625703|
|Covered15 all|174.251230|12.399599|16.852124|16.881678|
|Full class-mean projection ordinary|185.776210|11.981928|16.325942|16.325942|
|Full class-mean projection computational|57.546404|4.872539|6.596149|6.625703|
|Full class-mean projection all|243.322615|16.854466|22.922091|22.951645|

The computational SOURCE domain has no missingdraws; transferred checking
costs remain unmeasured for most modules. New sourcecost does not qualify
LowBlock's large goals for splitting. Only the previously measured ten
Envelope goals receive a chunk factor; unprofiled does not mean ineligible.
External once-only base cost / legal global stream ordering / memory segments
remain unidentified; selected closure ratios include their own dependencies.

The CSVs include nominal source-sampling-only95% intervals, excluding transfer
calibration, selection/nonresponse, misclassification and model uncertainty.
Examples covered15 build[0,379.030554]CPUh, serial[0,25.764820]CPUh;
full class-mean projection build[0,621.267553], serial[0,38.911283].
These are not whole-library frequentist guarantees.

The alternative NearPin/Amplitudes closure transfers are retained separately,
not pooled as independent native repetitions or confidence bounds.
The W077 observed-class-range scenarios207.894666–630.701677sourceCPUh
and10.826785–41.839086transferredstreamCPUh use a different assumption about
the ten unknown originaldraws; do not interchange them with class-mean projection.

## Chunk marginal after new coverage

Qualified-envelope c->d still saves149.605130 modeled summed-native-elapsed
seconds and adds106.393328CPU seconds. With the larger15cell denominator:
elapsed-0.398505%, CPU+0.175371%. Full class-mean projection elapsed-0.279618%,
CPU+0.128931%. Signed sampling intervals still cross zero; preparation and
eligibility CPU are unknown, and this is not observed library makespan.
A bigger computational source share33.024963% does not mean the same share
of checking elapsed is split-eligible. Serial->parallel also raises CPU even
while shortening elapsed. No guaranteed whole-library speedup follows.

## Reproduction and arithmetic

Run cost_staircase.py with --frame noM-hard19-source32/sample-costs.csv
and --out noM-source32-staircase under E8–15. Original defaults preserve W074.
96historical31numeric stage rows reproduce and96new stage totals independently
match direct originalN/2weighted per-module sums. No newnative execution.
Read calibration.csv for O/M raw experiment boundaries and one/three-repeat
support. This is a model update, not an experiment on32newcheckerinputs.
