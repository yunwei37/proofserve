# Official checker comparison protocol
No release performance ratios yet. All paper system numbers must come from
the committed checker executable; research prototype numbers are causal evidence.

Official4.34.1 default CLI selects modules by name prefix and replays each target
against trusted imports. Explicitly enumerate the same closure and confirm the
verbose selected set,including any prefix-expanded extras. Comparing one leaf
to a complete checked dependency closure is invalid. Import/scan/IO costs belong
in the actual CLI wall/CPU denominator. Its imported extensions execute normally;
ProofServe's declaration reader does not validate such extensions.

Official --fresh accepts one target,imports its final merged environment and
calls serial Kernel.Environment.replay from empty. ProofServe instead validates
each module in dependency order and checks incoming duplicate proof payloads.
Thus same target/closure is not sufficient to claim an identical declaration
work ledger. Default skips unsafe/partial;axioms are accepted as declared.
If the two procedures' proof sets cannot be matched,report separate procedures
and acceptance on their tested set;do not divide mismatched clocks into a speedup.
Source inspected: installed4.34.1 LeanChecker.lean and Lean/Replay.lean.
https://github.com/leanprover/lean4/blob/v4.34.1/src/LeanChecker.lean

Initial portable contract checks the two exact modules Base/Fixture,where there
are no additional prefix matches and no duplicate interfaces. Both tools accept
the same two names. This establishes that small functional comparison only.
Historical Barrier default65.423/fresh534.698/580.090 were single observations
with distinct procedures and are not release-level strong-baseline timing.
