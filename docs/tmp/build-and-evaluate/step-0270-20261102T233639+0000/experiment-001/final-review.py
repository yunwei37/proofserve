from pathlib import Path
import os,re,gzip,json,shutil,csv,subprocess
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-source35-root-step.txt').read_text().strip());e=s/'experiment-001';out=Path('/workspaces/.agent-state/gpu-smt-captures')/(s.name+'-paper')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
t=(r/'docs/paper/main.tex').read_text();old=gzip.decompress((e/'before-docs-paper-main.tex.gz').read_bytes()).decode()
for pat in [r'\\title\{.*?\}\n',r'\\begin\{abstract\}.*?\\end\{abstract\}',r'\\item\[RQ\d\].*?(?=\\item\[|\\end\{description\})',r'\\(?:sub)*section\{[^}]*\}',r'\\paragraph\{System-design implication\.\}.*?(?=\\section|\\subsection|\\paragraph|\Z)',r'\\begin\{tabular\}.*?\\end\{tabular\}']:
 assert re.findall(pat,t,re.S)==re.findall(pat,old,re.S),pat
assert t.count(r'\begin{tabular}')==20
rr=json.loads((e/'render-receipt.json').read_text());assert rr['pages']==24 and rr['PDF_bytes']==221094 and len(rr['contacts'])==6
links=0
for n in ['docs/research-status.md','docs/research-plan.md','docs/novelty-20261101.md','research/README.md',str((s/'step-report.md').relative_to(r)),str((s/'outer-audit.md').relative_to(r))]:
 p=r/n
 for x in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://'in x or x.startswith('#'):continue
  x=x.split('#',1)[0]
  if x:assert(p.parent/x).exists(),(n,x);links+=1
bib=(r/'docs/paper/references.bib').read_text();keys=set(re.findall(r'@\w+\{([^,]+),',bib));cites={k for x in re.findall(r'\\cite\{([^}]+)\}',t)for k in x.split(',')};assert cites<=keys
shutil.copy2(out/'main.pdf',r/'docs/paper/main.pdf')
imgs=[p for p in out.iterdir()if p.suffix in ['.jpg','.png']and p.name.startswith(('page','contact','preview-contact'))]
targets={str(p.resolve())for p in imgs}
for pr in Path('/proc').iterdir():
 if not pr.name.isdigit():continue
 try:
  for fd in(pr/'fd').iterdir():
   try:assert os.readlink(fd)not in targets
   except OSError:pass
 except OSError:pass
size=sum(p.stat().st_size for p in imgs)
with(e/'post-review-rendering-cleanup.csv').open('w',newline='')as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['path','bytes','reason'])
 for p in imgs:
  assert p.parent.resolve()==out.resolve();w.writerow([str(p),p.stat().st_size,'root0270 final rendering after all24page review']);p.unlink()
first=[]
for p in e.rglob('*'):
 if p.is_file()and p.suffix in['.stderr','.stdout','.log']:
  data=p.read_bytes();q=p.with_name(p.name+'.gz');q.write_bytes(gzip.compress(data));assert gzip.decompress(q.read_bytes())==data;p.unlink()
b=json.loads((e/'paper-build.json').read_text());du=shutil.disk_usage('/workspaces')
j=dict(pages=24,PDF_bytes=221094,contacts_viewed=6,all_old_tables_unchanged=20,title_abstract_RQs_sections_implications_unchanged=True,links=links,citation_keys=len(cites),labels={x:t.count('\\'+x+'{')for x in['measured','partialev','unproven']},final_renderings_removed=len(imgs),final_rendering_bytes_removed=size,initial_reviewed_renderings_removed=len(first),initial_rendering_bytes_removed=sum(int(x['bytes'])for x in first),PVC_free_bytes=du.free,PVC_used_percent=100*du.used/du.total,review='self-review',native_runs=0,agents=0)
(e/'final-self-review.json').write_text(json.dumps(j,indent=2)+'\n')
for n in ['step-report.md','outer-audit.md']:
 p=s/n;p.write_text(p.read_text()+f'''
## Actual completed final verification
Root reanalysis0.460621s/20496KiB. Final compiler rc0 in{b['elapsed_s']:.6f}s/
sample{b['own_tree_sample_peak_rss_bytes']}B/E22–23naturalretirement. Full raw/source/costs/entrybefore preserved.
Final24pages221094B/all6contacts statically viewed,no observed clipping/overlap.
All20table bodies/title/fullabstract/4RQ/sections/4designimplications identical
to root0268. No new table. Links{links}/citationkeys{len(cites)}pass;labels{j['labels']}.
Only{len(imgs)}final reviewed images/{size}B removed; per-file manifest
and FDchecks. AllPDF/log/raw/source/failed/partial/foreign objects remain.
CurrentPVCfree{du.free}B/{j['PVC_used_percent']:.3f}% used, not a repeated claim
of prior cleanup or a reason to delete other lines' runtime/snapshots.
Self-review only. Persist ownedmainpaths by ordinarypush; no stash/reset/force.
''')
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;ls=p.read_text().splitlines();p.write_text('\n'.join('Paper root0270:24pages/221094B,20oldtables/title/fullabstract/4RQ/sections/fourimplications unchanged;fullcompile/all-page self-review completed,0newrootnative/agent.'if z.startswith('Paper root0270:')else z for z in ls).rstrip()+'\n')
p=r/'docs/cleanup-20261101.md';drel=str(s.relative_to(r)).removeprefix('docs/')
p.write_text(p.read_text()+f'\n## Step0270 reviewed renderings only\nRemoved{len(imgs)}reviewed renderings/{size}B after24page/6contact self-review and FDcheck. [final manifest]({drel}/experiment-001/post-review-rendering-cleanup.csv). AllPDF/source/logs/raw/failed/partial/foreign data retained. Exact compiler logs byte-verified gzip. No native427/artifacts historical cache or tracked data deleted; PVCfree{du.free}B/{j["PVC_used_percent"]:.3f}% snapshot not prior cleanup attribution.\n')
owned=['docs/paper/main.tex','docs/paper/main.pdf','docs/research-status.md','docs/research-plan.md','research/README.md','docs/novelty-20261101.md','docs/evaluation.md','docs/cleanup-20261101.md',str(s.relative_to(r))]
q=subprocess.run(['git','diff','--check','--']+owned,cwd=r,text=True,capture_output=True);print('DIFFCHECK',q.returncode,q.stdout);assert q.returncode==0
print('FINAL269',json.dumps(j))
