from pathlib import Path
import os,re,gzip,json,shutil,csv,subprocess,datetime
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-cpu-coverage-root-step.txt').read_text().strip());e=s/'experiment-001';out=Path('/workspaces/.agent-state/gpu-smt-captures')/(s.name+'-paper');rel=str(s.relative_to(r));drel=rel.removeprefix('docs/')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
t=(r/'docs/paper/main.tex').read_text();old=gzip.decompress((e/'before-docs-paper-main.tex.gz').read_bytes()).decode()
for pat in [r'\\title\{.*?\}\n',r'\\begin\{abstract\}.*?\\end\{abstract\}',r'\\item\[RQ\d\].*?(?=\\item\[|\\end\{description\})',r'\\(?:sub)*section\{[^}]*\}',r'\\paragraph\{System-design implication\.\}.*?(?=\\section|\\subsection|\\paragraph|\Z)']:
 assert re.findall(pat,t,re.S)==re.findall(pat,old,re.S),pat
tabs=lambda x:re.findall(r'\\begin\{tabular\}.*?\\end\{tabular\}',x,re.S)
assert len(tabs(old))==19 and len(tabs(t))==20 and all(v in tabs(t)for v in tabs(old))
rr=json.loads((e/'render-receipt.json').read_text());assert rr['pages']==23 and rr['PDF_bytes']==219436 and len(rr['contacts'])==6
# Exact terminal accepted IDs independently confirm the source/dependency split.
state=json.loads(gzip.decompress((e/'whole-library-all-state.json.gz').read_bytes()))
accepted=state['accepted'];assert len(accepted)==len(set(accepted))==13232
source=[x for x in accepted if x.startswith('OAI.')];deps=[x for x in accepted if not x.startswith('OAI.')]
assert len(source)==2488 and len(deps)==10744
(e/'coverage-accepted-ids-check.json').write_text(json.dumps(dict(accepted_total=len(accepted),unique=True,source_OAI=len(source),dependencies=len(deps),source_frame=163097,source_unaccepted=163097-len(source)),indent=2)+'\n')
# Owner's newly visible uncommitted attribution is evidence for later qualification,
# not silently substituted for this step's raw-cost/coverage audit.
for n in ['whole-library-source-errors.md','whole-library-source-error-distribution.csv','whole-library-source-error-examples.json']:
 p=r/'research/decoupled-check'/n
 if p.exists():(e/('owner-late-'+n+'.gz')).write_bytes(gzip.compress(p.read_bytes()))
note='During final review, O owner produced a new offline error-classification report and CSV (still uncommitted on observation). Root read and froze the report, but did not independently qualify all9124raw log classifications or a controlled producer-environment repair. Thus this root qualifies the rc1count and partial coverage only; cause attribution is outside this step. Owner report is not ignored or claimed still nonexistent; no environment-failure or proof-rejection conclusion is newly added to paper. Follow actual new O terminal/report after publication, not stale pending descriptions.'
for n in ['step-report.md','outer-audit.md']:
 p=s/n;p.write_text(p.read_text()+'\n\n## Newly visible owner evidence at final review\n\n'+note+'\n')
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;v=p.read_text()
 if n.endswith('status.md'):
  v=re.sub(r'^\| Large Falconer closure .*$', '| Large Falconer closure |13205source/27segments; native CPU2038.444/32292.604s=6.31%; matched checkpoint Mathlib91.145/1018.219s=8.95%. Separate wall9.26%/historicalMathlib10.56%/checkpoint14.67%. Selected closures, one capture each, trusted metadata and Oshare deviation retained. | [0268]('+drel+'/step-report.md) |',v,flags=re.M)
 v=v.replace('Direct finalized-number update [0265]','Historical finalized-number update [0265]')
 v+='\nO newly visible source-error report is retained for later independent attribution qualification; root0268 audits9124rc1count and2488source accepted, not all log causes or a repaired producer run.\n'
 p.write_text(v)
links=0
for n in ['docs/research-status.md','docs/research-plan.md','docs/novelty-20261101.md','docs/cleanup-20261101.md','research/README.md',str((s/'step-report.md').relative_to(r)),str((s/'outer-audit.md').relative_to(r))]:
 p=r/n
 for x in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://'in x or x.startswith('#'):continue
  x=x.split('#',1)[0]
  if x:assert(p.parent/x).exists(),(n,x);links+=1
shutil.copy2(out/'main.pdf',r/'docs/paper/main.pdf')
imgs=[p for p in out.iterdir()if p.suffix in ['.jpg','.png']and(p.name.startswith('page')or p.name.startswith('contact')or p.name.startswith('preview-contact'))]
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
  assert p.parent.resolve()==out.resolve();w.writerow([str(p),p.stat().st_size,'root0268 rendering after all-page review']);p.unlink()
for p in e.rglob('*'):
 if p.is_file()and(p.suffix in['.stderr','.stdout','.log']or p.name=='source-cpu-wall.csv'):
  data=p.read_bytes();q=p.with_name(p.name+'.gz');q.write_bytes(gzip.compress(data));assert gzip.decompress(q.read_bytes())==data;p.unlink()
b=json.loads((e/'paper-build.json').read_text());st=os.statvfs('/workspaces')
j=dict(pages=23,PDF_bytes=219436,contacts_viewed=6,old_tables_unchanged=19,new_CPU_table=1,title_abstract_RQs_sections_implications_unchanged=True,links=links,labels={x:t.count('\\'+x+'{')for x in['measured','partialev','unproven']},renderings_removed=len(imgs),rendering_bytes_removed=size,PVC_available_bytes=st.f_bavail*st.f_frsize,PVC_used_bytes=(st.f_blocks-st.f_bfree)*st.f_frsize,PVC_total_bytes=st.f_blocks*st.f_frsize,review='self-review',native_runs=0,agents=0,cache_deletion=False)
j['PVC_used_percent']=100*j['PVC_used_bytes']/j['PVC_total_bytes']
(e/'final-self-review.json').write_text(json.dumps(j,indent=2)+'\n')
for n in ['step-report.md','outer-audit.md']:
 p=s/n;p.write_text(p.read_text()+f'''
## Completed verification
Full compiler rc0 in{b['elapsed_s']:.6f}s/sample{b['own_tree_sample_peak_rss_bytes']}B/E22–23naturalretirement.
23pages/219436B/6contacts all statically viewed; no observed clipping/overlap.
All19prior table bodies/title/fullabstract/4RQ/sections/4implication bodies unchanged;
one new two-row CPU table,20total. Links{links}; labels{j['labels']}.
Only{len(imgs)}rootrenderings/{size}B removed after review/FDcheck,manifest retained.
AllPDF/log/raw/source/failed/partial/foreign data retained; exact compiler logs byte-verified gzip.
No historical cache/SDK/ELF deleted. Current disk{j['PVC_used_percent']:.3f}% used,
available{j['PVC_available_bytes']}B; concurrent other-owner release not attributed to root.
Self-review only; no acceptance/independent review. Persist owned paths onmain with ordinarypush.
''')
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;ls=p.read_text().splitlines();p.write_text('\n'.join('Paper root0268:23pages/219436B,19prior table bodies/title/fullabstract/4RQ/sections/fourimplications unchanged;1newCPUtable/20total,fullcompile/all-page self-review completed,0newrootnative/agent.'if z.startswith('Paper root0268:')else z for z in ls).rstrip()+'\n')
p=r/'docs/cleanup-20261101.md';p.write_text(p.read_text()+f'\n## Step0268 current reviewed renderings\nOnly{len(imgs)}current root renderings/{size}B removed after23page/6contact self-review and FDcheck. [Manifest]({drel}/experiment-001/post-review-rendering-cleanup.csv). AllPDF/log/source/raw/failed/partial/foreign files retained. Current disk{j["PVC_used_percent"]:.3f}%/available{j["PVC_available_bytes"]}B; target<85% met by concurrent other-line cleanup, not credited to root. No native427/artifacts cache or tracked file deleted.\n')
owned=['docs/paper/main.tex','docs/paper/main.pdf','docs/novelty-20261101.md','docs/cleanup-20261101.md','docs/research-status.md','docs/research-plan.md','research/README.md','docs/evaluation.md','docs/user-instruction.md',str(s.relative_to(r))]
q=subprocess.run(['git','diff','--check','--']+owned,cwd=r,text=True,capture_output=True)
print('DIFFCHECK',q.returncode,q.stdout);assert q.returncode==0
print('FINAL',json.dumps(j))
