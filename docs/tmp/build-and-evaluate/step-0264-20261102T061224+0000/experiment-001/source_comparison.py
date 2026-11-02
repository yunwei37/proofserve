from pathlib import Path
import os,tarfile,json,time,csv
os.sched_setaffinity(0,{22,23});s=Path(Path('/workspaces/.agent-state/gpu-smt-falconer-root-step.txt').read_text().strip());e=s/'experiment-001'
b=Path('/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/scale-study/falconer-project-20261101')
frame=[v for v in json.loads((b/'build-frame.json').read_text())if v['module'].startswith('OAI.')]
wanted={'/'.join(v['module'].split('.'))+'.lean':v for v in frame}
archive=Path('/workspaces/.agent-state/gpu-smt-captures/step-0231-20261101T001556+0000-static/source.tar.gz')
start=time.monotonic();rows=[];done=set()
with tarfile.open(archive,'r|gz')as tf:
 for m in tf:
  if not m.isfile()or '/lean/'not in m.name:continue
  rel=m.name.split('/lean/',1)[1]
  if rel not in wanted:continue
  v=wanted[rel];data=tf.extractfile(m).read();assert data==Path(v['source']).read_bytes()
  assert rel not in done;done.add(rel);rows.append(dict(module=v['module'],archive_member=m.name,bytes=len(data),comparison='byte_equal'))
assert len(done)==len(wanted)==2461,(len(done),len(wanted))
with(e/'falconer-source-byte-comparison.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
j=dict(archive=str(archive),archive_bytes=archive.stat().st_size,selected_sources_compared=len(rows),selected_source_bytes=sum(v['bytes']for v in rows),all_byte_equal=True,elapsed_s=time.monotonic()-start,scope='selected Falconer source qualification only; no new whole-library lexical census or download')
(e/'falconer-source-byte-comparison.json').write_text(json.dumps(j,indent=2)+'\n')
(e/'fourth-sparse-source-lookup.txt').write_text('The familiar workload source directory is a partial extraction, as established earlier. Missing selected Falconer files there were a root lookup error, not source absence. Qualified all2461 selected sources against the existing fixed full archive instead; no download, full lexical census, foreign mutation or native Lean rerun.\n')
print('SOURCE_BYTES',json.dumps(j))
