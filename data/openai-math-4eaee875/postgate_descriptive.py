#!/usr/bin/env python3
"""Post-gate descriptive recomputation only; no native process or gate decision."""
import csv,gzip,json,statistics
from pathlib import Path
from analyze_census_gate import pct
D=Path(__file__).resolve().parent
mods=list(csv.DictReader((D/"measurement/census-gate/census-gate-modules.csv").open()))
with gzip.open(D/"measurement/census-gate/census-gate-attempts.csv.gz","rt")as f:
    rows=[r for r in csv.DictReader(f)if r["role"]=="foreground"]
out={}
for mode in ("user","kernel"):
    values=[float(r[mode+"_instruction_spread"])for r in mods]
    out[mode]=dict(median=statistics.median(values),P95=pct(values,.95),max=max(values))
out["kernel_fraction"]=sum(float(r["instructions_kernel"])for r in rows)/sum(float(r["instructions_total"])for r in rows)
out["kernel_fraction_row_median"]=statistics.median(float(r["instructions_kernel"])/float(r["instructions_total"])for r in rows)
for cond in ("P_loaded","E_loaded"):
    values=[];other=[]
    for n in {r["module"]for r in rows}:
        v=[float(r["cpu_s"])for r in rows if r["module"]==n and r["condition"]==cond]
        values.append(max(v)/min(v)-1);other.append((max(v)-min(v))/statistics.median(v))
    out[cond+"_CPU_repeat_range_over_min_P95"]=pct(values,.95)
    out[cond+"_CPU_repeat_range_over_median_P95"]=pct(other,.95)
if __name__=="__main__":print(json.dumps(out,indent=2))
