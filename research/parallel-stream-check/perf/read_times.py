"""Retain actual perf READ enabled/running fields before raw record cleanup."""
import csv,json,re,subprocess,sys
from pathlib import Path
data=Path(sys.argv[1]);out=Path(sys.argv[2])
assert data.exists() and out.is_dir()
cmd=['perf','report','-D','--stdio','--stats','-i',str(data)]
rows=[];cur=None;lines=0
rx=re.compile(r'PERF_RECORD_READ:\s+(\d+)\s+(\d+)\s+(.+?)\s+(\d+)\s*$')
z=subprocess.Popen(cmd,stdout=subprocess.PIPE,text=True,errors='replace')
for line in z.stdout:
 lines+=1;m=rx.search(line)
 if m:
  if cur:rows.append(cur)
  cur=dict(PID=int(m[1]),TID=int(m[2]),event=m[3],value=int(m[4]))
 elif cur:
  m=re.match(r'\.\.\.\s+(time enabled|time running|id|lost)\s*:\s*(\d+)',line)
  if m:cur[m[1].replace(' ','_')]=int(m[2])
if cur:rows.append(cur)
rc=z.wait()
keys=['PID','TID','event','value','time_enabled','time_running','id','lost']
with (out/'read-times.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=keys,lineterminator=chr(10));w.writeheader();w.writerows(rows)
(out/'read-times-terminal.json').write_text(json.dumps(dict(returncode=rc,records=len(rows),scanned_lines=lines,
 missing_time_fields=sum('time_enabled'not in r or'time_running'not in r for r in rows),command=cmd),indent=2))
if rc or not rows:raise SystemExit('no successful native READ dump; preserve')
print('READ_FIELDS_COMPLETE',len(rows),flush=True)
