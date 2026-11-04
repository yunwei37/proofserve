# Fresh retained-closure replay after certificate repair

Scope: M lane, checker/ only. Review label: 自审. No release freeze.
Native source: e0c92d51ab0faf24f1c7ac64323d5ea2f2e4575d.
Evidence: ../../certificate-reuse-fix/subexp-fresh-e0c92d51/README.md and its
summary.json, preview.csv, comparison.csv and retained-reference validation.

## EXPERIMENT node

Entry was the user's request for a fresh complete replay after the supplied
certificate failures had been repaired. The coordinator read the repair but
did not perform an independent review or add adversarial cases.

The actual public executable was copied from the qualified e0c92d51 build;
all native source blob identities were checked against that commit. The
run used an initially nonexistent checkpoint directory, original retained
roots and artifacts, E cores 17–23, two workers, a 40 GiB native-tree maximum
and an 8 GiB node reserve. It used no P-core lease or Lean -M.

The complete invocation returned 0 and accepted 14,721 modules with zero
rejections. All nine batches and their segment records were new. The final
compiled-empty parent passed the original importer and empty replay. The
receipt reports 14,720 module-check entries and 86,150 trusted import entries.

The 15 declared axiom names equal the old receipt. Acceptance equals the
previous result and O's complete 30-segment stream. All 14,401 available
module-local references agree; 320 have no such reference. O's stream has
no axiom field, so no independent aggregate-axiom equality is claimed.

All 36,209 recorded input paths and 64-bit hashes equal the historical union.
The repaired checker separately checked actual part presence and current
resolution. This identity is noncryptographic, not collision resistance.

Sampled tree peak RSS was 26.112801 GiB; wait4 peak was 25.884964 GiB; charged
peak was 19.921318 GiB. No resource or OOM stop occurred. Preview wall time
was 5,784.790577 seconds and cgroup CPU was 6,948.353055 seconds. These
E-core observations are not final performance data or a matched speedup.

An observation session exited, but the original PID/birth and native group
were confirmed alive. The run was never restarted. Its original controller
wrote a complete terminal; no derived terminal or stitched clocks were used.
The controller, native processes and cgroup were verified retired.

## WRITE node

Updated the repair's Outstanding text with the actual coordinator-reading
scope, independent-review absence and fresh replay result. Updated the large
library trust reference to state the 64-bit hash's lack of resistance to
deliberate collisions. Kept the old vulnerable-source run visibly superseded
and linked the new development qualification. Raw historical data were not
rewritten or removed.

## REVIEW node

Result inspection and document review were performed by this thread and are
marked 自审. The coordinator reading and the old O code review do not constitute
an independent review of the repaired source. Checked receipt/stdout equality,
native exit, exact accepted sets, reference availability, declared axiom set,
freshness flags, input identity maps, resource accounting and process retirement.

## Handoff

This retained case is complete. The checker remains unfrozen. Independent
review and the approved final evaluation remain pending. No full-corpus run,
matrix, new adversarial case, GPU work or service feature was started.
