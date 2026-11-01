"""Publish a completed, qualified-version matrix without rewriting historical v4."""
import csv,json,statistics
from pathlib import Path
from analyze import main as summarize
REPO=Path('/workspaces/repository')
M=REPO/'research/parallel-stream-check'
def publish(raw):
 out=raw/'analysis';out.mkdir(exist_ok=True)
 summarize(raw,out)
 rows=list(csv.DictReader((out/'math-cells.csv').open()))
 summary=list(csv.DictReader((out/'math-summary.csv').open()))
 for filename in ['math-cells.csv','math-summary.csv','math-completeness.json']:
  (M/('v14-'+filename)).write_bytes((out/filename).read_bytes())
 native=json.loads((raw/'matrix-results.json').read_text())
 complete=(raw/'matrix-complete.json').exists() and len(rows)==18 and all(
  r['returncode']==0 and r['native_retired'] and r.get('cgroup_retired',False)
  and len(r['accepted'])==1330 for r in native)
 controls=json.loads((raw/'controls-qualified.json').read_text())
 cert=json.loads((raw/'certificate-controls-qualified.json').read_text())
 reference=next(s for s in summary if s['variant']=='reference')
 base=float(reference['wall_s_median']);basecpu=float(reference['cpu_s_median'])
 lines=['# Repaired single-process Mathlib stream',
  '',f'Raw: {raw}. Frozen source 8c62fc3; all values in seconds.',
  f'Complete matrix: {complete}. Native control cases: {controls["cases"]}; actual certificate qualification: {cert["qualified"]}.',
  '', '| Method | Repeats | Wall median [min,max] | CPU median | Peak RSS MiB median | Reference / wall |',
  '|---|---:|---:|---:|---:|---:|']
 for s in summary:
  wall=float(s['wall_s_median']);cpu=float(s['cpu_s_median'])
  lines.append(f'| {s["variant"]} | {s["completed_repeats"]} | {wall:.3f} [{float(s["wall_s_min"]):.3f},{float(s["wall_s_max"]):.3f}] | {cpu:.3f} | {float(s["peak_rss_kib_median"])/1024:.1f} | {base/wall:.3f} |')
 lines+=['','## Paired repetitions','',
  '| Method | Same-repeat reference / wall, all three | Median CPU / reference CPU |',
  '|---|---|---:|']
 for s in summary:
  matches=[r for r in rows if r['variant']==s['variant']]
  ratios=[]
  for row in matches:
   ref=next(r for r in rows if r['repeat']==row['repeat']and r['variant']=='reference')
   ratios.append(float(ref['wall_s'])/float(row['wall_s']))
  lines.append(f'| {s["variant"]} | {", ".join(f"{x:.3f}" for x in ratios)} | {float(s["cpu_s_median"])/basecpu:.3f} |')
 lines+=['','All configurations traverse the same exact artifact path and 1,330 module IDs.',
  'The matrix checks IDs against the reference; unsafe/partial counts follow upstream replay.',
  'Declaration jobs and waves, local fallback counts and per-cell exits are in v14-math-cells.csv.',
  'Native bad-proof, sibling-context, duplicate-cycle and token corruption controls are separate qualifications.',
  '',
  'The ordered 18-cell matrix repeats reference/audited/1/2/4/8 three times in the same order.',
  'It is not randomized or an isolated production-service benchmark. No Lean -M or perf overhead.',
  'Only the bounded finite mathematical artifact cohort is measured. A requested worker count does',
  'not mean all workers are busy throughout serial fallback modules or narrow frontiers.',
  'The optional Fin proof rewrite is inactive in this mathematical cohort.',
  '',
  'Historical v4 tables remain unchanged and are not pooled with this repaired version.']
 (M/'v14-math-results.md').write_text('\n'.join(lines)+'\n')
 source=list(csv.DictReader((REPO/'research/decoupled-check/cohort-costs.csv').open()))
 math=next(x for x in source if x['cohort']=='math')
 steps=[dict(cohort='math1330',operation='source_construction_serial_sum',workers='stock compiler',wall_s=float(math['source_compiler_work_s']),scope='sum_of_per_module_invocations_not_parallel_Lake_wall',capture='O-construction',complete=True)]
 for s in summary:
  steps.append(dict(cohort='math1330',operation=s['variant'],workers=s['variant'].removeprefix('parallel')if s['variant'].startswith('parallel')else 1,wall_s=float(s['wall_s_median']),scope='complete_single_process_artifact_closure',capture=raw.name,complete=complete))
 with(M/'v14-cost-staircase.csv').open('w')as f:
  writer=csv.DictWriter(f,fieldnames=steps[0].keys(),lineterminator='\n');writer.writeheader();writer.writerows(steps)
 print('published complete=',complete)
if __name__=='__main__':
 import sys
 publish(Path(sys.argv[1]))
