#!/usr/bin/env python3
"""Actual complete-directory costs and exact acceptance sets."""
from pathlib import Path
import csv,json
D=Path(__file__).resolve().parent
A=Path("/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/subexponential-20261103")
def main():
 s=json.loads((A/"state.json").read_text());fr=json.loads((A/"frame.json").read_text())
 expected={v["module"]for v in fr};targets={v["module"]for v in fr if v["target"]}
 assert len(expected)==14721 and len(targets)==3977
 assert s["phase"]=="complete"and set(s["stream_ids"])==expected and expected<=set(s["oracle_ids"]),"incomplete coverage; no full cost ratio"
 bad=json.loads((A/"negative-controls-terminal.json").read_text())
 assert bad["complete"]and bad["rejected"]==3
 ledger=[json.loads(l)for l in(A/"ledger.jsonl").read_text().splitlines()]
 builds=[v for v in ledger if v["operation"]=="build"];checks=[v for v in ledger if v["operation"]=="stream"];refs=[v for v in ledger if v["operation"]=="oracle"]
 assert all(v["valid"]for v in checks+refs)
 cpu=lambda v:v["cell"]["user_s"]+v["cell"]["system_s"]
 reused=[v["reused"]for v in fr if"reused"in v]
 nc=sum(cpu(v)for v in builds);nw=sum(v["cell"]["wall_s"]for v in builds)
 rc=sum(v["source_cpu_s"]for v in reused);rw=sum(v["source_wall_s"]for v in reused)
 kc=sum(cpu(v)for v in checks);kw=sum(v["cell"]["wall_s"]for v in checks)
 out=dict(complete=True,source_pin="4eaee87548250b2682affda7d05d947c05554bae",source_targets=3977,dependencies=10744,closure=14721,
 accepted_set_equal=set(s["stream_ids"])==set(s["oracle_ids"])==expected,source_attempts=len(builds),source_failures=sum(not v["valid"]for v in builds),
 source_sorry_warnings=sum(v.get("sorry_warning",False)for v in builds),stream_segments=len(checks),
 source_target_cpu_s=nc,source_retained_dependency_cpu_s=rc,source_full_cpu_s=nc+rc,checker_cpu_s=kc,checker_cpu_h=kc/3600,
 source_target_wall_s=nw,source_retained_dependency_wall_s=rw,source_full_wall_s=nw+rw,checker_wall_s=kw,
 full_cpu_ratio=kc/(nc+rc),incremental_cpu_ratio=kc/nc,full_summed_child_wall_ratio=kw/(nw+rw),incremental_summed_child_wall_ratio=kw/nw,
 checker_peak_rss_gib=max(v["cell"]["peak_rss_kib"]for v in checks)/1024**2,separate_reference_cpu_s=sum(cpu(v)for v in refs),
 separate_reference_wall_s=sum(v["cell"]["wall_s"]for v in refs),negative_controls_rejected=3)
 final_events=[json.loads(l)for l in(A/(checks[-1]["cell"]["key"]+".stdout")).read_text().splitlines()if l.startswith("{")]
 terminal=next(v for v in reversed(final_events)if v.get("event")=="complete")
 assert terminal["modules"]==14721
 out["native_complete_event"]=terminal
 successful=[v for v in builds if v["valid"]];durations=sorted(cpu(v)for v in successful)
 source_max_rss=max(v["cell"]["peak_rss_kib"]for v in builds)/1024**2
 event_counts={}
 for v in builds:
  for line in v["cell"]["memory_events"].splitlines():
   key,value=line.split();event_counts[key]=event_counts.get(key,0)+int(value)
 bad_source=[v for v in builds if not v["valid"]]
 old_provider_terms=["unknown declaration","missing native","executable code","unknown module prefix","object file"]
 provider_failures=[]
 for v in bad_source:
  text=(A/(v["cell"]["key"]+".stdout")).read_text(errors="replace")+(A/(v["cell"]["key"]+".stderr")).read_text(errors="replace")
  if any(x in text.lower()for x in old_provider_terms):provider_failures.append(v["cell"]["key"])
 risks=dict(source_successful_attempt_mean_cpu_s=sum(durations)/len(durations),pilot_mean_cpu_s=4.22759456,
  source_attempt_p50_cpu_s=durations[(len(durations)-1)//2],source_attempt_p90_cpu_s=durations[int((len(durations)-1)*.9)],
  source_attempt_p99_cpu_s=durations[int((len(durations)-1)*.99)],source_attempt_max_cpu_s=max(durations),source_max_rss_gib=source_max_rss,
  source_returncode124_count=sum(v["cell"]["returncode"]==124 for v in builds),source_cgroup_events=event_counts,
  failed_attempts_with_old_provider_error_text=provider_failures,source_cleanup_pending_count=sum("cleanup_pending"in v["cell"]for v in builds),
  static_plain_by_decide_sites=26593,static_explicit_kernel_sites=0,
  plain_decide_runtime_attribution="not measured per tactic; cannot attribute aggregate cost or absence of heavy calls to markers",
  scope="Actual complete-directory outcomes; not a claim all9124old failures were rerun or all163097sources work.")
 out["post_run_risk_review"]=risks
 (D/"subexponential-risk-review.json").write_text(json.dumps(risks,indent=2)+"\n")
 review="# SubexponentialSAT: post-run review of9eea8be planning risks\n\nReview: 自审.\n\n"
 review+=f"- **Provider/runtime initialization:** {len(provider_failures)} failed attempts with text matching the earlier Meta/IR/provider failure family, out of{len(builds)}source attempts. Full native acceptance is directory scoped; historical9124environment failures remain unchanged and are not silently rerun.\n"
 review+=f"- **Cost transfer:** successful-source mean{risks['source_successful_attempt_mean_cpu_s']:.6f}CPU-s versus25-source pilot4.227595; P50/P90/P99/max = {risks['source_attempt_p50_cpu_s']:.3f}/{risks['source_attempt_p90_cpu_s']:.3f}/{risks['source_attempt_p99_cpu_s']:.3f}/{risks['source_attempt_max_cpu_s']:.3f}s. This is retrospective complete coverage, not a bounded predictor.\n"
 review+="- **Markers beyond+kernel:** zero explicit sites coexist with26593plain by-decide sites in1932files. Their tactic-specific CPU was not instrumented; the measured whole-stream fraction does not prove they were individually cheap or inactive. Large-source maximum147641bytes was a static risk indicator, not a cost bound.\n"
 review+=f"- **Operational limits:** source timeout-returncodes124={risks['source_returncode124_count']}; cgroupOOM-kill events={event_counts.get('oom_kill',0)}, max events={event_counts.get('max',0)}; maximum sourceRSS={source_max_rss:.3f}GiB. RSS and cgroup-charged memory are distinct observations. Pending native cgroup cleanup records={risks['source_cleanup_pending_count']}. Limits were not relaxed.\n"
 review+=f"- **Admissions/diagnostics:** {out['source_sorry_warnings']}source sorry-warning records. The six static sorry/admit matches were six English admit words in comments, zero sorry tokens; no dependency-axiom audit is claimed. Source failures(all causes)={out['source_failures']} remain charged and preserved.\n"
 review+="- **Checking correctness:** all14721stream IDs equal the complete source frame and original module-local reference set under the documented safe-declaration policy. Three in-memory malformed theorem bodies were actually rejected by the original kernel. Rejections do not imply hardened parsing of hostile binary oleans.\n"
 review+="- **Input condition:** checking consumes completed source-produced typed artifacts, not raw AI tactic scripts. Removing completed dependency production from the incremental denominator does not remove their fresh checking from the numerator. Startup/checkpoint work is included; no source-only RL-service throughput gain is inferred.\n"
 (D/"subexponential-risk-review.md").write_text(review)
 (D/"subexponential-complete-metrics.json").write_text(json.dumps(out,indent=2)+"\n")
 parts=[dict(component="retained dependency source work",cpu_s=rc,child_wall_s=rw,executed_now=False),
 dict(component="new target source work(all attempts)",cpu_s=nc,child_wall_s=nw,executed_now=True),
 dict(component="fresh full-closure checkpointed checking",cpu_s=kc,child_wall_s=kw,executed_now=True),
 dict(component="separate module-local reference qualification",cpu_s=out["separate_reference_cpu_s"],child_wall_s=out["separate_reference_wall_s"],executed_now=True)]
 with(D/"subexponential-component-costs.csv").open("w",newline="")as f:
  w=csv.DictWriter(f,fieldnames=parts[0],lineterminator="\n");w.writeheader();w.writerows(parts)
 text="# Complete SubexponentialSAT: production and original-kernel checking\n\nReview: 自审.\n\n"
 text+=f"**3977targets +10744dependencies =14721modules**, original4.34.1 kernel, exact accepted set equals measured-source frame and module-local reference set. Three deliberately malformed proofs rejected. Pins: source4eaee875, Mathlibd13f23b7. **{len(checks)}segments**,500new modules each. Startup/restore/export included in native clocks.\n\n"
 text+="| Accounting scope | Source CPU-s | Checker CPU-s | CPU ratio | Summed child-wall ratio |\n|---|---:|---:|---:|---:|\n"
 text+=f"| Full closure, retained dependencies included |{nc+rc:.3f}|{kc:.3f}|**{out['full_cpu_ratio']:.2%}**|{out['full_summed_child_wall_ratio']:.2%}|\n"
 text+=f"| New-target production only, retained dependencies excluded |{nc:.3f}|{kc:.3f}|**{out['incremental_cpu_ratio']:.2%}**|{out['incremental_summed_child_wall_ratio']:.2%}|\n\n"
 text+=f"Native final accounting: **{terminal.get('unique_shared_kernel_declarations','unknown')}** shared kernel declarations; **{terminal.get('module_local_fallbacks','unknown')}** original module-local fallbacks; **{terminal.get('skipped_unsafe_partial','unknown')}** unsafe/partial entries outside this safe-declaration replay policy. Fallback CPU is included. Accepted-module equality is under the identical documented stream/reference adapter policy, not a claim that every unsafe runtime definition was kernel-replayed or that all declarations used only one shared environment.\n\n"
 text+="Both rows use the **same fresh full-closure checker**, including dependency rechecking. The second removes only already-completed dependency source costs, so it is not target-only checking or a pure kernel fraction. Retained source costs are actual matching-artifact compiler records, charged once, never rerun or estimated. Source emits olean/ilean/C, excluding C linking; it is not a fresh parallel Lake service.\n\n"
 text+=f"Checker**{kc/3600:.6f}CPUh**, peakRSS**{out['checker_peak_rss_gib']:.3f}GiB**. Separate reference qualification**{out['separate_reference_cpu_s']/3600:.6f}CPUh**. Source failures{out['source_failures']}, sorry warnings{out['source_sorry_warnings']}; all source attempts charged. Negative controls and parent dispatch/publication excluded from primary ratios, retained separately.\n\n"
 text+="Wall ratios sum native child intervals including startup, excluding FIFO waits, Git, interruptions and untimed setup. No continuous from-scratch episode wall run or global163097-module total is claimed. P0–7/flock/no-M/external11.75GiB native cgroup+256MiB parent reserve; one O native at a time.\n\n"
 text+="| Input | Check/source CPU | Protocol |\n|---|---:|---|\n| Falconer |6.31%|Complete13205-node segmented stream, full source costs|\n| Matched Mathlib |8.95%|Complete1330-node matched segmented stream|\n"
 text+=f"| SubexponentialSAT |{out['full_cpu_ratio']:.2%}|Complete14721-node stream, full source costs|\n"
 text+="| Ramsey20sample |35.91%|Module-local190-built-prefix sample, trusted imports; not a whole stream|\n| RamseyK10 |20.66%|Supplemental single module, not a closure|\n\n"
 text+="The25-source pilot is included once. Superseded total-cost12h interpretation is retained; user clarified future new work only. See subexponential-risk-review.md for post-run evaluation of the9eea8be static risks; absence of kernel markers is not a semantic cost label.\n"
 (D/"subexponential-complete-result.md").write_text(text);print(json.dumps(out,indent=2))
if __name__=="__main__":main()
