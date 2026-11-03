# Four full-closure record profiles decoded

All four records returned the same 4,449 reference module IDs, 237,863 ordinary
checks and 3,283,925,639 allocation-counter units. This completes sampling,
not the original matrix: cell16, the trailing P2 plain run, remains pending.

The units below are billions of cycle-sample periods. They are estimates in
two separately reported call-stack scopes, not exact hardware counts and
not seconds obtained by rescaling another run.

## Strict checkOne + C++ kernel ancestry

| Family | 1P | 2P | 4P | 8P | 8P minus 4P |
|---|---:|---:|---:|---:|---:|
| Environment/hash/cache lookup (includes inline ownership) | 262.802 | 258.773 | 266.395 | 311.380 | 44.985 |
| Explicit RC and destruction | 87.889 | 82.688 | 88.560 | 107.170 | 18.610 |
| Allocation/free | 77.343 | 74.365 | 68.477 | 76.992 | 8.516 |
| whnf/defeq (unresolved inlines retained) | 140.998 | 128.719 | 140.837 | 149.643 | 8.806 |
| Other kernel inference | 104.861 | 83.415 | 87.945 | 92.923 | 4.978 |
| Other/unresolved | 0.130 | 0.064 | 1.216 | 0.085 | -1.132 |

## Additional worker + kernel ancestry without checkOne

| Family | 1P | 2P | 4P | 8P | 8P minus 4P |
|---|---:|---:|---:|---:|---:|
| Environment/hash/cache lookup (includes inline ownership) | 147.362 | 164.305 | 179.078 | 241.127 | 62.049 |
| Explicit RC and destruction | 27.231 | 27.215 | 34.107 | 44.546 | 10.439 |
| Allocation/free | 28.332 | 29.580 | 29.108 | 32.593 | 3.485 |
| whnf/defeq (unresolved inlines retained) | 129.228 | 130.556 | 141.620 | 151.349 | 9.729 |
| Other kernel inference | 4.747 | 5.068 | 4.827 | 5.071 | 0.245 |
| Other/unresolved | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

The largest coarse absolute growth is lookup: +44.985 G in the strict
scope and +62.049 G in the additional scope. Coarse lookup is not pure hash
arithmetic: the actual ownership instructions inside environment lookup
account for much of its growth. See ownership-localization.md for the
post-hoc IP analysis and its explicit skid/causality limits.

P2 recorded 35,176 cycle samples. All seven counter events retain every
captured CPU-shard READ for its three historical checking TIDs; their lifetime
IPCs are 1.936, 1.956 and 1.962. P1 also has complete worker READs. P4
completeness remains unknown; P8 has five incomplete worker READ sets.
The corresponding ratios remain blank in the primary CSV. Native acceptance
does not depend on counter-metadata completeness.

The prepared recorder repair has been narrowed to purpose-specific official
record --no-samples --stat: collect only inherited counts, without DWARF
sampling, after the original16 cells retire. The earlier uncompressed-only
proposal was never executed. No Lean/runtime or current native setting changes.
Any successful supplemental counts have their own run label and denominator.
The original incomplete capture remains failure evidence.
