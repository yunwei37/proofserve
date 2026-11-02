# Recovery preflight (self-review)

The adapter compiled with Lean4.34.1 and original native leanc. First compile
failed because a Nat mask was accidentally used as a ForIn set; the failed
compiler outputs remain on PVC. The forward fix iterates segregated modules
and tests membership in the bit mask. Both final compilation steps exit0.

Ten native boundary calls completed under P0–7 flock and an external cgroup:
ordinary duplicate theorems, corrupt duplicate proof, unimported sibling proof,
conflicting definitions, private auxiliary names, each in module-local and
indexed-audit modes. Both modes agree on all five verdicts; both bad-proof
cases have explicit reject events. This is adapter qualification, not full
Falconer parity. Complete raw commands/results/stdout/stderr and a terminal
are retained under bounded-recheck-v1/qualification-*.

The source diff changes only transitive-import visibility representation,
including quarantine membership queries, and adds ancestry/index state.
sameConstant, sameTheoremInterface, constantsOf, localReplay and both
checked.replay insertMap calls are unchanged. No unchecked declaration API,
skipKernelTC, altered kernel or trust-level setting is used.

An independent untimed source-graph DFS agrees with cached bit masks on all
13,205 modules. Its65.2s E-core diagnostic is not a verification numerator.
The full stream cell is now a fresh bounded check; source construction is not
repeated. Partial output must not be reduced as a complete result.
