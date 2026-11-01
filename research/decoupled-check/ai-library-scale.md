# AI-library selection, scaling scenarios and the environment boundary

This is O-line self-review and untimed preparation, not a completed AI-library
cost ratio. Raw inputs and preparation receipts remain at
`/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/scale-study`.
The existing four-cohort native collection continues unchanged.

## A complete AI mathematical subtree

We selected the entire `OAI.MeasureTheory.Falconer` directory at openai/math
revision `4eaee87548250b2682affda7d05d947c05554bae`: 2,461 modules,
9,279,240 source bytes and 7,312 lexical theorem/lemma sites. Its source graph
has 2,461 internal members and 222 external frontier module names; the latter
still require expansion through the matching compiler/library artifacts.
There are zero lexical decide-plus-kernel, native_decide or bv_decide sites.
This does not guarantee every statement is proved or every file builds.

All 2,461 pinned source files have now been extracted to the PVC outside the
checkout. The source-name selection is retained in falconer-selection.csv;
the complete import graph and exact inputs stay in the raw directory.
Extraction used an untimed E-core preparation process, with an external64MiB
cgroup: peak38,031,360 charged bytes, no OOM, natural exit and retired processes.
The earlier census process reached that cap without OOM; its separate receipt
is retained. No extra Lean process or timed capture was started for preparation.

Selection is a whole, clearly mathematical project with accessible sources,
not a random sample or a population estimate. The W-line45,251-member count is
a source-size/depth/computation *stratum*, not a directory to call a subtree.
The next measured point must reconstruct the full external closure and every
Falconer member with the stock compiler, then check those exact typed artifacts.
Costs from incomplete subsets or historical source-only runs cannot supply
that point's denominator. The existing NearPinDeletion closure contains only a
small part of Falconer and cannot stand in for the complete directory.

## What the import-set census establishes

W-line commit d8a7ef0, workloads/openai-math/import-set-reuse, reports163,097
source modules and143,637 distinct unordered direct-import-name sets.
The100 most frequent sets cover8,061 modules, or4.94246%; the largest covers
4,415. Exact direct-name-set repetitions cover19,460 modules(11.9315%) after
one producer per class. That count is not time saved.

Elaboration can depend on import order, syntax, instance priorities, simp
extensions, other persistent extensions and options. A common *superset*
environment can therefore change elaboration behavior. The census supports
the limited coverage of exact whole-import-name-key reuse. It does **not**
prove that elaboration cannot share dependencies, a prepared base or prefixes:
different name sets can even denote equivalent environments. The source census
does not expand external library dependency graphs and does not encode every
import modifier or semantic state component.

By contrast, an elaborated core term already records resolved constant
references and arguments. Kernel-only checking can avoid replaying tactic
search and tactic extension registries and share compatible, previously
checked declarations. The complete1,330-member Mathlib result demonstrates
one realized cost separation:65.69s checking versus622.38s source compiler
work(10.56%). It does not establish the same ratio for the AI library.
The workload's diverse elaboration inputs motivate decoupling; they do not
alone prove universal semantic transparency of a merged kernel environment.

## Name and theory boundaries

The original Lean4.34.1 kernel remains necessary, but a changed input theory
can still change an outcome. The adapter must preserve these distinctions:

- Public fully qualified names can collide across independently valid sibling
  modules. Different definitions under the same name cannot coexist in one
  kernel environment. They require context separation, not proof rejection.
- Same surface private names usually compile to module-qualified _private
  names. Surface-name or source-fingerprint collisions do not establish typed
  declaration conflicts. Generated auxiliaries also require actual compiled
  identities and their complete metadata.
- Lean/Replay.lean's theorem path skips a theorem already present with matching
  name, level parameters, type and mutual all-list; it does not compare the new
  proof value. Thus a corrupt sibling theorem can be hidden by a preceding
  same-name theorem in a naive union. A declaration-identity/visibility audit
  or separately checked context is required before claiming union parity.
- A new proof must not gain access to an unrelated sibling's constants or
  axioms. Check visibility from the module's actual dependency closure;
  checking with the same executable in a stronger environment is insufficient.
- Compare typed declaration kind, universes, type/body, safety/reducibility and
  inductive/constructor/recursor/mutual metadata, not hashes alone.
- Upstream replay excludes unsafe/partial constants. Normal axioms retain their
  original meaning; absent private proof bodies or exported axioms are not
  independently proof-checked bodies.

The existing measured closure had matching acceptance sets and three rejected
corrupt proofs; these results do not cover adversarial duplicate-name sibling
modules. The old frozen input/capture is preserved. Additional native controls
will target these boundaries before a multi-root Falconer union is qualified.

## Whole-library scale: scenarios, not forecasts

The pinned lexical inventory totals2,363,592 theorem/lemma sites and1,354,379
explicit decide-plus-kernel sites across163,097 modules.
These are source counts, not actual ConstantInfo counts, a guaranteed lower
bound, or a successful-build census. Macros, auxiliaries, ordinary definitions,
failed production and proof-expression size all matter.

scaling-observations.csv contains two complete streaming observations:
1,330-module Mathlib,132,484 input entries,0.719GiB peak RSS,65.69s; and the
3,793-module retained-cache Grid control,382,707 entries,2.167GiB,557.72s.
The latter is not yet the primary matched-artifact construction/check pair.
The respective ratios are5.69 and5.94KiB RSS/input entry, and0.496 and1.457ms
per input entry. They are distinct workloads, **not** an in-process growth
curve, confidence interval, asymptotic law or lower/upper bound.

For explicit capacity planning only, full-library-scenarios.csv assumes the
larger observed base plus1,2,4 or8 compiled entries per lexical theorem site.
At the two observed memory rates these scenarios span14.9–15.6GiB(1x) through
104.7–109.3GiB(8x). Associated linear time scenarios span0.38–1.11hours(1x)
through2.66–7.81hours(8x). These are conditional arithmetic, not a promise that
the library verifies in those times or proof it exceeds12GiB. Kernel
computation heavy tails make uniform time extrapolation especially weak.

We cannot assume the full library fits the O-line12GiB allocation. A real
large-subtree run needs within-process checkpoints of declarations, mapped
regions and RSS/PSS, with a separately identified profiling run if checkpoints
add cost. Context-compatible dependency segments may bound live environments,
but dependencies still required by a later proof cannot simply be discarded.
Rechecking/IO from segmentation must be included. A segmentation fallback
must not be described as one global environment.

Only1,647 OAI compiled artifacts were available in the retained typed cache at
preparation time; the163,097-source corpus is not a ready-to-check compiled
library. Independent checking is cheaper *after* typed proof artifacts exist.
Source-only AI candidates still pay their initial elaboration/production cost.
No end-to-end RL or source-validation speedup follows from the recheck ratio.

Sources: W-line d8a7ef0 import-set census; the pinned lexical CSVs under
workloads/openai-math/static-4eaee875; same-closure measured raw captures; stock
[replay implementation](https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Replay.lean)
and [module environments](https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Environment.lean).
