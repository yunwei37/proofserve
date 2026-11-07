"""Reduce the fixed sample; keep every requested module and unresolved cost."""
from pathlib import Path
import json,csv,gzip,sys,collections,statistics,datetime
root=Path(sys.argv[1]);repo=Path(sys.argv[2]);out=repo/'data/generation-vs-checking'
raw=Path((root/'measurement-current.txt').read_text().strip())
terminal=json.loads((raw/'sample-terminal.json').read_text())
assert terminal['cgroup_retired']
scope=json.loads((raw/'sampler-scope.json').read_text());assert not Path(scope['cgroup']).exists()
controller=json.loads((raw/'measure-controller.json').read_text());p=Path('/proc',str(controller['pid']),'stat')
assert not p.exists()or p.read_text().rsplit(')',1)[1].split()[19]!=controller['birth']or p.read_text().rsplit(')',1)[1].split()[0]=='Z'
plan=json.loads((raw/'sample-plan.json').read_text());selected={r['module']:r for r in plan['modules']}
observed=[json.loads(l)for l in(raw/'sample-results.jsonl').read_text().splitlines()]
assert len({r['module']for r in observed})==len(observed)
by_module={r['module']:r for r in observed};assert set(by_module)<=set(selected)
tokens={r['module']:r for r in csv.DictReader(gzip.open(out/'tokens.csv.gz','rt'))}
assert len(tokens)==163096 and set(selected)<=set(tokens)
pairing={r['module']:r for r in json.loads((root/'source-pairing.json').read_text())}
prestop={}
obsfile=raw/'pre-stop-cpu-observations.jsonl'
if obsfile.exists():
 for line in obsfile.read_text().splitlines():
  j=json.loads(line);prestop[j['module']]=max(prestop.get(j['module'],0),j['cpu_s'])
rows=[]
for m,r in sorted(selected.items()):
 t=tokens[m];v=by_module.get(m,{})
 row=dict(module=m,source_unit=r['source_unit'],sample_groups=';'.join(r['sample_groups']),source_bytes=int(t['bytes']),tokens=int(t['tokens']),
  has_decide_plus_kernel=int(int(r['decide_plus_kernel_occurrences']or'0')>0),decide_plus_kernel_occurrences=int(r['decide_plus_kernel_occurrences']or'0'),
  compile_cpu_s=float(r['cpu_s']),compile_wall_s=float(r['wall_s']),compile_pool=r['pool'],compile_source_bytes=int(r['source_bytes']),
  same_source_byte_count=int(t['bytes'])==int(r['source_bytes']),source_matches_compile_record=pairing[m]['source_matches_compile_record'],status=v.get('status','not_started_time_budget'),
  right_censored=v.get('right_censored',False),core=v.get('core',''),
  import_wall_s=v.get('import_wall_s',''),import_cpu_s=v.get('import_cpu_s',''),
  check_wall_s=v.get('check_wall_s',''),check_cpu_s=v.get('check_cpu_s',''),
  target_read_wall_s=v.get('target_read_wall_s',''),target_read_cpu_s=v.get('target_read_cpu_s',''),
  target_map_wall_s=v.get('target_map_wall_s',''),target_map_cpu_s=v.get('target_map_cpu_s',''),
  replay_wall_s=v.get('replay_wall_s',''),replay_cpu_s=v.get('replay_cpu_s',''),
  check_wall_observed_lower_s=v.get('check_wall_observed_lower_s',0),check_cpu_observed_lower_s=v.get('check_cpu_observed_lower_s',0),
  process_wall_s=v.get('process_wall_s',''),process_cpu_s=v.get('process_cpu_s',''),
  peak_rss_kib=v.get('peak_rss_kib',''),charged_memory_peak_bytes=v.get('charged_memory_peak_bytes',''),
  eligible_entries=v.get('eligible_entries',''),stop_reason=v.get('stop_reason')or'',raw=v.get('raw',''))
 # Use only live snapshots before timeout, excluding kill/cleanup CPU.
 if row['right_censored']and v.get('check_started')and m in prestop:
  baseline=v['process_cpu_s']-v.get('check_cpu_observed_lower_s',0)
  lower=max(0,prestop[m]-baseline)
 else:lower=0
 row['check_cpu_observed_lower_s']=lower+float(row['target_read_cpu_s']or 0)+float(row['target_map_cpu_s']or 0)
 row['check_wall_observed_lower_s']=lower+float(row['target_read_wall_s']or 0)+float(row['target_map_wall_s']or 0)
 if row['status']=='accepted':
  row['check_cpu_observed_lower_s']=row['check_cpu_s'];row['check_wall_observed_lower_s']=row['check_wall_s']
  assert row['check_wall_s']>=0 and row['check_cpu_s']>=0
  row['check_plus_import_wall_s']=row['check_wall_s']+row['import_wall_s']
  row['check_plus_import_cpu_s']=row['check_cpu_s']+row['import_cpu_s']
 else:
  row['check_plus_import_wall_s']='';row['check_plus_import_cpu_s']=''
 row['check_plus_import_wall_observed_lower_s']=float(row['import_wall_s']or 0)+row['check_wall_observed_lower_s']
 row['check_plus_import_cpu_observed_lower_s']=float(row['import_cpu_s']or 0)+row['check_cpu_observed_lower_s']
 rows.append(row)
with(out/'sample.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
rates=[100,1000,10000]
def compare(rs,metric,rate):
 positive=negative=unknown=0;ok=pos_ok=0
 lower_key=metric.removesuffix('_s')+'_observed_lower_s'
 for r in rs:
  threshold=r['tokens']/rate
  if r['status']=='accepted':
   ok+=1
   if r[metric]>threshold:positive+=1;pos_ok+=1
   else:negative+=1
  elif r.get(lower_key,0)>threshold:positive+=1
  else:unknown+=1
 return dict(definitely_exceeds=positive,definitely_not_exceeds=negative,unresolved=unknown,denominator=len(rs),
  fraction_lower=positive/len(rs),fraction_upper=(positive+unknown)/len(rs),
  completed_only_exceeds=pos_ok,completed_only_n=ok,completed_only_fraction=pos_ok/ok if ok else None)
def summarize(rs):
 ok=[r for r in rs if r['status']=='accepted'];nt=sum(r['tokens']for r in rs);accepted_tokens=sum(r['tokens']for r in ok)
 cc=sum(r['check_cpu_s']for r in ok);ic=sum(r['import_cpu_s']for r in ok)
 observed_lower=cc+sum(r['check_cpu_observed_lower_s']for r in rs if r['status']!='accepted')
 return dict(n=len(rs),statuses=dict(collections.Counter(r['status']for r in rs)),source_tokens=nt,
  comparisons={str(rate):{metric:compare(rs,metric,rate)for metric in ['check_wall_s','check_cpu_s','check_plus_import_wall_s','check_plus_import_cpu_s','replay_wall_s','replay_cpu_s']}for rate in rates},
  throughput=dict(completed_modules=len(ok),completed_source_tokens=accepted_tokens,completed_check_cpu_s=cc,completed_import_cpu_s=ic,
   completed_pure_replay_cpu_s=sum(r['replay_cpu_s']for r in ok),completed_tokens_per_pure_replay_cpu_s=accepted_tokens/sum(r['replay_cpu_s']for r in ok)if ok else None,
   completed_tokens_per_check_cpu_s=accepted_tokens/cc if cc else None,
   completed_tokens_per_import_plus_check_cpu_s=accepted_tokens/(cc+ic)if cc+ic else None,
   exact_all_sample_tokens_per_check_cpu_s=nt/cc if len(ok)==len(rs)and cc else None,
   all_sample_check_cpu_lower_s=observed_lower,
   all_sample_tokens_per_check_cpu_s_upper_bound=nt/observed_lower if observed_lower else None,
   all_sample_tokens_per_check_cpu_s_lower_bound=nt/cc if len(ok)==len(rs)and cc else 0))
cohorts={'combined':rows}
for name in ['uniform','top_cpu_1pct','decide_kernel']:
 cohorts[name]=[r for r in rows if name in r['sample_groups'].split(';')]
for mark in [0,1]:cohorts['has_decide_kernel_'+str(mark)]=[r for r in rows if r['has_decide_plus_kernel']==mark]
summary=dict(source=json.loads((root/'token-summary.json').read_text()),
 sampling={k:plan[k]for k in ['seed','eligible_completed','top_1pct_size','marked_pool','draws','unique_modules','campaign_started_utc','campaign_deadline_utc']},
 cohorts={k:summarize(rs)for k,rs in cohorts.items()if rs},
 terminal=terminal,memory=scope,
 source_byte_mismatches=[r['module']for r in rows if not r['same_source_byte_count']],
 source_digest_mismatches=[r['module']for r in rows if not r['source_matches_compile_record']],
 rate_interpretation='hypothetical full-file source emission rates; not measured LLM generation, prompts, reasoning, edits or pass@k',
 cost_interpretation='own-module read plus map plus original-kernel replay component, pure replay separately; imported dependencies trusted; separate import window; no project recompile',
 sample_interpretation='tail and decide are oversampled; combined fractions are not population estimates; uniform draws from completed-build frame only',
 raw_root=str(root),native_raw=str(raw),reduced_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
summary['source'].update(zero_token_files=sum(int(r['tokens'])==0 for r in tokens.values()),median_ratio_files=sum(int(r['tokens'])>0 for r in tokens.values()))
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:summary['cohorts']['combined'][k]for k in ['n','statuses','throughput']},indent=2))
