from pathlib import Path
import os,json,gzip,csv,re,shutil,subprocess,datetime
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-cleanup-correction-root-step.txt').read_text().strip());e=s/'experiment-001';out=Path('/workspaces/.agent-state/gpu-smt-captures')/(s.name+'-paper')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
sources=[('cleanup-generated-result.json','lastlink_reclaimed_blocks_bytes'),('cleanup-identical-result.json','reclaimed_lastlink_blocks_bytes'),('cleanup-retained-archive-result.json','reclaimed_lastlink_blocks_bytes'),('cleanup-tar-result.json','reclaimed_lastlink_blocks_bytes'),('small-identical-result.json','reclaimed_lastlink_blocks_bytes'),('cleanup-small-archive-result.json','reclaimed_lastlink_blocks_bytes'),('cleanup-empty-directories-result.json','reclaimed_directory_blocks_bytes'),('cleanup-bench-result.json','reclaimed_lastlink_blocks_bytes'),('git-repack-result.json','reclaimed_bytes')]
releases=[dict(receipt=n,bytes=json.loads((e/n).read_text())[k])for n,k in sources];total=sum(x['bytes']for x in releases)
du=shutil.disk_usage('/workspaces');assert total>=15*1024**3 and du.used/du.total<.75
# Every originally tracked artifact/source remains; foreign modifications are not staged or overwritten.
protected=set(gzip.decompress((e/'cleanup-protected-tracked-paths.txt.gz').read_bytes()).decode().splitlines())
missing=[p for p in protected if not os.path.lexists(p)]
assert not missing,missing[:10]
q=subprocess.run(['git','diff','--name-only','--diff-filter=D','--','artifacts','bench'],cwd=r,text=True,capture_output=True);assert not q.stdout,q.stdout
t=(r/'docs/paper/main.tex').read_text();old=gzip.decompress((e/'before-docs-paper-main.tex.gz').read_bytes()).decode()
for pattern in [r'\\title\{.*?\}\n',r'\\begin\{abstract\}.*?\\end\{abstract\}',r'\\item\[RQ\d\].*?(?=\\item\[|\\end\{description\})',r'\\(?:sub)*section\{[^}]*\}',r'\\paragraph\{System-design implication\.\}.*?(?=\\section|\\subsection|\\paragraph|\Z)',r'\\begin\{tabular\}.*?\\end\{tabular\}']:
 assert re.findall(pattern,t,re.S)==re.findall(pattern,old,re.S),pattern
assert t.count(r'\begin{tabular}')==20
rr=json.loads((e/'render-receipt.json').read_text());assert rr['pages']==26 and rr['PDF_bytes']==236622 and len(rr['contacts'])==7
shutil.copy2(out/'main.pdf',r/'docs/paper/main.pdf')
snapshot={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
b=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-persistence-20261103');snapshot['M_returned_cells']=len(list(b.glob('full-*-terminal.json')));snapshot['M_active']=json.loads((b/'matrix-active.json').read_text())['key'];snapshot['M_overall_terminal_exists']=(b/'matrix-terminal.json').exists()
if(b/'matrix-terminal.json').exists():snapshot['M_overall_state']=json.loads((b/'matrix-terminal.json').read_text())['state']
w=Path('/workspaces/.agent-state/gpu-smt-captures/workloads/openai4341-Eprep-AllocatedForecastPrimitiveCapBound-remaining-six-20261103T0325/preparation-terminal.json');a=json.loads(w.read_text());snapshot['W_preparation']={k:a[k]for k in ['utc','window_index','all_original_deps_ready','preparation_final','no_population_cost_measurements']}
snapshot['O_latest_commit']=subprocess.check_output(['git','log','-1','--format=%h %s','--','research/decoupled-check'],cwd=r,text=True).strip()
(e/'owner-final-read.json').write_text(json.dumps(snapshot,indent=2)+'\n')
rel=str(s.relative_to(r)).removeprefix('docs/')
cleanup=f"""
## 2026-11-03 UTC — root0279 actual historical reclamation
Direct user request is recorded verbatim in [user-instruction.md](user-instruction.md).
This replaces no historical observation: root0268 audited candidates without deleting
them; root0279 now actually reclaims the two named historical roots and retired
generated bench outputs within repository.

**Attributed released allocation: {total:,} bytes ({total/1024**3:.6f} GiB).**
This is the sum of last-link file blocks, removed empty-directory blocks and the
measured Git-object allocation reduction, never a repeated old cleanup claim or
a concurrent df delta. Current PVC used {du.used:,}/{du.total:,} bytes
({100*du.used/du.total:.4f}%), available {du.free:,} bytes.
Both requested targets (at least15GiB and below75%) are met.

- Retired generated Lean build caches/stock4.27 SDK libraries/native ELF/Rust outputs:
  {releases[0]['bytes']:,} B; [inventory]({rel}/experiment-001/cleanup-generated-candidates.json.gz).
  Sources/version/build commands and original reports/raw remain.
- Exact whole-file byte comparisons consolidate historical duplicates, preserving
  every path and raw byte: large-files {releases[1]['bytes']:,} B, small-files
  {releases[4]['bytes']:,} B. [Large manifest]({rel}/experiment-001/cleanup-identical-hardlinks.json.gz)
  and [small manifest]({rel}/experiment-001/small-identical-completed.jsonl.gz).
  Historical paths now share inodes; copy to a distinct inode before any future
  edit/append. Original per-path mtimes/modes are recorded for restoration.
- Expanded duplicates are removed only after comparison to existing retained
  ZIP/split-tar/tar member bytes: {releases[2]['bytes']+releases[3]['bytes']+releases[5]['bytes']:,} B,
  including a directly inspected archive containing only7517regenerable private
  compiler outputs. [ZIP/split-tar manifest]({rel}/experiment-001/cleanup-retained-archive-duplicates.json.gz),
  [tar manifest]({rel}/experiment-001/cleanup-tar-duplicates.jsonl.gz),
  [small duplicate receipts]({rel}/experiment-001/cleanup-small-archive-result.json).
  Existing raw/source archives remain; restore each recorded member to its
  recorded path/mode/mtime if an expanded view is needed.
- 149501empty retired intermediate directories: {releases[6]['bytes']:,} B;
  [manifest]({rel}/experiment-001/cleanup-empty-directories.json.gz).
- Two old bench .lake/build trees: {releases[7]['bytes']:,} B from39untracked
  compiled outputs, including sourceTrace/looseBVarReference/persistentKernel.
  Their Main.lean/LooseBVar.lean/toolchain/lake configuration and source package
  remain. [Manifest]({rel}/experiment-001/cleanup-bench-generated.json.gz).
- Git repack, no pruning/reflog expiration: {releases[8]['bytes']:,} B.
  All41669oldobjects remain readable, no commit rewritten/deleted;
  [receipt]({rel}/experiment-001/git-repack-result.json).

Protected: all38372initially enumerated tracked paths across the main and nested
source repositories still exist;17419tracked artifacts were protected at initial
scan. No tracked artifact/bench deletion. Dirty foreign files and root a.out
remain untouched. Current M/W/O runtime/captures/snapshots were outside cleanup.
Before mutations, commands/descriptors/mappings were checked for actual use.
No native collection, infrastructure, network, credentials or runtime policy changed.

Unique unreferenced raw data remain. In particular,156native427 JSONL files over
1MB had no exact absolute-filepath match in the scoped tracked-reference query;
this is not proof that no relative/report reference exists. They were not discarded
or converted into permission to delete. Existing partial/failure logs and the
historical invalid ZIP remain. Any future proposal to discard unique unreferenced
raw must be listed and put to the user under the current explicit instruction.
The user15GiBtarget is already met without doing so.

An inefficient root-only small-file archival traversal was interrupted using its
actual PID/birth; its completed exact comparisons/deletions were logged, then a
direct-path traversal completed. No M/W/O process was signaled. Evidence includes
[correction]({rel}/experiment-001/small-archive-loop-correction.json).
All root scripts, exact per-path inventories and results are retained in
[step0279]({rel}/step-report.md); review is self-review.
"""
p=r/'docs/cleanup-20261101.md';p.write_text(p.read_text()+cleanup)
summary=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),attributed_reclaimed_bytes=total,attributed_reclaimed_GiB=total/1024**3,goal15GiB_met=True,used_below75=True,PVC_used_bytes=du.used,PVC_total_bytes=du.total,PVC_free_bytes=du.free,PVC_used_percent=100*du.used/du.total,release_receipts=releases,protected_tracked_paths=len(protected),missing_tracked=missing,unique_raw_lost=0,foreign_native_signals=0)
(e/'cleanup-final-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
links=0
for n in ['docs/research-status.md','docs/research-plan.md','docs/novelty-20261101.md','docs/cleanup-20261101.md','research/README.md',str((s/'step-report.md').relative_to(r)),str((s/'outer-audit.md').relative_to(r))]:
 p=r/n
 # Compression below supplies .jsonl.gz links; check after it completes.
 for x in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://'in x or x.startswith('#'):continue
  x=x.split('#',1)[0]
  if x:links+=1
bib=(r/'docs/paper/references.bib').read_text();keys=set(re.findall(r'@\w+\{([^,]+),',bib));cites={k for a in re.findall(r'\\cite\{([^}]+)\}',t)for k in a.split(',')};assert cites<=keys
imgs=[p for p in out.iterdir()if p.suffix in ['.png','.jpg']and p.name.startswith(('page','contact','preview-contact'))];targets={str(p.resolve())for p in imgs}
for pr in Path('/proc').iterdir():
 if not pr.name.isdigit():continue
 try:
  for fd in(pr/'fd').iterdir():
   try:assert os.readlink(fd)not in targets
   except OSError:pass
 except OSError:pass
with(e/'post-review-rendering-cleanup.csv').open('w',newline='')as f:
 writer=csv.writer(f,lineterminator='\n');writer.writerow(['path','bytes','reason'])
 for p in imgs:writer.writerow([str(p),p.stat().st_size,'root0279 rendering, all26pages7contacts viewed']);p.unlink()
# Generated per-path evidence is compressed losslessly; this is not original experimental-data deletion.
for p in list(e.iterdir()):
 if p.suffix in ['.jsonl','.stdout','.stderr','.log']:
  data=p.read_bytes();q=p.with_name(p.name+'.gz');q.write_bytes(gzip.compress(data));assert gzip.decompress(q.read_bytes())==data;p.unlink()
for n in ['step-report.md','outer-audit.md']:
 p=s/n;p.write_text(p.read_text()+f"""
## Completed storage and paper verification
Attributed storage release{total:,}B={total/1024**3:.6f}GiB; current PVC
{100*du.used/du.total:.4f}% used/{du.free:,}Bavailable. Both requested targets met.
[Exact cleanup summary](experiment-001/cleanup-final-summary.json),
[protected tracked paths](experiment-001/cleanup-protected-tracked-paths.txt.gz),
[plain summary](experiment-001/plain-summary.csv),
[paired effects](experiment-001/paired-growth.csv),
[firstP1PMU](experiment-001/P1-pmu.csv),
[raw/source](experiment-001/qualified-original-raw-source.tar.gz).
All38372protected tracked paths exist. Git41669objects retained. No unique raw loss.
Expanded views may be restored from retained archive-member mappings; byte-identical
historical paths now share inodes, so copy before any future mutation.
All root scripts/manifests and offline assertion/traversal correction retained.
Actual owner read{snapshot['utc']}: M{snapshot['M_returned_cells']}/32returned;
overallterminal={snapshot['M_overall_terminal_exists']}; only requested24plain+P1pair
admitted. Wprerequisitesready={snapshot['W_preparation']['all_original_deps_ready']};
no new source population costs admitted. O remains a source prefix, not a complete ratio.
Final236622B/26pages, all7contact sheets statically reviewed. Compile rc0,
6.506911s/sample191938560B/E22–23naturalretirement. All20oldtable bodies,
title/fullabstract/4RQ/section hierarchy/4designimplication bodies equal to entry.
No new table/native verifier/Agent. Local historical-unmarked labels and scoped
method correction only. Self-review; not venue acceptance or research completion.
""")
for n in ['docs/research-status.md','docs/research-plan.md']:
 p=r/n;v=p.read_text()
 v=re.sub(r'^Paper root0278:.*$', 'Paper root0279:26pages/236622B;20table bodies/title/fullabstract/4RQ/sections/fourimplications preserved;fullcompile/all-page self-review,0newrootnative/agent.',v,flags=re.M)
 if n.endswith('research-plan.md'):
  v=re.sub(r'^Current owner snapshot at root0278:.*$',f"Current owner read{snapshot['utc']}: M{snapshot['M_returned_cells']}/32actual terminals, fullmatrix terminal={snapshot['M_overall_terminal_exists']}; this root independently qualifies only user-requested24plain/firstP1stat subset. Wsource38 remains last root-qualified frame; prerequisite windows continue without new admitted original costs. Osource prefixes remain partial. No root dispatch/restart.",v,flags=re.M)
 p.write_text(v.rstrip()+'\n')
for n in ['docs/research-status.md','docs/research-plan.md','docs/novelty-20261101.md','docs/cleanup-20261101.md','research/README.md',str((s/'step-report.md').relative_to(r)),str((s/'outer-audit.md').relative_to(r))]:
 p=r/n
 for x in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://'in x or x.startswith('#'):continue
  x=x.split('#',1)[0]
  if x:assert(p.parent/x).exists(),(n,x)
final=dict(pages=26,PDF_bytes=236622,contacts_viewed=7,old_table_bodies_unchanged=20,frozen_fields_preserved=True,citation_keys=len(cites),labels={x:t.count('\\'+x+'{')for x in['measured','partialev','unproven']},review='self-review',removed_renderings=len(imgs),cleanup=summary)
(e/'final-self-review.json').write_text(json.dumps(final,indent=2)+'\n')
owned=['docs/user-instruction.md','docs/paper/main.tex','docs/paper/main.pdf','docs/research-status.md','docs/research-plan.md','research/README.md','docs/novelty-20261101.md','docs/evaluation.md','docs/cleanup-20261101.md',str(s.relative_to(r))]
check=subprocess.run(['git','diff','--check','--']+owned,cwd=r,text=True,capture_output=True);print('DIFFCHECK',check.returncode,check.stdout);assert check.returncode==0
print('FINAL',json.dumps(dict(summary=summary,pages=26,PDF_bytes=236622,citation_keys=len(cites),labels=final['labels'],owner=snapshot)),flush=True)
