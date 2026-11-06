# Final installed-tool external-project evaluation

Review: 自审. All three fixed projects completed on 2026-11-06. This is the
post-census, post-matrix **final-system** collection, not an E-core functional
preview. No point is missing; no interrupted preview or partial CPU is reused.

## Results

Seconds; one fresh observation per arm. The module-count column is
**native full closure / official default local roots**. The last column is
the exact common-local-root pass-set comparison, not whole-closure equivalence.

| Project | Modules native / official | ProofServe CPU s | ProofServe wall s | Official CPU s | Official wall s | Common roots passed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| newspeak | 754 / 105 | 109.055 | 110.639 | 38.637 | 38.736 | 105/105 |
| solar | 2368 / 12 | 167.209 | 169.321 | 5.512 | 5.539 | 12/12 |
| samuelburbulla-proofs | 10753 / 9 | 2481.041 | 2579.748 | 37.377 | 40.993 | 9/9 |

ProofServe used **one worker** for each project, as in the qualified fixed
manifest. Each native command completed in one uninterrupted invocation from a
new empty checkpoint directory. All native, official and audit commands returned
0: nine complete commands, zero incomplete points. The complete AI CPU is now
available; its earlier interrupted-preview CPU remains unknown in its old records.

**There is no equal-obligation speedup comparison.** ProofServe checks the
transitive compiled-artifact closure; stock default replays the named local
roots while trusting imported proofs. All 126 common local roots were accepted
by both. The official run does not provide a separately checked full-closure
ledger, so neither whole-closure acceptance equivalence nor axiom-set parity is
established here. No ratio between these different costs is presented as a
ProofServe speedup. Official --fresh is a distinct protocol in
[M's final matrix](../../../checker/results/release-e000ed62bbf4/matrix/README.md),
not an extra arm of this fixed three-project evaluation.

## Versions and installed shape

Release/tool source: **818f74229434b888702a2d72b370cb2e07c79b36**.
Frozen native checker: **e000ed62bbf4b9c420bd99d0273a5d21829b4edc**.
Both native and original SDK leanchecker use **Lean 4.34.1**.
The prepared archive was rebuilt and relocated into a new installation by the
documented packaging/freeze.py --final --prepared-from command. The command
used the previously qualified immutable checker source/build, rather than M's
live build. No source checkout or build-host SDK path is needed by the installed
tool itself; the evaluator supplies already-built Lake projects as inputs.
The local bundle records glibc 2.41 and is a local Linux qualification artifact;
this is not a new portability test of the prepared Ubuntu release workflow.

Input commits:
- newspeak: e2232d8fdb9a6061d00419fa83134e4e60caf172.
- solar: f4f5c9a1d7443a0265a85eff8ee24824d9ab92a7.
- samuelburbulla-proofs: 3042904c5f7e96732c1ff4ac01745a8be9ae91ff.

The fixed AI collection is upstream
[samuelburbulla/proofs](https://github.com/samuelburbulla/proofs), whose repository
About description says **“AI generated proofs of open math problems”**.
This was rechecked through its public REST metadata before launch.
**整体声明、比例未披露**: model, per-proof attribution, AI-generated fraction
and human editing fraction are not disclosed. This is an upstream repository-level
claim, not an independent authorship audit or a claim that every line is AI-written.
The earlier AI-assisted CrocSwap case remains historical and is not substituted
into this final set.

## Audit conclusions and boundaries

- Newspeak: static declarative defaults cover **105/105** local source modules.
- Solar: defaults cover **12/32**, leaving **20 proof-input modules** outside that
  static graph. This does not show that the files are invalid or that custom
  executable/CI targets never check them.
- AI collection: defaults cover **9/9**. Eight source modules contain explicit
  decide +kernel syntax (11 lexical occurrences total); one does not. This is
  the audit's lexical regime proxy, not a measured per-module cost model.

All audits completed and linked the compiled receipts by reported module names.
They do **not** cryptographically bind current source text to checked artifacts.
Per-module cost inputs were not supplied to audit, so costs_status is unavailable;
the CSV reports whole-command costs only. Lexical counts are not executions or
kernel costs. No new source build or deeper attribution experiment was run.

The checker reports axiom **declaration inventories**, including sorryAx and
compiler/runtime declarations. Newspeak additionally reports its native_decide
certificate axiom. These inventories do not prove that particular theorems use
each listed axiom, do not form a minimal used-axiom closure, and do not certify
that a project is sorry-free. Exact inventories and omitted source names are
retained in final-acceptance.json.

The native policy is shared-checked, checkpoint ABI6. The documented
default/strict theorem-body semantic difference remains; passing these honest
inputs is not universal agreement on arbitrary crafted artifacts.
These runs reported no operational errors or rejected modules. Their success
does not establish behavior on unsupported or malformed inputs.

## Conditions and accounting

Started 2026-11-06T11:27:47.442461+00:00; finished 2026-11-06T12:20:12.850525+00:00.
The full bounded orchestration took **3145.408 s (52.42 min)**,
including E-core package assembly/install/qualification, below 7,200 s.
Those preparation costs are not included in individual check cells.

Measurements were serialized by the existing pcore.lock and restricted to
P cores **0–7**; preparation/decoding used E cores **8–9**. No Lean -M was used.
The fixed order was Newspeak, Solar, AI; within each, native then official
default then audit. Each cell has n=1; no confidence interval, randomized-order
or cold-cache claim is made.

zettai-dev and agentsight-dev remained running and unmodified. Preflight
metrics showed approximately **1.003 CPU cores** for zettai-dev and 0.002 for
agentsight-dev. The study Workspace had no competing compile/check task.
This was **not an exclusively idle host**. The brief observation-channel SSH
disconnect did not restart or interrupt the detached original controller;
its PID/birth identity was rechecked.

CPU is wait4 user+system for the completed command and its reaped descendants;
wall is the evaluator's monotonic interval. Memory columns distinguish sampled
own-tree RSS from cgroup memory charges. The existing 12 GiB policy was kept;
no timeout, OOM, sampler resource stop or disk-ceiling failure occurred.
The AI cgroup recorded **888 memory.max events**, with oom and oom_kill both
zero. This is a **resource-bounded** cost, not an unconstrained-memory measurement;
inspect the retained memory.events rather than treating memory.peak as RSS.

At 2026-11-06T12:21:01.003106+00:00, /proc/locks contained no entry for the P-core lock's
device/inode. A nonblocking lock probe succeeded and was released; no active
final-check process or live O external cgroup remained. The native slot is free
for M's built-subset check. Nothing here launches that next study.

## Files and raw provenance

- [final-measurements.csv](final-measurements.csv): six primary command costs,
  scope/counts, pins, one-worker setting, memory observations and eligibility.
- [final-acceptance.json](final-acceptance.json): exact common-root names, audit
  conclusions, upstream AI quote, inventories, conditions and lock retirement.
- [freeze-final-measurements.csv](freeze-final-measurements.csv) and
  [freeze-final-acceptance.json](freeze-final-acceptance.json): unchanged original
  helper exports, also retaining audit command costs. The curated files above
  derive from the same completed raw records; they add no independent samples.

Raw stdout/stderr, all 22 AI certified segments, receipts, memory/operational
records, fresh archive/install and command logs remain on the existing PVC at:

    /workspaces/.agent-state/proofserve-o-line/freeze-e000ed62-20261105/final

Launch, background, reconnect/identity, reducer and retirement evidence is at:

    /workspaces/.agent-state/proofserve-o-line/final-external-20261106

The reproducible maintainer command is in
[packaging/README.md](../../../packaging/README.md#one-command-final-external-timing).
No tag, registry upload, public announcement, checker change or source-input
repair occurred in this collection.
