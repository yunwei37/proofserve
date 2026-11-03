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
 text+="Both rows use the **same fresh full-closure checker**, including dependency rechecking. The second removes only already-completed dependency source costs, so it is not target-only checking or a pure kernel fraction. Retained source costs are actual matching-artifact compiler records, charged once, never rerun or estimated. Source emits olean/ilean/C, excluding C linking; it is not a fresh parallel Lake service.\n\n"
 text+=f"Checker**{kc/3600:.6f}CPUh**, peakRSS**{out['checker_peak_rss_gib']:.3f}GiB**. Separate reference qualification**{out['separate_reference_cpu_s']/3600:.6f}CPUh**. Source failures{out['source_failures']}, sorry warnings{out['source_sorry_warnings']}; all source attempts charged. Negative controls and parent dispatch/publication excluded from primary ratios, retained separately.\n\n"
 text+="Wall ratios sum native child intervals including startup, excluding FIFO waits, Git, interruptions and untimed setup. No continuous from-scratch episode wall run or global163097-module total is claimed. P0–7/flock/no-M/external11.75GiB native cgroup+256MiB parent reserve; one O native at a time.\n\n"
 text+="| Input | Check/source CPU | Protocol |\n|---|---:|---|\n| Falconer |6.31%|Complete13205-node segmented stream, full source costs|\n| Matched Mathlib |8.95%|Complete1330-node matched segmented stream|\n"
 text+=f"| SubexponentialSAT |{out['full_cpu_ratio']:.2%}|Complete14721-node stream, full source costs|\n"
 text+="| Ramsey20sample |35.91%|Module-local190-built-prefix sample, trusted imports; not a whole stream|\n| RamseyK10 |20.66%|Supplemental single module, not a closure|\n\n"
 text+="The25-source pilot is included once. Superseded total-cost12h interpretation is retained; user clarified future new work only. See subexponential-risk-review.md for post-run evaluation of the9eea8be static risks; absence of kernel markers is not a semantic cost label.\n"
 (D/"subexponential-complete-result.md").write_text(text);print(json.dumps(out,indent=2))
if __name__=="__main__":main()
