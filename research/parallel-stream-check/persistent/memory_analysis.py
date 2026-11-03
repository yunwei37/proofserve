"""Memory diagnostics only; never use these clocks as primary plain replicates."""
import sys,json,csv
from pathlib import Path
def write(p,rows):
 if not rows:return
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with p.open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=keys,lineterminator='\n');w.writeheader();w.writerows(rows)
def smaps(s):
 out={}
 for line in s.splitlines():
  if ':'not in line:continue
  k,v=line.split(':',1);parts=v.split()
  if len(parts)==2 and parts[1]=='kB':out[k]=int(parts[0])*1024
 return out
def collect(root,mode):
 key=f'full-plain-m{mode}-P8-memory-r1'
 p=root/(key+'-terminal.json')
 if not p.exists():return []
 t=json.loads(p.read_text())
 if t['state']!='complete':raise ValueError('incomplete memory control')
 rows=[];checks=units=frontiers=modules=0;last=None
 for s in(root/'runs'/key/'stdout').open():
  if not s.startswith('{'):continue
  x=json.loads(s)
  if x.get('event')=='profile_module':
   checks+=x['metrics']['checks'];units+=x['metrics']['raw_HB'];frontiers+=x['persistence']['calls']
  elif x.get('event')=='accept':modules+=1;last=x['module']
  elif x.get('event')=='memory_checkpoint':
   assert x['modules']==modules
   row=dict(persistent=bool(mode),modules=modules,last_module=last,
    input_entries=x['input_entries'],checked_declarations=checks,
    allocation_units=units,marked_or_off_frontiers=frontiers)
   row.update({k+'_bytes':v for k,v in smaps(x['smaps_rollup']).items()})
   rows.append(row)
 assert len(rows)==4449 and rows[-1]['modules']==4449,'step1 and exact endpoint required'
 return rows
def main():
 root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
 a,b=collect(root,0),collect(root,1)
 if not(a and b):print('memory pair not returned');return
 assert len(a)==len(b)
 delta=[]
 for x,y in zip(a,b):
  for key in ['modules','last_module','input_entries','checked_declarations','allocation_units','marked_or_off_frontiers']:
   assert x[key]==y[key],(key,x[key],y[key])
  row={k:x[k]for k in ['modules','last_module','input_entries','checked_declarations','allocation_units','marked_or_off_frontiers']}
  for k in ['Rss_bytes','Pss_bytes','Anonymous_bytes','Private_Dirty_bytes','Private_Clean_bytes']:
   if k in x and k in y:row.update({k+'_off':x[k],k+'_on':y[k],k+'_delta':y[k]-x[k]})
  delta.append(row)
 write(out/'memory-checkpoints.csv',a+b);write(out/'memory-deltas.csv',delta)
 print(json.dumps(dict(matched_module_boundaries=len(delta),final=delta[-1],
  interpretation='resident mappings/anonymous data, not exact retained-object sizes')))
if __name__=='__main__':main()
