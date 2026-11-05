# External installed-tool acceptance at e000ed62 (preview)

Checker: e000ed62bbf4b9c420bd99d0273a5d21829b4edc, ABI6, shared-checked.
CPU8–9 during the census; every timing is a preview. Packaging inputs were dirty
and recorded, not an immutable public release. No P-core lock was acquired.

| Project | Upstream commit | Native closure | Official common local roots | Equal roots | Covered / source | Omitted |
|---|---|---:|---:|---|---:|---:|
| newspeak | e2232d8fdb9a6061d00419fa83134e4e60caf172 | 754 | 105 | yes | 105/105 | 0 |
| solar | f4f5c9a1d7443a0265a85eff8ee24824d9ab92a7 | 2368 | 12 | yes | 12/32 | 20 |
| samuelburbulla-proofs | 3042904c5f7e96732c1ff4ac01745a8be9ae91ff | 10753 | 9 | yes | 9/9 | 0 |

samuelburbulla/proofs is upstream explicitly AI-generated, at the pinned commit
3042904c5f7e96732c1ff4ac01745a8be9ae91ff. Its earlier source preparation and
attribution remain in ../freeze-preview-results.md. CrocSwap is not substituted
for this AI requirement.

The official default replays named local roots and trusts imports. Equal roots
above do not establish identical full-closure obligations or a speedup. Native
receipts retain axioms and compiled input identities; source binding limitations
are explicit in audit. Solar omitted20 source modules from declarative defaults.

AI used three native invocations, two ending at the existing1740s preview bound.
Those calls keep CPU unknown; complete_native_cost_available is false. The tail
CPU is not complete-case CPU, and all intervals remain separate. Final runs use
fresh state and do not resume this preview.

Raw logs/results/checkpoints: /workspaces/.agent-state/proofserve-o-line/freeze-e000ed62-20261105/preview.
Bundle/container validation: ../../../packaging/FREEZE_E000ED62.md.
