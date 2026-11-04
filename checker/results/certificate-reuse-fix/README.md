# Certificate reuse repair after O's independent review

This is a correctness repair and an untimed development qualification. It is
not a release freeze or a new performance result. All work ran on E cores
17–23 with Lean 4.34.1, without Lean -M or the P-core lease.

## Confirmed causes

O's raw run-1 and run-2 records confirm both false acceptances at 2df1d9d7.
In new-private-part-resume, the exported .olean and certificate were unchanged;
new optional parts contained the invalid proof. validateBatchInputs iterated
only the old recorded paths. It did not establish that currently present
optional parts were exactly the recorded parts, and a completed batch skipped
the fresh child input scan.

In cross-project-authentic-certificate, certificate input paths still named
the donor project's good artifacts. The coordinator checked those old bytes,
roots, Lean identity and manifest, but did not compare the certificate's
project and search path against the current project, or re-resolve its closure.
The current project's bad artifact could therefore inherit genuine donor
acceptance. Neither case required editing a certificate.

The same validation omitted the child's checkpoint ABI and the receipt's Lean
version. wrong-identity-lean was checked, while wrong-receipt-lean and
wrong-child-abi were not.

For filesystem-full, run-2/009-filesystem-full.stdout records native_exit 0,
complete stdout, old_receipt_complete false, and a JSONDecodeError while reading
the on-disk receipt. This is the actual namespace control's native exit, not
the review harness's exit. The old writeJson used IO.FS.writeFile followed by
rename. The matching SDK's writeFile calls Handle.putStr without an explicit
checked flush. A buffered write could appear successful until handle disposal;
rename then published an unreadable receipt. We do not infer the lost file's
length from the JSON error.

## Repair

Completed batches now bind canonical project path, the actual Lake-selected
search path, manifest, roots, checker options, Lean identity, receipt version
and child ABI. Resume re-resolves the actual closure in a short-lived metadata
child and compares the full current file set and hashes. Every optional exported,
server or private part must have exactly the recorded presence or absence.
Final publication revalidates the union's bytes and current module resolution.

Child checkpoint ABI 3 and independent-closures-v5 invalidate previous state.
Use a new checkpoint directory. The original kernel and proof policy are
unchanged. No proof is repaired, replaced or accepted by this metadata code.

JSON publication now uses checked complete writes, file fsync, checked close,
atomic rename and parent-directory fsync. A publication failure returns
nonzero before complete stdout. An old receipt may remain valid on disk;
callers must always use the current process exit code too.

Editable certificate metadata remains trusted. The manual forged-missing-axioms
control still suppresses axioms, as expected outside the integrity guarantee.
The receipts now say this explicitly and README links the full trust statement.
The forged-extra-acceptance fixture now fails current resolution of its
nonexistent module; that does not turn local certificates into untrusted proofs.

## Exact replay scope and results

The three packaging review files are preserved byte for byte, including an
existing trailing blank line in the Python file (a diff-check warning), and included in
the repair commit. The retained Python harness hard-codes CPUs 8–9, whereas the
authorized allocation is 17–23. Its retained Lean mutator also fails to parse
two multiline structure updates on the pinned SDK today. Only PVC copies were
adapted: the affinity assertion was changed to the actual allocation, and those
two field lists were joined onto single lines. No fixture semantics, test
expectations or case selection were changed. The exact diff and original file
digests are included. We do not retroactively infer which text was present
during O's successful historical run.

| Control | Old result | Repaired result |
|---|---|---|
| Authentic foreign-project certificate | complete, exit 0 | refused, exit 2 |
| Added private part on resume | complete, exit 0 | refused, exit 2 |
| Same bad part, fresh native / official | rejected, exit 1 / 1 | rejected, exit 1 / 1 |
| Receipt Lean mismatch | complete, exit 0 | refused, exit 2 |
| Child ABI mismatch | complete, exit 0 | refused, exit 2 |
| Identity Lean mismatch | refused, exit 2 | refused, exit 2 |
| Full private tmpfs | complete stdout, native exit 0, receipt parse failed | native exit 2, no stdout, old receipt parseable |
| Read-only private tmpfs | error | native exit 2, old receipt parseable |
| Interrupted certificate publication, then resume | no certificate; resume succeeds | same |
| Valid reuse / replay / resume / private axiom controls | accepted with matching sets | same |

The base, extended and edge modes produced 44 rows covering 42 distinct case
names. All 42 required control rows passed their explicit exit, completion and
set-equality checks. The other two rows are deliberate trusted-metadata editing
observations, not security claims. cases.csv provides every row against the
retained historical run number and raw evidence; raw-case-results.json keeps
the exact returned observations. Official commands that print no JSON are not
misclassified as incomplete native receipts.

The expanded checker/tests/contract.py passed with the existing correctness,
axiom, three malformed-proof, scope, conflict and resume controls. Added CI
regressions cover authentic foreign project state, the added private part,
receipt Lean and child ABI mismatch, and ENOSPC in the final receipt writer.
The CI ENOSPC fixture uses an owned pending-file link to /dev/full; it needs no
mount privilege. The O replay additionally exercises its original real private
tmpfs-full and read-only controls. The sampled contract process-tree peak was
1.562 GiB; the O mode peaks were each below 1.561 GiB. No memory guard stopped
the contract and all controllers and native children retired.

Two unsuccessful development attempts are retained on the PVC: the initial
Main helper type syntax error, and the contract run that exposed the copied
multiline mutator syntax issue. They are not counted as successful tests.
The final native blob identities and complete contract output are in summary.json.
The harness's embedded checker_commit string still names its historical target;
it must not be read as the commit of the repaired binary.

## Outstanding

O's independent review concerns the old commit. This repair's result inspection
is 自审; the coordinator still needs to review it. The checker has not been
frozen. The prior SubexponentialSAT 14,721-module acceptance was obtained with
the defective certificate logic and is explicitly superseded as qualification.
Its raw data remain intact. A fresh replay on the repaired binary is still
required before final use. No full-corpus check, final matrix, service change,
or external publication was started.

Raw data and the exact qualified binary remain at:
/workspaces/.agent-state/gpu-smt-captures/checker-review-fix-20261104.
