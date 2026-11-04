#!/usr/bin/env python3
"""Frozen four-condition native compilation qualification; never starts a census."""
import argparse,collections,ctypes,fcntl,hashlib,json,os,resource,selectors,signal
import statistics,struct,subprocess,sys,time
from pathlib import Path
from census import append,utc
from perf_instructions import open_counters,read_counters,pmus
GIB=2**30
P=list(range(8));E=list(range(10,24))
def atomic(path,value):
    tmp=path.with_suffix(path.suffix+".writing")
    tmp.write_text(json.dumps(value,indent=2)+"\n");os.replace(tmp,path)
def mem():
    d={x.split(":")[0]:int(x.split()[1])*1024 for x in Path("/proc/meminfo").read_text().splitlines()if x.startswith(("MemTotal:","MemAvailable:"))}
    return d["MemTotal"],d["MemAvailable"]
def digest(path):
    h=hashlib.sha256()
    with path.open("rb")as f:
        for block in iter(lambda:f.read(1024*1024),b""):h.update(block)
    return h.hexdigest()
def statcpu():
    result={}
    for line in Path("/proc/stat").read_text().splitlines():
        if line.startswith("cpu")and line.split()[0][3:].isdigit():
            n=int(line.split()[0][3:]);v=list(map(int,line.split()[1:]));result[n]=(sum(v[:8]),v[3]+v[4])
    return result
class Gate:
    def __init__(self,config,out):
        self.c=config;self.out=out;self.live={};self.seq=0;self.counter=collections.Counter()
        self.sel=selectors.DefaultSelector();self.lastsample=0.;self.stop=None;self.rows=[]
        self.start=time.monotonic();self.lastcpu=statcpu();self.lastcpu_t=self.start
        self.minimum=mem()[1];self.maximumcharge=0;self.chargepeaks={}
        own=Path("/sys/fs/cgroup")/Path("/proc/self/cgroup").read_text().strip().split("::")[1].lstrip("/")
        self.cg=own.parent/("proofserve-W-census-gate-"+str(os.getpid())+".scope");self.cg.mkdir()
        total,avail=mem();(self.cg/"memory.max").write_text(str(max(GIB,avail-9*GIB)))
        if self.c.get("maximum_charge_bytes"):(self.cg/"memory.max").write_text(str(self.c["maximum_charge_bytes"]))
        (self.cg/"cgroup.subtree_control").write_text("+memory")
        atomic(out/"launch.json",dict(utc=utc(),pid=os.getpid(),birth=Path("/proc/self/stat").read_text().rsplit(")",1)[1].split()[19],cgroup=str(self.cg),full_census_started=False))
    def launch(self,module,pool,condition,rep,role,perf=True):
        self.seq+=1;num=self.seq;r=self.c["modules"][module];src=Path(r["source"])
        job=self.out/"attempts"/str(num).zfill(5);job.mkdir(parents=True)
        rel=Path(*module.split("."));obj=job/rel.with_suffix(".olean")
        il=job/rel.with_suffix(".ilean");c=job/rel.with_suffix(".c")
        obj.parent.mkdir(parents=True,exist_ok=True)
        cmd=[self.c["lean_binary"],"--root="+r["root"],"-j8",*self.c["lean_options"],"-o",str(obj),"-i",str(il),"-c",str(c),str(src)]
        env=dict(os.environ);env.update(self.c["env"]);env["LEAN_NUM_THREADS"]="8"
        cg=self.cg/str(num);cg.mkdir()
        rd,wr=os.pipe();er,ew=os.pipe2(os.O_CLOEXEC);before=time.monotonic();wallstart=utc();parent=os.getpid()
        pid=os.fork()
        if pid==0:
            os.close(wr);os.close(er)
            try:
                ctypes.CDLL(None).prctl(1,signal.SIGKILL,0,0,0)
                if os.getppid()!=parent:os._exit(125)
                (cg/"cgroup.procs").write_text(str(os.getpid()))
                os.sched_setaffinity(0,P if pool=="P"else E)
                os.chdir(self.c["cwd"])
                log=os.open(job/"native.log",os.O_WRONLY|os.O_CREAT,0o644)
                os.dup2(log,1);os.dup2(log,2);os.close(log)
                os.read(rd,1);os.close(rd)
                os.execve(cmd[0],cmd,env)
            except BaseException as exc:
                os.write(ew,repr(exc).encode());os._exit(126)
        os.close(rd);os.close(ew)
        try:fds=open_counters(pid)if perf else {}
        except BaseException:
            os.kill(pid,signal.SIGKILL);os.close(wr);os.waitpid(pid,0);cg.rmdir();raise
        meta=dict(module=module,pool=pool,condition=condition,rep=rep,role=role,perf=perf,
             sequence=num,pid=pid,birth=Path("/proc",str(pid),"stat").read_text().rsplit(")",1)[1].split()[19],
             source_revision=self.c["source_revision"],source_sha256=r["source_sha256"],
             measurement_commit=self.c["measurement_commit"],toolchain=self.c["toolchain"],
             attempt=self.c.get("attempts",{}).get(module,0)+1,start_utc=wallstart,argv=cmd,affinity=P if pool=="P"else E,
             lean_num_threads=8,log=str(job/"native.log"),cgroup=str(cg))
        if "attempts"in self.c:self.c["attempts"][module]=meta["attempt"]
        append(self.out/"lifecycle.jsonl",dict(event="native_start",**meta))
        self.live[pid]=dict(meta=meta,start=before,fds=fds,cg=cg,job=job,products=[obj,il,c],killed=None,errorpipe=er)
        self.sel.register(os.pidfd_open(pid),selectors.EVENT_READ,pid)
        os.write(wr,b"x");os.close(wr)
        return pid
    def sample(self):
        total,available=mem();charge=int((self.cg/"memory.current").read_text())
        self.minimum=min(self.minimum,available);self.maximumcharge=max(self.maximumcharge,charge)
        # Keep one GiB of response slack above the requested eight GiB reserve.
        cap=max(GIB,min(total-9*GIB,charge+available-9*GIB))
        if self.c.get("maximum_charge_bytes"):cap=min(cap,self.c["maximum_charge_bytes"])
        (self.cg/"memory.max").write_text(str(cap))
        charges={}
        for pid,j in self.live.items():
            current=int((j["cg"]/"memory.current").read_text())
            charges[pid]=current;self.chargepeaks[pid]=max(self.chargepeaks.get(pid,0),current)
        now=time.monotonic();cp=statcpu();busy={}
        for n in P+E:
            dt=cp[n][0]-self.lastcpu[n][0];di=cp[n][1]-self.lastcpu[n][1]
            busy[n]=1-di/dt if dt else None
        self.lastcpu=cp;self.lastcpu_t=now
        append(self.out/"memory.jsonl",dict(utc=utc(),elapsed_s=now-self.start,available=available,charge=charge,limit=cap,charges=charges,busy=busy,active=len(self.live)))
        if available<8*GIB and self.live:
            victim=max(self.live,key=lambda p:charges[p]);self.live[victim]["killed"]="memory_reserve"
            os.kill(victim,signal.SIGKILL)
            if not self.c.get("memory_preempt_requeue"):self.stop="memory_reserve"
        disk=os.statvfs(self.out);used=1-disk.f_bavail/disk.f_blocks
        if used>=.85:self.stop="disk_85_percent"
        self.lastsample=now
    def collect(self,wait=.2):
        now=time.monotonic()
        if self.c.get("validation_deadline") is not None and now>=self.c["validation_deadline"]:
            self.stop="subset_validation_six_hour_limit"
            for pid,j in self.live.items():
                if not j["killed"]:
                    j["killed"]=self.stop
                    try:os.kill(pid,signal.SIGKILL)
                    except ProcessLookupError:pass
        if now-self.lastsample>=1:self.sample()
        for key,_ in self.sel.select(wait):
            pid=key.data;j=self.live.pop(pid)
            _,status,u=os.wait4(pid,0);end=utc();elapsed=time.monotonic()-j["start"]
            counts=read_counters(j["fds"])if j["fds"]else {}
            err=os.read(j["errorpipe"],65536).decode();os.close(j["errorpipe"])
            rc=os.waitstatus_to_exitcode(status)
            events=(j["cg"]/"memory.events").read_text();chargepeak=int((j["cg"]/"memory.peak").read_text())
            members=(j["cg"]/"cgroup.procs").read_text().split()
            for child in members:
                try:os.kill(int(child),signal.SIGKILL)
                except ProcessLookupError:pass
            if members:self.stop="unexpected_native_descendant";j["killed"]="unretired_descendant"
            for _ in range(20):
                if not(j["cg"]/"cgroup.procs").read_text().strip():break
                time.sleep(.01)
            j["cg"].rmdir()
            artifacts={p.suffix:dict(bytes=p.stat().st_size,sha256=digest(p),path=str(p))for p in j["products"]if p.is_file()}
            good=rc==0 and not err and not j["killed"]and len(artifacts)==3
            row=dict(record="result",**j["meta"],end_utc=end,returncode=rc,status="completed"if good else "failure",
                user_cpu_s=u.ru_utime,system_cpu_s=u.ru_stime,wall_s=elapsed,peak_rss_kib=u.ru_maxrss,
                cgroup_peak=chargepeak,memory_events=events,interruption=j["killed"],exec_error=err,
                counters=counts,artifacts=artifacts,driver_elapsed_s=time.monotonic()-self.start)
            if self.c.get("functional_only"):
                for field in ("user_cpu_s","system_cpu_s","wall_s","peak_rss_kib","cgroup_peak","driver_elapsed_s","counters"):row.pop(field,None)
            append(self.out/"records.jsonl",row);self.rows.append(row)
            self.sel.unregister(key.fd);os.close(key.fd)
            self.counter[j["meta"]["role"]]+=1
            if not good and not self.c.get("continue_native_failures"):self.stop="native_or_resource_failure"
        for pid,j in self.live.items():
            if self.c.get("native_wall_s",180) is not None and time.monotonic()-j["start"]>self.c.get("native_wall_s",180) and not j["killed"]:
                j["killed"]="wall_180s";os.kill(pid,signal.SIGKILL);self.stop="wall_180s"
        if self.stop:
            for pid,j in self.live.items():
                if not j["killed"]:
                    j["killed"]="group_stop_"+self.stop
                    try:os.kill(pid,signal.SIGTERM)
                    except ProcessLookupError:pass
    def waitfor(self,pid):
        while pid in self.live:self.collect()
    def drain(self):
        while self.live:self.collect()
    def run(self):
        selected=list(self.c["modules"])
        # Interleave repetition order so warm page cache is not synonymous with a condition.
        for rep in range(3):
            conditions=["P_quiet","P_loaded","E_quiet","E_loaded"]
            conditions=conditions[rep:]+conditions[:rep]
            for condition in conditions:
                if self.stop:break
                pool=condition[0];loaded=condition.endswith("loaded")
                queue=collections.deque()
                for i,name in enumerate(selected[rep:]+selected[:rep]):queue.append(name)
                backgrounds=collections.Counter()
                def replenish():
                    if not loaded or self.stop:return
                    caps={"P":8-(pool=="P"),"E":14-(pool=="E")}
                    for p,cap in caps.items():
                        active=sum(j["meta"]["role"]=="load"and j["meta"]["pool"]==p for j in self.live.values())
                        for _ in range(max(0,cap-active)):
                            # Use measured heavy pure-computation modules as real compiler load.
                            name=self.c["load_modules"][backgrounds[p]%len(self.c["load_modules"])]
                            backgrounds[p]+=1;self.launch(name,p,condition,rep,"load",False)
                replenish()
                if loaded:
                    # Begin foreground only after native compilation load has actually started.
                    until=time.monotonic()+2
                    while time.monotonic()<until and not self.stop:self.collect();replenish()
                while queue and not self.stop:
                    name=queue.popleft();pid=self.launch(name,pool,condition,rep,"foreground",True)
                    while pid in self.live:
                        self.collect();replenish()
                    atomic(self.out/"status.json",dict(utc=utc(),condition=condition,rep=rep,foreground=self.counter["foreground"],load=self.counter["load"],active=len(self.live),stop=self.stop))
                # Do not signal normal load jobs: let all bounded real compilations finish.
                self.drain()
            if self.stop:break
        # Separate no-counter controls in quiet pools, alternating treatment order by repetition.
        for rep in range(3):
            for pool in("P","E"):
                for name in selected:
                    for perf in ([False,True]if rep%2==0 else [True,False]):
                        if self.stop:break
                        pid=self.launch(name,pool,pool+"_overhead",rep,"overhead",perf);self.waitfor(pid)
                    if self.stop:break
                if self.stop:break
            if self.stop:break
        self.drain()
        terminal=dict(utc=utc(),stop=self.stop,foreground=self.counter["foreground"],load=self.counter["load"],overhead=self.counter["overhead"],
            minimum_mem_available=self.minimum,maximum_cgroup_charge=self.maximumcharge,
            elapsed_s=time.monotonic()-self.start,full_census_started=False)
        atomic(self.out/"terminal.json",terminal);self.cg.rmdir()
        print(json.dumps(terminal),flush=True)
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--config",type=Path,required=True);ap.add_argument("--out",type=Path,required=True);a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    if(a.out/"launch.json").exists():raise RuntimeError("gate run directories are immutable; no silent resume")
    lock=open("/workspaces/.agent-state/gpu-smt-captures/pcore.lock","a")
    atomic(a.out/"waiting.json",dict(utc=utc(),pid=os.getpid(),full_census_started=False))
    fcntl.flock(lock,fcntl.LOCK_EX)
    config=json.loads(a.config.read_text());atomic(a.out/"protocol.json",config)
    Gate(config,a.out).run()
if __name__=="__main__":main()
