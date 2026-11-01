# Prior-work check and the remaining claim

M same-thread review, 2026-11-01. Search is for independent proof checking,
automatic decomposition of expensive computation inside a proof, and trusted
recombination. It is **not** a claim that parallel proof checking is new.
Only primary papers, official documentation and the pinned SDK source below
are used for conclusions.

| Prior system/work | Verified overlap | Difference to the proposed measurement |
|---|---|---|
| Wenzel, *Parallel Proof Checking in Isabelle/Isar*, PLMMS2009 | Parallel full proof checking, future values and the structure of nested proofs; this directly occupies the broad parallel-proof claim. | Our question is whether large closed reduction obligations in a modern generated Lean corpus can be decomposed automatically with a useful complete cost, not whether proofs can run concurrently. |
| Barras, Tankink, Tassi, *Asynchronous processing of Coq documents*, 2015; Rocq documentation | Decoupling statement/definition processing and opaque proof construction/checking. Official documentation distinguishes asynchronous progress from final kernel checking. | Our prototype waits for every original-kernel child check and checks the assembled theorem. It does not count delegated or unfinished tasks as accepted proofs. |
| Rocq `par:` selector | Applies a terminating tactic across focused goals in parallel; goal-level parallelism already exists. | The target problem initially has one closed computation, not an already supplied list of independent subgoals. Splitting and merge overhead need measurement. |
| Lean4.34.1 asynchronous environment and `Lean.Elab.Parallel` | Theorem elaboration/task utilities and asynchronous signatures are existing mechanisms. SDK environment documentation explicitly chains the checked kernel environment. | Merely enabling async elaboration is not evidence that one large kernel reduction is parallel. Our prototype uses immutable imported bases, checked children and ordinary module loading, and measures that extra work. |
| Färber, *Safe, Fast, Concurrent Proof Checking for the lambda-Pi Calculus Modulo Rewriting*, CPP2022 (Kontroli) | A thread-safe concurrent proof checker with multicore results; strong same-mechanism precedent. | Different logic/checker and exported proof datasets; our requested prototype keeps Lean's C++ kernel and examines generated arithmetic reductions. This does not establish mechanism novelty. |
| Heule, Kullmann, Wieringa, Biere, *Cube and Conquer*, HVC2011/proceedings2012 | Decomposition into independently solved subproblems and a subsequent combination is established in SAT. | SAT cubes partition search under assumptions. Record equality/finite-universal chunks partition deterministic checking; existentials need witness/disjunction-aware recombination, not an unconditional conjunction. |
| Strub et al., *Self-Certification*, POPL2012 | Certificate splitting into smaller definitions is used to make certificates manageable for Coq. Splitting certificates is itself prior art. | Our data must show whether an automatic decomposition and placement has a new workload-specific opportunity, rather than naming certificate splitting as a contribution. |

## Verified primary sources

- [Wenzel paper](https://www21.in.tum.de/~wenzelm/papers/parallel-isabelle.pdf)
  and [author's publication metadata](https://www21.in.tum.de/~wenzelm/papers/).
  Primary PDF text was returned by search after a direct fetch timeout; metadata
  names PLMMS2009. Search-engine “published last year” is not the paper year.
- [Coq asynchronous processing paper](https://arxiv.org/abs/1506.05605);
  [Rocq asynchronous documentation](https://rocq-prover.org/doc/v9.2/refman/addendum/parallel-proof-processing.html);
  [official par-selector history](https://rocq-prover.org/doc/V9.2.0/refman/changes.html).
- [Lean task utilities](https://leanprover.github.io/hex/docs/Lean/Elab/Parallel.html);
  [pinned environment implementation](https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Environment.lean);
  [pinned declaration implementation](https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/AddDecl.lean);
  [pinned decide implementation](https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Elab/Tactic/Decide.lean).
  The local installed SDK source, not the moving latest manual, is the authority
  for our running implementation.
- [Kontroli primary paper metadata/abstract](https://arxiv.org/abs/2102.08766):
  CPP2022, revised2022; published results concern that checker's own evaluated
  datasets and are not predictions for Lean.
- [Cube-and-conquer primary paper](https://www.cs.utexas.edu/~marijn/publications/cube.pdf)
  and [publisher/authors' institutional metadata](https://research.tudelft.nl/en/publications/cube-and-conquer-guiding-cdcl-sat-solvers-by-lookaheads/).
- [Self-Certification primary paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/popl2012-paper211.pdf).

The current latest Lean manual explicitly distinguishes `decide +kernel`
from native compilation and says the kernel mode avoids a second elaborator
evaluation. Therefore the phrase “the computation is repeated” needs a boundary:
independent replay can repeat kernel work, while an ordinary single `+kernel`
call does not intrinsically evaluate twice.
[Official tactic description](https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Tactic-Reference).

## Query coverage and disposition

Queries (2026-11-01 UTC): “Isabelle parallel proof checking futures computational
reflection proof checking parallel”; “Coq Rocq par tactic proof checking
asynchronous proofs kernel parallel”; “Lean parallel elaboration theorem checking
parallel kernel decide”; “cube and conquer guiding CDCL SAT solvers lookaheads”;
“parallel proof by reflection Coq split computations lists certificate parallel”;
“parallel reduction kernel computation proof assistant reflection parallel checking
chunks”. Adjacent checking/certificate results exposed Kontroli and
Self-Certification as additional overlap.

**High same-claim risk** for parallel proof checking, futures, proof reflection
or certificate splitting in isolation. No verified source in this finite search
establishes the identical automatic Lean record/finite-domain transformation
evaluated on this pinned corpus, but absence from this search is not proof of
firstness. The defensible current contribution is the measured distinction
between workload cost regimes and a causal test of whether decomposition
helps the expensive regime. Performance, coverage, sharing lost on splitting
and complete serialization/import/merge costs must decide the claim.

No competing system was installed or reproduced. No source paper is treated as
authority to change the user's scope or select a different thesis.

## Focused follow-up: splitting and loading costs already have precedent

Reopened the primary Self-Certification paper, section7.2–7.3, on2026-11-01.
It describes both source-level and further Coq-level certificate splitting,
reuse through opaque lemmas, and substantial dependency-loading costs when
checking later pieces. This directly overlaps not only splitting, but the
serialization/import cost concern of our prototype. It is sequential checking
in that description; the paper does not establish our specific automatic
numeric-record transformation or its multicore curve.
[Primary paper, sections7.2–7.3](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/popl2012-paper211.pdf).

A primary practitioner account describes restructuring a large Lean matrix
computation into row certificates, but its demonstrated verification uses
native_decide and explicitly trusts compiled evaluation. It is another
precedent for arithmetic decomposition; it does not demonstrate unchanged-
kernel parallel checking. Its performance numbers are the author's report,
not results reproduced here.
[Huang,2026-06-27](https://infsup.com/en/tell-dont-compute/).

The pinned Lean C++ source gives each theorem checker its own reduction and
conversion caches. Splitting one theorem across separate checkers therefore
does not share those caches. This supports *possible repeated work*, not a
measured attribution of all extra CPU. Other costs include changing one record
decision into field conjunctions and writing/loading child modules.
[Checker state](https://raw.githubusercontent.com/leanprover/lean4/v4.34.1/src/kernel/type_checker.h),
[theorem-checking entry](https://raw.githubusercontent.com/leanprover/lean4/v4.34.1/src/kernel/environment.cpp).

Local Lean/Environment.lean2307–2400shows that normal finalizeImport builds new
constant maps and initializes imported extensions;2438–2449performs a fresh
import traversal. It is not an incremental merge into our existing base.
A stock leakEnv option may alter marking costs, but no result here measures
that option and no import time is claimed to be a fundamental lower bound.
No unchecked environment mutation is used to bypass this cost.
