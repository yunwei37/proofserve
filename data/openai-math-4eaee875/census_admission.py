"""Census segment-2 admission: actual cgroups, measured family peaks, no source-cost sorting."""
import collections,heapq,math
GIB=2**30
RESOURCE={"memory_reserve","cgroup_memory_oom"}
def family(n):return n.rsplit(".",1)[0]
def root_family(n):return ".".join(n.split(".")[:3])
class Policy:
    def __init__(self,rows):
        self.peaks={};self.root_peaks={};self.risky=set();self.failures=collections.Counter()
        for r in rows:self.observe(r)
    def observe(self,r):
        n=r["module"];f=family(n);g=root_family(n);p=r.get("cgroup_peak",0)
        self.peaks[f]=max(self.peaks.get(f,0),p);self.root_peaks[g]=max(self.root_peaks.get(g,0),p)
        if r.get("interruption")in RESOURCE:
            self.risky.add(g);self.failures[n]+=1
            self.peaks[f]=max(self.peaks[f],math.ceil(p*1.5))
    def decide(self,n,engine,available):
        live=[]
        for j in list(engine.live.values()):
            try:c=int((j["cg"]/"memory.current").read_text())
            except FileNotFoundError:continue
            live.append((j["meta"]["module"],c))
        def estimate(x):return max(GIB,math.ceil(self.peaks.get(family(x),GIB)*1.25))
        reserve=sum(max(0,estimate(x)-c)for x,c in live)
        free=max(0,available-12*GIB)
        own=int((engine.cg/"memory.current").read_text())
        ancestor_headroom=None
        for q in [engine.cg,*engine.cg.parents]:
            if not(q/"memory.max").exists():continue
            v=(q/"memory.max").read_text().strip()
            if v!="max":
                h=max(0,int(v)-int((q/"memory.current").read_text()))
                ancestor_headroom=h if ancestor_headroom is None else min(ancestor_headroom,h)
        if ancestor_headroom is not None:free=min(free,max(0,ancestor_headroom-4*GIB))
        g=root_family(n);active=sum(root_family(x)==g for x,c in live)
        root_peak=max(GIB,math.ceil(self.root_peaks.get(g,GIB)*1.25))

        need=estimate(n)
        standalone=not live and available>=16*GIB
        return dict(allowed=(reserve+need<=free or standalone),standalone_prediction_exceeds_budget=standalone and need>free,
            family=family(n),risk_root=g,risky_root=g in self.risky,risk_root_active=active,
            predicted_peak_bytes=need,risk_root_peak_bytes=root_peak,reserved_future_bytes=reserve,
            available_bytes=available,ancestor_headroom_bytes=ancestor_headroom,soft_reserve_bytes=12*GIB,active_at_launch=len(live))
class Ready:
    def __init__(self):self.queues=collections.defaultdict(list)
    def push(self,n):heapq.heappush(self.queues[family(n)],n)
    def take(self,valid,admit):
        for key,q in self.queues.items():
            while q and not valid(q[0]):heapq.heappop(q)
        for n,key in sorted((q[0],key)for key,q in self.queues.items()if q):
            state=admit(n)
            if state["allowed"]:heapq.heappop(self.queues[key]);return n,state
        return None,None


def deferred_closure(prefix,pending,active,children):
    todo=[(n,None)for n in sorted(pending)if n not in active and(n==prefix or n.startswith(prefix+"."))]
    result={}
    while todo:
        n,parent=todo.pop()
        if n not in pending or n in active or n in result:continue
        result[n]=parent
        todo.extend((child,n)for child in sorted(children.get(n,())))
    return result
