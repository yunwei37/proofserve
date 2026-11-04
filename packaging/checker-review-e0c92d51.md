# Soundness review of proofserve-check at e0c92d51

A fresh Claude agent wrote this review on 2026-11-04. It had no access to M's or
the coordinator's conclusions, and it read the code only: nothing was built or
run, so every test below is unconfirmed. The coordinator spot-checked findings 1,
2 and 5 by reading the cited lines, and they match. Status: **open**.

**Answer: yes to both questions.** proofserve-check can report status complete
and exit 0 on input the official checker rejects, and on a module whose real file
never reached the kernel. The receipt can also claim more than was checked, most
seriously in the axiom list.

Paths are repo-relative at e0c92d51; upstream means Lean v4.34.1. "Shared path"
means the default single-frontier visit. "Segregated" means a module that conflicts
with the frontier, so it is checked alone and kept out of the frontier.

## Findings, most severe first

**1. Axioms of segregated modules are dropped from the receipt.**
Aaa has `def clash : Nat := 1`. Bbb has `def clash : Nat := 2` and `axiom cheat : False`.
Ccc imports Bbb and uses cheat. This is plain source, and it builds because nothing
imports both Aaa and Bbb. checker/ProofServe/Stream.lean:335-336 records the segregation
but adds nothing to checked or declaredAxioms; only :150 and :323-326 add declared
axioms, and the list is computed at :251 and :423. The result is complete, exit 0, and
cheat is missing, contradicting docs/receipt-schema.md:18-20 and README.md:145-146.
Confidence high. Test: build that project and assert cheat is in axioms; --closure-roots 1
should list it, which gives a second oracle. For the real run, the 15-name SubexponentialSAT
list was only compared with the earlier checker, which has the same logic: grep its raw
segment logs for fallback_reason values different_constant, unimported_reference and
segregated_dependency.

**2. The child searches the checkpoint directory first, so the file checked is not the
file hashed.** Main.lean:698 puts dir first on LEAN_PATH. The input scan (:136-138), the
identity (:666) and the final check (:580) all use the path without dir.
(a) A good Foo.olean sits in the state directory or batch-K/ and the project's real
Foo.olean is bad. The default state directory is inside the project. This is arguably
tampering with protected state, but it is not a certificate edit.
(b) No foreign file is needed: a project module named ProofServeSegment0, visited after
the first checkpoint, resolves to the snapshot, so its real file is never replayed.
The result is complete, exit 0, while official rejects the real file. A certificate
obtained this way stays valid after the shadow is removed. Confidence high.
Tests: (a) copy the good .olean into the state directory, mutate the real one, run with
--closure-roots 0. (b) modules A and a mutated ProofServeSegment0, run with
--closure-roots 0 --segment-modules 1.

**3. The shared path never runs the importer for nonempty modules, so identical
duplicates pass.** Take upstream's PrivateConflict{A,A2,B,B2,C} fixtures and make foo
identical in A and B; this is an honest module-system build. Variants: a module that
redeclares a privately imported definition identically; a module artifact missing .server
or .private, with a dependent in the same frontier. Stream.lean:299 has no branch for the
identical case. Upstream rejects at Environment.lean:2340-2343, Replay.lean:82-83 and
Environment.lean:2087-2090. Official rejects C; the default run reports complete. No false
theorem results, but the verdict differs from official and contradicts README.md:74-75, and
it depends on batching: --closure-roots 1 should fail the import, fall back and reject.
Confidence high. Test: the fixture at default and at --closure-roots 1, plus leanchecker
...PrivateConflictC.

**4. The part checked is chosen by file existence; the importer chooses by isModule.**
A non-module M.olean holds a bad theorem, and its .server and .private parts hold good or
empty data, present from the first run. Stream.lean:39-48 and :261 check the last part.
Importers load only parts[0] (upstream Environment.lean:2083-2084, :2023-2031). So the
constants importers actually see are never replayed. If the private part is empty,
ModulePlan.lean:25-26 also classifies M as import-only. Limit: official default has the
same blind spot; only leanchecker --fresh rejects. ProofServe's own --official path uses
--fresh, so its two paths disagree. Lake clears stale parts on rebuild, so this needs a
crafted or hand-copied artifact. Confidence high for the code path, medium that the crafted
artifact loads as described. Test: build the parts with saveModuleDataParts and
isModule := false, add N importing the bad theorem, compare with --fresh N.

**5. Any JSON on the child's stdout counts as an event, and complete overrides a nonzero
exit.** Main.lean:81-82, :725, :733-735, :745, :756. The kernel can run project IR through
Lean.reduceBool (upstream type_checker.cpp:618-619). If that code prints a complete event,
a real kernel rejection later in the run still yields status complete and exit 0. It could
equally forge accept events. A crash after a flushed complete reaches the same logic in a
very narrow window. Limit: this needs hostile but well-formed project code, and official
can also be fooled with IO.Process.exit 0. It matters most for a lakefile.toml project with
untrusted modules. Confidence high for the override logic, medium for the IR route. Test:
M defines the printing constant; X imports M, uses Lean.ofReduceBool and has a name clash
that forces local replay; a bad module follows. Expect complete with nonempty rejected.

**6. import_only_modules claims a context check that may not have run.** Main.lean:544-545
and :564 skip the empty-context child if the module was already accepted as a dependency.
docs/receipt-schema.md:108-111 says the importer accepted every member. Confidence high.
Test: roots Pkg, Pkg.Child, Pkg.Z, where empty Pkg imports Pkg.Child and Pkg.Z imports Pkg.
Assert Pkg is listed and empty-context-0.stdout does not exist. With finding 3's conflict
underneath, official rejects Pkg.

**7. The visibility check can be bypassed by names that are in the module's map but never
inserted.** Y has `unsafe def foo` (or a constNames entry differing from ci.name) and a safe
theorem using foo; unrelated A, visited earlier, has a safe foo. Stream.lean:292-293 and
:305-307. The kernel resolves foo from A; official fails with an unknown constant (upstream
Replay.lean:179-183). Limit: needs a crafted artifact. Confidence medium. Test: build that
pair, run --closure-roots 0, compare with leanchecker Y.

**8. The single-frontier path has no root coverage check, and roots.txt is written
unchecked.** Main.lean:673 and :135 still use IO.FS.writeFile, whose silent ENOSPC loss is
described in results/certificate-reuse-fix/README.md:30-33. The receipt at :744-756 has no
equivalent of :501-503 or :570-572. A truncated list on a line boundary, with later writes
succeeding, gives complete with requested roots unchecked. Close variant of the
filesystem-full bug. Confidence: logic high, reachability low. Test: symlink roots.txt to a
file on a small full tmpfs, use more than 4 KB of roots, assert roots are a subset of accepted.

**9. Entry counts and the project revision say more than they establish.**
module_check_entries (Main.lean:498) counts modules that sent zero declarations to the
kernel, because Stream.lean:305 inserted nothing. The top-level receipt has no per-module
split between fresh and reused modules. project_revision (:165-169, :594) is the current
HEAD, with no dirty flag and no binding to any artifact. Confidence high. Test: compare
unique_shared_kernel_declarations in the segment log with one and two identical modules;
for the revision, make an empty commit and resume.

**10. Two low-severity differences remain between the frontier and the declared context.**
With a duplicate theorem, the frontier keeps the first body (Stream.lean:299-301), even when
that body comes from a module the importer cannot see; a crafted proof that needs that body
to unfold passes here, and official rejects it. Restored or cached environments set quotInit
true (upstream Environment.lean:2365, Stream.lean:126, :236); official has it false for a
no-import module, which matters only in prelude-only closures with a crafted artifact.
Confidence low to medium. Test: one crafted module for each case, compared with official.

## Status of the certificate fix

Closed on the resume path, by reading: foreign-project certificates, and certificates reused
after the project's bytes changed; parts added or removed, including on transitive certified
imports and empty rows; a later shadow in an earlier search entry; search-path, manifest,
roots, receipt Lean and ABI mismatches; JSON publication failures.

Not closed: parts present from the first run (finding 4); search-path shadowing through the
state directory (finding 2). Certificates are bound to ABI constant 3, not to the checker
binary, so any behaviour fix, such as for finding 1, needs an ABI bump or old certificates
keep their old axiom lists.

## Examined, nothing to report beyond the above

Validation order (certificate checks run before use); closure-path root coverage and reuse of
closure-plan.json; the cache boundary (prepareModuleCache and certifiedBase send an uncertified
module in a cached context to fallback and then local replay; hasData is always true at private
level, and the header arrays stay aligned); axioms under reuse (the union across batches is
correct, the only loss is finding 1); names (String.toName round-trips, invalid names fail
closed); the kernel path (the wave planner, FFI commit and checkpointDone handling never bypass
the kernel); segment resume (the identity comparison and the rule that failed segments are not
logged both hold). Declared limits, not counted: snapshots are not hash-bound;
--trusted-module-cache can be forged; changing artifacts during a run is unsupported (the
closure path rehashes at the end, the single-frontier path does not).

## Verified versus suspected

Code path traced by reading: findings 1, 2, 3, 6 and 9, plus the logic of 5 and 8.
Suspected: the IR route in 5 and the reachability of 8. Finding 4 still needs the crafted
artifact to load, and 7 and 10 still need crafted-artifact runs. The claim that exported parts
carry no proof bodies, relevant to 3's missing-parts variant, comes from one upstream comment
plus mkModuleData.
