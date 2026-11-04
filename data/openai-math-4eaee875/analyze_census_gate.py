#!/usr/bin/env python3
"""Summarize native census qualification without treating missing data as passes."""
import argparse,collections,csv,hashlib,json,math,statistics
from pathlib import Path
def pct(values,p):
    v=sorted(values)
    if not v:return None
    x=(len(v)-1)*p;i=int(x);return v[i]+(v[min(i+1,len(v)-1)]-v[i])*(x-i)
def med(v):return statistics.median(v)if v else None
def digest(p):
    h=hashlib.sha256()
    with p.open("rb")as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()
def csvout(p,rows,cols):
    with p.open("w",newline="")as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore",lineterminator="\n");w.writeheader();w.writerows(rows)
def analyze(point,out):
    out.mkdir(parents=True,exist_ok=True);c=json.loads((point/"protocol.json").read_text())
    rows=[json.loads(s)for s in(point/"records.jsonl").read_text().splitlines()]
    fg=[r for r in rows if r["role"]=="foreground"];controls=[r for r in rows if r["role"]=="overhead"]
    names=list(c["modules"]);conditions=["P_quiet","P_loaded","E_quiet","E_loaded"]
    flat=[]
    for r in rows:
        active="cpu_core"if r["pool"]=="P"else "cpu_atom";ct=r["counters"]
        user=ct.get(active+"_user",{}).get("instructions");kernel=ct.get(active+"_kernel",{}).get("instructions")
        z={k:r.get(k)for k in("sequence","module","role","condition","rep","pool","status","returncode","measurement_commit","source_revision","source_sha256","start_utc","end_utc","attempt","perf","user_cpu_s","system_cpu_s","wall_s","peak_rss_kib","cgroup_peak","interruption")}
        z.update(cpu_s=r["user_cpu_s"]+r["system_cpu_s"],instructions_user=user,instructions_kernel=kernel,
                 instructions_total=user+kernel if user is not None and kernel is not None else None,
                 user_coverage=ct.get(active+"_user",{}).get("coverage"),kernel_coverage=ct.get(active+"_kernel",{}).get("coverage"),
                 lean_threads=r["lean_num_threads"],affinity=",".join(map(str,r["affinity"])),
                 lean_version=r["toolchain"]["lean"],lean_binary=r["toolchain"]["binary"],mathlib_commit=c["mathlib"],
                 argv=json.dumps(r["argv"],separators=(",",":")))
        for pmu in ("cpu_core","cpu_atom"):
            for mode in ("user","kernel"):z[pmu+"_"+mode+"_instructions"]=ct.get(pmu+"_"+mode,{}).get("instructions")
        flat.append(z)
    cv={};per=[];deviations=[]
    for name in names:
        z={"module":name,"regime_proxy":c["modules"][name]["regime"],"source_bytes":c["modules"][name]["bytes"]}
        totals=[]
        for cond in conditions:
            rr=[r for r in flat if r["role"]=="foreground"and r["module"]==name and r["condition"]==cond and r["status"]=="completed"]
            z[cond+"_n"]=len(rr)
            total=med([r["instructions_total"]for r in rr]);cpu=med([r["cpu_s"]for r in rr])
            z[cond+"_instructions_median"]=total;z[cond+"_CPU_median_s"]=cpu;z[cond+"_wall_median_s"]=med([r["wall_s"]for r in rr])
            if total is not None:totals.append(total)
            cv[(name,cond)]=(total,cpu)
        complete=all(z[x+"_n"]==3 for x in conditions);z["complete"]=complete
        for mode in ("user","kernel"):
            vals=[]
            for cond in conditions:
                rr=[r for r in flat if r["role"]=="foreground"and r["module"]==name and r["condition"]==cond and r["status"]=="completed"]
                v=med([r["instructions_"+mode]for r in rr])
                z[cond+"_"+mode+"_instructions_median"]=v
                if v is not None:vals.append(v)
            z[mode+"_instruction_spread"]=max(vals)/min(vals)-1 if complete and min(vals)>0 else None
        z["cross_condition_spread"]=max(totals)/min(totals)-1 if complete else None
        if complete:
            b=z["P_quiet_instructions_median"]
            for cond in conditions[1:]:deviations.append(abs(z[cond+"_instructions_median"]/b-1))
        for pool in("P","E"):
            q=z[pool+"_quiet_CPU_median_s"];l=z[pool+"_loaded_CPU_median_s"]
            z[pool+"_loaded_quiet_CPU_ratio"]=l/q if q and l else None
        per.append(z)
    parity=[]
    for n in names:
        rr=[r for r in rows if r["module"]==n and r["status"]=="completed"]
        a={"module":n,"successful_rows":len(rr)}
        for suffix in(".olean",".ilean",".c"):
            hh={r["artifacts"].get(suffix,{}).get("sha256")for r in rr}
            a[suffix[1:]+"_distinct_hashes"]=len(hh)
            a[suffix[1:]+"_all_equal"]=len(hh)==1 and None not in hh
            old=c.get("historical_products",{}).get(n,{}).get(suffix)
            a[suffix[1:]+"_historical_available"]=bool(old and Path(old).is_file())
            a[suffix[1:]+"_historical_equal"]=(digest(Path(old))in hh and len(hh)==1)if old and Path(old).is_file()else None
        parity.append(a)
    overhead=[]
    for pool in("P","E"):
        for n in names:
            allrat=[];wallrat=[]
            for rep in range(3):
                rr=[r for r in controls if r["module"]==n and r["pool"]==pool and r["rep"]==rep and r["status"]=="completed"]
                yes=next((r for r in rr if r["perf"]),None);no=next((r for r in rr if not r["perf"]),None)
                if yes and no:
                    allrat.append((yes["user_cpu_s"]+yes["system_cpu_s"])/(no["user_cpu_s"]+no["system_cpu_s"])-1)
                    wallrat.append(yes["wall_s"]/no["wall_s"]-1)
            overhead.append(dict(module=n,pool=pool,pairs=len(allrat),CPU_overhead_median=med(allrat),wall_overhead_median=med(wallrat)))
    spread=[r["cross_condition_spread"]for r in per if r["complete"]]
    goodcoverage=all(r["user_coverage"]==1 and r["kernel_coverage"]==1 for r in flat if r["perf"])
    summary=dict(measurement_commit=c["measurement_commit"],foreground=len(fg),expected_foreground=240,foreground_success=sum(r["status"]=="completed"for r in fg),
        completed_module_conditions=sum(r["complete"]for r in per),failures=sum(r["status"]!="completed"for r in rows),
        instruction_spread_median=med(spread),instruction_spread_P95=pct(spread,.95),
        relative_to_Pquiet_absolute_deviation_median=med(deviations),relative_to_Pquiet_absolute_deviation_P95=pct(deviations,.95),
        active_counter_coverage_all_one=goodcoverage,full_census_started=False)
    for pool in("P","E"):
        rr=[r for r in overhead if r["pool"]==pool and r["pairs"]==3]
        summary[pool+"_counter_CPU_overhead_median"]=med([r["CPU_overhead_median"]for r in rr])
        summary[pool+"_counter_wall_overhead_median"]=med([r["wall_overhead_median"]for r in rr])
        summary[pool+"_overhead_complete_modules"]=len(rr)
        summary[pool+"_loaded_quiet_CPU_ratio_median"]=med([r[pool+"_loaded_quiet_CPU_ratio"]for r in per if r[pool+"_loaded_quiet_CPU_ratio"]is not None])
    summary["new_artifacts_all_byte_identical"]=all(r[k]for r in parity for k in("olean_all_equal","ilean_all_equal","c_all_equal"))
    complete=len(fg)==240 and len(spread)==20 and all(summary[p+"_overhead_complete_modules"]==20 for p in("P","E"))
    summary["matrix_complete"]=complete
    instruction_pass=complete and med(spread)<=.01 and pct(spread,.95)<=.03
    overhead_pass=complete and all(summary[p+"_counter_CPU_overhead_median"]<=.01 and summary[p+"_counter_wall_overhead_median"]<=.01 for p in("P","E"))
    summary["instruction_threshold_pass"]=instruction_pass;summary["overhead_threshold_pass"]=overhead_pass
    summary["primary_instruction_metric"]="per-module range of four condition medians: max/min minus one; median and linearly interpolated (n-1)*p P95 across 20 modules"
    summary["overhead_threshold_basis"]="median across module-level paired overhead medians in each pool; not a uniform bound"
    summary["overhead_all_module_medians_at_most_one_percent"]=complete and all(r["CPU_overhead_median"]<=.01 and r["wall_overhead_median"]<=.01 for r in overhead)
    summary["foreground_user_instruction_spread_median"]=med([r["user_instruction_spread"]for r in per if r["complete"]])
    summary["foreground_kernel_instruction_spread_median"]=med([r["kernel_instruction_spread"]for r in per if r["complete"]])
    summary["gate_pass"]=bool(complete and instruction_pass and overhead_pass and goodcoverage and summary["new_artifacts_all_byte_identical"]and summary["failures"]==0)
    summary["terminal"]=json.loads((point/"terminal.json").read_text())if(point/"terminal.json").exists()else None
    memory=[]
    if(point/"memory.jsonl").exists():
        for line in(point/"memory.jsonl").open():
            try:memory.append(json.loads(line))
            except ValueError:pass
    saturated=[m for m in memory if m["active"]==22]
    summary["samples_with_22_native_jobs"]=len(saturated)
    summary["22_job_mean_busy_P"]=med([statistics.mean(v for k,v in m["busy"].items()if int(k)<8 and v is not None)for m in saturated])
    summary["22_job_mean_busy_E"]=med([statistics.mean(v for k,v in m["busy"].items()if int(k)>=10 and v is not None)for m in saturated])
    csvout(out/"census-gate-attempts.csv",flat,list(flat[0])if flat else ["module"])
    csvout(out/"census-gate-modules.csv",per,list(per[0]))
    csvout(out/"census-gate-artifact-parity.csv",parity,list(parity[0]))
    csvout(out/"census-gate-overhead.csv",overhead,list(overhead[0]))
    (out/"census-gate-summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    return summary
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("point",type=Path);a.add_argument("out",type=Path);v=a.parse_args();print(json.dumps(analyze(v.point,v.out),indent=2))
