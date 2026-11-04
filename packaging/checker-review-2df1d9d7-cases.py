#!/usr/bin/env python3
"""Untimed, own-fixture adversarial review of checker 2df1d9d7. No production paths modified."""
from pathlib import Path
import argparse,os,json,subprocess,signal,time,shutil,threading,stat

class Review:
    def __init__(self,a):
        self.a=a; self.root=a.out.resolve();self.root.mkdir(parents=True,exist_ok=False)
        self.rows=[];self.count=0;self.peak=0
        self.env=dict(os.environ,PATH=str(a.sdk/"bin")+":"+os.environ.get("PATH",""),
                      LEAN_SYSROOT=str(a.sdk),LEAN_NUM_THREADS="1",PROOFSERVE_WORKERS="1")
        for k in list(self.env):
            if k.startswith("DECOUPLED_") or k.startswith("PROOFSERVE_VALIDATED_"):
                self.env.pop(k)
        current=Path("/sys/fs/cgroup")/Path("/proc/self/cgroup").read_text().strip().split("::")[1].lstrip("/")
        self.cg=current.parent/("proofserve-o-review-"+str(os.getpid())+".scope")
        self.cg.mkdir();(self.cg/"memory.max").write_text(str(7*1024**3))
        (self.cg/"memory.oom.group").write_text("1")
        self.mut=Path(__file__).with_name("checker-review-2df1d9d7-Mutate.lean")
    def close(self):
        try:self.cg.rmdir()
        except OSError:pass
    def run(self,label,argv,cwd=None,env=None,timeout=90,callback=None):
        self.count+=1;stem=self.root/(f"{self.count:03}-"+label)
        def enter():(self.cg/"cgroup.procs").write_text("0")
        with stem.with_suffix(".stdout").open("w")as so,stem.with_suffix(".stderr").open("w")as se:
            p=subprocess.Popen(list(map(str,argv)),cwd=cwd,env=env or self.env,stdout=so,stderr=se,
                               preexec_fn=enter,start_new_session=True)
            stop=None;deadline=time.monotonic()+timeout;fired=False
            while p.poll()is None:
                rss=0
                for pid in(self.cg/"cgroup.procs").read_text().split():
                    try:rss+=int(Path("/proc",pid,"stat").read_text().split(") ")[1].split()[21])*os.sysconf("SC_PAGE_SIZE")
                    except OSError:pass
                self.peak=max(self.peak,rss)
                if callback and not fired:fired=callback(p)
                if rss>8*1024**3 or time.monotonic()>deadline:
                    stop="own-resource-or-self-limit";(self.cg/"cgroup.kill").write_text("1");break
                time.sleep(.01)
            p.wait()
        text=stem.with_suffix(".stdout").read_text()
        try:value=json.loads(text)
        except ValueError:value=None
        row=dict(label=label,command=list(map(str,argv)),exit=p.returncode,stdout=str(stem.with_suffix(".stdout")),
                 stderr=str(stem.with_suffix(".stderr")),stop=stop,callback_fired=fired)
        (stem.with_suffix(".json")).write_text(json.dumps(row,indent=2)+"\n")
        return row,value
    def project(self,name,sources):
        p=self.root/name;p.mkdir()
        (p/"lean-toolchain").write_text("leanprover/lean4:v4.34.1\n")
        targets=list(sources)
        cfg='name = "reviewInput"\ndefaultTargets = ['+",".join(json.dumps(n)for n in targets)+"]\n"
        cfg+="".join('\n[[lean_lib]]\nname = '+json.dumps(n)+'\n'for n in targets)
        (p/"lakefile.toml").write_text(cfg)
        for n,text in sources.items():(p/(n+".lean")).write_text(text)
        r,_=self.run("build-"+name,["lake","build"],p,timeout=180)
        if r["exit"]:raise RuntimeError("fixture compilation failed: "+r["stderr"])
        return p
    def check(self,label,p,state,roots,extra=(),callback=None):
        args=[self.a.checker,p,"--workers","1","--closure-roots","1","--checkpoint-dir",state,"--json"]
        for n in roots:args+=["--root",n]
        args+=list(extra)
        return self.run(label,args,p,callback=callback)
    def note(self,name,expect,run,value,**extra):
        ok=run["exit"]==0 and isinstance(value,dict)and value.get("status")=="complete"
        self.rows.append(dict(case=name,expected=expect,exit=run["exit"],complete=ok,
                              accepted=value.get("accepted")if isinstance(value,dict)else None,
                              axioms=value.get("axioms")if isinstance(value,dict)else None,
                              evidence=run,**extra))
        self.save()
    def save(self):
        (self.root/"results.json").write_text(json.dumps(dict(untimed=True,checker_commit="2df1d9d70259d2630edda2aa1a4a8663753e5f9d",
           affinity=sorted(os.sched_getaffinity(0)),peak_owned_child_rss_bytes=self.peak,
           scope="own frozen binary and fixtures; production checker and active M data untouched",cases=self.rows),indent=2)+"\n")
    def mutate(self,p,name,kind):
        f=p/".lake/build/lib/lean"/(name+".olean")
        target=self.root/(name+"-"+kind+"-"+str(self.count)+".olean")
        r,_=self.run("mutate-"+name,["lean","--run",self.mut,f,name,target,kind],p)
        if r["exit"]:raise RuntimeError("mutation failed: "+r["stderr"])
        old=f.read_bytes();os.replace(target,f);return f,old
    def copy_state(self,old,name):
        d=self.root/name;shutil.copytree(old,d);return d

def main():
    q=argparse.ArgumentParser(description=__doc__);q.add_argument("--checker",type=Path,required=True)
    q.add_argument("--sdk",type=Path,required=True);q.add_argument("--out",type=Path,required=True)
    q.add_argument("--extended",action="store_true")
    q.add_argument("--private-only",action="store_true")
    q.add_argument("--edges",action="store_true")
    q.add_argument("--parts-only",action="store_true")
    a=q.parse_args();assert sorted(os.sched_getaffinity(0))==[8,9]
    a.checker=a.checker.resolve(strict=True);a.sdk=a.sdk.resolve(strict=True)
    t=Review(a)
    try:
        if a.parts_only:part_cases(t)
        elif a.edges:edge_cases(t)
        elif a.private_only:private_cases(t)
        elif a.extended:extended_cases(t)
        else:cases(t)
    finally:t.save();t.close()

def cases(t):
    good='prelude\naxiom ReviewP : Prop\naxiom reviewWitness : ReviewP\ntheorem reviewed : ReviewP := reviewWitness\n'
    p=t.project("project-good",{"Token":good})
    donor=t.root/"donor-state"
    r,v=t.check("good-donor",p,donor,["Token"]);t.note("good-control","complete",r,v)
    assert r["exit"]==0
    bad=t.project("project-bad",{"Token":good})
    f,old=t.mutate(bad,"Token","bad")
    r,v=t.check("bad-fresh",bad,t.root/"bad-fresh",["Token"]);t.note("bad-body-fresh","reject",r,v)
    # An unchanged, authentic certificate from a different project, with its own
    # recorded artifacts still present. No JSON content or hashes are edited.
    transplanted=t.root/"transplanted-state";(transplanted/"batch-0").mkdir(parents=True)
    shutil.copy2(donor/"batch-0/certified.json",transplanted/"batch-0/certified.json")
    r,v=t.check("cross-project-authentic-certificate",bad,transplanted,["Token"])
    t.note("cross-project-authentic-certificate","must refuse wrong-project certificate",r,v,
           certificate_json_modified=False,donor_artifact_unchanged=True,current_artifact_has_bad_body=True)
    r,v=t.run("bad-official",["lake","env","leanchecker","-v","Token"],bad)
    t.note("bad-body-official","reject",r,v)
    # Baseline corpus for dependency reuse, axioms and duplicate/unknown names.
    sources={"Base":good,"BranchA":"prelude\nimport Base\ntheorem branchA : ReviewP := reviewed\n",
             "BranchB":"prelude\nimport Base\naxiom extraWitness : ReviewP\ntheorem branchB : ReviewP := extraWitness\n",
             "Umbrella":"prelude\nimport BranchA\nimport BranchB\n"}
    chain=t.project("chain",sources)
    roots=["Base","BranchA","BranchB"]
    normal=t.root/"chain-normal"
    r,v=t.check("chain-reuse",chain,normal,roots);t.note("reuse-baseline","complete",r,v)
    assert r["exit"]==0
    r,w=t.check("chain-no-reuse",chain,t.root/"chain-no-reuse",roots,["--replay-shared-imports"])
    t.note("no-reuse-baseline","same accepted and declared axioms",r,w,same_accepted=v["accepted"]==w["accepted"],same_axioms=v["axioms"]==w["axioms"])
    r,w=t.check("chain-resume",chain,normal,roots)
    t.note("completed-resume","same set, no fresh replay",r,w,same_accepted=v["accepted"]==w["accepted"],
           all_batches_reused=all(x["reused"]for x in w["batches"]),module_check_entries=w["module_check_entries"],
           trusted_import_entries=w["trusted_import_entries"])
    r,w=t.run("chain-official",["lake","env","leanchecker","-v"]+roots,chain)
    t.note("official-reference","same requested roots accepted",r,w)
    paths=subprocess.check_output(["lake","env","printenv","LEAN_PATH"],cwd=chain,env=t.env,text=True).strip()
    paths=":".join(str((chain/x).resolve())for x in paths.split(":"))
    e=dict(t.env,LEAN_PATH=paths)
    r,axes=t.run("original-importer-axioms",["lean","--run",t.mut,"axioms"]+roots,chain,e)
    t.note("axiom-reference","declared closure set equals original importer",r,None,original_axioms=axes,same_axioms=axes==v["axioms"])
    # Toolchain identity mismatches, partial certificates, and forged receipt
    # fields: the latter deliberately crosses documented trusted-state bounds.
    for label,edit in [
        ("wrong-identity-lean",lambda c:c["input_identity"].update(lean="Lean (version 4.35.0)\n")),
        ("wrong-receipt-lean",lambda c:c["receipt"].update(lean_version="Lean (version 4.35.0)\n")),
        ("forged-extra-acceptance",lambda c:c["receipt"]["accepted"].append("NeverChecked")),
        ("forged-missing-axioms",lambda c:c["receipt"].update(axioms=[])),
        ("wrong-child-abi",lambda c:c["input_identity"].update(checker_checkpoint_abi=999)),
    ]:
        d=t.copy_state(donor,label);cert=d/"batch-0/certified.json";value=json.loads(cert.read_text());edit(value);cert.write_text(json.dumps(value))
        r,w=t.check(label,p,d,["Token"]);t.note(label,"toolchain mismatch must refuse; tampering capability is separately scoped",r,w,trusted_metadata_deliberately_modified=True)
    d=t.copy_state(donor,"torn-certificate");(d/"batch-0/certified.json").write_text('{"receipt":')
    r,w=t.check("torn-certificate",p,d,["Token"]);t.note("torn-certificate","fail closed",r,w)
    d=t.copy_state(donor,"torn-segment");(d/"batch-0/certified.json").unlink();(d/"batch-0/segment-0.json").write_text('{"events":')
    r,w=t.check("torn-segment",p,d,["Token"]);t.note("torn-segment","fail closed",r,w)
    # Changed bytes after genuine success cannot inherit old proof acceptance.
    artifact=chain/".lake/build/lib/lean/Base.olean";f,before=t.mutate(chain,"Base","bad")
    try:
        r,w=t.check("changed-complete-dependency",chain,normal,roots);t.note("changed-complete-dependency","fail closed",r,w)
        r,w=t.check("bad-beneath-empty",chain,t.root/"bad-empty",["Umbrella"]);t.note("bad-beneath-empty","reject dependency, not empty success",r,w)
    finally:f.write_bytes(before)
    # A proof-bearing root must not be replaced by import-only expansion.
    r,w=t.check("nonempty-root",chain,t.root/"nonempty",["BranchA"]);t.note("nonempty-root","actual replay, not import_only",r,w,not_empty="BranchA"not in w.get("import_only_modules",[]))
    r,w=t.check("empty-root",chain,t.root/"empty",["Umbrella"]);t.note("empty-root","accept only after dependency/context checks",r,w)
    for label,names in [("duplicates",["Base","Base","BranchA"]),("unknown-name",["Base","NeverBuilt"])]:
        rootfile=t.root/(label+".txt");rootfile.write_text("\n".join(names)+"\n")
        r,w=t.check(label,chain,t.root/(label+"-state"),[],["--root-file",rootfile])
        t.note(label,"deduplicate accepted modules"if label=="duplicates"else"fail, not synthetic acceptance",r,w)
    # Each separate context is valid; a consumer combining both is not.
    clash=t.project("clashes",{
        "ClashLeft":"prelude\ninductive Paint where | light\ndef chosen : Paint := Paint.light\n",
        "ClashRight":"prelude\ninductive Paint where | dark\ndef chosen : Paint := Paint.dark\n",
        "UseLeft":"prelude\nimport ClashLeft\ndef leftUse : Paint := chosen\n",
        "UseRight":"prelude\nimport ClashRight\ndef rightUse : Paint := chosen\n",
        "Combined":"prelude\nimport ClashLeft\n"})
    for label,extra in [("clashes-reuse",[]),("clashes-replay",["--replay-shared-imports"])]:
        r,w=t.check(label,clash,t.root/label,["ClashLeft","ClashRight","UseLeft","UseRight"],extra)
        t.note(label,"valid separate contexts complete",r,w)
    f,before=t.mutate(clash,"Combined","conflict")
    try:
        r,w=t.check("combined-conflict",clash,t.root/"combined-conflict",["Combined"])
        t.note("combined-conflict","refuse combined incompatible imports",r,w)
        r,w=t.run("combined-official",["lake","env","leanchecker","-v","Combined"],clash)
        t.note("combined-official","refuse combined incompatible imports",r,w)
    finally:f.write_bytes(before)
    # Block an atomic certificate write on an own FIFO, kill the invocation,
    # then verify a partial pending file is not used as a completed certificate.
    state=t.root/"killed-write";(state/"batch-0").mkdir(parents=True)
    fifo=state/"batch-0/certified.json.pending";os.mkfifo(fifo)
    def stop_after_replay(proc):
        if (state/"batch-0/receipt.json").exists():
            (t.cg/"cgroup.kill").write_text("1");return True
        return False
    r,w=t.check("kill-certificate-write",p,state,["Token"],callback=stop_after_replay)
    t.note("kill-certificate-write","no complete stdout; no certified.json",r,w,
           final_certificate_exists=(state/"batch-0/certified.json").exists())
    fifo.unlink();fifo.write_text('{"receipt":')
    r,w=t.check("resume-pending-write",p,state,["Token"])
    t.note("resume-pending-write","pending partial ignored, successful work resumes",r,w)
    # Private-namespace real ENOSPC/EROFS tests are run separately by fs_cases.
    fs_cases(t,p,donor)

def fs_cases(t,p,donor):
    for mode in ["full","readonly"]:
        mount=t.root/("fs-"+mode);mount.mkdir()
        script=t.root/("fs-"+mode+".py")
        code=r"""from pathlib import Path
import subprocess,shutil,sys,os,json
mount=Path(sys.argv[1]);donor=Path(sys.argv[2]);checker=sys.argv[3];project=sys.argv[4];mode=sys.argv[5]
subprocess.run(["mount","-t","tmpfs","-o","size=2m","tmpfs",str(mount)],check=True)
state=mount/"state";shutil.copytree(donor,state)
if mode=="readonly":
 subprocess.run(["mount","-o","remount,ro",str(mount)],check=True)
else:
 try:
  with(mount/"filler").open("wb",buffering=0)as f:
   while True:f.write(bytes(4096))
 except OSError as e:
  assert e.errno==28,e
r=subprocess.run([checker,project,"--workers","1","--closure-roots","1","--checkpoint-dir",str(state),"--root","Token","--json"],capture_output=True,text=True,timeout=45)
try:
 old=json.loads((state/"receipt.json").read_text());old_complete=old.get("status")=="complete";read_error=None
except (OSError,ValueError)as e:
 old_complete=False;read_error=repr(e)
print(json.dumps(dict(native_exit=r.returncode,native_stdout=r.stdout,native_stderr=r.stderr,old_receipt_complete=old_complete,receipt_read_error=read_error,mode=mode)))
"""
        script.write_text(code)
        r,w=t.run("filesystem-"+mode,["unshare","--mount","--propagation","private","python3",script,mount,donor,t.a.checker,p,mode],p,timeout=60)
        t.note("filesystem-"+mode,"native nonzero and no new complete stdout; old receipt may remain",r,None,
               namespace_control=w,namespace_available=r["exit"]==0)

def part_cases(t):
    good='prelude\naxiom PartsP : Prop\naxiom partsWitness : PartsP\ntheorem partsProof : PartsP := partsWitness\n'
    p=t.project("part-project",{"Token":good})
    original=p/".lake/build/lib/lean/Token.olean"
    staged=t.root/"staged.olean"
    r,_=t.run("make-optional-parts",["lean","--run",t.mut,original,"Token",staged,"staged"],p)
    assert r["exit"]==0
    original.write_bytes(staged.read_bytes())
    state=t.root/"part-certificate"
    r,v=t.check("base-only",p,state,["Token"]);t.note("base-only-certificate","good base actually checked",r,v)
    assert r["exit"]==0
    before=original.read_bytes();cert_before=(state/"batch-0/certified.json").read_bytes()
    for suffix in [".server",".private"]:
        shutil.copy2(Path(str(staged)+suffix),Path(str(original)+suffix))
    assert original.read_bytes()==before
    r,v=t.check("new-private-part-fresh",p,t.root/"new-private-fresh",["Token"])
    t.note("new-private-part-fresh","reject bad body in additional part",r,v,original_exported_bytes_unchanged=True)
    r,v=t.run("new-private-part-official",["lake","env","leanchecker","-v","Token"],p)
    t.note("new-private-part-official","reject bad body",r,v)
    r,v=t.check("new-private-part-resume",p,state,["Token"])
    t.note("new-private-part-resume","reject changed part inventory",r,v,
           certificate_json_unchanged=cert_before==(state/"batch-0/certified.json").read_bytes(),
           original_exported_bytes_unchanged=original.read_bytes()==before)
    paths=subprocess.check_output(["lake","env","printenv","LEAN_PATH"],cwd=p,env=t.env,text=True).strip()
    paths=":".join(str((p/x).resolve())for x in paths.split(":"))
    r,axes=t.run("new-private-actual-axioms",["lean","--run",t.mut,"axioms","Token"],p,dict(t.env,LEAN_PATH=paths))
    t.note("new-private-part-actual-axioms","current private part has additional declared axiom",r,None,original_axioms=axes)

def extended_cases(t):
    part_cases(t)
    good='prelude\naxiom PartsP : Prop\naxiom partsWitness : PartsP\ntheorem partsProof : PartsP := partsWitness\n'
    # Verify genuine ENOSPC and EROFS on a separate, ordinary single-part input.
    q=t.project("filesystem-input",{"Token":good});d=t.root/"fs-donor"
    r,v=t.check("fs-donor",q,d,["Token"]);assert r["exit"]==0
    fs_cases(t,q,d)
    private_cases(t)

def private_cases(t):
    # No implicit Init import: this is a correctness fixture, not a library run.
    private=t.project("private-axioms",{
      "PrivateBase":"module\nprelude\npublic axiom PrivateP : Prop\nprivate axiom hiddenWitness : PrivateP\npublic theorem exposed : PrivateP := hiddenWitness\n",
      "PrivateUse":"module\nprelude\npublic import PrivateBase\npublic theorem usePrivate : PrivateP := exposed\n"})
    roots=["PrivateBase","PrivateUse"]
    r,v=t.check("private-reuse",private,t.root/"private-cache",roots)
    t.note("private-axioms-reuse","complete, include hidden declared axiom",r,v)
    r,w=t.check("private-no-reuse",private,t.root/"private-replay",roots,["--replay-shared-imports"])
    t.note("private-axioms-reference","same accepted/axioms",r,w,same_accepted=isinstance(v,dict) and isinstance(w,dict) and v["accepted"]==w["accepted"],same_axioms=isinstance(v,dict) and isinstance(w,dict) and v["axioms"]==w["axioms"])
    r,w=t.run("private-official",["lake","env","leanchecker","-v"]+roots,private)
    t.note("private-official","requested roots accepted",r,w)


def edge_cases(t):
    p=t.project("empty-plan-input",{
      "Core":"prelude\naxiom CoreP : Prop\naxiom coreWitness : CoreP\n",
      "NonEmpty":"prelude\nimport Core\ntheorem content : CoreP := coreWitness\n",
      "Decoy":"prelude\naxiom DecoyP : Prop\naxiom decoyWitness : DecoyP\ntheorem decoyProof : DecoyP := decoyWitness\n"})
    rootfile=t.root/"roots.txt";rootfile.write_text("NonEmpty\nDecoy\nDecoy\n")
    r,v=t.check("unrelated-root-file",p,t.root/"mixed",[],["--root-file",rootfile])
    t.note("existing-unrelated-root-file","check all explicit roots, no duplicate accepted names",r,v,
           actual_closure=set(v["accepted"])=={"Core","NonEmpty","Decoy"})
    r,w=t.run("mixed-root-official",["lake","env","leanchecker","-v","NonEmpty","Decoy"],p)
    t.note("mixed-root-official","both explicit roots accepted",r,w)
    f,old=t.mutate(p,"NonEmpty","bad")
    r,h=t.run("nonempty-current-hash",["lean","--run",t.mut,"hash",f],p);assert r["exit"]==0
    state=t.root/"forged-empty-plan";state.mkdir()
    row=dict(module="NonEmpty",empty=True,imports=["Core"],declarations=0,inputs=[[str(f),h]])
    (state/"closure-plan.json").write_text(json.dumps(dict(roots=["Core"],import_only=[row])))
    r,w=t.check("spoof-nonempty-as-empty",p,state,["NonEmpty"])
    t.note("spoof-nonempty-as-empty","actual nonempty module must refuse despite correct bytes/forged plan",r,w,
           trusted_plan_deliberately_modified=True,artifact_hash_correct=True)
    # Original SDK axiom oracle for the separate private-module control.
    private=t.project("private-reference",{
      "PrivateBase":"module\nprelude\npublic axiom PrivateP : Prop\nprivate axiom hiddenWitness : PrivateP\npublic theorem exposed : PrivateP := hiddenWitness\n",
      "PrivateUse":"module\nprelude\npublic import PrivateBase\npublic theorem usePrivate : PrivateP := exposed\n"})
    roots=["PrivateBase","PrivateUse"]
    paths=subprocess.check_output(["lake","env","printenv","LEAN_PATH"],cwd=private,env=t.env,text=True).strip()
    paths=":".join(str((private/x).resolve())for x in paths.split(":"))
    r,axes=t.run("private-original-axioms",["lean","--run",t.mut,"axioms"]+roots,private,dict(t.env,LEAN_PATH=paths))
    t.note("private-original-axioms","original importer reports hidden axiom too",r,None,original_axioms=axes)

if __name__=="__main__":main()


