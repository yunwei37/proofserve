# What the shape census does and does not prove

> Current classification uses only direct explicit-header proofs. Earlier
> stale-header ratios are superseded; their original source and raw data remain
> in PVC lexical-census-v1. Native type and cost-panel data are unaffected.


The complete lexical census covers163,097 pinned source files /1,785,499,363bytes.
Its1,354,379masked sites exactly match both the unmasked narrow regex and W's
existing complete-corpus count. These are source occurrences, not executions.
5,848files contain a site (3.5856%of the corpus). Raw source archive and derived
per-site rows remain PVC-only; the small per-file totals are module-counts.csv.

The scanner masks ordinary strings/comments and recovers a local/declaration
header only when the body before the tactic is exactly whitespace plus by.
Inline proof arguments and goals transformed by earlier tactics remain unknown. This is **not Lean parsing or elaboration**. It does
not resolve notation, binders, namespaces or named predicates globally.
It recognizes538explicit conjunction/finite-domain candidates (0.03972%).
That number is **not** the global semantic splittable fraction: hidden finite
domains and record equalities are deliberately unresolved. In particular
816,321sites (60.2727%) have an equality-shaped recovered header with unknown
type, 459,167(33.9024%)are embedded/unresolved and9,316(0.6878%)are applications/other. A universal-only detector
would miss much of the observed hot regime.

| Shape | Safe logical decomposition, once types are known | Required conditions | Implemented here |
|---|---|---|---|
| Fin n universal | Partition outer index intervals; prove coverage and reconstruct the universal | Concrete finite domain; children closed after elaboration | census/design only |
| Bounded interval universal | Closed subrange universals plus original-kernel interval-coverage lemma | Actual bounded domain, not just a range token somewhere in a formula | census/design only |
| List universal / Boolean all | Split list segments and use an append/all equivalence | Preserve element predicate and dependent index meanings | census/design only |
| Finset universal | Prove each subset and coverage of the original set | Set coverage; overlap is sound but duplicates work | inferred domains remain unresolved |
| Nested enumeration | Split the outer finite quantifier, retain inner quantifiers locally | No shared unassigned metavariables; avoid repeated common preprocessing | census/design only |
| Conjunction | Each closed conjunct separately, original-kernel And introduction at merge | All conjuncts required; short-circuit failure/resource behavior can differ | generated conjunction groups |
| Nondependent record equality | Equality of all fields, recursively; constructor extensionality checks merge | Know constructors/fields, especially dependency/proof fields | actual PointBox/RBox/CBox generator;18Int leaves |
| Atomic scalar equality/comparison | Needs a computation-DAG/checkpoint certificate, not a blind field or range split | Proved bridge from partial computations to original expression | not implemented |
| Existential / mixed | Independent witnesses per outer universal, or a disjunction/coverage-aware search for an existential | Do not replace existential alternatives with an unconditional And | unsupported in prototype |
| Named predicate / unresolved header | Native elaborated type and controlled unfolding required | Text alone does not reveal logical/compute structure | native probes on compiled inputs |

The explicit interval/nested-Fin/Boolean-all categories have zero recognizer
matches in this pass. That is a property of this recognizer, not evidence those
computations do not occur. Mixed existentials are kept separate even when an
outer finite universal might later admit a split.

## Native evidence

The native probe reads actual mkDecideProof-headed helper theorem types from
compiled modules. It excludes unrelated auxiliaries such as omega-generated
proofs and numeral typeclass obligations. In the three first measured hot
modules, the counts equal their source-site totals, but that coincidence is not
assumed for other modules or type-indexed helper caches.

- Grid:1536RBox equalities +1536PointBox equalities +1536expanded conjunctions.
- UMoments9:1164CBox equalities.
- BarrierData41:1246Box equalities +74atomic integer comparisons.

These are7,092native helper declarations, of which7,018(98.9566%) have a known
structural split. Known record layouts have2/4/18Int fields, no dependent/proof
fields. This demonstrates logical decomposition in the hot subset, **not**
a measured fraction of its CPU that parallel execution will remove.

A read-only census of W's31completed no-M module attempts provides additional
scope. Its completed batches plus the first3-module probe yield26usable helper
mixes or zero-site cases. Five mixtures remain unknown: one missing global
compiled lookup, two no-matching-helper cases despite lexical sites, and two
in an interrupted metadata batch. Three90s metadata attempts remain as censored
queries, not rejected proofs or zero coverage. The full cost-weighted scope and
unknown list are in cost-weighted-summary.json.

## Time weighting

W's31selected attempts have811.2593s summed native wall /1342.9222s summedCPU.
Known-shape modules expose62.21%of that wall and60.19%of thatCPU. **Exposure is not
exclusive tactic time.** A module includes imports, elaboration, other proofs
and export, and its kernel helper bodies need not cost the same amount.

For the requested time-weighted opportunity, weight each observed module by
its own complete time and use its native-helper split proportion as a *model*:
sum_m(time_m * structural_helpers_m/helpers_m) / sum_m(time_m).
Under this uniform-within-module assumption, assigning the unknown mixtures
0..1 gives58.89–84.24%wall /57.64–83.79%CPU. These bounds apply to that
**model**, not to actually saved runtime. They are not a global Amdahl bound,
a confidence interval or a whole-library estimate.

A true work-weighted splittable fraction needs per-helper unperturbed timings,
or C-level traces linked to these exact elaborated types, with all module work
as its own denominator. We have not substituted whole-module clocks for those
missing tactic times. Nor do the two synthetic/hand-built grid examples predict
the real Grid point's sharing, task and merge costs.

## Conditional record-type refinement

The two known interval-certificate prefixes contain448,275sites in751files.
Same-file unambiguous definition annotations nominate277,963record-equality
sites (20.5233%of all1,354,379sites):193,460CBox,1,543PointBox,2,960RBox,
80,000Box. Field projections follow the original record schemas:
p0_0.t is an RBox candidate, while p0_0.t.lo is scalar and excluded.
The first naive parent-type pass remains in PVC record-hints-v1; the later
direct-header correction and its completed raw results are in record-hints-v2.

These candidates lie in the lexical equality category, separate from the
538explicit structural forms. Their union is278,501sites (20.5630%).
This is a **conditional lexical nomination set**, not a certified lower bound
or an execution-time share. Namespace resolution, binder shadowing, true
elaborated types and remaining named predicates still require native checks.
The actual transformer has been demonstrated on one real Grid equality;
its schema recognizer is not claimed to transform all these source sites.

The three native hot modules corroborate why inferred targets remain unknown:
the direct-header hints contain3072Grid record equalities,1152UMoments9
CBox equalities and1246BarrierData41Box equalities (5470total).
Native extraction additionally finds1536Grid conjunctions supplied as inline
arguments and12UMoments9CBox equalities reached after change and simp_rw.
All7018native structural targets remain known; they are not reduced to the
5470lexically recoverable record headers. Aggregate agreement in these types
is not a measured per-call classification precision across the whole corpus.

## Logical independence is not independent computational work

The pinned PointBox.calc source has two record-valued exponential components:
directArgBox(a).exp(3) and quarterArgBox(a).exp(3). Each CBox.exp evaluates
a32-step Horner expression followed by repeated squaring. This is a source
observation, not an attributed runtime percentage.

Naive equal-leaf groups put both components in one job at k2. At k8 they
expose the two outputs across five checker/component pairs; one job still
touches both outputs. Different C++ theorem checkers do not share reduction
caches, so logical field independence does not guarantee independent work.
The exact extra work remains a measurement question.

A second automatic partition is prepared: detect explicit .exp calls in the
root constructor, preserve each corresponding record's complete leaf group,
then distribute other leaves. At k2/4/8 it exposes the two heavy outputs to two
different jobs without splitting either. The heuristic has no timing oracle.
All eighteen equalities still occur exactly once and no group is empty.
partition-exposure.csv records this source structure; its counts are **not**
measured invocations, cycles, speedup or a general-purpose optimizer result.

ComponentBase.lean and generated-components-schema.json are generated from
the same original numeric input. Native qualification and a full matrix must
still succeed before using performance or acceptance claims for this variant.
The existing flat matrix's frozen source is unchanged.

P-core serialization does not isolate shared LLC, DRAM, storage or all other
host work. Background preparation may use E cores under the joint memory
budget. Three repetitions describe these controlled attempts, not a whole-
machine-isolation or cold-cache guarantee.
