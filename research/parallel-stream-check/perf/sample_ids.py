"""Audit inherited sample event IDs without resolving full stacks."""
import csv,collections,os
from pathlib import Path
counts=collections.Counter();periods=collections.Counter()
def process_event(p):
 s=p['sample'];k=(s['pid'],s['tid'],p['ev_name'],s['id'])
 counts[k]+=1;periods[k]+=s.get('period',0)
def trace_end():
 with Path(os.environ['PERF_SAMPLE_IDS_OUT']).open('w',newline='') as f:
  w=csv.writer(f,lineterminator=chr(10));w.writerow(['PID','TID','event','id','samples','period_sum'])
  for k,v in sorted(counts.items()):w.writerow([*k,v,periods[k]])
