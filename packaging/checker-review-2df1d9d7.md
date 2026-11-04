# Independent review of the checker at 2df1d9d7

The O lane designed and ran these cases against checker commit 2df1d9d7. It did
not write this code. The lane stopped at 11:18 UTC on 2026-11-04 when the model
provider's content filter ended its session, before it wrote its report. Claude,
the coordinator, wrote this summary from the raw results on the Workspace PVC.
M did not write it. Status: **open, do not freeze the checker on 2df1d9d7.**

Raw results: /workspaces/.agent-state/proofserve-o-line/checker-review-2df1d9d7/run-{1,2,3,4}/results.json
Cases: checker-review-2df1d9d7-cases.py and checker-review-2df1d9d7-Mutate.lean, committed as O left them.

## False acceptance

Both cases report status complete and exit 0 on a project holding a bad proof.
The no-certificate path and the official leanchecker both reject the same input.

| Case | Run | Input | proofserve check | No certificate | Official |
|---|---|---|---|---|---|
| new-private-part-resume | run-2 | Certificate and recorded .olean unchanged; one new valid module part holding a bad proof is added | exit 0, complete, 1 accepted | exit 1, 0 accepted | exit 1 |
| cross-project-authentic-certificate | run-1 | Another project's unmodified certificate is copied into the checkpoint directory; this project's module holds a bad proof | exit 0, complete, 1 accepted | exit 1, 0 accepted | exit 1 |

In the first case the official tool reports "leanchecker found a problem in Token".
Neither case needs an edited certificate, so neither falls under the documented
limit below. O's reading is that the certificate does not bind the complete set
of input files, or the files the current project actually resolves to. M must
confirm the cause in the code.

## Other defects

- **filesystem-full (run-2).** With the disk full, native exit is 0 and stdout
  reports complete. O reported that the receipt on disk could not then be parsed.
  Confirm this from the raw case output. A check must not report success when it
  could not store its receipt.
- **wrong-receipt-lean and wrong-child-abi (run-1).** A certificate whose receipt
  records a different Lean version or child ABI is still reused, exit 0 and
  complete. wrong-identity-lean is refused, exit 2. The two should behave alike.
- **Documentation.** checker/docs/large-library-checking.md says no unchecked
  imported proof is accepted merely because an earlier module was built. With
  the two false acceptances above, that statement does not currently hold.

## Documented limit, not a defect

forged-extra-acceptance and forged-missing-axioms hand-edit a certificate and
obtain a forged accepted list or a shorter axiom list, exit 0. Local certificates
are trusted state and not cryptographic proofs, as the documents say. This must
stay prominent in the README and in every receipt that reuses certificates.

## Cases that behaved as expected

good-control, bad-body-fresh, bad-body-official, reuse-baseline, no-reuse-baseline
(same accepted and axiom sets), completed-resume, official-reference, axiom-reference,
wrong-identity-lean, torn-certificate, torn-segment, changed-complete-dependency,
bad-beneath-empty, nonempty-root, empty-root, duplicates, unknown-name, clashes-reuse,
clashes-replay, combined-conflict, combined-official, kill-certificate-write,
resume-pending-write, filesystem-readonly (native exit 2, old receipt retained),
base-only-certificate, new-private-part-fresh, new-private-part-official,
private-axioms-reuse, private-axioms-reference, private-official,
existing-unrelated-root-file, mixed-root-official, spoof-nonempty-as-empty,
private-original-axioms.

## Not finished

run-5, a further variant of the module-part case, ended on a harness assertion
and has no results. Review item 7 was covered only on these small fixtures. The
review did not re-run the 14,721-module closure. That run had no modified inputs,
but it used the certificate logic above, so it needs repeating on the fixed binary
before it is reported as final.
