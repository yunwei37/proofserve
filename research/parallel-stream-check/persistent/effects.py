"""Offline primary-matrix effects; no native launch and no input mutation."""
import json,csv,sys,statistics
from pathlib import Path
from decimal import Decimal
def emit(path,rows):
 if not rows:return
 fields=list(dict.fromkeys(k for r in rows for k in r))
 with path.open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
def terminal(root,arm,mode,n,rep):
 p=root/f'full-{arm}-m{mode}-P{n}-r{rep}-terminal.json'
 if not p.exists():return None
 t=json.loads(p.read_text())
 return t['cell']if t.get('state')=='complete'else None
def measures(c):
 return dict(wall_s=c['wall_s'],CPU_s=c['user_s']+c['system_s'],
  observer_CPU_s=c['kernel_CPU_ns']/1e9,
  sampled_peak_GiB=c['sampled_tree_peak_bytes']/1024**3)
def statcounts(path):
 out={}
 for s in path.read_text().splitlines():
  if not s.strip():continue
  x=json.loads(s);name=x['event'].split('/')[1]
  try:value=Decimal(x['counter-value'])
  except Exception:raise ValueError('counter unavailable: '+str(x))
  if Decimal(str(x['pcnt-running']))<99.9:raise ValueError('counter multiplexed: '+str(x))
  out[name]=value
 return out
def main():
 root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
 interaction=[];effects=[];pmu=[];pmueffects=[];overhead=[]
 for rep in [1,2,3]:
  cc={(m,n):terminal(root,'plain',m,n,rep)for m in [0,1]for n in [1,2,4,8]}
  for n in [1,2,4,8]:
   if not(cc[0,n]and cc[1,n]):continue
   a,b=measures(cc[0,n]),measures(cc[1,n])
   for k in a:effects.append(dict(repetition=rep,workers=n,metric=k,off=a[k],on=b[k],
    on_over_off=b[k]/a[k],delta=b[k]-a[k],scope='same-repetition plain pair'))
  if all(cc[m,n]for m in [0,1]for n in [4,8]):
   v={mn:measures(c)for mn,c in cc.items()if c}
   for k in ['wall_s','CPU_s','observer_CPU_s']:
    off=v[0,8][k]-v[0,4][k];on=v[1,8][k]-v[1,4][k]
    interaction.append(dict(repetition=rep,metric=k,off_8_minus_4=off,on_8_minus_4=on,
     interaction=on-off,reduction_of_off_growth=(off-on)/off if off>0 else '',
     interpretation='factorial difference; not an exact atomic-RC stall fraction'))
 counters={}
 for n in [1,2,4,8]:
  for mode in [0,1]:
   c=terminal(root,'stat',mode,n,1)
   if not c:continue
   path=root/f'full-stat-m{mode}-P{n}-r1-stat.json'
   v=statcounts(path);counters[mode,n]=v
   row=dict(workers=n,persistent=bool(mode),repetitions=1,
    IPC=float(v['instructions']/v['cpu-cycles']),scope='whole-command user-mode; not gated kernel interval')
   row.update({k:str(x)for k,x in v.items()});pmu.append(row)
   plain=[measures(x)for rep in [1,2,3]if(x:=terminal(root,'plain',mode,n,rep))]
   if plain:
    for k,val in measures(c).items():
     base=statistics.median(x[k]for x in plain)
     overhead.append(dict(workers=n,persistent=bool(mode),metric=k,stat=val,
      plain_median=base,plain_repetitions=len(plain),relative_change=val/base-1,
      caveat='one stat vs plain median; order and run variance remain, not a precise observer-only estimate'))
  if all((mode,n)in counters for mode in [0,1]):
   a,b=counters[0,n],counters[1,n]
   for k in a:
    pmueffects.append(dict(workers=n,event=k,off=str(a[k]),on=str(b[k]),relative_change=float(b[k]/a[k]-1),
     repetitions_per_arm=1,scope='whole-command user-mode; raw event semantics retained'))
 emit(out/'paired-effects.csv',effects);emit(out/'paired-interaction.csv',interaction)
 emit(out/'stat-summary.csv',pmu);emit(out/'stat-effects.csv',pmueffects)
 emit(out/'stat-vs-plain.csv',overhead)
 print(json.dumps(dict(paired_observations=len(effects),interaction_observations=len(interaction),
  stat_cells=len(pmu))))
if __name__=='__main__':main()
