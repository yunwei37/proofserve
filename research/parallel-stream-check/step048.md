# Step048: retain the incomplete P4 count-only observation
EXPERIMENT_GATE: native P4r2 returned normally but4/5 checking TIDs have
incomplete exit READ sets. Exact exporter assertion failed before creating
complete counter output. Counts-only mode is not a universal repair; P8r2
qualification remains valid for that point. Preserve partial raw/metadata.

WRITE_GATE: raw coverage CSV and P4-counter-partial.md. Prepare an explicit
single tail-drain control: same native/C work/counter mode,5s in an external
parent after Lean/time exits. It changes recorder termination, not any Lean
computation or kernel timer. Source syntax checked; not yet executed.

REVIEW_GATE 自审: separate native acceptance from counter-metadata failure;
do not weaken the completeness guard. Actual READ records prove the partial
sets. No added sampling, runtime optimization, foreign files or host change.
The next one-at-a-time control tests a concrete teardown explanation.
