# Receipt regression provenance

native-v1.json is a byte-for-byte copy of M's completed native receipt:
checker-release-51769793/math-P1-r1/receipt.json, root Mathlib.Data.Nat.Basic.
It is retained to exercise actual Lean UInt64 JSON encoding, ordered module
ledger and aggregate clocks. Parsing it is not a new checker experiment,
current-source binding, external-project qualification or a performance claim.
The original capture remains unchanged. Its original kernel/FFI/checkpoint trust
boundary is preserved. No native run was started to produce this regression.
