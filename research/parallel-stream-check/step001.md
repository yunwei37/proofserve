# Step 001 — checked declaration frontiers (自审)

## EXPERIMENT
Question: can the existing streaming reader reuse original-kernel checked wave
results without public replay checking every proof twice?
Implemented a pinned checked-token commit adapter. Lean compilation and native
linking passed. 16 actual controls pass at workers 1 and 8: ordinary duplicates,
private declarations, conflicting definitions, valid dependent waves, bad duplicate
proof, unimported sibling proof, duplicated token, and stale frontier.
The four negative categories require explicit reject events, not merely nonzero
process exits. All processes retired. Full closure timing/acceptance remains open.

An initial control implicitly imported full Init and took 139.65s on E cores.
Strict proof-body duplicate comparison cascaded into module-local fallbacks.
That finite diagnostic was stopped because its 16 cells could not fit its 1740s
window; raw partial/cancellation records remain in parallel-stream-check/. Explicit
Init.Prelude fixtures now isolate the intended controls. The intermediate Waves
fixture used notation absent from Prelude and failed to compile; retained v2 logs.
The final v3 uses explicit Eq/Eq.refl and qualifies all controls.

## WRITE
README documents adapter trust, ordinary-declaration coverage, complex fallback,
and separate large-goal integration status. O's source remains read-only.

## REVIEW — 自审
No claim of unchanged implementation TCB, full Mathlib acceptance, scalability or
library speedup. Full constants and frontier/index identities are tested but are
not a machine-checked proof of the coordinator. Whole-closure duplicate handling
still requires a real native run. No additional agents used.

## Next
Run the exact 1330-module artifact closure with O reference, audited serial, and
parallel 1/2/4/8 in a finite P-core window, retaining failures. While it runs,
prepare same-process certificate integration and analysis without another Lean
process. Original build reference is serial compiler work, not parallel Lake wall.
