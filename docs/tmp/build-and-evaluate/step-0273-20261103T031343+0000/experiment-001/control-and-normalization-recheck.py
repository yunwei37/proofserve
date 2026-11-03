from pathlib import Path
import json,statistics,collections
b=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-attribution-20261102-v2');s=Path(Path('/workspaces/.agent-state/gpu-smt-attribution-root-step.txt').read_text().strip());e=s/'experiment-001';out={}
for k in ['attribution-control','attribution-two-core-control','attribution-bad-control']:
 v=json.loads((b/'runs'/k/'result.json').read_text());ev=dict(x.split()for x in v['memory_events'].splitlines());assert not v['stop_reasons']and int(ev['oom'])==int(ev['oom_kill'])==0 and v['wait4_usage_complete']
 assert v['cgroup_charged_memory_max_gib']==14 and not any(x.startswith('-M')for x in v['argv'])
 out[k]=v['returncode']
cores=collections.Counter()
for l in(b/'runs/attribution-two-core-control/stdout').open():
 j=json.loads(l)
 if j['event']=='profile_module':
  for w in j['metrics']['workers']:cores[w['cpu']]+=w['checks']
assert set(cores)=={0,1}and all(cores.values())
groups={};cur=None
for l in(b/'runs/hardware-leaf/stdout').open():
 j=json.loads(l)
 if j['event']=='curve_begin':cur=(j['kind'],j['repeat']);groups[cur]=[]
 elif j['event']=='unit_check':groups[cur].append(j)
solos={kind:{t:statistics.median(int(x['cpu_ns'])for(k,rep),rs in groups.items()if k==kind for x in rs if x['target']==t)for t in {x['target']for x in next(iter(groups.values()))}}for kind in ['p1','e1']}
ratios={'P':[],'E':[]}
for(k,rep),rs in groups.items():
 if k=='mixed24':
  for x in rs:
   typ='P'if x['cpu']<8 else'E';ratios[typ].append(int(x['cpu_ns'])/solos['p1'if typ=='P'else'e1'][x['target']])
assert all(min(v)>1 for v in ratios.values())
j=dict(control_rcs=out,actual_two_core_checks=dict(cores),same_type_ratios={k:dict(count=len(v),minimum=min(v),median=statistics.median(v),maximum=max(v))for k,v in ratios.items()})
(e/'control-and-normalization-recheck.json').write_text(json.dumps(j,indent=2)+'\n')
p=s/'outer-audit.md';p.write_text(p.read_text().replace('Biological/hardwarecausality','Hardwarecausality'))
print(json.dumps(j))
