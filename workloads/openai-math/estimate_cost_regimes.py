#!/usr/bin/env python3
"""Stratified no-M CPU-domain estimates from source-only marker rules."""
import argparse
import collections
import csv
import gzip
import json
import math
import os
from pathlib import Path
import statistics
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, "/workspaces/.agent-state/gpu-smt-captures/workloads/statistics-python-deps")
from scipy.stats import t, norm
from plan_build import load

RULES = ["explicit_any", "explicit_0p1_per_KiB", "explicit_1_per_KiB",
         "including_plain_decide"]


def rules(p):
    k = p["decide_plus_kernel"]
    n = k + p["native_decide"] + p["bv_decide"] + p["ofReduceBool"]
    expanded = n + max(0, p["decide"] - k)
    size = p["bytes"]
    return dict(explicit_any=n>0,
        explicit_0p1_per_KiB=n>0 and 10240*n>=size,
        explicit_1_per_KiB=n>0 and 1024*n>=size,
        including_plain_decide=expanded>0)


def write_csv(path, rows):
    if not rows:
        return
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "wt", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def moments(N, values):
    n = len(values)
    estimate = N * statistics.mean(values)
    variance = N*N*(1-n/N)*statistics.variance(values)/n if n>1 else 0.
    return dict(estimate=estimate, variance=max(0., variance), df=n-1)


def aggregate(parts, confidence=.95):
    est = sum(x["estimate"] for x in parts)
    var = sum(x["variance"] for x in parts)
    den = sum(x["variance"]**2/x["df"] for x in parts if x["variance"]>0)
    df = var*var/den if den else math.inf
    critical = float(t.ppf((1+confidence)/2,df)) if math.isfinite(df) else float(norm.ppf((1+confidence)/2))
    margin = critical*math.sqrt(var)
    return est, var, df, max(0.,est-margin), est+margin


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inventory",type=Path,required=True)
    ap.add_argument("--targets",type=Path,required=True)
    ap.add_argument("--strata",type=Path,required=True)
    ap.add_argument("--results",type=Path,nargs="+",required=True)
    ap.add_argument("--legacy-profiles",type=Path)
    ap.add_argument("--out",type=Path,required=True)
    a = ap.parse_args()
    os.sched_setaffinity(0,set(range(8,16)))
    a.out.mkdir(parents=True,exist_ok=False)
    profiles,modules,deps,external,reverse,order,depth = load(a.inventory)
    del deps,external,reverse,order
    sizes=sorted(p["bytes"] for p in profiles.values())
    cuts=[sizes[int((len(sizes)-1)*q)] for q in [.5,.9,.99]]
    labels={}
    population=collections.defaultdict(list)
    fullrows=[]
    for m,path in modules.items():
        p=profiles[path];size=p["bytes"]
        sizebin="0-50" if size<=cuts[0] else "50-90" if size<=cuts[1] else "90-99" if size<=cuts[2] else "99-100"
        db="1-10" if depth[m]<=10 else "11-100" if depth[m]<=100 else "101+"
        h=";".join([sizebin,db,str(int(p["decide_plus_kernel"]>0))])
        n=p["decide_plus_kernel"]+p["native_decide"]+p["bv_decide"]+p["ofReduceBool"]
        row=dict(module=m,path=path,stratum=h,source_bytes=size,
            decide_plus_kernel=p["decide_plus_kernel"],plain_decide=max(0,p["decide"]-p["decide_plus_kernel"]),
            native_decide=p["native_decide"],bv_decide=p["bv_decide"],
            ofReduceBool=p["ofReduceBool"],
            explicit_markers_per_KiB=1024*n/size if size else 0.,
            **rules(p))
        labels[m]=row;population[h].append(m);fullrows.append(row)
    frame=[x for x in csv.DictReader(a.targets.open()) if x["role"]=="probability_sample"]
    strata={";".join([x["size_percentile_bin"],x["import_depth_bin"],x["has_decide_kernel"]]):x
            for x in csv.DictReader(a.strata.open())}
    assert len(frame)==42 and len(population)==len(strata)==21
    assert all(len(population[h])==int(s["population_modules"]) for h,s in strata.items())
    target={x["module"]:x for x in frame}
    completed={};attempts={};all_native={};excluded=collections.Counter()
    for file in a.results:
        for lineno,line in enumerate(file.read_text().splitlines(),1):
            row=json.loads(line);m=row["module"]
            if row.get("native_invoked") is False:
                attempts[m]=row["status"];continue
            valid=(row.get("lean_memory_option_MiB")==0 and row.get("threads")==8
                and row.get("pcore_lock") is True and row.get("profiled") is False
                and not any(x.startswith("-M") for x in row.get("args",[])))
            if row.get("source_exact") is not True:
                valid=False
            if not valid:
                excluded["legacy_or_unmatched_point"]+=1;continue
            if m in labels:
                all_native[m]=dict(row,source_file=str(file),source_line=lineno)
            if m not in target:
                excluded["not_original_random_draw"]+=1;continue
            if row.get("heartbeat_budget")!="authored_or_native_default" or row.get("compilation_outputs")!="olean_ilean_c":
                excluded["wrong_heartbeat_or_artifacts"]+=1;continue
            attempts[m]=row["status"]
            if row["status"]=="compile_ok" and m not in completed:
                completed[m]=dict(row,source_file=str(file),source_line=lineno)
    poprows=[]
    for rule in RULES:
        C=[x for x in fullrows if x[rule]]
        poprows.append(dict(rule=rule,modules=len(modules),certificate_proxy_modules=len(C),
            ordinary_proxy_modules=len(modules)-len(C),
            certificate_file_fraction=len(C)/len(modules),
            certificate_source_bytes=sum(x["source_bytes"] for x in C),
            label_scope="lexical source proxy; not dynamic checker dominance"))
    sample_rows=[]
    for m,row in all_native.items():
        sample_rows.append(dict(**labels[m],native_status=row["status"],
            CPU_s=row["user_cpu_s"]+row["system_cpu_s"],wall_s=row["wall_s"],
            original_random_draw=m in target,completed_cost=m in completed,
            population_weight=1/float(target[m]["inclusion_probability"]) if m in completed else None,
            source_file=row["source_file"],source_line=row["source_line"]))
    bystratum=[];summaries=[]
    complete_h=[h for h,s in strata.items() if sum(x["module"] in completed for x in frame if x["stratum"]==h)==int(s["sample_modules"])]
    for rule in RULES:
        parts_C=[];parts_O=[];parts_total=[]
        domain_gaps=[]
        for h,s in strata.items():
            N=int(s["population_modules"]);planned=int(s["sample_modules"])
            selected=[x["module"] for x in frame if x["stratum"]==h]
            available=[m for m in selected if m in completed]
            n=len(available);PC=sum(labels[m][rule] for m in population[h]);PO=N-PC
            ys=[completed[m]["user_cpu_s"]+completed[m]["system_cpu_s"] for m in available]
            cvals=[y*labels[m][rule] for m,y in zip(available,ys)]
            ovals=[y*(not labels[m][rule]) for m,y in zip(available,ys)]
            complete=n==planned
            gap_C=PC>0 and not any(labels[m][rule] for m in available)
            gap_O=PO>0 and not any(not labels[m][rule] for m in available)
            if complete and (gap_C or gap_O):domain_gaps.append(h)
            mc=moments(N,cvals) if complete else None
            mo=moments(N,ovals) if complete else None
            mt=moments(N,ys) if complete else None
            if complete:parts_C.append(mc);parts_O.append(mo);parts_total.append(mt)
            cc = aggregate([mc], .975) if complete else None
            oo = aggregate([mo], .975) if complete else None
            within_lo = 0. if PC == 0 else 1. if PO == 0 else cc[3]/(cc[3]+oo[4]) if complete and cc[3]+oo[4] else None
            within_hi = 0. if PC == 0 else 1. if PO == 0 else cc[4]/(cc[4]+oo[3]) if complete and cc[4]+oo[3] else None
            if complete and (gap_C or gap_O) and PC and PO:
                within_lo, within_hi = 0., 1.

            bystratum.append(dict(rule=rule,stratum=h,population_modules=N,
                population_certificate_proxy=PC,population_ordinary_proxy=PO,
                planned_draws=planned,completed_costs=n,complete_cell=complete,
                certificate_cost_samples=sum(labels[m][rule] for m in available),
                ordinary_cost_samples=sum(not labels[m][rule] for m in available),
                estimated_certificate_CPU_h=mc["estimate"]/3600 if complete else None,
                estimated_ordinary_CPU_h=mo["estimate"]/3600 if complete else None,
                estimated_total_CPU_h=mt["estimate"]/3600 if complete else None,
                nominal97p5_certificate_CPU_low_h=cc[3]/3600 if complete and not gap_C else None,
                nominal97p5_certificate_CPU_high_h=cc[4]/3600 if complete and not gap_C else None,
                nominal97p5_ordinary_CPU_low_h=oo[3]/3600 if complete and not gap_O else None,
                nominal97p5_ordinary_CPU_high_h=oo[4]/3600 if complete and not gap_O else None,
                nominal_joint95_within_cell_share_low=within_lo,
                nominal_joint95_within_cell_share_high=within_hi,
                certificate_variance_CPU_s2=mc["variance"] if complete else None,
                ordinary_variance_CPU_s2=mo["variance"] if complete else None,
                within_cell_certificate_share=PC/N if PC in [0,N] else mc["estimate"]/mt["estimate"] if complete else None,
                positive_population_domain_unsampled=gap_C or gap_O,
                certificate_domain_unsampled=gap_C,ordinary_domain_unsampled=gap_O))
        TC,VC,dfC,LC,UC=aggregate(parts_C,.975)
        TO,VO,dfO,LO,UO=aggregate(parts_O,.975)
        total=TC+TO;R=TC/total if total else None
        zparts=[]
        for h in complete_h:
            s=strata[h];N=int(s["population_modules"])
            ms=[x["module"] for x in frame if x["stratum"]==h]
            z=[(labels[m][rule]-R)*(completed[m]["user_cpu_s"]+completed[m]["system_cpu_s"]) for m in ms]
            zparts.append(moments(N,z))
        zvar=sum(x["variance"] for x in zparts)
        zd=sum(x["variance"]**2/x["df"] for x in zparts if x["variance"]>0)
        dfR=zvar*zvar/zd if zd else math.inf
        crit=float(t.ppf(.975,dfR)) if math.isfinite(dfR) else float(norm.ppf(.975))
        margin=crit*math.sqrt(zvar)/total if total else 1.
        bonfL=LC/(LC+UO) if LC+UO else 0.
        bonfU=UC/(UC+LO) if UC+LO else 1.
        if domain_gaps:bonfL,bonfU=0.,1.
        for cell in bystratum:
            if cell["rule"] != rule:
                continue
            cell["covered_certificate_CPU_contribution"] = cell["estimated_certificate_CPU_h"]*3600/total if cell["complete_cell"] and total else None
            cell["covered_ordinary_CPU_contribution"] = cell["estimated_ordinary_CPU_h"]*3600/total if cell["complete_cell"] and total else None
            cell["whole_library_certificate_CPU_contribution"] = None
            cell["whole_library_ordinary_CPU_contribution"] = None
        all_complete=len(complete_h)==len(strata)
        missing=[h for h in strata if h not in complete_h]
        summaries.append(dict(rule=rule,scope="entire_library" if all_complete else "completed_strata_only",
            observed_original_costs=len(completed),planned_costs=42,
            completed_strata=len(complete_h),total_strata=21,
            covered_population_modules=sum(int(strata[h]["population_modules"]) for h in complete_h),
            conditional_certificate_CPU_h=TC/3600,conditional_ordinary_CPU_h=TO/3600,
            conditional_certificate_share=R,conditional_ordinary_share=1-R if R is not None else None,
            nominal95_delta_share_low=max(0.,R-margin) if R is not None and not domain_gaps else None,
            nominal95_delta_share_high=min(1.,R+margin) if R is not None and not domain_gaps else None,
            nominal_delta_df=dfR if math.isfinite(dfR) else None,
            nominal_joint95_Bonferroni_share_low=bonfL,nominal_joint95_Bonferroni_share_high=bonfU,
            certificate_domain97p5_CPU_low_h=LC/3600 if not any(x["rule"]==rule and x["complete_cell"] and x["certificate_domain_unsampled"] for x in bystratum) else None,
            certificate_domain97p5_CPU_high_h=UC/3600 if not any(x["rule"]==rule and x["complete_cell"] and x["certificate_domain_unsampled"] for x in bystratum) else None,
            ordinary_domain97p5_CPU_low_h=LO/3600 if not any(x["rule"]==rule and x["complete_cell"] and x["ordinary_domain_unsampled"] for x in bystratum) else None,
            ordinary_domain97p5_CPU_high_h=UO/3600 if not any(x["rule"]==rule and x["complete_cell"] and x["ordinary_domain_unsampled"] for x in bystratum) else None,
            covered_positive_domain_no_sample_cells=json.dumps(domain_gaps),
            whole_library_certificate_share=R if all_complete else None,
            whole_library_share_CI_low=bonfL if all_complete else None,
            whole_library_share_CI_high=bonfU if all_complete else None,
            missing_population_certificate_modules=sum(sum(labels[m][rule] for m in population[h]) for h in missing),
            missing_population_ordinary_modules=sum(sum(not labels[m][rule] for m in population[h]) for h in missing),
            interval_scope="normal-cost/t approximation; two draws/cell; conditional coverage; no nonresponse or misclassification correction"))
    cross=[]
    if a.legacy_profiles:
        for p in csv.DictReader(a.legacy_profiles.open()):
            m=p["module"];l=labels[m];share=float(p["cpp_type_checker_usercycle_share"])
            cross.append(dict(module=m,explicit_markers_per_KiB=l["explicit_markers_per_KiB"],
                explicit_any=l["explicit_any"],explicit_0p1_per_KiB=l["explicit_0p1_per_KiB"],
                explicit_1_per_KiB=l["explicit_1_per_KiB"],
                cpp_type_checker_usercycle_share=share,checker_majority=share>=.5,
                primary_agrees_majority=l["explicit_any"]==(share>=.5),
                profile_convention="legacy_M_methodology_only",
                valid_current_noM_cross_validation=False,
                interpretation="purposeful five-module diagnostic; user cycles not wall or all kernel work"))
    write_csv(a.out/"all-module-labels.csv.gz",fullrows)
    write_csv(a.out/"population-classification.csv",poprows)
    write_csv(a.out/"sample-classification.csv",sample_rows)
    write_csv(a.out/"stratum-domain-estimates.csv",bystratum)
    write_csv(a.out/"domain-share-summary.csv",summaries)
    write_csv(a.out/"legacy-profile-cross-check.csv",cross)
    receipt=dict(modules=len(modules),complete_noM_original_costs=len(completed),
        original_sample=42,complete_cells=len(complete_h),population_cells=21,
        primary_rule="explicit_any: masked explicit-marker density>0; not cost-tuned",
        marker_terms=["decide_plus_kernel","native_decide","bv_decide","ofReduceBool"],
        current_noM_Cpp_profile_cross_validation_cases=0,
        legacy_profile_cases=len(cross),no_new_native_run=True,
        input_results=[str(x) for x in a.results],excluded=dict(excluded),
        all_module_labels_gzip=str(a.out/"all-module-labels.csv.gz"),
        global_CI_established=len(complete_h)==21)
    (a.out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt),flush=True)
    print(json.dumps(summaries),flush=True)


if __name__=="__main__":
    main()
