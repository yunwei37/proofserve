# Sampling uncertainty is different from missing-draw sensitivity

All numbers here use the already-published source38 measurements. No new native
run or replacement sample is used. The fixed remaining four originals continue.

For the19complete strata(161034modules), the weighted source-compiler CPU point
is246.8630398h. The existing approximate stratified t/Satterthwaite95% interval
is43.9877057–449.7383739h(df2.130943). This is a **nominal model-based interval
for the covered domain**, with n=2 per stratum. It excludes nonresponse and
calibration/model/runtime uncertainty and is fragile for unseen heavy tails.
It is not a finite-population or distribution-free bound.

The full-frame missing-draw scenario247.5533–270.2389h instead assumes costs
for the four missing originals from observed within-class extrema. Its1.09164
high/low ratio is **not precision of the total-cost estimate**. Completing the
four removes missing-draw assumptions, not this sampling uncertainty.

The45,251-module ordinary cell0-50;11-100;0 contributes62.4086% of the estimated
covered-domain variance; the1,164-module computation-proxy cell99-100;11-100;1
contributes27.6065%. Together90.0151%. This diagnosis comes from the fixed
two-draw variance formula, not a census of population tails.

Narrow conditional build/check ratio intervals are also largely mechanical:
each regime is multiplied by a fixed closure calibration ratio. They do not
include uncertainty of transferring the selected closures to unseen modules.
Neither a narrowed missingness range nor that ratio interval establishes a
measured whole-library checker result.

No additional/adaptively chosen original is added in this step. A future
precision-focused sample expansion would need a declared probability design;
it must not replace slow or failed fixed originals. For this batch the four
remaining identities, weights, source flags and native budgets remain frozen.
