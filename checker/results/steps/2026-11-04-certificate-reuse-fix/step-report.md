# Repair step: input-bound certificate reuse and durable receipts

Review label: 自审. O's independent review of 2df1d9d7 is the input, not an
independent acceptance of the repaired target.

## EXPERIMENT node

Goal: reproduce the meaning of O's two authentic-certificate failures, actual
ENOSPC publication failure and receipt/ABI mismatches from original captures,
then rerun the existing fixtures on the repaired public executable.

Evidence: ../../certificate-reuse-fix/README.md, cases.csv, summary.json and
raw-case-results.json. All 42 required control rows passed; two deliberate
trusted-metadata modification observations remain separately scoped. The
expanded portable native contract passed. Failed development attempts and all
original O data remain on PVC. Tests ran serially on E17–23, not as timing cells.

## WRITE node

Updated the user trust reference, receipt ABI/publication semantics and large
library documentation. Marked the old 14,721-module qualification invalidated
by the review, without altering historical raw data or pretending a fixed replay
was performed. Preserved O's three packaging files without edits.

## REVIEW node

Inspected source changes, exact replay adaptation diff and each case's native
versus wrapper exit, accepted/axiom equality, and old-receipt parse result.
All native/controller handles retired. Original O file digests still match.
No further adversarial cases were invented.

## Handoff

Do not freeze yet. Coordinator review and a fresh 14,721-module replay remain.
Full-corpus checking and final paper evaluation did not start.
