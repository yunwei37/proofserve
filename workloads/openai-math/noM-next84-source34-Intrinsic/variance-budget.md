# Remaining uncertainty after recovering a half-filled cell
This is an E-core analysis of source34, not a new sampling run.
Covered16-cell variance uses N_h²(1−2/N_h)s_h²/2 from the two original
observations. It excludes five missing strata, timing/calibration variation
and tail-model error. Individual contributions are in covered-variance-budget.csv.
The largest ordinary cell (45251 small modules at depth11–100) remains the main
estimated variance source. A narrowed missing-cost scenario is not a narrowed
population confidence interval.

The previously frozen six supplemental random remainder draws are still not
launched. Under a pilot assumption that the remaining finite-population
variance equals this observed pair's variance, six remainder measurements would
reduce that cell variance by about two-thirds. This is not a predicted realized
CI: the true remainder tail is unknown. The conditional unbiased remainder
total would be sum(the known2 actual costs)+(N−2)*mean(new6), with remainder
finite-population variance (N−2)²(1−6/(N−2))*s_remainder²/6. It must not be
naively pooled into an eight-draw SRS or overwrite original42 HT weights.
No extra source draw or native request was submitted by this analysis.
