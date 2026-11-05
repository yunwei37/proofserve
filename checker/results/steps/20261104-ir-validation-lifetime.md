# IR validation lifetime follow-up — 2026-11-04

Post-push implementation self-review (自审) found that the new IR format check
discarded compacted-region handles without freeing their buffers. The original
public API explicitly requires caller-managed region lifetime. This defect
belongs to the added adapter path.

## EXPERIMENT

Sixteen discarded validation reads left two file mappings for the IR signature/
data prefix. The public-API repair returns only region handles from a non-inlined
helper after dropping ModuleData references, then frees dependent regions first.
A short control returns from zero mappings to zero after 16 reads. A separate
live owner's two mappings and data survive another 16 reads. Generated C and
SDK ownership documentation were inspected; no private layout write was added.

The initial new unit used non-module Base, which has no IR signature; that
three-second setup failure is retained. The unit now runs against the existing
module-system IRBase fixture. Final-contract8 completed the actual combined
entry: core contract, 90 earlier command records, 109 new records. All 198 common
outcomes preserve exits, status, accepted/rejected module sets and axiom sets.
The finite process group retired with no budget stop at about 2.40 GiB sampled
own-tree RSS. All work used CPU 8–9 / 12 GiB and no P lock or -M.

## WRITE and REVIEW — 自审

The result README, new lifetime CSV/manifest and attempt index preserve every
failed intermediate and separate lifetime evidence from performance. Initial
981d544d engine41935144828 and smoke41935144829 both succeeded; the new source
requires its own CI. No independent execution review, publication or freeze
is claimed. The kernel, receipt schema and checkpoint layout are unchanged;
the executable identity still invalidates state from a different binary.

This forward correction is necessary because the earlier commit cannot be
rewritten. Large ABI 5 replay and final evaluation remain deferred until W
retires. Small mapping controls do not establish whole-library memory capacity.
