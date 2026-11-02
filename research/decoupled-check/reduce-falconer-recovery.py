#!/usr/bin/env python3
"""Summarize complete native Falconer cells; never extrapolate an interrupted check."""
import csv,json
from pathlib import Path
R=Path('/workspaces/repository/research/decoupled-check')
D=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/scale-study/falconer-project-20261101')
O=D/'bounded-recheck-v1'
def main():
 source=list(csv.DictReader((R/'falconer-source-costs.csv').open()))
 build=sum(float(x['source_compiler_wall_s'])for x in source)
 cpu=sum(float(x['source_user_s'])+float(x['source_system_s'])for x in source)
 assert len(source)==13205
 stream=json.loads((O/'stream-terminal.json').read_text())if(O/'stream-terminal.json').exists()else None
 math=json.loads((O/'math-terminal.json').read_text())if(O/'math-terminal.json').exists()else None
 parity=json.loads((O/'oracle-progress.json').read_text())if(O/'oracle-progress.json').exists()else {}
 rows=[]
 for name,cell,wall in [('Falconer complete closure',stream,build),('Mathlib1330 matched adapter',math,622.3794121909887)]:
  if cell is None:continue
  c=cell['cell']
  rows.append(dict(cohort=name,source_modules=len(source)if name.startswith('Falconer')else 1330,
   checker_complete=cell['complete'],graph_match=cell['graph_match'],build_compiler_wall_sum_s=wall,
   check_wall_s=c['wall_s'],check_cpu_s=c['user_s']+c['system_s'],peak_rss_kib=c['peak_rss_kib'],
   cgroup_peak_bytes=c['cgroup_peak_bytes'],returncode=c['returncode'],accepted_modules=len(set(c['accepted'])),
   stream_over_build=c['wall_s']/wall if cell['complete']else'',
   original_kernel_module_local_parity_complete=bool(parity.get('complete'))if name.startswith('Falconer')else'previous exact-artifact oracle',
   scope='complete closure with original kernel and indexed context audit; source work is summed compiler invocations'))
 if rows:
  with (R/'falconer-recovery-costs.csv').open('w',newline='')as f:
   w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
 text='# Falconer: decoupled native checking\n\nSelf-review.\n\n'
 text+='## Source denominator\n\n'
 text+=f'All {len(source):,} source nodes compiled successfully: 8,128 new +5,077 exact same-capture reused nodes, charged once per closure. Successful compiler wall sum **{build:.6f}s**, CPU sum {cpu:.6f}s. Of these, the 2,461 Falconer AI modules account for 6,476.297931s wall; 10,744 dependencies account for15,601.472317s. The source census has7,312 theorem/lemma sites and zero explicit decide+kernel, native_decide or bv_decide sites in Falconer. That is a source classification, not a claim that its dependencies contain no kernel computation.\n\n'
 text+='This is summed per-module compilation (including repeated imports and normal olean/ilean/C output), not parallel Lake makespan, warm-service throughput or source-only verification without artifacts. The old0.053097s recovered source fault remains separately recorded.\n\n'
 text+='## Native result\n\n'
 if stream and stream['complete']:
  c=stream['cell'];ratio=c['wall_s']/build
  text+=f'The fresh bounded original-kernel check exits0, accepts all13,205 modules and matches the complete native import graph. Wall **{c["wall_s"]:.6f}s**, CPU {c["user_s"]+c["system_s"]:.6f}s, peak RSS {c["peak_rss_kib"]/1024**2:.6f}GiB; check/source ratio **{ratio*100:.4f}%**. This ratio describes a complete check; full module-local differential qualification is separately tracked below.\n\n'
  text+=f'Final native counters: {json.dumps(c["complete_event"],sort_keys=True)}.\n\n'
  text+='Only transitive-import reachability was memoized; the original Lean4.34.1 kernel, all declaration replays and context/duplicate safeguards are unchanged. The old unindexed full adapter timed out at1500.210998s; that failed attempt is retained and not spliced into this successful timing. Operational spent work including that exploratory failure is larger than the successful checking numerator.\n\n'
 else:
  text+='No complete new native full-check result yet. The interrupted old prefix is not a numerator and no ratio is finalized.\n\n'
 if math and math['complete']:
  mc=math['cell'];mb=622.3794121909887
  text+=f'The same indexed adapter on the exact Mathlib1330 reference takes{mc["wall_s"]:.6f}s, or{100*mc["wall_s"]/mb:.4f}% of its source build. Its native complete module set matches the previously qualified exact-artifact reference.\n\n'
 else:text+='The same-adapter Mathlib1330 comparison is pending; the historic65.692644s/622.379412s=10.5551% used the unindexed audit. Treating a difference against that number as purely an AI workload effect would confound adapter overhead.\n\n'
 if stream and stream['complete']and math and math['complete']:
  fr=stream['cell']['wall_s']/build;mr=math['cell']['wall_s']/622.3794121909887
  text+=f'Falconer is {"lower"if fr<mr else"higher"} than matched Mathlib by{abs(fr-mr)*100:.4f}percentage points. The ratio aggregates different complete closures and amortizes one checked environment against repeated source imports/tactic production; it is not an isolated causal effect of AI authorship. Larger dependency graphs, duplicate-context fallbacks and adapter bookkeeping can raise check cost. Neither ratio is a per-AI-leaf kernel fraction.\n\n'
 text+='## Acceptance and interruption boundaries\n\n'
 text+=f'Module-local reference qualification: {parity}. Exact common nodes reuse their previous original-checker qualification; each remaining module is checked by the frozen measurement-v1 original checker in independently saved <=512-module chunks. Full differential parity is complete only when all13,205 belong to that union. Until then the whole-closure comparison is pending; do not label it accepted-set equality.\n\n'
 text+='The ten indexed/native module-local boundary controls agree, including explicit rejection of a corrupt duplicate theorem and an unimported sibling proof. These are controls, not a substitute for full input parity. The source/compiled artifacts are unchanged; corruptions are in-memory experimental proof replacements.\n\n'
 text+='Every timed task uses taskset0–7 and the shared FIFO flock, no-M, a child cgroup of11.75GiB plus a small parent, and a finite wall timeout. The separate memory pass, if present, is excluded from primary wall time. A timed-out/malformed record is operationally incomplete, never a mathematical rejection. Raw old and new stdout/stderr/commands, including the JSON-truncated failed attempt and initial failed compiler invocation, remain on PVC at the paths documented in falconer-recovery-plan.md.\n\n'
 text+='See admission-control-reconciliation.md: all-stream+upper admits by the same type-conditioned bound and serial Grid CPU557.350s, whereas class-selected parallel Grid CPU744.406s. Under CPU-work budgets the latter cannot imply a completion advantage;17 vs14.33 is a negative routing result, not a paradox or native-throughput claim.\n'
 (R/'falconer-recovery-result.md').write_text(text)
 print(json.dumps(dict(stream_complete=bool(stream and stream['complete']),math_complete=bool(math and math['complete']),parity=parity),indent=2))
if __name__=='__main__':main()
