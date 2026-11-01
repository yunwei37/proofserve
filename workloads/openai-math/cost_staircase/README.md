# Conditional library cost staircase (2026-11-01, W074)

**This is an offline scenario calculation, not an observed whole-library speedup.**
It accounts for source/compiler CPU separately from verification CPU and native
elapsed time. The fixed original frame has 163,097 OAI source modules; 31 of
42 original draws have qualified no-`-M` source costs. Only 14 of 21 strata,
containing 103,468 modules, are complete. The other 59,629 modules (36.56%)
are not assigned zero cost.

The main answer is that proof production/checking separation can remove much
work in the measured closures, while multicore checking trades extra CPU for
lower elapsed time. The available qualified large-target split has a small
modeled library-level marginal effect. Neither result supplies an empirical
full-library total or proves a general acceleration of source construction.

## CPU work: four stages

Fixed-ratio transfer scenario **Nat.Basic / Grid**, CPU hours. Parentheses
are nominal sampling-only 95% intervals, conditional on the stated model.

| Coverage / source proxy | (a) build | (b) serial stream | (c) parallel stream | (d) plus qualified chunk |
|---|---:|---:|---:|---:|
| Complete 14 strata, ordinary |116.705 (0–439.891)|7.527 (0–28.371)|10.256 (0–38.657)|10.256 (0–38.657)|
| Complete 14 strata, marked computational |24.147 (3.785–44.509)|2.045 (0.320–3.769)|2.819 (0–6.080)|2.849 (0–6.463)|
| Complete 14 strata, sum |140.852 (0–455.504)|9.572 (0–29.491)|13.075 (0–39.856)|13.105 (0–39.736)|
| **Full-frame class-mean projection**, ordinary |185.776 (0–700.240)|11.982 (0–45.163)|16.326 (0–61.537)|16.326 (0–61.537)|
| **Full-frame class-mean projection**, marked |30.147 (4.725–55.569)|2.553 (0.400–4.705)|3.520 (0–7.590)|3.556 (0–8.069)|
| **Full-frame class-mean projection**, sum |215.924 (0–721.914)|14.535 (0–46.789)|19.846 (0–63.420)|19.882 (0–63.300)|

**The last three rows additionally assume missing modules have the same
within-proxy mean as the complete-stratum population. This is unvalidated.**
They are the requested whole-frame conditional *projection*, not a completed
Horvitz–Thompson estimate for all strata, a prediction interval, or a measured
library bill. Missing-class modules are 58,465 ordinary and 1,164 marked.
The complete-stratum source marked share is 17.14%; the extra class-mean
projection changes it to 13.96%, illustrating the dependence on assumptions.

The intervals are already very wide with only two draws per cell; zero lower
limits are clipped approximations, not a suggestion that construction is free.
They exclude transfer-factor uncertainty, heavy-tail nonresponse, proxy
misclassification, artifact context changes and missing-cell selection bias.
No unconditional finite upper bound on full-library CPU follows.

### What each stage means

- **(a)** measured native compiler user+system CPU with exact original source,
  already-built imports, eight requested threads, `.olean/.ilean/C` output.
  Per-module imports, elaboration, tactics, first kernel checks and artifact
  emission are charged. This is not clean toolchain bootstrap, C/C++ linking,
  or measured parallel Lake makespan. The frame is all source files, not only
  Lake's default roots.
- **(b)** hypothetical amortized one-process stream using O's complete-closure
  CPU ratios, applied to each original sampled module's compiler CPU by proxy.
  O's stock-kernel replay checks all selected dependency modules from an empty
  checked kernel environment. It retains upstream unsafe/partial exclusions
  and ordinary axiom semantics. This is artifact checking, not regeneration.
- **(c)** applies M's full-process parallel CPU ratios, **not reciprocal wall
  speedups**: ordinary 1.362547, marked 1.335617. For Envelope specifically the
  actually measured same-prefix leaf factor is 1.580502 instead. This special
  case makes the product a transparent transfer scenario, not a single measured
  full-library configuration.
- **(d)** changes **only EnvelopePsiB**, whose ten >=1 CPU-second goals have an
  integrated source-qualified chunk8 result: CPU x1.051857 and leaf elapsed
  x0.758274 relative to declaration-parallel8. Thesecond observed large-goal module, ResiduesModThree (two goals), has no
qualified split curve and gets **no invented saving**. Unprofiled modules are
not classified as having no large goals. Chunk paths deliberately replace ten original proof bodies after source/type and axiom checks; this is not byte-identical original-proof replay. Chunk preparation/eligibility/support
generation CPU is unknown and excluded; payload reading and child/merge checks
are included. Thus d is a checking-model subtotal, not a complete deployment bill.

## Calibration and scope

[calibration.csv](calibration.csv) recomputes O's ratios from its original
cohort-plan.json and measured.jsonl; M ratios use its published native tables.

| Calibration | CPU method/reference | Elapsed method/reference | Boundary |
|---|---:|---:|---|
| O Nat.Basic stream/build |0.064497|0.105551|1,330-module matched closure|
| O NearPin stream/build |0.039699|0.067593|3,333-module matched closure|
| O Grid stream/build |0.084671|0.145173|3,793-module matched closure|
| O Amplitudes stream/build |0.084421|0.145473|5,083-module matched closure|
| M math parallel8/reference |1.362547|0.656656|three-repeat medians, complete closure|
| M Grid parallel4/reference |1.335617|0.531404|one complete pair; repair gap retained|
| M Envelope parallel8/serial |1.580502|0.283282|leaf only after fixed checked prefix|
| M Envelope chunk8/parallel8 |1.051857|0.758274|ten qualified splits, same leaf|

**1.52x / 1.88x are elapsed improvements, not CPU reductions.** Dividing CPU
hours by them is incorrect. Alternative complete-closure transfer NearPin /
Amplitudes yields full-frame scenario CPU hours 215.924 -> 9.920 -> 13.558 ->
13.595. This between-anchor variation is sensitivity, not a confidence interval.

The selected closures contain many shared ordinary dependencies. Their elapsed
6.76–14.55% ratios do not establish the same ratio for every constituent file.
O's target read/map/replay components are **0.46% NearPin, 80.28% Grid and
82.35% Amplitudes**, a much sharper regime contrast. Those are elapsed
subclocks, not CPU; we do not multiply them into CPU hours. The closure-transfer
model can wash out the distinction under study and is not a headline empirical
claim about full-library regime costs.

The exact once-only external SDK/Mathlib bill, valid global checking order,
memory/segmentation overhead and actual shared-state reuse for all163,097OAI
modules remain unmeasured. No per-sample dependency closures are summed as
disjoint, and no extra shared-base CPU is fabricated. This is the explicit
model requested while original sampling is incomplete, not the missing
whole-library execution. The compiler frame is all source files, not just
default Lake roots. Compiler CPU excludes clean toolchain bootstrap/linking.

## Elapsed and marginal splitting benefit

These models sum native module durations; they are **not parallel Lake or
whole-library scheduled makespan**, and omit queues, admission and inter-module
overlap. Applying the measured parallel factors to each module is a transfer
assumption.

| Scope | build | serial stream | parallel stream | +qualified chunk |
|---|---:|---:|---:|---:|
| Complete 14 strata |126.877 h|14.137 h|8.791 h|8.749 h|
| Full-frame class-mean projection |195.518 h|21.567 h|13.547 h|13.495 h|

The complete-stratum c->d effect is **149.605 elapsed seconds less (0.473% of c)**
and **106.393 CPU seconds more (0.226% of c)**. The full-frame projection gives
186.783elapsed seconds less (**0.383%**) and132.833CPU seconds more (**0.186%**).
These are modeled weighted marginals, not measured library savings. Signed
sampling-only95% intervals cross zero widely: covered elapsed delta
-0.04156 h [-0.56845,+0.48534], CPU delta +0.02955 h [-0.34515,+0.40426].
One original Envelope draw, inclusion weight232, supplies nearly all leverage.

If computation represented17.14% **at stage c**, and all of it received the
observed24.17% chunk elapsed reduction, the arithmetic benefit would be
**4.14%**; at10% eligible coverage, **0.414%**. Actual17.14% is complete-stratum
**source compiler CPU** share, not stage-c elapsed share. These are illustrations,
not global Amdahl bounds. See chunk-share-sensitivity.csv. Observed chunk CPU
goes up, not down.

**Paper implication:** splitting is currently a targeted mechanism example,
not the main whole-library CPU-saving contribution or an established large
incremental library latency improvement. Applying it to every marked module
would invent eligibility. Ordinary-module parallel checking also reduces
elapsed in M's actual matrix; parallelism is not useful only to computational
modules.

## Statistics and missing costs

For complete original two-draw SRS cells:
T = sum_h N_h mean(y_h);
V = sum_h N_h^2 (1-2/N_h) s_h^2/2.
Each stage transforms original costs with the declared module/class factors.
Nominal t intervals use Welch–Satterthwaite degrees of freedom. Paired ratios
retain covariance using residual y_stage-R*y_build. Signed marginal intervals
are not clipped at zero. Two draws and heavy tails make intervals fragile.

The separate full-frame projection scales complete-domain totals by known
full-domain / covered-domain counts: ordinary157249/98784, marked5848/4684.
It is a class-mean nonresponse model, **not modified original probabilities**.
Calibration factors are treated fixed, so reported intervals omit their
uncertainty and model bias. They are not unconditional whole-library95% bounds.

Hard and deep missing draws could raise the current class-mean projection;
cheap missing draws could lower it. Direction is not guaranteed; marked share
can move either way. Eventual original HT sensitivity is +10.842CPU hours for
+1CPU second on each of the11missing draws; Hodge alone is +5.546h per second.
The known31terms sum165.188CPU h, not a population lower confidence bound.
See ../missing-cost-impact/README.md. There is no finite unconditional upper
cost inferred from the observed subset.

## Reproduction and evidence

Run untimed on E cores:
```sh
taskset -c 8-15 python3 workloads/openai-math/cost_staircase.py
```
This launches no Lean, capture or lock contender and writes only small CSVs.
No-M/external-cgroup rules of original measurements remain unchanged. W's
healthy31-target fresh replay is not substituted for O's empty-environment
closure stream: the former trusts imported dependencies and repeats imports.

module-staircase.csv keeps all42original draws in two clock/two scenario
views (31measured,11blank). Other files: conditional-staircase.csv,
chunk-marginal.csv, calibration.csv, chunk-share-sensitivity.csv, receipt.json,
arithmetic-audit.json. Full raw ledgers remain on PVC.

Primary inputs: research/decoupled-check/{cohort-costs.csv,root-components.csv},
its PVC measured.jsonl and cohort-plan.json;
research/parallel-stream-check/{v14-math-summary.csv,full-pairs.csv,compute-cells.csv};
research/chunked-kernel-check/declaration-distribution.csv;
workloads/openai-math/noM-original-c-suffix48/sample-costs.csv and its original
raw native rows. Prototype-specific trust and proof-generation boundaries remain
in those owning reports. This thread's review is **自审**, not independent review.
