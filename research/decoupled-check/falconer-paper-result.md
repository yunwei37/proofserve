# Falconer: kernel-only validation costs 9.26% of measured source construction

**Result for RQ2; 2026-11-02 UTC; review: 自审 (self-review).**
For the complete dependency closure of the AI-generated Falconer mathematical
subtree, original-kernel validation took **2,043.59 s across 27 resumable
processes**, versus **22,077.77 s of successful source compiler work**.
The ratio is **0.092563 (9.26%)**. All **13,205 module acceptance IDs** and
their import graph agree with the planned closure; an independently executed,
original module-local checker accepts the identical set.

These are complete-closure costs on frozen artifacts, including checkpoint
export and reload. They measure the separation between proof production and
validation, rather than parallel Lake build latency or verification-service
throughput.

## Inputs and reproducible scope

| Input | Pinned identity / extent |
|---|---|
| AI library | openai/math commit `4eaee87548250b2682affda7d05d947c05554bae` |
| Selected source subtree | Entire `OAI.MeasureTheory.Falconer` directory: 2,461 modules |
| Expanded source / compiled dependency closure | 13,205 modules, including 10,744 dependencies |
| Original compiler and kernel | Lean 4.34.1, commit `5045d0056413266e57c625dcd7c365b10e377c52` |
| Matching Mathlib checkout | `d13f23b723b8a846827a245b89c10fc7d3f11612`; dependency package revisions retained in its `lake-manifest.json` |
| Checker implementation | [CheckpointAudit.lean](CheckpointAudit.lean), qualified protocol introduced at `51f41a8`; frozen source equals this file byte-for-byte |
| Recorded completed reduction | `fa295de`; raw records independently re-audited for this report |

The inputs to checking are the exact typed artifacts emitted by measured
source construction. Construction includes 8,128 newly constructed modules
and 5,077 immutable common modules already constructed in the **same pinned
experiment**. Each common module's actual construction cost is included once
in this closure. This is not a fresh rebuild of those shared nodes. Both source
and validation use the same installed Lean toolchain; neither denominator
includes building Lean itself.

The Falconer source subtree contains 9,279,240 bytes and 7,312 lexical
lemma/theorem sites. A source census finds **zero explicit `decide +kernel`,
`native_decide`, or `bv_decide` sites in those 2,461 files**.
This is a source-level classification: it does not prove that every kernel
operation is cheap or that the 10,744 dependencies contain no computation.

## Complete costs and the Mathlib comparison

The machine is phobos-vt (i9-14900K). All timed native calls hold the shared
P-core lock and run on CPUs 0–7, with no Lean `-M`. Falconer child processes
use an external 11.75 GiB cgroup, leaving room for the small parent within the
12 GiB O-line allocation. Peak RSS below is the largest individual process
`wait4` RSS, not the sum across sequential processes.

| Closure / checking protocol | Modules | Processes | Successful source wall sum (s) | Checking wall sum (s) | Check / source | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|---:|
| Falconer, persistent checkpoints | 13,205 | 27 | 22,077.770248 | 2,043.585476 | **9.2563%** | 10.368 |
| Mathlib Nat.Basic, historical uninterrupted stream | 1,330 | 1 | 622.379412 | 65.692644 | **10.5551%** | 0.719 |
| Mathlib Nat.Basic, matched checkpoint protocol | 1,330 | 3 | 622.379412 | 91.279127 | **14.6662%** | 1.324 |

Exact machine-readable numbers are in
[falconer-paper-table.csv](falconer-paper-table.csv). Falconer native user plus
system CPU sums to **2,038.443942 s**; the primary ratio above uses wall sums
on both sides.

The Falconer ratio is 1.30 percentage points below the historical Mathlib
10.56% result. Both support a mathematical cost regime in which checking typed
terms costs a small fraction of producing them: tactics and repeated
per-module frontend imports need not run again. Falconer's zero explicit
kernel-decision sites make this interpretation consistent with its source
structure. It is not evidence that AI authorship itself reduces checking cost.

The historical Mathlib stream used a different audit adapter and no persistent
checkpoint. The **matched checkpoint-protocol comparison is 9.26% versus
14.67%**, a 5.41 percentage-point difference. That comparison uses the same
500-new-module checkpoint policy, including its costs. The increase from
65.69 to 91.28 s for Mathlib is an observed **25.59 s combined protocol/adapter
difference**, not an isolated measurement of snapshot I/O. Workload composition,
context fallbacks, fixed startup costs and prefix serialization were not
causally isolated. Neither comparison supplies a population estimate or a
guaranteed service speedup.

For scope, Falconer's AI files account for 6,476.297931 s of source work and
its dependencies for 15,601.472317 s. The 2,043.59 s checker numerator covers
**both**, so it cannot be divided by only the AI-file denominator.

## What was checked, and correctness evidence

The checker reads the original compiled core terms in dependency order and
uses the **unmodified Lean 4.34.1 kernel replay** for newly checked eligible
declarations. It preserves declaration identity and module visibility rather
than assuming that all sibling module environments may be merged safely.
The final event records 800,218 input declaration entries, 794,694 unique
declarations in the shared kernel environment, and **19 module-local context
fallbacks**. Those fallback checks are included in the measured numerator.

The correctness observations are:

- Segmented acceptance union: exactly the 13,205 planned module IDs, with no
  duplicate new-module charges, rejection events or malformed JSON records.
  The native import graph equals the planned graph.
- Independent module-local reference: the same 13,205 accepted IDs, using
  independently finalized per-module environments and the frozen original
  auditor. Its union comprises 5,077 exact common-node qualifications and
  8,128 further modules in 16 completed chunks. Reference cost is separate
  from the evaluated check cost.
- Checkpoint/restore qualification: five cases across 18 naturally completed
  processes preserve ordinary duplicates, conflicting definitions and private
  names, and reject a corrupt duplicate proof and an illicit sibling reference
  **after restore**. The earlier original-kernel qualification separately
  rejected three mutated proofs in distinct Nat theorems through both checking
  paths.

This establishes agreement on the measured acceptance sets and named negative
controls, not a universal proof of transparency. Lean's replay policy excludes
unsafe/partial declarations (4,451 entries here); axioms retain Lean's normal
meaning. Accepting a module is not a no-axiom/no-sorry guarantee. The artifact
reader, declaration/visibility audit, checkpoint provenance and serialization
remain explicit correctness obligations.

## Why this run uses durable segments

Two uninterrupted attempts reached their **1,500 s process timeout** before
finishing: 1,500.210998 s with 8,942 surviving acceptance events, and
1,500.204755 s with 9,040. Neither is a completed validation result. Their
combined **3,000.415754 s** remains in the recovery records and is excluded
from the successful segmented-protocol cost, rather than erased or amortized
away. A prior 0.053097 s source-overlay failure is likewise retained outside
the successful-source denominator.

**Segmentation answers an operational process-timeout constraint; it is not a
logical requirement of original-kernel checking.** We do not claim that a
longer-lived unsegmented process is impossible or that its runtime would equal
the segmented total.

Each of the first 26 processes accepts 500 new modules and exports a delta
containing only original-kernel-accepted constants plus private audit metadata.
The next process imports only that certified predecessor chain, restores the
module visibility/audit state, and checks new terms. The final process checks
the remaining 205 modules. There are **26 exports and 26 restores**; the saved
delta files total **6,059,893,600 bytes (5.644 GiB logical file size)**.
This is a private chain for frozen inputs, not a verifier that trusts arbitrary
user-supplied snapshots or a cross-candidate result cache.

A streaming validation service with these process lifetime bounds therefore
needs durable, provenance-bound checkpoints to make progress across restarts.
The result suggests this operational design requirement; it does not establish
a novel checkpoint technique. Certification of the prefix and its input
identity must survive a restart. It is unnecessary to replay tactic search
or recheck that same certified prefix after every segment. Releasing a process
does not imply that all transitive dependency state can be discarded.

**The 2,043.59 s already includes checkpoint costs.** In the frozen native
runner, `time.monotonic()` starts immediately before `subprocess.Popen`
and stops after `os.wait4` returns. Inside that interval, the checker
restores the preceding snapshot before visiting new terms and calls
`saveModuleData` before emitting its checkpoint event and exiting.
Thus process startup, original-kernel checks, all 26 prefix reloads,
all 26 snapshot serializations/writes and process exit are charged. The
snapshot write-return cost is included under normal OS page-cache semantics;
no separate physical-disk-flush durability latency was measured.

No snapshot time needs to be added to this numerator, and a new Lean run is
unnecessary to establish inclusion. The export/import components were not
timed separately, so their isolated seconds and counterfactual cost without
checkpoints are **unknown**, not zero. Lock waits, Python reduction/commit
work, checker compilation, correctness-reference runs and the failed full
attempts are outside the successful native-process sum. This is neither one
uninterrupted stopwatch measurement nor total investigator recovery time.

## Reproduction, evidence and index status

Run the offline audit against the retained PVC (no native validation is started):

```sh
taskset -c 8 python3 research/decoupled-check/audit-falconer-paper.py
```

It checks raw segment verdicts, predecessor identity, module quotas, acceptance
sets, graph equality, original-reference events and resource/cost records, then
regenerates [falconer-paper-evidence.json](falconer-paper-evidence.json) and
[falconer-paper-table.csv](falconer-paper-table.csv). The native worker and
original protocol are [falconer-checkpoint.py](falconer-checkpoint.py) and
[falconer-checkpoint-plan.md](falconer-checkpoint-plan.md).
[Per-segment costs](falconer-segmented-costs.csv) and
[reference completion](falconer-parity-progress.md) retain their own records.

Raw root on the existing PVC:
`/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031`.
Falconer commands, stdout/stderr, source artifacts and frozen worker are under
`scale-study/falconer-project-20261101/`; completed segments, snapshots and
their original runner outputs are in `checkpoint-recheck-v2/`; original
module-local chunks are in `bounded-recheck-v1/`.
The source frame, dependency package lockfiles and earlier unsuccessful attempts
remain in place.

The shared `research/README.md` was checked on 2026-11-02 at parent
`fa295de`: its decoupled-check row still described only four closures, and
its root0260 historical entry still reported Falconer as incomplete. It had
**not yet indexed this completed result**. This O-line change updates the
owned [directory index](README.md); it leaves the shared parent index untouched
under the user's `research/decoupled-check/`-only ownership rule.
The main thread can add the following **new current result** without rewriting
historical root0260:

> Falconer mathematical closure: 13,205 source nodes / original-kernel accepts,
> 27 checkpointed processes; 2,043.59 / 22,077.77 s = 9.26%. Snapshot I/O charged;
> identical module-local acceptance set. Matched checkpointed Mathlib 14.67%;
> historical unsegmented Mathlib 10.56%. See decoupled-check/falconer-paper-result.md.

The data support additional RQ2 evidence on one complete AI mathematical
subtree. They do not measure all 163,097 openai/math modules, establish
calibrated uncertainty from repeated runs, or isolate a general speedup caused
by checkpoints.
