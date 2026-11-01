# Correctness scope and remaining obligations (自审)

Each newly accepted ordinary declaration is checked by the original
Lean4.34.1 C++ kernel. Checked-frontier merging additionally trusts the coordinator
and small C insertion adapter. Finite differential tests are not a theorem of
equivalence for every Lean artifact or library context.

## Ordinary frontiers

A planned wave has unique new names, no references to another job in the wave,
and no free metavariable/tactic state. Dependencies are already in the immutable
base. The kernel returns the actual typed CI; structural fields must match the
job. Joined results must cover original indices exactly. The C adapter checks
all frontier owners before inserting any CI. Original order is retained.

The reasoning is monotonic weakening: adding other fresh independent constants
does not change the meaning of any constant used by an already checked proof.
This relies on complete dependency discovery, correct visibility/binding
resolution, stable input, faithful ABI handling and the coordinator's implementation.
It is not justified merely by successful tests or the word "kernel".

Inductives/constructors/recursors/quotient declarations and cyclic plans use
upstream replay. Context conflicts use O's module-local path. The real v4
indirect duplicate-cycle counterexample demonstrates why a prior sibling's
binding must not discharge a cyclic local reference. V10+ reject it.

## Fin certificates

A selector matches the complete incoming CI to the owner-prepared reference from
the frozen profiled workload. It is trusted **eligibility policy metadata**,
not an untrusted client-supplied promise. Child/support terms are not trusted
for truth: support, all child theorems and final merge go through the original
kernel in the current context. The parent has its original name/type/levels;
only its proof changes. New root axioms must be a subset of [propext]; sorry and
new axiom payloads are rejected.

Native controls now cover all10 actual-source matches/80 pooled chunks/10 merges,
bad original proof and bad chunk. The two corruptions reach explicit original
kernel rejection. This does not establish acceptance equivalence after arbitrary
future dependency-definition changes, arbitrary option changes, or a corrupted
selector. The benchmark context is frozen. Unknown CIs use original checking.

## Scope boundaries

- A checked artifact body is not a check of source elaboration or all serialized
  environment extensions. Binary-format memory safety/authenticity are separate.
- Unsafe/partial exclusions follow upstream replay and are counted.
- Multiple failing tasks may select a different diagnostic order; byte-identical
  diagnostics or source-service behavior are not claimed.
- Tasks are joined before error propagation. Cancellation latency is not assumed
  free, and this prototype is not a low-latency failure scheduler.
- The short certificate controls import the prefix through stock APIs. That is
  different from independently rechecking every dependency in a cold stream.
- Resource stop/native failure is neither mathematical rejection nor a zero-time
  completed observation. RSS protection is sampled, with explicit headroom,
  and is not a kernel-enforced RSS quota.

The historical v4 throughput table applies to its real valid input only. Its
discovered malformed-cycle defect is retained; final repaired-version throughput
and complete computational-module curves remain open.
