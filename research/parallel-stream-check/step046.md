# Step046: actual P8 count-only point has complete worker evidence
EXPERIMENT_GATE: official -n/-s full-closure run retired, all9 check-worker
TIDs have complete unique seven-event/eight-shard READs. Fixed reference IDs/
checks/units, inherited attrs, zero samples and no resource stop. Installed
report-T produces no table with no samples despite exit0; first table-parser
attempt failed visibly and did not produce a false result. Native READ dump
has1019 records, so use its values with strict completeness checks. The
aggregation exactly matches200 independent native report-T values from three
original sampled captures. No native rerun was needed for this decoder issue.

WRITE_GATE: actual P8 worker CSV/attrs/READ terminal, aggregation source/
crosscheck and P8-count-only.md. Time/counters remain separately labeled;
do not normalize original sampling with them. Original partial raw retained.

REVIEW_GATE 自审: each worker/event/ID is unique and complete; checks/units
sum to the full reference. No-sample behavior actually confirmed, no silent
empty-table success. This validates count evidence, not compression causality,
runtime optimization or a perfectly check-gated counter. P4 matching is next.
