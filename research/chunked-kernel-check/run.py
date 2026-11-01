"""Bounded one-Lean cells; shared P-core lock released after each retired child."""
from pathlib import Path
import os,sys,json,time,fcntl,signal,subprocess,threading,resource,argparse
HERE=Path(__file__).resolve().parent
RAW=Path('/workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check')
PROTO=RAW/'frozen-grid-v3'
SDK=Path('/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux')
LOCK=Path('/workspaces/.agent-state/gpu-smt-captures/pcore.lock')
def cell(label,k,negative=False):
    out=RAW/'runs'/label;out.mkdir(parents=True,exist_ok=False)
    env=dict(os.environ,CK_K=str(k),CK_OUT=str(out),LEAN_NUM_THREADS='8')
    env.pop('CK_PREPARE',None)
    env.pop('CK_NEGATIVE',None)
    if negative:env['CK_NEGATIVE']='1'
    old=json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime/inputs.json').read_text())
    env['LEAN_PATH']=str(out)+':'+str(PROTO)+':'+old['LEAN_PATH']
    command=[str(SDK/'bin/lean'),'--root='+str(PROTO),'-j8','-DmaxHeartbeats=2000000',
             '--load-dynlib='+str(PROTO/'clock.so'),str(PROTO/'Driver.lean')]
    waiters=subprocess.run(['lslocks','-o','PID,COMMAND,PATH,BLOCKER'],capture_output=True,text=True).stdout
    (out/'lock-before.txt').write_text(waiters)
    (out/'command.json').write_text(json.dumps(dict(argv=command,k=k,negative=negative,pcore='0-7',
        self_wall_s=180,own_tree_rss_stop_gib=14,reason_for_headroom='M16GiB includes concurrent E-core scan',
        env={n:env[n] for n in ['CK_K','CK_OUT','LEAN_NUM_THREADS','LEAN_PATH']}),indent=2)+'\n')
    with LOCK.open('a+') as lock:
      fcntl.flock(lock,fcntl.LOCK_EX)
      def child():
        os.setsid();os.sched_setaffinity(0,set(range(8)));signal.alarm(180)
      done=threading.Event();peak=[0];stops=[]
      with (out/'native.log').open('w') as log,(out/'memory.jsonl').open('w') as memory:
        start=time.monotonic()
        proc=subprocess.Popen(command,env=env,stdout=log,stderr=subprocess.STDOUT,preexec_fn=child)
        birth=Path(f'/proc/{proc.pid}/stat').read_text().split(') ',1)[1].split()[19]
        (out/'identity.json').write_text(json.dumps(dict(pid=proc.pid,birth=birth))+'\n')
        def monitor():
          while not done.is_set():
            try:
              info={}
              for d in Path('/proc').iterdir():
                if not d.name.isdigit():continue
                try:
                  fields=(d/'stat').read_text().split(') ',1)[1].split()
                  info[int(d.name)]=(int(fields[1]),int(fields[21])*os.sysconf('SC_PAGE_SIZE'))
                except (OSError,IndexError,ValueError):pass
              owned={proc.pid}
              while True:
                expanded=owned|{pid for pid,(parent,_) in info.items() if parent in owned}
                if expanded==owned:break
                owned=expanded
              rss=sum(v[1] for pid,v in info.items() if pid in owned)
              peak[0]=max(peak[0],rss)
              memory.write(json.dumps(dict(t=time.monotonic()-start,tree_rss_bytes=rss))+'\n');memory.flush()
              if rss>14*1024**3:
                stops.append('M_RSS_HEADROOM_STOP');os.killpg(proc.pid,signal.SIGKILL);return
            except OSError:pass
            done.wait(1)
        thread=threading.Thread(target=monitor);thread.start()
        _,status,ru=os.wait4(proc.pid,0);proc.returncode=os.waitstatus_to_exitcode(status)
        done.set();thread.join()
        elapsed=time.monotonic()-start
      assert not Path(f'/proc/{proc.pid}').exists()
      result=dict(label=label,k=k,negative=negative,returncode=proc.returncode,retired=True,
                  wall_s=elapsed,user_s=ru.ru_utime,system_s=ru.ru_stime,peak_rss_kib=ru.ru_maxrss,
                  sampled_tree_peak_bytes=peak[0],stop_reasons=stops,raw=str(out))
      (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
      print(json.dumps(result),flush=True)
    return result
if __name__=='__main__':
 os.sched_setaffinity(0,set(range(8,16)))
 p=argparse.ArgumentParser();p.add_argument('label');p.add_argument('k',type=int);p.add_argument('--negative',action='store_true');a=p.parse_args()
 cell(a.label,a.k,a.negative)
