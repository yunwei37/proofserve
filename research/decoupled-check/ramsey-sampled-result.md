# Ramsey: measured module-local distribution, incomplete-directory limits

Review: 自审. Source pin4eaee875; original Lean4.34.1. Production stopped190/444, all records retained. Stream coverage0/444; no full-closure fraction.

**All20 size-stratified samples passed the original module-local checker.** Individual CPU fractions P10/median/P90: **35.51%/40.62%/48.83%**. Sample-pooled CPU fraction: **35.91%**.

| Retained-size stratum | n/N | Sampled source CPU-s | Checker CPU-s | Pooled CPU ratio |
|---|---:|---:|---:|---:|
| 1 |4/38|6.755|3.370|49.89%|
| 2 |4/38|7.159|3.224|45.04%|
| 3 |4/38|9.147|3.293|36.00%|
| 4 |4/38|8.287|3.269|39.45%|
| 5 |4/38|2240.009|802.523|35.83%|

Equal-probability sampling within each retained size quintile estimates **7748.95CPU-s** for checking the190retained modules in **independent module-local processes**, versus their actual **22146.10sourceCPU-s**: **34.99%**. Stratified within-quintile percentile bootstrap(10000draws,seed20261103) gives **[29.41%,40.41%]**. This interval describes resampling variability inside the observed prefix; n=4per stratum is small and it does not cover dependency-order selection bias or missing targets. Do not multiply it by444.

K10 is supplemental and excluded from that random-sample estimate: original module-local kernel356.442522CPU-s / source1725.133882CPU-s =20.6617%; wall357.111161/674.563076 =52.9396%, peak checker3.083GiB. Absence of+kernel did not make its plain-decide finite certificates cheap.

The190built files all belong to Construction; their median size4457bytes contrasts with81652.5bytes in254unbuilt files. Only24/180kernel-marked files and8/20unmarked certificate-family files are built. The unseen part is much more certificate-heavy; no acceptance/cost claim is made for it. See ramsey-prefix-bias.json.

## Comparison with complete mathematical closures

| Input | Coverage/protocol | Check/source CPU fraction |
|---|---|---:|
| Falconer |13205-node complete segmented stream|6.31%|
| Mathlib matched protocol |1330-node complete segmented stream|8.95%|
| Ramsey retained-prefix sample |20/190 module-local references; trusted imports; full444incomplete|See strata above; **not a comparable closure ratio**|

Startup/import are charged separately for every Ramsey sampled file, while complete streams share their kernel environment and checkpoint its accepted prefix. The tiny-file floor cannot establish kernel computation dominance. Large certificate ratios show substantial original-kernel work survives production, but no full-directory conclusion follows. Source compilers emitted olean/ilean/C with original authored options and no-M; all timed tasks used P0–7/flock/external11.75GiB cgroup. Existing native malformed-proof controls qualify the original adapter, not an independent all444acceptance test.
