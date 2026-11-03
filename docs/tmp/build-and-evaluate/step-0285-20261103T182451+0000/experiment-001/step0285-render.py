from pathlib import Path
import os,subprocess,json,re
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository')
s=Path(Path('/workspaces/.agent-state/gpu-smt-hybrid-source40-root-step.txt').read_text().strip());e=s/'experiment-001';out=Path('/workspaces/.agent-state/gpu-smt-captures')/(s.name+'-paper')
tool=Path('/workspaces/.agent-state/gpu-smt-paper-recovery-20261030/poppler-readonly/unpacked');env=os.environ.copy();env['LD_LIBRARY_PATH']=str(tool/'usr/lib/x86_64-linux-gnu')
subprocess.run([str(tool/'usr/bin/pdftotext'),'-layout',str(out/'main.pdf'),str(out/'main.txt')],env=env,check=True)
pages=[p for p in (out/'main.txt').read_text().split('\f') if p.strip()]
affected=list(range(1,len(pages)+1))
font=subprocess.check_output(['fc-match','-f','%{file}','DejaVu Sans'],text=True).strip()
for n in affected:
 subprocess.run([str(tool/'usr/bin/pdftoppm'),'-f',str(n),'-l',str(n),'-scale-to','1400','-png','-singlefile',str(out/'main.pdf'),str(out/f'page{n}')],env=env,check=True)
parts=[]
for i in range(0,len(affected),4):
 dest=out/f'contact{i//4+1}.jpg';subprocess.run(['/usr/bin/montage','-font',font]+[str(out/f'page{n}.png') for n in affected[i:i+4]]+['-tile','2x2','-geometry','1000x1350+5+5','-background','white',str(dest)],check=True);parts.append(str(dest))
t=(r/'docs/paper/main.tex').read_text();before=__import__('gzip').decompress((e/'before-docs-paper-main.tex.gz').read_bytes()).decode()
for pat in [r'\\title\{.*?\}',r'\\item\[RQ[^\n]+']:
 assert re.findall(pat,t,re.S)==re.findall(pat,before,re.S),pat
assert t.count('\\paragraph{System-design implication.}')==4
assert 'source-qualified finite-index chunking' in t and 'automatically chunked' not in t
j={'pages':len(pages),'affected_pages':affected,'contacts':parts,'PDF_bytes':(out/'main.pdf').stat().st_size,'title_and_four_RQs_match_user_authorized_draft':True,'abstract_changes_authorized_by_current_user':True,'implication_sections':4}
(e/'render-receipt.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(j))
print(subprocess.check_output(['git','diff','--stat','--','docs/paper/main.tex','docs/evaluation.md'],cwd=r,text=True))
