# Official checker comparison protocol

The initial small contract is functional evidence, not a release speed result.

Official Lean 4.34.1 default mode selects modules by name prefix and replays each
selected module against trusted imports. To compare full closures, enumerate the
same modules and inspect verbose output for prefix-expanded extras. Include
import, scan, and I/O costs in the actual CLI denominator. A leaf-only check is
not comparable to a fully checked dependency closure.

Official --fresh accepts one target, imports its final merged environment, and
calls Kernel.Environment.replay from empty. ProofServe checks each module in
dependency order and validates incoming duplicate proof payloads. A matching
target name alone does not prove matching declaration work. If the proof ledgers
cannot be matched, report both procedures without a speedup ratio.

Both preserve the upstream exclusions of unsafe and partial declarations.
Axioms are accepted as declared. Official imports normally execute environment
extensions; ProofServe's declaration reader does not validate those extensions.

The portable Base/Fixture contract has no prefix-expanded extras or duplicate
interfaces. Both tools accept those two modules. Historical single observations
of Barrier default mode (65.423 seconds) and fresh mode (534.698 and 580.090
seconds) are not release-level strong-baseline timing.

Source: the installed SDK's LeanChecker.lean and Lean/Replay.lean.
https://github.com/leanprover/lean4/blob/v4.34.1/src/LeanChecker.lean
