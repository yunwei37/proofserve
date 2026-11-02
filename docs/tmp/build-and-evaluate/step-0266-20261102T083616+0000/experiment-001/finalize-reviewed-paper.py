from pathlib import Path
import os,json,re,gzip,shutil,csv,subprocess
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-heterogeneous-root-step.txt').read_text().strip());e=s/'experiment-001';out=Path('/workspaces/.agent-state/gpu-smt-captures')/(s.name+'-paper')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
t=(r/'docs/paper/main.tex').read_text();old=gzip.decompress((e/'before-docs-paper-main.tex.gz').read_bytes()).decode()
patterns=[r'\\begin\{tabular\}.*?\\end\{tabular\}',r'\\title\{.*?\}\n',r'\\begin\{abstract\}.*?\\end\{abstract\}',r'\\item\[RQ\d\].*?(?=\\item\[|\\end\{description\})',r'\\(?:sub)*section\{[^}]*\}',r'\\paragraph\{System-design implication\.\}.*?(?=\\section|\\subsection|\\paragraph|\Z)']
for pat in patterns[1:]:assert re.findall(pat,t,re.S)==re.findall(pat,old,re.S),pat
oldtabs=re.findall(patterns[0],old,re.S);newtabs=re.findall(patterns[0],t,re.S)
assert len(oldtabs)==18 and len(newtabs)==19 and [v for v in newtabs if 'Hardware / workers'not in v]==oldtabs
rr=json.loads((e/'render-receipt.json').read_text());assert rr['pages']==23 and rr['PDF_bytes']==215085 and len(rr['contacts'])==6
links=0
for n in ['docs/research-status.md','docs/research-plan.md','docs/novelty-20261101.md','research/README.md',str((s/'step-report.md').relative_to(r)),str((s/'outer-audit.md').relative_to(r))]:
 p=r/n
 for x in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://'in x or x.startswith('#'):continue
  x=x.split('#',1)[0]
  if x:assert(p.parent/x).exists(),[n,x];links+=1
shutil.copy2(out/'main.pdf',r/'docs/paper/main.pdf')
imgs=sorted(p for p in out.iterdir()if p.is_file()and p.suffix.lower()in['.png','.jpg']and(p.name.startswith('page')or p.name.startswith('contact')or p.name.startswith('preview-contact')))
paths={str(p.resolve())for p in imgs}
for proc in Path('/proc').iterdir():
 if not proc.name.isdigit():continue
 try:
  for fd in (proc/'fd').iterdir():
   try:target=os.readlink(fd)
   except OSError:continue
   assert target not in paths,target
 except OSError:pass
size=sum(p.stat().st_size for p in imgs)
with(e/'post-review-rendering-cleanup.csv').open('w',newline='')as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['path','bytes','reason'])
 for p in imgs:
  assert p.parent.resolve()==out.resolve()
  w.writerow([str(p),p.stat().st_size,'current root rendering after complete all-page self-review'])
for p in imgs:p.unlink()
# Preserve exact compiler log bytes, including trailing spaces, in compressed evidence.
compressed=[]
for p in e.rglob('*'):
 if p.is_file()and p.suffix in ['.log','.stdout','.stderr','.xdv']:
  data=p.read_bytes();dest=p.with_name(p.name+'.gz');dest.write_bytes(gzip.compress(data))
  assert gzip.decompress(dest.read_bytes())==data;compressed.append(str(p.relative_to(s)));p.unlink()
b=json.loads((e/'paper-build.json').read_text());analysis=json.loads((e/'reanalysis.json').read_text())
bib=(r/'docs/paper/references.bib').read_text();keys=set(re.findall(r'@\w+\{([^,]+),',bib));cites={k for group in re.findall(r'\\cite\{([^}]+)\}',t)for k in group.split(',')};assert cites<=keys
j=dict(pages=23,PDF_bytes=215085,contacts_viewed=6,old_table_bodies_unchanged=18,new_tables=1,title_abstract_RQs_sections_four_implication_bodies_unchanged=True,labels={x:t.count('\\'+x+'{')for x in ['measured','partialev','unproven']},canonical_links_checked=links,citation_keys=len(cites),new_root_native=0,review='self-review, not independent or venue acceptance',renderings_removed=len(imgs),rendering_bytes_removed=size,PVC_free_bytes=shutil.disk_usage('/workspaces').free,compiler_exact_log_files_gzipped=compressed)
(e/'final-self-review.json').write_text(json.dumps(j,indent=2)+'\n')
for n in ['step-report.md','outer-audit.md']:
 p=s/n;p.write_text(p.read_text()+f'''
## Completed full verification and publication readiness
Final23pages/215085bytes, Tectonicrc0/{b['elapsed_s']:.6f}s/
sample{b['own_tree_sample_peak_rss_bytes']}B/E22–23 naturallyretired.
Sixcontacts/all23pages statically viewed; no observed clipping/overlap/blank body.
All18oldtable bodies, title/fullabstract/4RQ/sections/four designimplication
bodies match entry; exactly1newtable. Labels{j['labels']};{links}links and
{len(cites)}citation keys resolve. This is self-review, not independent acceptance.
Rootreduction{analysis['root_analysis_seconds']:.6f}s/{analysis['root_analysis_maxrss_kib']}KiB;
raw/source/command/stdout/stderr/memory/terminal gzip{analysis['raw_gzip_bytes']}B.
Only{len(imgs)}current rootrenderings/{size}B removed after review/FDcheck.
Exact compiler logs with original trailing whitespace are byte-checked gzip;
allPDF/log/source/raw/failed/partial and foreign artifacts remain.
Oowner resumed its corrected original path: new all-check-00013stdout observed;
not a root restart or complete wholelibrary result.
One owned main commit/push follows; no stash/reset/force or foreign staging.
''')
p=r/'docs/cleanup-20261101.md';(e/'before-docs-cleanup-20261101.md.gz').write_bytes(gzip.compress(p.read_bytes()))
drel=str(s.relative_to(r)).removeprefix('docs/')
p.write_text(p.read_text()+f'''
## After current paper review, step0266
Remove only{len(imgs)}current rootrenderings/{size}bytes after all23pages/6contacts
self-review. [Manifest]({drel}/experiment-001/post-review-rendering-cleanup.csv).
AllPDF/log/source/raw/failed/partial and foreign artifacts retained. Exact
compiler logs gzip preserves originalbytes, not data deletion. PVCfree snapshot
{j['PVC_free_bytes']}B is concurrent state, not oldcleanup reclaimed storage.
''')
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;lines=p.read_text().splitlines()
 replacement='Paper root0266:23pages/215085bytes,complete compile and all-page self-review;18prior tables/title/fullabstract/4RQ/sections/four implication bodies unchanged,+1heterogeneous table. Self-review,not independent/venue acceptance;0newrootnative/agent.'
 p.write_text('\n'.join(replacement if x.startswith('Paper root0266:')else x for x in lines)+'\n')
p=r/'docs/evaluation.md';p.write_text(p.read_text()+f'\nFinal0266paper23pages/215085B,compile{b["elapsed_s"]:.6f}s/sample{b["own_tree_sample_peak_rss_bytes"]}B/E22–23;6contacts/allpages self-reviewed;18oldtables/title/fullabstract/4RQ/sections/4implications unchanged,+1table. Removedonly{len(imgs)}rootrenderings/{size}B; allraw/source/failed/partial preserved.\n')
check=subprocess.run(['git','diff','--check','--','docs/paper','docs/evaluation.md','docs/novelty-20261101.md','docs/research-status.md','docs/research-plan.md','docs/cleanup-20261101.md','research/README.md',str(s.relative_to(r))],cwd=r,capture_output=True,text=True);assert check.returncode==0,check.stdout
print('FINAL',json.dumps(j))
