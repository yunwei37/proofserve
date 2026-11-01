"""Lexical corpus census; conservative candidates are not semantic split proofs."""
import os,re,json,csv,gzip,collections,argparse,tarfile,urllib.request,signal
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=Path('/workspaces/.agent-state/gpu-smt-workloads/openai-math-4eaee875/lean')
RAW=Path('/workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check')
SITES=re.compile(r'\bdecide\s+\+kernel\b')
TOKENS=re.compile(r'/-|-/|--[^\n]*|"(?:[^"\\]|\\.)*"',re.S)
DECL=re.compile(r'\b(?:lemma|theorem|have|show|example|def)\b')
def mask(s):
    spans=[];depth=0;begin=None
    for m in TOKENS.finditer(s):
        v=m.group()
        if depth:
            if v=='/-':depth+=1
            elif v=='-/':
                depth-=1
                if not depth:spans.append((begin,m.end()))
        elif v=='/-':depth=1;begin=m.start()
        elif v!='-/':spans.append((m.start(),m.end()))
    if depth:spans.append((begin,len(s)))
    parts=[];prev=0
    for a,b in spans:
        parts.append(s[prev:a]);parts.append(''.join('\n' if c=='\n' else ' ' for c in s[a:b]));prev=b
    parts.append(s[prev:]);return ''.join(parts)
def header(s,pos):
    start=s.rfind(':=',max(0,pos-8192),pos)
    if start<0:return '',False
    # Inline argument proofs and tactics after earlier statements have inferred
    # targets; never borrow a preceding have/declaration's explicit header.
    if re.fullmatch(r'\s*by\s*',s[start+2:pos]) is None:return '',False
    # Only a direct explicit-header proof is recoverable without elaboration.
    h=s[max(0,start-4096):start]
    matches=list(DECL.finditer(h))
    if not matches:return '',False
    h=h[matches[-1].start():]
    stack=[];colons=[]
    pairs={')':'(',']':'[','}':'{','⟩':'⟨'}
    for i,c in enumerate(h):
        if c in '([{⟨':stack.append(c)
        elif c in pairs and stack and stack[-1]==pairs[c]:stack.pop()
        elif c==':' and not stack:colons.append(i)
    if not colons:return '',False
    return h[colons[0]+1:].strip(),True
def classify(t,known):
    if not known:return 'embedded_or_unresolved',False
    if re.search(r'∃|\bExists\b',t):return 'existential_or_mixed',False
    quant=len(re.findall(r'∀|\bforall\b',t))
    if quant:
        finite=bool(re.search(r'\bFin\s+(?:\d+|\()',t))
        if quant>=2:return 'nested_forall_explicit_fin' if finite else 'nested_forall_unresolved_domain',finite
        if finite:return 'forall_explicit_fin',True
        if re.search(r'\b(?:Finset\.)?(?:range|Icc|Ico|Ioc|Ioo)\b',t):return 'forall_range_or_interval',True
        if re.search(r'\bList\b|∈\s*\[',t):return 'forall_list',True
        if '∈' in t or '⊆' in t:return 'forall_membership_or_subset_unresolved',False
        return 'forall_inferred_or_unresolved',False
    if '∧' in t:return 'conjunction',True
    if re.search(r'\b(?:List\.all|Array\.all|Finset\.all)\b',t):return 'boolean_container_all',True
    if re.search(r'(?<![<>=!:])=(?!=|>)',t):return 'equality_unresolved_type',False
    if re.search(r'[≤≥<>]|≠',t):return 'atomic_comparison',False
    return 'application_or_other',False
def write(name,rows):
    with (HERE/name).open('w') as f:
        w=csv.DictWriter(f,lineterminator='\n',fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def sources():
    frame=HERE.parents[1]/'workloads/openai-math/static-4eaee875/files.csv.gz'
    with gzip.open(frame,'rt') as f: expected={r['path']:int(r['size']) for r in csv.DictReader(f)}
    archive=RAW/'openai-math-4eaee875.tar.gz'
    if not archive.exists():
        part=archive.with_suffix('.partial')
        with urllib.request.urlopen('https://codeload.github.com/openai/math/tar.gz/4eaee87548250b2682affda7d05d947c05554bae',timeout=60) as src,part.open('wb') as dst:
            while block:=src.read(1024*1024):dst.write(block)
        part.rename(archive)
    seen=set();total=0
    with tarfile.open(archive,'r|gz') as t:
      for member in t:
        rel=member.name.split('/',1)[-1]
        if rel not in expected:continue
        assert rel not in seen and member.size==expected[rel]
        seen.add(rel);total+=member.size
        yield rel.removeprefix('lean/'),t.extractfile(member).read().decode()
        if len(seen)%20000==0:print('scanned',len(seen),flush=True)
    assert seen==set(expected) and total==1785499363,(len(seen),len(expected),total)
def main():
    os.sched_setaffinity(0,set(range(8,16)))
    signal.alarm(1800)
    RAW.mkdir(exist_ok=True);totals=collections.Counter();eligible=collections.Counter();files=[];examples={}
    codehits=rawhits=nfiles=0
    with gzip.open(RAW/'lexical-sites.jsonl.gz','wt',compresslevel=1) as out:
      for rel,s in sources():
        nfiles+=1;rawhits+=len(SITES.findall(s))
        if 'kernel' not in s:continue
        clean=mask(s);hits=list(SITES.finditer(clean))
        if not hits:continue
        categories=collections.Counter();cand=0
        lines=[0]+[m.end() for m in re.finditer('\n',clean)]
        import bisect
        for h in hits:
            target,known=header(clean,h.start());cat,possible=classify(target,known)
            categories[cat]+=1;totals[cat]+=1;eligible[cat]+=possible;cand+=possible;codehits+=1
            row=dict(path=rel,line=bisect.bisect_right(lines,h.start()),
                     category=cat,lexical_candidate=possible,target=target[:300],header_recovered=known)
            out.write(json.dumps(row,ensure_ascii=False)+'\n')
            if cat not in examples:examples[cat]=row
        files.append(dict(module='.'.join(Path(rel).with_suffix('').parts),path=rel,
            sites=len(hits),lexical_candidates=cand,lexical_fraction=cand/len(hits),**categories))
    keys=sorted(set(totals)|{"nested_forall_explicit_fin","forall_range_or_interval","boolean_container_all"})
    write('shape-counts.csv',[dict(category=k,sites=totals[k],fraction=totals[k]/codehits,
        lexical_candidate_sites=eligible[k],evidence='lexical only; requires native type/closedness/dependency validation') for k in keys])
    # Sparse per-file categories are kept raw; compact module totals enter Git.
    write('module-counts.csv',[{k:v for k,v in r.items() if k in ['module','path','sites','lexical_candidates','lexical_fraction']} for r in files])
    (RAW/'module-category-counts.json').write_text(json.dumps(files)+'\n')
    (HERE/'shape-examples.json').write_text(json.dumps(examples,ensure_ascii=False,indent=2)+'\n')
    summary=dict(target_header_scope='direct explicit := by decide only; inline inferred goals unresolved',source_files=nfiles,frame_source_bytes=1785499363,pin="4eaee87548250b2682affda7d05d947c05554bae",raw_regex_sites=rawhits,code_regex_sites=codehits,files_with_sites=len(files),
        lexical_candidates=sum(eligible.values()),lexical_candidate_fraction=sum(eligible.values())/codehits,
        semantic_coverage='unknown until native validation; lexical candidate count is not proven splittable coverage',
        raw_sites=str(RAW/'lexical-sites.jsonl.gz'))
    (HERE/'static-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
