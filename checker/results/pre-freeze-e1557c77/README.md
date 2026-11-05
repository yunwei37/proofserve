# Real-closure regression and native-source freeze

> Superseded freeze decision: the coordinator replaced this default on
> 2026-11-05 with shared-checked plus an explicit strict mode. The measurements
> below remain unchanged historical e1557c77 data. See ../theorem-body-policy/.

Native source is frozen at e1557c770fcc585e722399e56a3c3be77b2f0e7f.
The freeze uses the coordinator's explicit correctness-first exception:
**the fallback-growth performance threshold did not pass**. This is not a
release, an independent execution review, or a qualified speedup claim.

## Actual closure checks

The fixed e155 binary ran with two workers on E cores 8–9, at most 12 GiB
of its own native group, no Lean -M and no P-core lock while W's census continued.
Both roots used fresh checkpoint directories initially. Nat.Basic is its
1,330-module dependency closure, not the complete Mathlib library.
Grid is the retained 3,793-module dependency closure.

The retained 3fe83c5a binary was run on exactly these roots and E-core settings
to separate the old axiom-report correction from this repair. Its known
small-fixture correctness defects make it a diagnostic reference, not a release
candidate. The ba316991 row shows one retained P-core preview for each root;
its CPU must not be divided into E-core CPU and called a source speedup.

| Root | Source | CPUs | Accepted | Declared axioms | Whole-module serial replay | Segments | Peak tree GiB | Attempt CPU s | Complete-segment CPU s |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| nat | ba316991 | P0-7 | 1330 | 7 | 4 | 3 | 1.643 | 84.79 | 83.30 |
| nat | 3fe83c5a | E8-9 | 1330 | 15 | 49 | 3 | 1.699 | 183.56 | 178.48 |
| nat | e1557c77 | E8-9 | 1330 | 15 | 1016 | 3 | 1.464 | 411.41 | 405.10 |
| grid | ba316991 | P0-7 | 3793 | 7 | 7 | 8 | 3.125 | 636.69 | 633.69 |
| grid | 3fe83c5a | E8-9 | 3793 | 15 | 157 | 8 | 3.441 | 1496.23 | 1485.57 |
| grid | e1557c77 | E8-9 | 3793 | 15 | 3465 | 8 | 3.080 | 3508.94 | 3370.43 |

Both new acceptance sets equal their retained ba316991 and same-root 3fe83c5a
sets. The new 15-name declared axiom sets equal the same-root 3fe83c5a sets.
The earlier ba316991 report listed only seven; the eight additional names
(Quot.lcInv, isScalarObj, lcAny, lcCast, lcErased, lcProof, lcUnreachable,
lcVoid) were already in the unchanged inputs and were omitted by that older
report. They are not new assumptions inserted by this qualification.

All previously recorded input path/hash pairs match the new inventories;
the new inventory additionally validates IR presence and bytes. See
summary.json for exact comparison counts and declared names. These 64-bit
identities detect ordinary changes, not deliberately constructed collisions.

Module-local counts use successful committed-segment accept records and
their unique module names; those two counts agree in this run. They do not
count internal complex-prefix declaration replay or unknown overwritten
partial events. fallback-reasons.csv gives the exact recorded reason categories.

## Why the threshold fails

- nat: whole-module replay rose from 49 to 1016, exceeding the allowed 10% growth.
- grid: whole-module replay rose from 157 to 3465, exceeding the allowed 10% growth.

The real first divergent theorem is List.drop.eq_def in Init.Data.List.TakeDrop.
The two bodies mention different private splitter constants. Removing metadata
and let nondependency annotations does not make them equal; a bounded beta/zeta
diagnostic also did not equate them. diagnosis.json records the actual output.

A same-interface or imported-ancestor exemption is not a safe small repair:
the upstream importer can replace a theorem body with a later imported body,
and the genuine WellFounded/Acc regressions show that retaining the wrong
body can change downstream checking. No unqualified proof-body normalization,
alias substitution or correctness rollback is shipped to recover throughput.
Context-aware optimization remains unimplemented; this is a known cost, not
a claim that a safe optimization is impossible.

The quarantine causes subsequent missing-frontier and segregated-dependency
fallbacks. CPU is reported as a preview under the census, not an isolated
causal measurement of this one code branch or a quiet-machine performance result.

## Interruption, memory and evidence

Nat.Basic finished in one invocation. Grid reached the first 1,800-second
finite window and then completed from the same binary/checkpoint. Its two
wall-clock intervals remain separate. Attempt CPU includes interrupted work,
revalidation and repeated work; complete-segment CPU is reported separately.
All guarded native processes and cgroups retired. There were no memory,
node-reserve or OOM stops. See data-quality.md for the unarchived first partial
Grid event file; do not claim every partial event survived.

Raw binaries, receipts, complete segments, memory samples and failed attempts:

/workspaces/.agent-state/gpu-smt-captures/checker-freeze-e1557c77-20261105

The public small tables can be regenerated with:

    python3 checker/results/pre-freeze-e1557c77/analyze.py RAW_DIRECTORY

## Freeze and remaining work

freeze.json binds the native source files, binary receipt identity and CI
evidence. Both code-only independent reviews have regression repairs; the
repaired source has no independent execution review. The current execution and
result interpretation are self-review (自审). The earlier repair's CI passed
the core contract plus 90 earlier and 109 new review command records; these
are command counts, not counts of distinct defects or theorems.

After freeze, only real defects justify native changes, and relevant results
must be rerun after a change. Documents and new evaluation results may still
be added. No tag or public release is created.

Still pending: the post-census quiet-machine final matrix and official controls,
O's external-project acceptance/timings, the repaired-source 14,721-module replay
and bounded corpus checking. Earlier ABI 4 large results do not qualify ABI 5.
The final closeout order and deadlines supersede the historical capacity-first
driver; see ../../docs/release-evaluation.md. There is no PlanarPacking-only
comparison and no new performance number from this preview enters the paper.
