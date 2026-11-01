"""Offline source nominations among measured >=1s helpers, not certified coverage."""
from pathlib import Path
import csv,json,re,argparse
HERE=Path(__file__).resolve().parent
def analyze(source):
 rows=list(csv.DictReader((HERE/'declaration-distribution.csv').open()))
 inputs={v['module']:v for v in json.loads((HERE/'distribution-inputs.json').read_text())}
 def weight(module):
  p=inputs[module]['inclusion_probability'];return 1/float(p) if p else 0.0
 large=[]
 for row in rows:
  if not int(row['large_decision_count_ge1s_cpu']):continue
  for line in (Path(row['raw'])/'stdout').open():
   if not line.startswith('{'):continue
   e=json.loads(line)
   if e.get('event')!='kernel_declaration' or not e['decide_helper'] or int(e['thread_cpu_ns'])<1e9:continue
   name=';'.join(e['names']);match=re.search(r'(envelopeExpB\d+_calc)\.',name)
   hit=None
   if match and 'forall (j : Fin (' in e['goal']:
    hit=re.search(r'lemma '+re.escape(match[1])+r' \(j : Fin (\d+)\) : ([^\n]+?) := by\s+revert j\s+decide \+kernel',source)
   large.append(dict(module=row['module'],name=name,cpu_s=int(e['thread_cpu_ns'])/1e9,wall_s=int(e['wall_ns'])/1e9,
    source_supported_Fin_schema=hit is not None,source_Fin_bound=int(hit[1]) if hit else None,
    native_goal_prefix=e['goal'][:180],classification='source nomination only; largest EnvelopeB16 schema compiled; other candidate curves unrun'))
 with (HERE/'large-goal-source-nominations.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(large[0]),lineterminator='\n');w.writeheader();w.writerows(large)
 nom=sum(x['cpu_s'] for x in large if x['source_supported_Fin_schema']);total=sum(x['cpu_s'] for x in large)
 w_nom=sum(x['cpu_s']*weight(x['module']) for x in large if x['source_supported_Fin_schema'])
 w_total=sum(x['cpu_s']*weight(x['module']) for x in large)
 denom=sum(float(x['all_kernel_call_cpu_s'])*weight(x['module']) for x in rows)
 remainder=[x for x in rows if not x['module'].endswith('.EnvelopePsiB')]
 rden=sum(float(x['all_kernel_call_cpu_s'])*weight(x['module']) for x in remainder)
 rlarge=sum(float(x['large_decision_cpu_s'])*weight(x['module']) for x in remainder)
 j=dict(large_goals=len(large),source_nominated_goals=sum(x['source_supported_Fin_schema'] for x in large),
  nominated_checker_cpu_s=nom,all_large_checker_cpu_s=total,unweighted_share_of_large_goal_cpu=nom/total,
  available_case_weighted_nomination_share_of_large_goal_cpu=w_nom/w_total,
  available_case_weighted_nomination_share_of_all_checker_cpu=w_nom/denom,
  scope='31 retained panel; weighted original29only;13original draws absent; source nomination not measured chunk acceptance or speedup',
  actual_compiled_schema_control='EnvelopeB16 schema qualified; other9source-only; actual runtime evidence separate in envelope-validation.json',
  weight_sensitivity=dict(envelope_module_inverse_probability=weight('OAI.Analysis.Triangular.Envelope.EnvelopePsiB'),
   weighted_large_share_with_envelope=w_total/denom,
   weighted_large_share_after_omitting_envelope=rlarge/rden,
   scope='leave-one-module-out sensitivity of available-case statistic only; not an experiment or bound; one high-leverage sample'))
 (HERE/'large-goal-nomination-summary.json').write_text(json.dumps(j,indent=2)+'\n')
 return j
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);args=ap.parse_args()
 print(json.dumps(analyze(args.source.read_text())))
