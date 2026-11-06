#!/usr/bin/env python3
"""Export a retired census; never starts Lean or changes its frozen protocol."""
import argparse,collections,csv,datetime,gzip,json,statistics,math
from pathlib import Path

def load_rows(path):
    rows=[];damaged=0
    if not path.exists():return rows,damaged
    with path.open("rb")as f:
        for line in f:
            if not line.endswith(b"\n"):damaged+=1;continue
            try:rows.append(json.loads(line))
            except ValueError:damaged+=1
    return rows,damaged

def write_csv(path,rows,columns):
    opener=gzip.open if path.suffix==".gz"else open
    with opener(path,"wt",newline="")as f:
        w=csv.DictWriter(f,fieldnames=columns,extrasaction="ignore",lineterminator="\n");w.writeheader();w.writerows(rows)


def render_readme(out,s):
    rows=["| Segment | Completed modules | P CPU h | E CPU h | Observed wall h |",
          "|---|---:|---:|---:|---:|"]
    for r in s["segment_times"]:
        rows.append(f'| {r["segment"]} | {r["completed_modules"]:,} | {r["P_cpu_h"]:.3f} | {r["E_cpu_h"]:.3f} | {r["wall_s"]/3600:.3f} |')
    categories=[]
    groups={}
    for r in csv.DictReader((out/"aggregates.csv").open()):
        if r["dimension"] not in {"marker","default_graph"}:continue
        key=(r["dimension"],r["value"]);g=groups.setdefault(key,dict(count=0,P=0.,E=0.,instructions=0))
        g["count"]+=int(r["successful_modules"]);g[r["pool"]]+=float(r["cpu_s"])/3600;g["instructions"]+=int(r["instructions_user"])
    for (dim,value),g in sorted(groups.items()):
        name=("static decide +kernel present"if value=="1"else"static decide +kernel absent")if dim=="marker"else("inside default OAI import graph"if value=="1"else"outside default OAI import graph")
        categories.append(f'| {name} | {g["count"]:,} | {g["P"]:.3f} | {g["E"]:.3f} | {g["instructions"]:,} |')
    text=f"""# Measured completed subset of openai/math 4eaee875

**{s["completed_source_modules"]:,} / {s["source_modules"]:,} source modules completed.**
There is also one uncharged Lake configuration unit.
{s["unfinished_source_modules"]:,} source modules have no successful compilation
cost, including {s["deferred_source_modules"]:,} postponed at the user's request.
This dependency-ordered, memory-selected subset is not a random sample.
**No whole-corpus point estimate or confidence interval is inferred.**

## Observed costs of completed modules

{chr(10).join(rows)}

Successful native CPU is P **{s["successful_CPU_hours_by_pool"]["P"]:.3f} h**
and E **{s["successful_CPU_hours_by_pool"]["E"]:.3f} h**.
Their raw OS CPU-hour sum is {s["raw_OS_CPU_hours_sum_not_P_equivalent"]:.3f};
it is not a conversion to P-core equivalent work.
Primary user-mode instructions (the selected affinity-pool PMU, as in the
qualification analysis) total **{s["user_instruction_total"]:,}**. All four raw
core/atom user/kernel instruction counts remain available in module tables;
record-validation.json also reports other-pool counts. No rescaling is applied.

The sum of measured segment walls is {s["measured_segment_wall_hours"]:.3f} h.
Calendar span is {s["overall_calendar_hours"]:.3f} h, including a separately
reported transition gap of {s["transition_gap_s"]:.3f} s.
Successful CPU excludes failed/interrupted attempts; segment wall includes
preparation, all attempts, hashing, publication and cleanup.
Per-module wall is observed fork-to-reap time and may include collection lag.
Do not add overlapping per-module walls to obtain whole-run wall.

These are observed lower bounds on cumulative work already spent in this
collection's per-module protocol, not a full-library cost estimate. Costs of unmeasured modules remain
unknown. Missing rows have blank costs, never imputed zero.

## Observed subset by static marker and build scope

The two partitions below each cover only completed modules; they are not
independent sets to add together. The lexical marker is not dynamic kernel
attribution.

| Group | Completed modules | P CPU h | E CPU h | User-mode instructions |
|---|---:|---:|---:|---:|
{chr(10).join(categories)}

## Input and execution

Source commit: 4eaee87548250b2682affda7d05d947c05554bae.
Lean 4.34.1; Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612.
The real exported Lake context has 44 search entries and 42 pinned packages,
with 23 verified repository compatibility patches for dependency packages.
The measured machine topology and late-run observation timestamp are recorded
in summary.json measured_hardware. All recorded segments use the same canonical folded import view, -j8,
LEAN_NUM_THREADS=8, and no -M. Pools are P CPU 0-7 and E CPU 10-23.
Implementation commits by segment are recorded in summary.json.

Segment 1 admits up to 22 concurrent modules under actual-memory guarding,
then drains for exclusive resource retries. It completed 128,331 sources.
Segment 2 changes admission and explicitly postpones observed memory-heavy
families (including remaining PadicHodge) and their dependent closure. It
keeps dependency-ready lexical ordering among memory-eligible work.
Already completed segment-1 modules in those families remain included.
Segment 3 continues the 51 eligible modules left by the superseded 03:00
admission boundary. It uses the segment-2 admission policy without UTC deadlines;
no completed work is repeated. The gap is reported separately, not hidden.
See ../census-plan.md for recorded boundaries and the user continuation decision.
summary.json metadata_errata identifies a stale inherited generic retry label
in the raw segment-2 config; its top-level segment-specific label and frozen
code describe the actual user-deferral behavior. Raw metadata is preserved.
This cohort change prevents attributing throughput differences to admission
alone. The omitted tail may have a substantially higher average cost.

Generated C is produced normally, then hashed/sized in a durable record
before successful C files are removed. Olean/ilean and companions remain on
the capture PVC for subsequent independent checking. External package builds,
a separate downstream compilation/link step for the emitted C files, and
downstream checking are outside these totals. Work invoked internally by Lean
is part of its inherited process accounting. Source compilation does not establish
axiom freedom or replace independent kernel checking.

## Counter choice and resource observations

The original TOTAL-instruction qualification failed: median 1.33%,
P95 3.15%; thresholds were not changed. Claude chose execution after the
user requested progress. User-only instructions were selected POST HOC:
the four-condition qualification sample had median 0.018% and P95 0.14%.
This is not a substitute passing gate or a universal invariance proof.
OS kernel-mode counters are retained but not used for cross-module ranking;
they do not attribute work to Lean's trusted C++ kernel.

record-validation.json reports every return's provenance/counter checks and
active-PMU coverage. Resource attempts are separate from native rejections. The raw
cgroup_memory_oom label records an OOM-kill counter accompanying a failed
return; limiting-kernel-context attribution was not independently established
for every attempt. Owned-job OOM counters do not certify absence of all system
OOM events.
The guard targets available memory by sampling; it is not a hard guarantee.
Across captures, minimum sampled node availability was
{s["resource_observations"]["minimum_available_bytes"]/2**30:.3f} GiB,
with {s["resource_observations"]["samples_below_8_GiB"]} samples below 8 GiB
and maximum observed sampling gap
{s["resource_observations"]["max_observed_sample_gap_s"]:.3f} s.
Per-segment observations and interruption categories are in summary.json.

## Tables and units

- modules.csv.gz: one row per frozen source/configuration unit, with fate,
  measured segment, native cost, PMU coverage, source/artifact provenance and
  explicit deferral or dependency reason.
- failed-attempts.csv.gz: unsuccessful attempts, including recovered ones;
  they never enter completed-module cost aggregates.
- unfinished-modules.csv.gz and unfinished-by-family.csv: all missing successful
  costs, separated by fate; deferred-modules.csv.gz isolates user postponements.
- aggregates.csv: completed costs by stratum, static marker, default-root graph
  membership and core pool. Frame counts are explicitly named as frame counts.
- segment-totals.csv: observed segment walls and successful native CPU.
- top20-user-instructions.csv: primary post hoc ranking; top20-cpu.csv records
  raw charged CPU with pool identity, without normalizing P and E.
- original42-pairs.csv: {s["original42_completed_matches"]}/42 calibration modules
  matched to completed observations. P-only ratios are descriptive; E
  assignments are listed without a P-equivalent ratio.
- summary.json: machine-readable totals and limitations; export.py reproduces
  these tables from the retained retired capture and its segment registry.

Segment-2/3 admission_state_json and active_at_launch are recorded natively;
active_at_launch counts other in-flight attempts before this launch, excluding
the new attempt itself. Those fields are blank for segment 1, which did not
record them. cgroup_peak is the observed own-job cgroup charge high-water,
including charged shared/file pages; it is not summed RSS or a required-memory
guarantee. Failed peaks may be censored.

Native-attempt interruptions, never-started units and user deferrals have
distinct statuses. The original controller status is retained alongside the
normalized unit fate.

The marker is static decide +kernel presence, not dynamic kernel cost ground
truth. Sampling-frame count differences are disclosed in summary.json; old
weights are preserved and are not used to fill missing costs.

## Historical comparison

The original quiet-P 42-module estimate was 279.12 P CPU h (nominal interval
95.18-463.06), under a different concurrency/environment context. It is a
historical calibration record, not an estimator for the excluded tail here.

The [nealmcb report](https://github.com/nealmcb/openai-math-lean-tooling/blob/c9570a82f79b78a1a969a6316ac0fdd69aabef55/REPORT.md)
uses corpus fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb, 122,458 OAI modules,
a different cloud machine and -j4. Its approximately 330 CPU h is a
26-module laptop extrapolation, distinct from its measured 13.8-hour cloud
wall. The reported 116 GB is the whole finished build including packages;
Lean lib artifacts are about 68 GB. These are different scopes and protocols.

Re-export from this directory after all recorded supervisors retire:

    python3 export.py --point CAPTURE_ROOT --out OUTPUT --package ..

A capture archive can be moved as a whole: registry descendants resolve
relative to CAPTURE_ROOT. Artifact paths in rows preserve original provenance.
The export starts no Lean process. The compressed tables themselves suffice
to recompute cost totals without the capture: read modules.csv.gz with Python's
gzip/csv modules, keep status=completed, and sum cpu_s or instructions_user
by segment and pool. Sum segment-totals.csv wall_s separately. No model or
hardware conversion is involved. For checker comparisons, restrict native rows
to the exact checked source-module set and state external dependency treatment.
"""
    (out/"README.md").write_text(text)

def export(point,out,package):
    registry=json.loads((point/"census-segments.json").read_text())if(point/"census-segments.json").exists()else dict(segments=[dict(segment=1,point=str(point))])
    original_root=Path(registry["segments"][0]["point"])
    def capture_path(value):
        value=Path(value)
        if not value.is_absolute():return point/value
        if value.is_relative_to(original_root):return point/value.relative_to(original_root)
        return value
    captures=[(x["segment"],capture_path(x["point"]))for x in registry["segments"]]
    for sid,capture in captures:
        if not(capture/"supervisor-terminal.json").exists():raise ValueError("segment "+str(sid)+" is not retired; no progress publication")
    final_capture=captures[-1][1]
    manifest=json.loads((point/"manifest.json").read_text());mods={r["module"]:r for r in manifest["modules"]}
    outcome_path=final_capture/"run/outcomes.json"
    if not outcome_path.exists():
        if(final_capture/"derived-outcomes.json").exists():outcome_path=final_capture/"derived-outcomes.json"
        else:raise ValueError("retired segment lacks outcomes; derive terminal accounting explicitly before export")
    outcomes=json.loads(outcome_path.read_text())
    records=[];damaged=0
    for sid,capture in captures:
        rr,dd=load_rows(capture/"run/records.jsonl");damaged+=dd
        records.extend(dict(r,segment=r.get("segment",sid))for r in rr)
    deferred={r["module"]:r for r in outcomes.get("deferred",[])}
    last_native={r["module"]:r for r in records}
    accepted={r["module"]:r for r in records if r["status"]=="completed"}
    failures=[r for r in records if r["status"]!="completed"]
    blocked={r["module"]:r for r in outcomes.get("blocked",[])}
    failed=set(outcomes.get("failed",[]))
    configuration={n for n,r in mods.items()if Path(r["source"]).name=="lakefile.lean"}
    default=set();todo=["OAI"]
    while todo:
        n=todo.pop()
        if n in default:continue
        default.add(n);todo.extend(mods[n]["deps"])
    depths={}
    def depth(n):
        if n not in depths:depths[n]=1+max((depth(p)for p in mods[n]["deps"]),default=0)
        return depths[n]
    def stratum(r):
        size=r["bytes"];a="0-50"if size<=4400 else"50-90"if size<=15057 else"90-99"if size<=80757 else"99-100"
        d=depth(r["module"]);return a+";"+("1-10"if d<=10 else"11-100"if d<=100 else"101+")+";"+str(int(bool(r["decide_plus_kernel"])))
    flat=[]
    for n,r in sorted(mods.items()):
        source=str(Path(r["source"]).relative_to(Path(manifest["source_project_root"]).parent))
        fate="completed"if n in accepted else"configuration"if n in configuration else"failure"if n in failed else "deferred_by_user"if n in deferred else blocked.get(n,{}).get("status","unknown")
        if fate=="not_attempted":fate="unfinished_after_attempt"if n in last_native else"not_started_before_stop"
        x=dict(module=n,source_unit=source,status=fate,segment="",decision_segment=(captures[-1][0]if n in deferred or n in blocked else ""),family=n.rsplit(".",1)[0],source_bytes=r["bytes"],stratum=stratum(r),
            marked=int(bool(r["decide_plus_kernel"])),decide_plus_kernel_occurrences=r["decide_plus_kernel"],
            default_graph=int(n in default),source_revision=manifest["source_revision"],mathlib_commit=manifest["mathlib"],
            failed_dependencies=json.dumps(blocked.get(n,{}).get("failed_dependencies",[])),missing_external=json.dumps(blocked.get(n,{}).get("missing_external",[])))
        x["measurement_commit"]=""
        if n in last_native:
            last=last_native[n]
            for key in ["pool","attempt","segment","active_at_launch","source_sha256","measurement_commit","start_utc","end_utc","log","returncode","interruption"]:x[key]=last.get(key)
        x["controller_reported_status"]=blocked.get(n,{}).get("status","")
        x["blocked_reason"]=blocked.get(n,{}).get("reason","")
        x["uncompleted_dependencies"]=json.dumps(blocked.get(n,{}).get("uncompleted_dependencies",[]))
        d=deferred.get(n,{})
        for k in ["utc","reason","family_prefix","trigger_module","deferred_dependency"]:x[k if k=="deferred_dependency"else"deferred_"+k]=d.get(k,"")
        if n in accepted:
            row=accepted[n];x["admission_state_json"]=json.dumps(row["admission"],sort_keys=True)if"admission"in row else"";pmu="cpu_core"if row["pool"]=="P"else"cpu_atom"
            x.update({k:row.get(k)for k in ["pool","attempt","segment","active_at_launch","cgroup_peak","user_cpu_s","system_cpu_s","wall_s","peak_rss_kib","source_sha256","measurement_commit","start_utc","end_utc","lean_num_threads"]})
            x["cpu_s"]=row["user_cpu_s"]+row["system_cpu_s"]
            for mode in ["user","kernel"]:
                event=row["counters"][pmu+"_"+mode];x["instructions_"+mode]=event["instructions"];x[mode+"_coverage"]=event["coverage"]
            for event_name,event in row["counters"].items():
                x[event_name+"_instructions"]=event.get("instructions")
            for suffix in [".olean",".ilean",".c"]:
                value=row["artifacts"][suffix];x[suffix[1:]+"_bytes"]=value["bytes"];x[suffix[1:]+"_sha256"]=value["sha256"];x[suffix[1:]+"_path"]=value["path"]
            x["c_retained"]=row["artifacts"][".c"].get("retained",True)
        flat.append(x)
    out.mkdir(parents=True,exist_ok=True)
    columns=["module","source_unit","status","segment","decision_segment","controller_reported_status","family","uncompleted_dependencies","deferred_utc","deferred_reason","deferred_family_prefix","deferred_trigger_module","deferred_dependency","source_bytes","stratum","marked","decide_plus_kernel_occurrences","default_graph","source_revision","mathlib_commit",
        "pool","attempt","active_at_launch","admission_state_json","cgroup_peak","user_cpu_s","system_cpu_s","cpu_s","wall_s","peak_rss_kib","source_sha256","measurement_commit","start_utc","end_utc","lean_num_threads",
        "instructions_user","instructions_kernel","cpu_core_user_instructions","cpu_core_kernel_instructions","cpu_atom_user_instructions","cpu_atom_kernel_instructions","user_coverage","kernel_coverage","olean_bytes","ilean_bytes","c_bytes","olean_sha256","ilean_sha256","c_sha256","c_retained","olean_path","ilean_path","c_path","log","returncode","interruption","blocked_reason","failed_dependencies","missing_external"]
    write_csv(out/"modules.csv.gz",flat,columns)
    attempt_columns=["module","attempt","sequence","pool","memory_events_json","active_at_launch","admission_state_json","cgroup_peak","status","returncode","interruption","user_cpu_s","system_cpu_s","wall_s","peak_rss_kib","source_sha256","source_revision","measurement_commit","start_utc","end_utc","log"]
    for row in failures:
        row["memory_events_json"]=json.dumps({k:int(v)for k,v in (line.split()for line in row.get("memory_events","").splitlines())},sort_keys=True)if"memory_events"in row else""
        row["admission_state_json"]=json.dumps(row["admission"],sort_keys=True)if"admission"in row else""
        pmu="cpu_core"if row["pool"]=="P"else"cpu_atom"
        for event_name,event in row.get("counters",{}).items():row[event_name+"_instructions"]=event.get("instructions")
        for mode in ["user","kernel"]:
            event=row.get("counters",{}).get(pmu+"_"+mode,{})
            row["instructions_"+mode]=event.get("instructions");row[mode+"_coverage"]=event.get("coverage")
    write_csv(out/"failed-attempts.csv.gz",failures,attempt_columns+["segment","instructions_user","instructions_kernel","cpu_core_user_instructions","cpu_core_kernel_instructions","cpu_atom_user_instructions","cpu_atom_kernel_instructions","user_coverage","kernel_coverage"])
    unfinished=[x for x in flat if x["status"]not in {"completed","configuration"}]
    write_csv(out/"unfinished-modules.csv.gz",unfinished,columns)
    write_csv(out/"deferred-modules.csv.gz",[x for x in unfinished if x["status"]=="deferred_by_user"],columns)
    uf=collections.Counter((x["family"],x["status"])for x in unfinished)
    write_csv(out/"unfinished-by-family.csv",[dict(family=f,status=st,unfinished_modules=n)for(f,st),n in sorted(uf.items())],["family","status","unfinished_modules"])
    sums=collections.defaultdict(lambda:dict(successful_modules=0,cpu_s=0.,user_cpu_s=0.,system_cpu_s=0.,instructions_user=0,instructions_kernel=0))
    for x in flat:
        if x["status"]!="completed":continue
        for kind,key in [("pool",x["pool"]),("stratum",x["stratum"]),("marker",str(x["marked"])),("default_graph",str(x["default_graph"]))]:
            z=sums[(kind,key,x["pool"])];z["successful_modules"]+=1
            for metric in ["cpu_s","user_cpu_s","system_cpu_s","instructions_user","instructions_kernel"]:z[metric]+=x[metric]
    aggregate=[dict(dimension=k[0],value=k[1],pool=k[2],**v)for k,v in sorted(sums.items())]
    write_csv(out/"aggregates.csv",aggregate,["dimension","value","pool","successful_modules","cpu_s","user_cpu_s","system_cpu_s","instructions_user","instructions_kernel"])
    good=[x for x in flat if x["status"]=="completed"]
    write_csv(out/"top20-cpu.csv",sorted(good,key=lambda r:r["cpu_s"],reverse=True)[:20],columns)
    write_csv(out/"top20-user-instructions.csv",sorted(good,key=lambda r:r["instructions_user"],reverse=True)[:20],columns)
    byname={r["module"]:r for r in flat};pairs=[]
    for old in csv.DictReader((package/"sample-costs.csv").open()):
        current=byname.get(old["module"],{})
        x=dict(module=old["module"],sample_P_cpu_s=old["cpu_s"],sample_P_wall_s=old["wall_s"],sample_stratum=old["stratum"],
            measured_segment=current.get("segment"),measured_status=current.get("status"),measured_pool=current.get("pool"),measured_cpu_s=current.get("cpu_s"),measured_wall_s=current.get("wall_s"),
            measured_instructions_user=current.get("instructions_user"),measured_stratum=current.get("stratum"))
        if x["measured_status"]=="completed"and x["measured_pool"]=="P":x["P_measured_to_quiet_sample_cpu_ratio"]=x["measured_cpu_s"]/float(old["cpu_s"])
        pairs.append(x)
    write_csv(out/"original42-pairs.csv",pairs,["module","sample_P_cpu_s","sample_P_wall_s","sample_stratum","measured_segment","measured_status","measured_pool","measured_cpu_s","measured_wall_s","measured_instructions_user","measured_stratum","P_measured_to_quiet_sample_cpu_ratio"])
    phase_seconds=0.;boots=set();phases=[];segment_times=[]
    for sid,capture in captures:
        pp,_=load_rows(capture/"run/execution-phases.jsonl");phases.extend(pp)
        sup=json.loads((capture/"supervisor.json").read_text());term=json.loads((capture/"supervisor-terminal.json").read_text())
        wall=term["monotonic_s"]-sup["monotonic_s"]
        if wall<0:raise ValueError("invalid monotonic segment span")
        acquired=next((x for x in pp if x["event"]=="lease_acquired"),None)
        if acquired:boots.add(acquired["boot_id"]);phase_seconds+=term["monotonic_s"]-acquired["monotonic_s"]
        segment_times.append(dict(segment=sid,start_utc=sup["start_utc"],end_utc=term["end_utc"],wall_s=wall,returncode=term["returncode"],capture=str(capture)))
    total_wall=sum(x["wall_s"]for x in segment_times)
    existing={r["stratum"]:int(r["population_modules"])for r in csv.DictReader((package/"strata.csv").open())}
    actual=collections.Counter(x["stratum"]for x in flat)
    summary=dict(source_units=len(mods),source_modules=len(mods)-len(configuration),configuration_units=len(configuration),
        outcome_counts=dict(collections.Counter(x["status"]for x in flat)),record_returns=len(records),failed_attempts=len(failures),
        damaged_record_lines=damaged,full_compile_success=outcomes.get("complete",False),
        all_source_units_accounted_for=all(x["status"]in {"completed","configuration","failure","blocked","not_attempted","not_started_before_stop","unfinished_after_attempt","deferred_by_user"}for x in flat),
        all_source_modules_have_native_or_dependency_outcome=all(x["status"]in {"completed","configuration","failure","blocked"}for x in flat),
        stop=outcomes.get("stop"),active_phase_wall_s=phase_seconds,phase_count=sum(x["event"]=="lease_acquired"for x in phases),boot_ids=sorted(boots),supervisor_wall_s=total_wall,
        successful_pool_totals={p:sums[("pool",p,p)]for p in ["P","E"]},user_instruction_total=sum(x["instructions_user"]for x in good),
        kernel_instruction_total_recorded_not_comparison=sum(x["instructions_kernel"]for x in good),
        frame_default_graph_units=len(default),frame_outside_default_units=len(mods)-len(default),frame_marked_source_modules=sum(bool(x["marked"])for x in flat if x["status"]!="configuration"),
        frame_stratum_count_differences=[dict(stratum=n,current=actual[n],original=existing.get(n))for n in sorted(set(actual)|set(existing))if actual[n]!=existing.get(n)],
        historical_original42_estimate_P_CPU_hours=279.12,historical_original42_nominal_interval_P_CPU_hours=[95.18,463.06],
        nealmcb_reference_CPU_hours=330,nealmcb_reference_module_count=122458,
        comparison_scope="P and E CPU seconds are not converted; old 42 is quiet P and different environment path; nealmcb is another commit/module set and extrapolated CPU, not measured aggregate.",
        primary_instruction_choice="User-only instructions selected after failed total-instruction gate; thresholds unchanged and failed gate preserved.",
        measurement_commit=json.loads((point/"run/run-config.json").read_text())["measurement_commit"],
        measured_hardware=json.loads((point/"hardware-observation.json").read_text())if(point/"hardware-observation.json").exists()else None)
    guard_count=0;guard_min=None;guard_under=0;max_sample_gap=0.;guard_segments=[]
    for sid,capture in captures:
        count=0;minimum=None;under=0;gap=0.;previous_stamp=None
        with(capture/"run/memory.jsonl").open("rb")as fh:
            for raw in fh:
                if not raw.endswith(b"\n"):continue
                try:g=json.loads(raw)
                except ValueError:continue
                count+=1;available=g.get("available");stamp=datetime.datetime.fromisoformat(g["utc"])
                if previous_stamp is not None:gap=max(gap,(stamp-previous_stamp).total_seconds())
                previous_stamp=stamp
                if available is not None:minimum=available if minimum is None else min(minimum,available);under+=available<8*2**30
        guard_segments.append(dict(segment=sid,samples=count,minimum_available_bytes=minimum,samples_below_8_GiB=under,max_observed_sample_gap_s=gap))
        guard_count+=count;guard_under+=under;max_sample_gap=max(max_sample_gap,gap)
        if minimum is not None:guard_min=minimum if guard_min is None else min(guard_min,minimum)
    summary["resource_observations"]=dict(samples=guard_count,minimum_available_bytes=guard_min,samples_below_8_GiB=guard_under,max_observed_sample_gap_s=max_sample_gap,
        by_segment=guard_segments,failed_attempt_reasons=dict(collections.Counter(r.get("interruption")or r["status"]for r in failures)),
        recovered_failed_modules=len({r["module"]for r in failures}&set(accepted)),
        excluded_failed_CPU_seconds=sum(r.get("user_cpu_s",0)+r.get("system_cpu_s",0)for r in failures))
    required=["pool","user_cpu_s","system_cpu_s","wall_s","peak_rss_kib","source_sha256","source_revision","measurement_commit","attempt","start_utc","end_utc"]
    issues=collections.Counter();examples=[];coverage=collections.defaultdict(list)
    for row in records:
        found=[k for k in required if row.get(k)is None]
        for pmu in ["cpu_core","cpu_atom"]:
            for mode in ["user","kernel"]:
                event=row.get("counters",{}).get(pmu+"_"+mode,{})
                found.extend(pmu+"_"+mode+"."+k for k in ["instructions","enabled_ns","running_ns","coverage"]if k not in event)
        if row["status"]=="completed":
            pmu="cpu_core"if row["pool"]=="P"else"cpu_atom"
            for mode in ["user","kernel"]:
                ev=row.get("counters",{}).get(pmu+"_"+mode,{})
                if ev.get("coverage")is None or ev.get("instructions",0)<=0:found.append(pmu+"_"+mode+".inactive")
                else:coverage[(row["pool"],mode)].append(ev["coverage"])
        issues.update(found)
        if found and len(examples)<20:examples.append(dict(module=row["module"],attempt=row.get("attempt"),issues=found))
    validation=dict(raw_record_count=len(records),damaged_record_lines=damaged,
        duplicate_successful_modules=len([r for r in records if r["status"]=="completed"])-len(accepted),
        modules_outside_frozen_manifest=sorted({r["module"]for r in records}-set(mods)),
        issue_counts=dict(issues),examples=examples,
        active_coverage={p+"_"+mode:dict(count=len(v),minimum=min(v),maximum=max(v),below_one=sum(x<.999999 for x in v))for(p,mode),v in coverage.items()})
    summary["owned_job_oom_accounting_by_segment"]={}
    for sid,capture in captures:
        rr=[r for r in records if r["segment"]==sid]
        values=[dict(line.split()for line in r.get("memory_events","").splitlines()).get("oom_kill")for r in rr]
        summary["owned_job_oom_accounting_by_segment"][str(sid)]=dict(attempts_with_oom_kill=sum(int(v)>0 for v in values if v is not None),oom_kill_counter_sum=sum(int(v)for v in values if v is not None),missing_memory_events=sum(v is None for v in values))
    validation["other_pool_instructions"]={mode:sum(r.get("counters",{}).get(("cpu_atom"if r["pool"]=="P"else"cpu_core")+"_"+mode,{}).get("instructions",0)for r in records)for mode in ["user","kernel"]}
    expected_commits={sid:json.loads((capture/"run/run-config.json").read_text())["measurement_commit"]for sid,capture in captures}
    validation.update(
        duplicate_attempt_sequences=len(records)-len({r["sequence"]for r in records}),
        source_revision_mismatches=sum(r.get("source_revision")!=manifest["source_revision"]for r in records),
        segment_commit_mismatches=sum(r.get("measurement_commit")!=expected_commits[r["segment"]]for r in records),
        thread_count_mismatches=sum(r.get("lean_num_threads")!=8 for r in records),
        malformed_source_hashes=sum(len(r.get("source_sha256",""))!=64 for r in records),
        compiler_arguments_with_M=[r["sequence"]for r in records if any(x=="-M"or x.startswith("-M")and x[2:].isdigit()for x in r.get("argv",[]))],
        second_segment_missing_admission=[r["sequence"]for r in records if r["segment"]>=2 and("admission"not in r or"active_at_launch"not in r)])
    (out/"record-validation.json").write_text(json.dumps(validation,indent=2)+"\n")
    terminal_rows=[]
    for segment in segment_times:
        sid=segment["segment"];gg=[x for x in good if x["segment"]==sid];ff=[x for x in failures if x["segment"]==sid]
        terminal_rows.append(dict(**segment,completed_modules=len(gg),failed_attempts=len(ff),
            P_cpu_h=sum(x["cpu_s"]for x in gg if x["pool"]=="P")/3600,
            E_cpu_h=sum(x["cpu_s"]for x in gg if x["pool"]=="E")/3600,
            instructions_user=sum(x["instructions_user"]for x in gg)))
    write_csv(out/"segment-totals.csv",terminal_rows,list(terminal_rows[0]))
    calendar=(datetime.datetime.fromisoformat(segment_times[-1]["end_utc"])-datetime.datetime.fromisoformat(segment_times[0]["start_utc"])).total_seconds()
    summary.update(scope="Completed dependency-ordered subset with explicit user-deferred memory families; no extrapolation",whole_corpus_point_estimate=None,extrapolation_used=False,
        stop_reason=outcomes.get("stop")or("eligible_work_exhausted"if outcomes.get("eligible_complete")else"recorded_retirement"),
        segment_count=len(captures),segment2_launched=len(captures)>1,segment_times=terminal_rows,
        completed_source_modules=len(good),unfinished_source_modules=len(unfinished),deferred_source_modules=len(deferred),
        completed_fraction_of_source_modules=len(good)/(len(mods)-len(configuration)),
        measured_segment_wall_hours=total_wall/3600,overall_calendar_hours=calendar/3600,transition_gap_s=calendar-total_wall,
        successful_CPU_hours_by_pool={p:summary["successful_pool_totals"][p]["cpu_s"]/3600 for p in ["P","E"]},
        raw_OS_CPU_hours_sum_not_P_equivalent=sum(x["cpu_s"]for x in good)/3600,
        completed_default_graph_modules=sum(x["default_graph"]for x in good),completed_outside_default_graph_modules=sum(not x["default_graph"]for x in good),
        completed_marked_modules=sum(x["marked"]for x in good),completed_unmarked_modules=sum(not x["marked"]for x in good),
        whole_corpus_lower_bound_scope="Observed completed-module CPU vector only; unmeasured cost unknown, no P/E conversion or whole-corpus extrapolation",
        original42_completed_matches=sum(x["measured_status"]=="completed"for x in pairs),
        original42_completed_matches_by_pool=dict(collections.Counter(x["measured_pool"]for x in pairs if x["measured_status"]=="completed")),
        sampled_279h_estimate_not_used_for_extrapolation=True,
        pending_composition_warning="Nonrandom dependency prefix, then user exclusion of remaining high-memory families and descendants. Segment-1 completed modules in these families remain included.",
        metadata_errata=[dict(segment=sid,field="run-config.json.protocol_rules.resource_retry",issue="Inherited segment-1 generic value; segment-specific top-level resource_retry and frozen source implement user deferral, not drain/exclusive retries") for sid,capture in captures if sid>=2],
        known_final_native_failures=len(failed),known_failed_dependency_blocks=sum(x["status"]=="blocked"for x in flat),
        measurement_commits_by_segment={str(sid):json.loads((capture/"run/run-config.json").read_text())["measurement_commit"]for sid,capture in captures})
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    render_readme(out,summary)
    return summary
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--point",type=Path,required=True);ap.add_argument("--out",type=Path,required=True);ap.add_argument("--package",type=Path,required=True);a=ap.parse_args()
    print(json.dumps(export(a.point,a.out,a.package),indent=2))
