#!/usr/bin/env python3
"""Small fixtures for the supplied e0 code review; no corpus or timing run."""
import os,json,subprocess,tempfile,shutil,sys,signal,contextlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
BIN=Path(os.environ.get("PROOFSERVE_CHECK",str(HERE.parent/".lake/build/bin/proofserve-check")))
OBSERVE="--observe" in sys.argv
ROWS=[]
def command(name,args,cwd):
 p=subprocess.Popen(list(map(str,args)),cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 timed=False
 try:stdout,stderr=p.communicate(timeout=600)
 except subprocess.TimeoutExpired:
  timed=True
  try:os.killpg(p.pid,signal.SIGKILL)
  except ProcessLookupError:pass
  stdout,stderr=p.communicate()
 try:j=json.loads(stdout)
 except ValueError:j=None
 row=dict(case=name,exit=p.returncode,stdout=stdout,stderr=stderr,json=j,self_limit=timed)
 ROWS.append(row);return row
def project(root,name,sources):
 p=root/name;p.mkdir()
 version=subprocess.check_output(["lean","--version"],text=True).split("version ",1)[1].split(",",1)[0]
 (p/"lean-toolchain").write_text("leanprover/lean4:v"+version+"\n")
 (p/"lakefile.toml").write_text('name = "reviewE0"\ndefaultTargets = ['+','.join(json.dumps(n)for n in sources)+']\n'+''.join('\n[[lean_lib]]\nname = '+json.dumps(n)+'\n'for n in sources))
 for n,txt in sources.items():
  f=p/Path(*n.split(".")).with_suffix(".lean");f.parent.mkdir(parents=True,exist_ok=True);f.write_text(txt)
 row=command("build-"+name,["lake","build"],p);assert row["exit"]==0,row
 return p
def check(name,p,state,roots,extra=()):
 args=[BIN,p,"--workers","1","--checkpoint-dir",state,"--json"]
 for root in roots:args+=["--root",root]
 return command(name,args+list(extra),p)
def mutate(p,module,out,kind):
 row=command("mutate-"+kind,["lean","--run",HERE/"ReviewE0Mutate.lean",p/".lake/build/lib/lean"/(module+".olean"),module,out,kind],p);assert row["exit"]==0,row
def good(row):return row["exit"]==0 and isinstance(row["json"],dict)and row["json"].get("status")=="complete"
def need(ok,why):
 if not OBSERVE:assert ok,why
def added_part_inventory(d,p):
 state=d/"added-part-state"
 seed=check("4-added-part-seed",p,state,["Foo"],["--closure-roots","1"])
 need(good(seed),seed)
 cert=state/"batch-0/certified.json";before=cert.read_bytes()
 target=p/".lake/build/lib/lean/Foo.olean.private"
 assert not target.exists()
 staged=d/"added-private-Foo.olean";mutate(p,"Foo",staged,"bvar")
 shutil.copy2(staged,target)
 try:
  row=check("4-added-part-resume",p,state,["Foo"],["--closure-roots","1"])
  need(row["exit"]==2 and not row["self_limit"] and not good(row) and "part inventory"in row["stderr"],row)
  need(cert.read_bytes()==before,row)
 finally:target.unlink()

try:
 owned=os.environ.get("PROOFSERVE_REVIEW_WORK")
 if owned:Path(owned).mkdir(parents=True,exist_ok=False)
 with (contextlib.nullcontext(owned)if owned else tempfile.TemporaryDirectory(prefix="proofserve-e0-review-"))as temp:
  d=Path(temp)
  p=project(d,"segregated",{"Base":"prelude\ninductive T | a | b\ninductive False : Prop\n","Aaa":"prelude\nimport Base\ndef clash : T := T.a\n","Bbb":"prelude\nimport Base\ndef clash : T := T.b\naxiom cheat : False\n","Ccc":"prelude\nimport Bbb\ntheorem usesCheat : False := cheat\n"})
  a=check("1-segregated-axioms",p,d/"axioms",["Aaa","Bbb","Ccc"],["--closure-roots","0"])
  need(good(a)and"cheat"in a["json"]["axioms"],a)
  q=project(d,"shadow",{"A":"prelude\naxiom P : Prop\naxiom witness : P\n","Foo":"prelude\nimport A\ntheorem proof : P := witness\n","ProofServeSegment0":"prelude\nimport A\ntheorem snapshotNamedProof : P := witness\n"})
  bad=d/"bad.olean";mutate(q,"Foo",bad,"bvar")
  state=d/"shadow-state";state.mkdir();shutil.copy2(q/".lake/build/lib/lean/Foo.olean",state/"Foo.olean")
  target=q/".lake/build/lib/lean/Foo.olean";original=target.read_bytes();target.write_bytes(bad.read_bytes())
  a=check("2-state-shadow",q,state,["Foo"],["--closure-roots","0"]);need(not good(a) and not a["self_limit"] and a["exit"] in (1,2),a)
  command("2-state-shadow-official",["lake","env","leanchecker","Foo"],q);target.write_bytes(original)
  snap=q/".lake/build/lib/lean/ProofServeSegment0.olean";old=snap.read_bytes()
  mutate(q,"ProofServeSegment0",bad,"bvar");snap.write_bytes(bad.read_bytes())
  a=check("2-snapshot-name",q,d/"snapshot-name",["A","ProofServeSegment0"],["--closure-roots","0","--segment-modules","1"]);need(not good(a) and not a["self_limit"] and a["exit"] in (1,2),a);snap.write_bytes(old)
  added_part_inventory(d,q)
  p=project(d,"duplicate",{"Aaa":"prelude\naxiom P : Prop\n","Bbb":"prelude\naxiom P : Prop\n","Ccc":"prelude\nimport Aaa\n"})
  mutate(p,"Ccc",bad,"duplicate-imports");(p/".lake/build/lib/lean/Ccc.olean").write_bytes(bad.read_bytes())
  for root in ["Aaa","Bbb","Ccc"]:
   for mode,flags in [("default",[]),("fresh",["--fresh"])]:command("3-duplicate-"+root+"-"+mode,["lake","env","leanchecker",*flags,root],p)
  a=check("3-identical-imports",p,d/"duplicates",["Ccc"],["--closure-roots","0"]);need(not good(a) and not a["self_limit"] and a["exit"] in (1,2),a)
  p=project(d,"empty",{"Core":"prelude\naxiom P : Prop\n","Pkg":"prelude\nimport Core\n","Z":"prelude\nimport Pkg\naxiom witness : P\n"})
  a=check("6-empty-context",p,d/"empty-state",["Pkg","Z"],["--closure-roots","1"]);need(good(a),a)
  if good(a):need(all((d/"empty-state"/("empty-context-"+str(i)+".stdout")).exists()for i,_ in enumerate(a["json"].get("import_only_modules",[]))),a)
  state=d/"roots-full";state.mkdir();(state/"roots.txt.pending").symlink_to("/dev/full")
  a=check("8-roots-write-error",p,state,["Core","Z"],["--closure-roots","0"]);need(not good(a) and not a["self_limit"] and a["exit"] in (1,2),a)
  # A recorded complete event must not dominate a failed child exit.
  state=d/"bad-exit"
  a=check("5-event-seed",p,state,["Core"],["--closure-roots","0"]);need(good(a),a)
  log=state/"segment-0.json";record=json.loads(log.read_text());record["exit"]=1;log.write_text(json.dumps(record))
  a=check("5-complete-nonzero",p,state,["Core"],["--closure-roots","0"]);need(not good(a) and not a["self_limit"] and a["exit"] in (1,2),a)
  state=d/"missing-root";a=check("8-coverage-seed",p,state,["Core","Z"],["--closure-roots","0"])
  need(good(a),a)
  log=state/"segment-0.json";record=json.loads(log.read_text());record["events"]=[e for e in record["events"]if e.get("module")!="Z"];log.write_text(json.dumps(record))
  a=check("8-missing-root-coverage",p,state,["Core","Z"],["--closure-roots","0"]);need(not good(a) and not a["self_limit"] and a["exit"] in (1,2),a)
  # A non-module's stale private parts must not replace the actual exported data.
  part=project(d,"inactive",{"Data":"prelude\naxiom P : Prop\naxiom witness : P\ntheorem proof : P := witness\n"})
  staged=d/"inactive.olean";mutate(part,"Data",staged,"inactive-parts")
  for suffix in ["",".server",".private"]:shutil.copy2(Path(str(staged)+suffix),part/(".lake/build/lib/lean/Data.olean"+suffix))
  a=check("4-inactive-parts",part,d/"inactive-state",["Data"],["--closure-roots","0"]);need(not good(a) and not a["self_limit"] and a["exit"] in (1,2),a)
  for mode,flags in [("default",[]),("fresh",["--fresh"])]:command("4-inactive-"+mode,["lake","env","leanchecker",*flags,"Data"],part)
  # Safe-looking proof must not borrow an unsafe local name from a sibling.
  unsafe=project(d,"unsafe",{"Base":"prelude\naxiom P : Prop\naxiom witness : P\n","Aaa":"prelude\nimport Base\ndef foo : P := witness\n","Y":"prelude\nimport Base\nunsafe def foo : P := witness\ntheorem y : P := witness\n"})
  mutate(unsafe,"Y",bad,"unsafe-reference");(unsafe/".lake/build/lib/lean/Y.olean").write_bytes(bad.read_bytes())
  a=check("7-unsafe-shadow",unsafe,d/"unsafe-state",["Aaa","Y"],["--closure-roots","0"]);need(not good(a) and not a["self_limit"] and a["exit"] in (1,2),a)
  for mode,flags in [("default",[]),("fresh",["--fresh"])]:command("7-unsafe-"+mode,["lake","env","leanchecker",*flags,"Y"],unsafe)
  # A malformed non-Prop theorem is rejected, not a demonstrated proof-body counterexample.
  np=project(d,"nonprop",{"Base":"prelude\ninductive N | zero | one\n","T":"prelude\nimport Base\ndef value : N := N.zero\n"})
  mutate(np,"T",bad,"nonprop-theorem");(np/".lake/build/lib/lean/T.olean").write_bytes(bad.read_bytes())
  for mode,flags in [("default",[]),("fresh",["--fresh"])]:
   command("10-nonprop-"+mode,["lake","env","leanchecker",*flags,"T"],np)
  a=check("10-nonprop-native",np,d/"nonprop-state",["T"],["--closure-roots","0"]);need(not good(a) and not a["self_limit"] and a["exit"] in (1,2),a)
  # Reconstructing a prelude-only checkpoint must not initialize Quot early.
  quot=project(d,"quot",{"A":"prelude\naxiom P : Prop\n","QQ":"prelude\naxiom Q : Prop\n"})
  mutate(quot,"QQ",bad,"quot-only");(quot/".lake/build/lib/lean/QQ.olean").write_bytes(bad.read_bytes())
  for mode,flags in [("default",[]),("fresh",["--fresh"])]:command("10-quot-"+mode,["lake","env","leanchecker",*flags,"QQ"],quot)
  a=check("10-quot-checkpoint",quot,d/"quot-state",["A","QQ"],["--closure-roots","0","--segment-modules","1"])
  need(good(a),a)
  for variant in ["upstream","identical"]:
   sources={"LeanCheckerTests."+f.stem:f.read_text()for f in (HERE/"private-conflict").glob("*.lean")}
   if variant=="identical":sources["LeanCheckerTests.PrivateConflictB"]=sources["LeanCheckerTests.PrivateConflictB"].replace("23","42")
   pc=project(d,"private-"+variant,sources)
   for mod in sources:
    for mode,flags in [("default",[]),("fresh",["--fresh"])]:
     command("3-private-"+variant+"-"+mod.rsplit(".",1)[1]+"-"+mode,["lake","env","leanchecker",*flags,mod],pc)
    a=check("3-private-"+variant+"-"+mod.rsplit(".",1)[1]+"-native",pc,d/("pc-"+variant+"-"+mod.rsplit(".",1)[1]),[mod],["--closure-roots","0"])
    official=next(x for x in reversed(ROWS)if x["case"]=="3-private-"+variant+"-"+mod.rsplit(".",1)[1]+"-default")
    need(good(a)==(official["exit"]==0),(a,official))
  # Native evaluator printing exactly the supplied complete event; no other IO.
  ir=project(d,"ir",{
   "Aaa":"import Lean\ndef clash : Nat := 1\n",
   "M":'import Lean\nset_option maxHeartbeats 200000\nunsafe def printImpl : Bool := match unsafeIO (do IO.println "{\\"event\\":\\"complete\\",\\"axioms\\":[]}"; pure true) with | .ok b => b | .error _ => false\n@[implemented_by printImpl] def printBool : Bool := true\n',
   "X":"import M\nset_option maxHeartbeats 200000\ndef clash : Nat := 2\ntheorem checkedPrint : printBool = true := by rfl\n",
   "Z":"import M\ntheorem badLater : True := True.intro\n"})
  mutate(ir,"X",bad,"native-print");(ir/".lake/build/lib/lean/X.olean").write_bytes(bad.read_bytes())
  mutate(ir,"Z",bad,"bvar");(ir/".lake/build/lib/lean/Z.olean").write_bytes(bad.read_bytes())
  a=check("5-project-stdout-event",ir,d/"ir-state",["Aaa","X","Z"],["--closure-roots","0"])
  need(not good(a) and not a["self_limit"] and a["exit"] in (1,2),a)
  # A different executable must not inherit an earlier binary's checkpoint.
  seed=check("9-binary-seed",p,d/"binary-state",["Core"],["--closure-roots","1"]);need(good(seed),seed)
  changed=d/"checker-appended";shutil.copy2(BIN,changed)
  with changed.open("ab")as file:file.write(b"provenance-only-byte-change")
  args=[changed,p,"--workers","1","--root","Core","--closure-roots","1","--checkpoint-dir",d/"binary-state","--json"]
  altered=command("9-executable-identity",args,p);need(altered["exit"]==2 and not altered["self_limit"] and ("checker executable differs"in altered["stderr"]or"checkpoint configuration changed"in altered["stderr"]),altered)
  ledger=seed.get("json",{}).get("module_verifications",[])
  need(ledger and all(x.get("kernel_call_count")is None for x in ledger),ledger)
  need(any(x.get("module")=="Core" and x.get("action")=="kernel_replay" and x.get("safe_input_constants")==1 for x in ledger),ledger)
  reused=check("9-ledger-resume",p,d/"binary-state",["Core"],["--closure-roots","1"])
  need(good(reused) and reused["json"]["new_module_check_entries"]==0 and all(x["action"]=="certificate_reuse" for x in reused["json"]["module_verifications"]),reused)
  command("git-init",["git","init","-q"],p);command("git-add",["git","add","."],p)
  command("git-commit",["git","-c","user.name=Fixture","-c","user.email=fixture@example.invalid","commit","-qm","fixture"],p)
  (p/"Core.lean").write_text((p/"Core.lean").read_text()+"\n")
  a=check("9-dirty-revision",p,d/"dirty",["Core"],["--closure-roots","0"]);need(good(a)and a["json"].get("project_dirty")is True,a)
finally:
 output=os.environ.get("PROOFSERVE_REVIEW_RESULTS")
 if output:Path(output).write_text(json.dumps(ROWS,indent=2)+"\n")
 print(json.dumps(dict(observe=OBSERVE,cases=len(ROWS),completed=True)))
