# Frozen e000ed62 package acceptance (preview)

All work used CPU 8–9 without pcore.lock, within the 12 GiB O limit, while W's
census continued. This is functional package acceptance and self-review (自审),
not quiet-machine system timing or an independent soundness proof. No new
adversarial case was constructed; only repository cases and benign strict-mode
checks on the existing valid fixture were used.

Native source: e000ed62bbf4b9c420bd99d0273a5d21829b4edc. O packaging inputs were
dirty preview changes, recorded explicitly; no container/archive is represented
as an immutable published release. The native checker directory was not edited.

## Completed

- Fresh Rust workspace tests, clippy, formatting, release build and all four
  crate dry-runs; no package upload.
- Fresh frozen checker build and existing contracts, including the 90- and
  142-command suites; command counts are not defect-class counts.
- Twenty audit tests.
- New archive extraction/relocation and original installed check/audit.
- Three existing malformed-proof categories actually rejected by the original
  kernel; unsupported-version control failed explicitly.
- Real strict flag forwarding, help, default/strict policy fields, ABI 6 and
  module/operational evidence fields checked on the installed valid fixture.
- Fresh full image build and network-disabled container run without host mounts,
  including both Mathlib service requests, accept/reject/sorry handling,
  installed project check/audit, strict policy and version error.
- Temporary builder and private test daemon retired.

The local six legacy native-REPL tests remain ignored; that is not counted as
local execution. Frozen-source GitHub CI separately ran the native/checker jobs;
its container job was skipped, so this local image result supplies that lane.

## External projects

| Project | Native closure | Official common roots | Common-root set equal | Audit |
|---|---:|---:|---|---|
| newspeak | 754 | 105 | yes | 105/105 source modules covered; 0 omitted |
| solar | 2368 | 12 | yes | 12/32 source modules covered; 20 omitted |
| samuelburbulla-proofs | 10753 | 9 | yes | 9/9 source modules covered; 0 omitted |

All projects are the pinned, already-built inputs in the manifest. The third
is upstream's explicitly AI-generated samuelburbulla/proofs collection at
3042904c5f7e96732c1ff4ac01745a8be9ae91ff; the retained earlier provenance
describes its preparation. No new project or reduced root set was substituted.

Official default trusts imports and replays the common local roots. Equality
above is that exact root set, not a claim that official checked the complete
native dependency closure or that these are equal-obligation speed comparisons.
Solar's twenty omitted source modules remain an explicit audit result.
Small summaries and cost CSVs are in data/external-projects/e000ed62-preview/.
Every cost is a preview; any interrupted native invocation keeps unknown CPU.

## README first thirty lines

````markdown
# ProofServe

**Independent checking and coverage audit for Lean projects.** Check compiled
proofs with the original Lean kernel; audit what the project actually covers.

The unpublished Linux bundle includes Lean 4.34.1, checker and audit tools.
With the prepared archive, installer and Python 3.11+, run without cloning:

~~~sh
python3 install.py --archive proofserve-0.1.0-linux-x86_64.tar.gz
~/.local/bin/proofserve check /path/to/built-lake-project
~/.local/bin/proofserve audit /path/to/built-lake-project --json -
~~~

**Trust:** original kernel, adapter, toolchain, declared axioms and protected
local checkpoints. This does not prove the specification, eliminate axioms,
sandbox project code, or safely parse arbitrary hostile binaries.

**Known default-mode difference:** a crafted artifact may be accepted while
official replay rejects its proof because it depends on another module's
theorem body. The statement still follows from kernel-checked proofs in the
checked closure. Use --strict-theorem-bodies for the tested artifact-context
agreement; unsupported native-evaluation inputs can still be refused.

**Cost:** retained Grid previews used 22.1× as many module-local replays and 2.33×
the CPU under the older strict-context strategy. This is historical evidence;
the new strict implementation has not been remeasured on Grid. [Policy data](checker/results/theorem-body-policy/).
**Speed versus official:** final same-obligation results are pending; preview
figures are not a release speed claim. [Trust and modes](packaging/INTERFACES.md).

````

## Final handoff

The exact prepared --final command is in packaging/README.md. Its manifest,
new output-directory path and existing P-core lock are ready on the PVC.
It rebuilds/installs a fresh archive around the same qualified frozen checker,
uses fresh native checkpoints and does not resume previews. Container and full
contract builds stay outside the final two-hour external window. CPU8–9 is
used for preparation; only external cells take P0–7 and pcore.lock.

This final command has been syntax/path checked, not executed while W runs.
The conservative handoff estimate is 95–115 minutes. The external preview cells
used about 92.9 minutes of accumulated wall intervals, including two AI window
interruptions; complete AI CPU is unknown. This is planning evidence, not an
uninterrupted end-to-end or P-core speed claim. Cold image/full contract work
is outside the final window; no project/root is trimmed.

Remaining: W completes its full census, M runs the final matrix, O is dispatched
for the final external run, then the agreed bounded corpus check and paper
completion. Only a real native defect changes the frozen checker.

Publication requires the user's explicit go-ahead. The GitHub release assets,
crates.io packages and image are not published or tagged here. If registry
publication is selected, the user supplies the existing workflow's
CARGO_REGISTRY_TOKEN secret; no credential was read or configured for that task.

Raw logs, intermediate/failed output, manifest and resource records remain under:
/workspaces/.agent-state/proofserve-o-line/freeze-e000ed62-20261105
