#!/usr/bin/env python3
"""Small executable checks for the supplied second code-only review."""
import contextlib,json,os,shutil,subprocess,tempfile,sys,signal
from pathlib import Path
HERE=Path(__file__).resolve().parent
BIN=Path(os.environ.get("PROOFSERVE_CHECK",str(HERE.parent/".lake/build/bin/proofserve-check"))).resolve()
OBSERVE="--observe" in sys.argv
ROWS=[]
HIGHER_SOURCE='import F\nset_option linter.deprecated false\ndef invokePrimitive (g : Bool → Bool) : Bool := g f\ntheorem higher : invokePrimitive Lean.reduceBool = true := by decide +kernel\n'
QUOT_SOURCE='import Init.Core\nnoncomputable def quotValue : Nat := Quot.lift (fun n : Nat => n) (fun _ _ h => h) (Quot.mk (fun a b : Nat => a = b) Nat.zero)\ntheorem quotRfl : quotValue = Nat.zero := rfl\n'
def command(name,args,cwd):
 proc=subprocess.Popen(list(map(str,args)),cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 try:out,err=proc.communicate(timeout=180)
 except subprocess.TimeoutExpired:
  os.killpg(proc.pid,signal.SIGKILL);out,err=proc.communicate()
  ROWS.append(dict(case=name,exit=proc.returncode,stdout=out,stderr=err,self_limit=True))
  raise
 r=subprocess.CompletedProcess(args,proc.returncode,out,err)
 try:j=json.loads(r.stdout)
 except ValueError:j=None
 row=dict(case=name,exit=r.returncode,stdout=r.stdout,stderr=r.stderr,json=j)
 ROWS.append(row)
 if os.environ.get("PROOFSERVE_REVIEW2628_WORK"):(Path(os.environ["PROOFSERVE_REVIEW2628_WORK"])/"results.json").write_text(json.dumps(ROWS,indent=2)+"\n")
 return row
def need(ok,value):
 if not OBSERVE:assert ok,value
def good(row):return row["exit"]==0 and (row["json"]or{}).get("status")=="complete"
def project(d,name,sources,libs=None):
 p=d/name;p.mkdir()
 version=subprocess.check_output(["lean","--version"],text=True).split("version ",1)[1].split(",",1)[0]
 (p/"lean-toolchain").write_text("leanprover/lean4:v"+version+"\n")
 libs=libs or list(sources)
 (p/"lakefile.toml").write_text('name = "secondReview"\ndefaultTargets = '+json.dumps(libs)+'\n'+''.join('\n[[lean_lib]]\nname = '+json.dumps(n)+'\n'for n in libs))
 for n,body in sources.items():
  f=p/Path(*n.split(".")).with_suffix(".lean");f.parent.mkdir(parents=True,exist_ok=True);f.write_text(body if body.startswith(("prelude","module")) else "prelude\n"+body)
 row=command("build-"+name,["lake","build"],p);assert row["exit"]==0,row
 return p
def check(name,p,d,roots=(),flags=()):
 args=[BIN,p,"--workers","1","--checkpoint-dir",d,"--json"]
 for root in roots:args+=["--root",root]
 row=command(name,args+list(flags),p)
 strict_args=list(args)
 strict_args[strict_args.index("--checkpoint-dir")+1]=Path(str(d)+"-strict")
 strict=command(name+"-strict",strict_args+list(flags)+["--strict-theorem-bodies"],p)
 if row["json"]:need(row["json"].get("theorem_body_policy")=="shared-checked",row)
 if strict["json"]:need(strict["json"].get("theorem_body_policy")=="strict",strict)
 if name=="2-crafted-body-native":
  need(row["exit"]==0 and strict["exit"]==1,[row,strict])
 else:
  need(row["exit"]==strict["exit"],[row,strict])
 return row
def official(name,p,root):
 return [command(name+"-"+mode,["lake","env","leanchecker",*flags,root],p)for mode,flags in [("default",[]),("fresh",["--fresh"])]]
def parity(name,p,d,root,expected=0):
 refs=official(name,p,root);n=check(name+"-native",p,d,[root],["--closure-roots","0"])
 need(all(x["exit"]==expected for x in refs+[n]),refs+[n]);return n
def run(d):
 # Same upstream PrivateConflict layout, only unsafe/partial definitions differ.
 original=HERE/"private-conflict"
 for kind in ["unsafe","partial"]:
  src={}
  for f in original.glob("*.lean"):
   text=f.read_text().replace("LeanCheckerTests.","")
   text=text.replace("public def foo", "public "+kind+" def foo")
   text=text.replace("if foo = 42 then trivial else trivial","trivial").replace("if foo = 23 then trivial else trivial","trivial")
   src[f.stem]=text
  p=project(d,"private-"+kind,src)
  for root in sorted(src):parity("1-"+kind+"-"+root,p,d/(kind+"-"+root),root,1 if root.endswith("C")else 0)
  n=check("1-"+kind+"-batched",p,d/(kind+"-batched"),sorted(src),["--closure-roots","1"])
  need(n["exit"]==1,n)
 # Private unsafe import followed by a same-named safe definition.
 p=project(d,"private-unsafe-safe",{
  "X":'module\nprelude\npublic import Init.Core\npublic unsafe def foo : Nat := 7\n',
  "Y":'module\nprelude\nimport X\n',
  "M":'module\nprelude\npublic import Init.Core\nimport Y\npublic def foo : Nat := 9\n'})
 parity("1-unsafe-then-safe",p,d/"unsafe-safe","M",1)
 # One root's opaque well-founded theorem must not replace another's body.
 base='import Init.WFComputable\ndef R (_ _: Nat) : Prop := False\naxiom seed : WellFounded R\n'
 a='import Base\ntheorem wf : WellFounded R := seed\n'
 m='import Base\ntheorem wf : WellFounded R := ⟨fun a => Acc.intro a (fun _ h => False.elim h)⟩\n'
 child='import M\ndef computation : Nat := wf.fix (fun _ _ => 42) 0\ntheorem result : computation = 42 := by decide +kernel\n'
 p=project(d,"body-context",{"Base":base,"A":a,"M":m,"D":child})
 refs=official("2-body-D",p,"D");need(all(x["exit"]==0 for x in refs),refs)
 n=check("2-body-native",p,d/"body-native",["A","D"],["--closure-roots","0"]);need(good(n),n)
 if n["json"]:
  accepted=set(n["json"].get("accepted",[]));rejected={x.get("module")for x in n["json"].get("rejected",[])}
  need(not accepted&rejected,n)
 # A cached union must not lend M's proof body to a root importing only A.
 af=p/".lake/build/lib/lean/A.olean";mf=p/".lake/build/lib/lean/M.olean";saved_a=af.read_bytes()
 zsource=child.replace("import M","import A").replace("computation","zComputation").replace("result","zResult")
 (p/"ZBroken.lean").write_text(zsource if zsource.startswith("prelude") else "prelude\n"+zsource)
 try:
  af.write_bytes(mf.read_bytes())
  row=command("2-cache-compile",["lake","env","lean","ZBroken.lean","-o",p/".lake/build/lib/lean/ZBroken.olean"],p)
  assert row["exit"]==0,row
 finally:af.write_bytes(saved_a)
 refs=official("2-cache-body",p,"ZBroken")
 n=check("2-cache-body-native",p,d/"cached-bodies",["A","M","D","ZBroken"],["--closure-roots","2"])
 need(n["exit"]==1 and all(x["exit"]!=0 for x in refs),refs+[n])
 if n["json"]:
  need("D" in n["json"]["accepted"] and any(x.get("module")=="ZBroken" for x in n["json"]["rejected"]),n)
 # Swap only the two locally valid theorem bodies, keeping D's original proof.
 af=p/".lake/build/lib/lean/A.olean";mf=p/".lake/build/lib/lean/M.olean"
 aa=af.read_bytes();mm=mf.read_bytes()
 try:
  af.write_bytes(mm);mf.write_bytes(aa)
  refs=official("2-crafted-body",p,"D")
  n=check("2-crafted-body-native",p,d/"body-swapped",["A","D"],["--closure-roots","0"])
  need(all(x["exit"]==1 for x in refs) and good(n),refs+[n])
 finally:af.write_bytes(aa);mf.write_bytes(mm)
 # The same body-dependent declaration inside M exercises frontier insertion.
 local_child="def computation"+child.split("def computation",1)[1]
 p=project(d,"body-same-module",{"Base":base,"A":a,"M":m+local_child})
 refs=official("6-body-same-module",p,"M")
 n=check("6-body-same-module-native",p,d/"body-same-state",["A","M"],["--closure-roots","0"])
 need(good(n)and all(x["exit"]==0 for x in refs),refs+[n])
 if n["json"]:need(not set(n["json"].get("accepted",[]))&{x.get("module")for x in n["json"].get("rejected",[])},n)
 # A mention is not a closed native computation.
 p=project(d,"mention",{"Mention":"import Init.Core\nset_option linter.deprecated false\ntheorem wrap (b : Bool) (h : Lean.reduceBool b = true) : b = true := Lean.ofReduceBool b true h\n"})
 parity("3-mention",p,d/"mention-state","Mention")
 p=project(d,"name-taint",{"Aaa":"import Init.Core\nset_option linter.deprecated false\nunsafe def helper : Bool := Lean.reduceBool true\n","Bbb":"import Init.Core\ndef helper : Bool := true\ntheorem ok : helper = true := rfl\n"})
 for root in ["Aaa","Bbb"]:official("3-taint-"+root,p,root)
 n=check("3-taint-native",p,d/"taint-state",["Aaa","Bbb"],["--closure-roots","0"]);need(good(n),n)
 p=project(d,"evaluation",{"F":"import Init.Core\ndef f : Bool := true\n","Eval":"import F\nset_option linter.deprecated false\ntheorem evaluated : f = true := Lean.ofReduceBool f true (Eq.refl true)\n"})
 official("3-evaluation",p,"Eval")
 n=check("3-evaluation-native",p,d/"eval-native",["Eval"]);need(n["exit"]==2 and not good(n),n)
 n=command("3-evaluation-official-path",[BIN,p,"--official","--root","Eval","--checkpoint-dir",d/"eval-official","--json"],p)
 need(n["exit"]==1 and (n["json"]or{}).get("status")=="official_failure",n)
 p=project(d,"higher-native",{"F":'import Init.Core\ndef f : Bool := true\n',"Higher":HIGHER_SOURCE})
 refs=official("3-higher",p,"Higher")
 n=check("3-higher-native",p,d/"higher-native-state",["Higher"])
 need(n["exit"]==2 and not good(n),n)
 # Original importer reads IR for dependencies when a signature is present.
 p=project(d,"ir-input",{"IRBase":"module\nprelude\npublic import Init.Core\npublic def a : Nat := 1\n","IRUse":"module\nprelude\npublic import IRBase\npublic theorem ok : a = a := rfl\n"})
 ir=p/".lake/build/lib/lean/IRBase.ir";sig=ir.with_suffix(".ir.sig");assert sig.exists()and ir.exists()
 row=command("4-ir-region-lifetime",["lake","env","lean","--run",HERE/"IRLifetime.lean",sig,ir],HERE.parent)
 need(row["exit"]==0 and (row["json"]or{}).get("ir_region_lifetime")is True,row)
 saved=ir.read_bytes()
 for kind in ["missing","corrupt"]:
  if kind=="missing":ir.unlink()
  else:ir.write_bytes(b"invalid IR fixture")
  refs=official("4-ir-"+kind,p,"IRUse")
  n=check("4-ir-"+kind+"-native",p,d/("ir-"+kind),["IRUse"])
  need(n["exit"]!=0 and all(x["exit"]!=0 for x in refs),refs+[n])
  ir.write_bytes(saved)
 # Empty context conflict must have the same verification exit at every grouping.
 p=project(d,"context",{"ShadowLeft":(HERE/"ShadowLeft.lean").read_text(),"ShadowRight":(HERE/"ShadowRight.lean").read_text(),"Pkg":"prelude\n"})
 file=p/".lake/build/lib/lean/Pkg.olean";bad=d/"conflicting-context.olean"
 row=command("5-context-mutate",["lean","--run",HERE/"Mutate.lean",file,"Pkg",bad,"imports"],p);assert row["exit"]==0,row
 file.write_bytes(bad.read_bytes())
 refs=official("5-context",p,"Pkg");need(all(x["exit"]!=0 for x in refs),refs)
 for size in ["0","1"]:
  n=check("5-context-native-"+size,p,d/("context-"+size),["Pkg"],["--closure-roots",size])
  need(n["exit"]==1 and (n["json"]or{}).get("status")=="rejected",n)
 # Checker-owned untracked state must not make a clean checkout look dirty.
 p=project(d,"dirty",{"Clean":"prelude\naxiom P : Prop\n"})
 (p/".gitignore").write_text(".lake/\n")
 for args in [["git","init","-b","main"],["git","add","."],["git","-c","user.name=Fixture","-c","user.email=fixture@example.invalid","commit","-m","fixture"]]:
  assert command("7-"+args[1],args,p)["exit"]==0
 n=command("7-default-state",[BIN,p,"--workers","1","--json"],p);need(good(n)and n["json"].get("project_dirty")is False,n)
 (p/"Clean.lean").write_text((p/"Clean.lean").read_text()+"-- edit\n")
 n=command("7-real-edit",[BIN,p,"--workers","1","--json"],p);need(good(n)and n["json"].get("project_dirty")is True,n)
 # File components are encoded as escaped Lean identifiers during discovery.
 p=project(d,"escaped",{"Foo":"prelude\nimport Foo.«bar-baz»\n","Foo.bar-baz":"prelude\naxiom P : Prop\n"},["Foo"])
 parity("9-escaped",p,d/"escaped-explicit","Foo.«bar-baz»")
 n=check("9-default-discovery",p,d/"escaped-default");need(good(n)and"Foo.«bar-baz»"in n["json"]["accepted"],n)
 # max-segments bounds new work per invocation, not all historical segments.
 p=project(d,"segments",{"A":"prelude\naxiom P : Prop\n","B":"prelude\nimport A\naxiom p : P\n"})
 args=["--closure-roots","0","--segment-modules","1","--max-segments","1"]
 first=check("10-segment-first",p,d/"segment-state",["B"],args)
 second=check("10-segment-second",p,d/"segment-state",["B"],args)
 need(first["exit"]==2 and second["exit"]==2, [first,second])
 need(len(second["json"]["accepted"])>len(first["json"]["accepted"]),[first,second])
 third=check("10-segment-third",p,d/"segment-state",["B"],args);need(good(third),third)
 # Namespace-triggered batches inspect empty leaf roots as well as prefixes.
 p=project(d,"empty-leaf",{'Pkg': 'prelude\nimport Pkg.Child\naxiom P : Prop\n', 'Pkg.Child': 'prelude\naxiom A : Prop\n', 'Leaf': 'prelude\n'},["Pkg","Leaf"])
 n=check("10-empty-leaf",p,d/"empty-leaf-state")
 need(good(n)and "Leaf"in n["json"].get("import_only_modules",[]),n)
 # The second review's axiom-tagged quotient records are unsupported.
 p=project(d,"quot-records",{"QSource":QUOT_SOURCE,"ASeed":'prelude\naxiom Seed : Prop\n'})
 lib=p/".lake/build/lib/lean"
 row=command("8-quot-metadata",["lake","env","lean","--run",HERE/"ReviewQuot.lean","QSource",lib/"ZFake.olean"],p);assert row["exit"]==0,row
 refs=official("8-quot",p,"ZFake");need(all(x["exit"]!=0 for x in refs),refs)
 for label,roots,flags in [
  ("plain",["ZFake"],["--closure-roots","0"]),
  ("segmented",["ASeed","ZFake"],["--closure-roots","0","--segment-modules","1"])]:
  n=check("8-quot-"+label,p,d/("quot-"+label),roots,flags)
  need(n["exit"]==2 and not good(n)and "nonprimitive quotient metadata"in n["stderr"],n)
owned=os.environ.get("PROOFSERVE_REVIEW2628_WORK")
if owned:Path(owned).mkdir(parents=True,exist_ok=False)
with(contextlib.nullcontext(owned)if owned else tempfile.TemporaryDirectory(prefix="proofserve-second-review-"))as td:
 d=Path(td)
 try:run(d)
 finally:
  if owned:(d/"results.json").write_text(json.dumps(ROWS,indent=2)+"\n")
 print(json.dumps(dict(observe=OBSERVE,cases=len(ROWS),completed=True)))
