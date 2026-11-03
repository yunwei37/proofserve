#!/usr/bin/env python3
"""Report original-kernel sampled costs; never infer unbuilt444-target coverage."""
from pathlib import Path
import csv,json,statistics,random,math
D=Path(__file__).resolve().parent
def quant(v,q):
 v=sorted(v);p=(len(v)-1)*q;i=int(p);return v[i]+(v[min(i+1,len(v)-1)]-v[i])*(p-i)
def main():
 rows=list(csv.DictReader((D/"ramsey-sample-costs.csv").open()))
 assert len(rows)==20 and all(v["valid"]=="True"for v in rows),"incomplete/operational failures remain unestimated"
 for v in rows:
  for k in ["stratum","bytes"]:v[k]=int(v[k])
  for k in ["source_cpu_s","check_cpu_s","cpu_ratio","wall_ratio"]:v[k]=float(v[k])
 population=[v for v in csv.DictReader((D/"ramsey-source-costs.csv").open())if v["target"]=="True"]
 assert len(population)==190
 denominator=sum(float(v["source_cpu_s"])for v in population)
 rng=random.Random(20261103);boot=[];groups=[]
 for k in range(1,6):
  rr=[v for v in rows if v["stratum"]==k];assert len(rr)==4
  groups.append(dict(stratum=k,N=38,n=4,min_sample_bytes=min(v["bytes"]for v in rr),max_sample_bytes=max(v["bytes"]for v in rr),source_cpu_s=sum(v["source_cpu_s"]for v in rr),check_cpu_s=sum(v["check_cpu_s"]for v in rr),pooled_cpu_ratio=sum(v["check_cpu_s"]for v in rr)/sum(v["source_cpu_s"]for v in rr),median_individual_cpu_ratio=statistics.median(v["cpu_ratio"]for v in rr)))
 for _ in range(10000):
  total=0.
  for k in range(1,6):
   rr=[v["check_cpu_s"]for v in rows if v["stratum"]==k]
   total+=38*statistics.mean(rng.choices(rr,k=4))
  boot.append(total/denominator)
 estimated=sum(38*g["check_cpu_s"]/4 for g in groups)
 summary=dict(complete_sample=True,accepted=20,ordinary_process_failures=0,selected=20,eligible_retained_prefix=190,full_target_population=444,
  individual_ratio_p10=quant([v["cpu_ratio"]for v in rows],.1),individual_ratio_median=statistics.median(v["cpu_ratio"]for v in rows),individual_ratio_p90=quant([v["cpu_ratio"]for v in rows],.9),
  sampled_pooled_cpu_ratio=sum(v["check_cpu_s"]for v in rows)/sum(v["source_cpu_s"]for v in rows),
  estimated_retained190_independent_module_local_cpu_s=estimated,observed_retained190_source_cpu_s=denominator,
  estimated_retained190_independent_module_local_ratio=estimated/denominator,
  bootstrap95_low=quant(boot,.025),bootstrap95_high=quant(boot,.975),bootstrap_reps=10000,
  scope="Only size-stratified190-built-prefix estimate of independent module-local references; not444 or streaming.",full_closure_ratio=None)
 (D/"ramsey-sample-estimate.json").write_text(json.dumps(summary,indent=2)+"\n")
 with(D/"ramsey-sample-strata.csv").open("w",newline="")as f:
  w=csv.DictWriter(f,fieldnames=groups[0],lineterminator="\n");w.writeheader();w.writerows(groups)
 text="# Ramsey: measured module-local distribution, incomplete-directory limits\n\nReview: 自审. Source pin4eaee875; original Lean4.34.1. Production stopped190/444, all records retained. Stream coverage0/444; no full-closure fraction.\n\n"
 text+=f"**All20 size-stratified samples passed the original module-local checker.** Individual CPU fractions P10/median/P90: **{summary['individual_ratio_p10']:.2%}/{summary['individual_ratio_median']:.2%}/{summary['individual_ratio_p90']:.2%}**. Sample-pooled CPU fraction: **{summary['sampled_pooled_cpu_ratio']:.2%}**.\n\n"
 text+="| Retained-size stratum | n/N | Sampled source CPU-s | Checker CPU-s | Pooled CPU ratio |\n|---|---:|---:|---:|---:|\n"
 for g in groups:text+=f"| {g['stratum']} |4/38|{g['source_cpu_s']:.3f}|{g['check_cpu_s']:.3f}|{g['pooled_cpu_ratio']:.2%}|\n"
 text+=f"\nEqual-probability sampling within each retained size quintile estimates **{estimated:.2f}CPU-s** for checking the190retained modules in **independent module-local processes**, versus their actual **{denominator:.2f}sourceCPU-s**: **{estimated/denominator:.2%}**. Stratified within-quintile percentile bootstrap(10000draws,seed20261103) gives **[{summary['bootstrap95_low']:.2%},{summary['bootstrap95_high']:.2%}]**. This interval describes resampling variability inside the observed prefix; n=4per stratum is small and it does not cover dependency-order selection bias or missing targets. Do not multiply it by444.\n\n"
 text+="K10 is supplemental and excluded from that random-sample estimate: original module-local kernel356.442522CPU-s / source1725.133882CPU-s =20.6617%; wall357.111161/674.563076 =52.9396%, peak checker3.083GiB. Absence of+kernel did not make its plain-decide finite certificates cheap.\n\n"
 text+="The190built files all belong to Construction; their median size4457bytes contrasts with81652.5bytes in254unbuilt files. Only24/180kernel-marked files and8/20unmarked certificate-family files are built. The unseen part is much more certificate-heavy; no acceptance/cost claim is made for it. See ramsey-prefix-bias.json.\n\n"
 text+="## Comparison with complete mathematical closures\n\n| Input | Coverage/protocol | Check/source CPU fraction |\n|---|---|---:|\n| Falconer |13205-node complete segmented stream|6.31%|\n| Mathlib matched protocol |1330-node complete segmented stream|8.95%|\n| Ramsey retained-prefix sample |20/190 module-local references; trusted imports; full444incomplete|See strata above; **not a comparable closure ratio**|\n\n"
 text+="Startup/import are charged separately for every Ramsey sampled file, while complete streams share their kernel environment and checkpoint its accepted prefix. The tiny-file floor cannot establish kernel computation dominance. Large certificate ratios show substantial original-kernel work survives production, but no full-directory conclusion follows. Source compilers emitted olean/ilean/C with original authored options and no-M; all timed tasks used P0–7/flock/external11.75GiB cgroup. Existing native malformed-proof controls qualify the original adapter, not an independent all444acceptance test.\n"
 (D/"ramsey-sampled-result.md").write_text(text)
 print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
