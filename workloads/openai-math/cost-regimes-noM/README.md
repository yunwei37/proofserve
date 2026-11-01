# Two source-defined cost domains, current no-M convention

RQ1 asks how much native compiler CPU belongs to computation-bearing modules
versus ordinary mathematical modules. This classifies all163,097sources at
4eaee875 and weights only original random draws with completed no-Mcosts.
Source labels are not dynamic kernel-dominance labels.

## Source rule fixed independently of measured cost

D_i=1024*(kernel_decide+native_decide+bv_decide+ofReduceBool)/source_bytes.
Counts use the existing comment/string-masked scanner. Primary certificate
proxy:D_i>0;other modules:ordinary-mathematics proxy. The other explicit
markers are absent here,so primary equals the existing kernel-presence strata.
Positive density retains large calculations with only one proof command.

Sensitivity rules:D>=0.1sites/KiB(one/10KiB),D>=1site/KiB,and any plain decide
in addition to explicit markers. No CPU threshold selects labels.

|Rule|Certificate-proxy files|Fraction|
|---|---:|---:|
|Primary,explicit D>0|5,848|3.58560%|
|D>=0.1/KiB|5,630|3.45193%|
|D>=1/KiB|4,056|2.48686%|
|Include plain decide|16,766|10.27977%|

Primary-positive source655,100,740bytes. File/source fractions are not time.
Full163,097labels remain onPVC; published native table includes prerequisites/
purposeful cases with population_weight blank,never treating them as draws.

## Estimates apply only to completed strata

31/42original costs,14/21complete strata are available. Those14cover103,468
modules.59,629modules lie in incomplete strata:1,164primary-positive and
58,465ordinary. Those incomplete strata still prevent any whole-library estimate.

For completed strata only:
- certificate native CPU estimate24.146735hours;
- ordinary native CPU estimate116.704826hours;
- certificate share17.1434%,ordinary82.8566%;
- nominal delta-method95%certificate-share interval[0%,43.6646%];
- conservative joint95%Bonferroni interval[0%,100%].

Two draws/cell do not give precise time weights. These are conditional
complete-stratum estimates,not whole-library CPU hours,proof-check-only CPU,
accepted-library build totals,or calibrated whole-corpus intervals.
Global point/CI fields remain blank. No-Mpair/legacy-Mtimes or partial costs
fill missing draws. Missing1,164positive modules can change the conclusion.

Sensitivity covered-stratum point shares:17.1385%at D>=0.1,13.4320%at D>=1,
19.1365%including plain decide. Some sensitivity domains have positive known
population but no observed member in a completedcell. Their misleading
zero-width domain/delta intervals are suppressed;bounds remain[0,1].

## Calculation and intervals

Original seed20261030SRSWOR frame:21size/depth/kernel-presence strata,n_h=2.
Prerequisites,Grid/Amplitudes,purposeful profiles and repetitions get no weight.
For a complete stratum:
    T_C,h=N_h*mean(y_i*C_i)
    T_O,h=N_h*mean(y_i*(1-C_i))
    V_C,h=N_h^2*(1-n_h/N_h)*s^2(y_i*C_i)/n_h
and analogously for O. y_i=the same native wait4user+system CPU,including
imports/elaboration/checking/output emission,excluding queue/observer.
Require no-M,P0–7lock,j8,unprofiled,authored/defaultHB,three artifacts,exact
source and a successful completed native response.

For R=T_C/(T_C+T_O),delta variance uses z_i=y_i*(C_i-R),summed finite-population
stratum variances divided by total^2. Nominal t critical values use
Welch–Satterthwaite degrees of freedom. Another interval uses97.5%domain-total
intervals and L_C/(L_C+U_O),U_C/(U_C+L_O),giving joint nominal95%Bonferroni
scope. Positive domains without any native member remain unsupported.

Normal-cost/t assumptions at n=2under heavy tails are fragile. Intervals do
not cover incomplete-cell nonresponse,wrong labels,runtime drift,compiler
errors or time/resource censoring. Successful-response cost does not prove
all published sources build. Per-stratum costs,intervals,sample counts and
conditional contributions are provided. Within-cell shares0/1for pure marker
strata are classification identities,not fractions of kernel computation.

## Profiles and misclassification

The five-source C++user-cycle panel used-M:legacy methodology only. Its3
marker-positive sources have checker-family fractions74.9–94.0%;2negative
sources about1.9–2.1%. Primary agrees5/5in this purposeful diagnostic panel,
not heldout accuracy or population evidence. D>=1misses EnvelopePsiB
(D0.571/KiB,legacy94.0%checker),showing density dilution.

There is no qualified no-Mproducer C++stack cross-check for these labels yet.
M's90cell matrix has noMplain/stat/trace but no noMrecord arm. Legacy fractions
are not reused as new timings or multiplied into unrelated native CPU.
The smalllegacy table is marked invalid_for_current_noMvalidation.
Fresh noMprofiles remain necessary before calling the source rule a measured
kernel-dominance classifier.

False positives:trivial computational lemmas,helper definitions/code quotations,
unexecuted commands,and import-dominated small files. False negatives:rfl/
eqRefl/definitional reduction without markers,plain decide excluded by strict
rule,and work in imported definitions. A module can mix both activities;
native CPU also includes tactics,imports and emission. native_decide/
ofReduceBool can have a different trust boundary;source absence is not an
axiom-closure proof. C++checker includes inference/equality/normalization/
cleanup,not exclusively final proof validation.

## Reproduce and retain

    estimate_cost_regimes.py --inventory static-4eaee875 \
      --targets build-planning-4eaee875/phaseA-targets.csv \
      --strata build-planning-4eaee875/strata.csv \
      --results [qualified noM results.jsonl ...] \
      --legacy-profiles native-profile-five/case-summary.csv --out NEW_PVC_DIR

Full labels gzip,source snapshot,analysis logs and smalltables:
PVC workloads/openai4341-cost-regimes-20261101-v3.
v1and original unsupported-domain plug-in intervals remain unchanged.
Independent arithmetic from the existing estimator reconciles primary domain
totals/variances;all four partitions and fullbytes1,785,499,363checked.
Review is same-thread self-review.

Original hard draws continue noM-only.48jobs submit sequentially,one stockflock
request at a time,after each prior native/cgroup retires. Every command releases
P0–7 before the next submission;no batchheldlock,profilepriority or strictFIFO
claim. Queue/setup/copy/cleanup are separate from native CPU cost.

W065 update: suffix48 adds two unchanged original random draws and completes
two more strata. Previous v1/v2raw results remain; only current small tables
are refreshed. 31/42draws and14/21cells are not a full-library result.
