# Soundness review of proofserve-check at 2628d727

A fresh Claude agent wrote this second review on 2026-11-04 by reading only. Nothing was built
or run, so every test below is unconfirmed until run. Paths are repo-relative at 2628d727;
upstream means Lean v4.34.1. Status: **open**.

## Answers

- **Wrong accept:** yes. An honest-source module-system project can reach status complete, exit 0,
  while both official modes reject it (finding 1).
- **Receipt overclaims:** the accepted list, axiom list and import_only_modules are accurate on
  complete receipts. The defects found are on non-complete receipts or in project_dirty (6, 7).
- **Wrong refusal:** native IR refusal, yes, but only for hand-written reduceBool/ofReduceBool (3);
  native_decide and bv_decide are unaffected. Complete module parts: no honest case. Snapshot name
  collisions: no. A false kernel rejection is also possible (2).

## Findings

**1. Unsafe duplicates escape the conflict check (wrong accept).** Stream.lean:358 skips duplicate
detection for unsafe and partial constants, so they never enter the frontier. Upstream's importer
has no such exemption (Environment.lean:2334-2343, :2283). Variant A: PrivateConflict fixtures with
`public unsafe def foo` in A and B, thm1/thm2 by trivial; C builds, both official modes reject C,
native reports complete. Variant B: X has public unsafe def foo, Y privately imports X, M imports Y
and declares safe public def foo; official rejects (Replay.lean:98-99 path), native inserts M's foo.
Contradicts large-library-checking.md:282-284. Confidence high. Test: variant A with --closure-roots 0
against leanchecker in both modes, then all five roots with --closure-roots 1, which should reject
through the importer fallback, so the verdict depends on batching.

**2. The frontier keeps the first theorem body (false rejection, or crafted wrong accept).**
Stream.lean:364-369 validates M locally but leaves A's body in the frontier. D, importing only M, is
then checked against A's body at :421, and :431-433 reports any failure as a rejection. The kernel
can unfold theorems through Acc.rec (Environment.lean:2261-2266). Honest case: A's wf proof does not
reduce, M's does, D uses decide +kernel; official accepts, native exits 1. Crafted case: swap the
bodies; native completes, official rejects. The docs disclose this limit but not the false-rejection
direction. Confidence: code path high, kernel outcome medium. Test: those three modules, --closure-roots 0.

**3. The native refusal is broader than documented, and --official is not a working route.**
Mention-only: Stream.lean:73-82 refuses any safe declaration mentioning the primitives.
`theorem wrap (b) (h : Lean.reduceBool b = true) : b = true := Lean.ofReduceBool b true h` never
evaluates anything (type_checker.cpp:617), yet exits 2; compare README.md:139 "require project IR".
Name-keyed taint: :68-71 taints unsafe constants by name across unrelated modules; with unsafe def
helper using reduceBool in Aaa, an independent Bbb with def helper and a theorem using it is refused,
and renaming so Bbb sorts first avoids it. --official (suspected): a real evaluation of f from an
imported module should pass official default, but --official runs --fresh (Main.lean:208), which
replays into an empty environment with no IR (LeanChecker.lean:36-38, ir_interpreter.cpp:872-875,
CompilerM.lean:146-154), so the hint at Stream.lean:82 and receipt-schema.md:189-190 would be wrong.
Unaffected: native_decide and bv_decide assert an axiom (Native.lean:75-87). Confidence high for the
first two, medium for the third. Test: the three small projects above.

**4. The importer's IR reads are not mirrored (verdict difference).** At private level the importer
always loads .ir.sig and .ir and fails if .ir is missing or corrupt (Environment.lean:2182, :2190,
:2093-2105). The shared path, moduleParts and inputIdentity never touch them. No false theorem,
because IR is not executed. Confidence medium-high. Test: delete a dependency's .ir, keep .ir.sig,
compare a default native run with official.

**5. An import-only context rejection is misclassified.** Main.lean:592-593 throws, giving exit 2,
status error, no receipt and no rejected entry; receipt-schema.md:4-6 says importer rejections exit 1.
The same input under --closure-roots 0 gives rejected, exit 1. The author's O-cases.csv row
combined-conflict,2 matches, and contract.py:162-166 only asserts nonzero. Confidence high. Test: the
incompatible Pkg fixture at limits 0 and 1, asserting equal exit codes.

**6. A module can appear as both accepted and rejected.** Stream.lean:401 emits accept before the
frontier insert at :408, and failure then emits reject at :415. An exit 1 receipt lists M in both
lists with action kernel_replay, and the parent also adds it (Main.lean:547-550). Non-complete
receipts only. Confidence high for the code path, low for reachability. Test: a duplicate theorem plus
a new declaration needing M's own body, using finding 2's setup.

**7. project_dirty is a false positive with the default state directory.** The state directory is
created at Main.lean:661, then git status --untracked-files=normal runs (:81-83, :414, :706). An
unignored .proofserve/ makes a clean repo report dirty. review_e0.py:149 uses an external state
directory and a real edit, so it misses this. Confidence high. Test: a clean repo ignoring only .lake,
run with defaults, assert project_dirty is false.

**8. The Quot difference was not actually exercised (crafted only).** A restored or cached frontier has
quotInit true (Environment.lean:2365). The kernel gates reduction on that flag and matches by name
(type_checker.cpp:394, quot.h). A no-import module with axioms named Quot.* and an rfl proof: official
rejects, native after a checkpoint may accept. The author's control (ReviewE0Mutate.lean:30-46) uses
genuine Quot declarations, which flip the flag in every mode. Confidence medium-low. Test: that module
after an earlier module with --segment-modules 1.

**9. Default discovery refuses escaped module names (wrong refusal, pre-existing).** Foo.«bar-baz» is
discovered as Foo.bar-baz (Main.lean:92), which toName turns into anonymous, so the identity scan
fails. Official resolves names from file paths (LeanChecker.lean:91-92). An explicit --root with the
escaped name should work. Confidence medium. Test: one such module, default roots.

**10. Remaining doc mismatches.** README.md:69-70 and large-library-checking.md:85 say all batch roots
are inspected, but Main.lean:309-316 inspects only prefix parents for a namespace-triggered batch within
the limit, so an empty leaf gets no context child and no import_only_modules entry. integration.md:10
says repeating --max-segments resumes, but Main.lean:823-826 counts saved segments, so repeating the
same N makes no progress; the contract test resumes without the flag (contract.py:38, :75). Confidence
high. Test: a two-segment project, run twice with --max-segments 1.

## Verified versus suspected

Traced by reading: 1, 3 (first two parts), 4, 5, 6, 7, 10, and the code paths of 2 and 9. Suspected: the
kernel outcomes in 2, the --official claim in 3, finding 8. The 5-project-stdout-event fixture cannot
confirm or refute the IR route: printBool has implemented_by, so it probably has no IR declaration and
"unknown declaration" is a fixture artifact; the route is closed by the refusal anyway. Not checked: raw
artifacts on the PVC. The 320 missing module-local references remain an oracle gap.

## Earlier findings at this commit

1 complete. 2 complete. 3 incomplete: safe duplicates closed, unsafe not (finding 1). 4 complete and
matches the importer; native and --fresh accept a good non-module with bad stale parts while official
default rejects it, defensible but a verdict difference. 5 complete; no path lets a safe constant reach
native evaluation without being refused. 6 complete apart from the exit code in finding 5. 7 complete.
8 complete. 9 mostly complete: project_dirty wrong by default, module_check_entries still counts
interface-only modules, disclosed and offset by per-module rows. 10 not fixed: body disclosed but
understated (finding 2), Quot control inconclusive (finding 8).

## Areas examined, nothing further to report

Worker event file, unique terminal rule and nonzero-exit dominance; snapshot prefix and explicit
ImportArtifacts; resolved search path across coordinator, identity child and worker; part inventory
checks, certificate context checks and prepareModuleCache; certifiedBase fallback, including native
refusal inside its catch; restoreCheckpoint metadata and axiom union across paths; wave planner,
complexPrefix, FFI commit and ps_write_atomic; module-level visibility.
