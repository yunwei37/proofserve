from pathlib import Path
import os,datetime,subprocess,gzip,json,tarfile,time,resource
os.sched_setaffinity(0,{22,23});start=time.monotonic();r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000');s=r/'docs/tmp/build-and-evaluate'/('step-0282-'+stamp);e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-reboot-method-root-step.txt').write_text(str(s)+'\n')
owned=['docs/user-instruction.md','docs/paper/main.tex','docs/paper/main.pdf','docs/paper/references.bib','docs/research-status.md','docs/research-plan.md','research/README.md','docs/novelty-20261101.md','docs/evaluation.md','docs/cleanup-20261101.md']
for n in owned:(e/('before-'+n.replace('/','-')+'.gz')).write_bytes(gzip.compress((r/n).read_bytes()))
dirty=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=r,text=True)
(e/'entry-tracked-dirty.txt').write_text(dirty)
checks=[];prior=r/'docs/tmp/build-and-evaluate/step-0281-20261103T141838+0000'
paths=owned[1:]+[str(p.relative_to(r))for p in prior.rglob('*')if p.is_file()]
for n in paths:
 p=r/n;gitbytes=subprocess.check_output(['git','show','ac032095d469baae0c45dfe5402a5266777b9fbf:'+n],cwd=r)
 assert p.read_bytes()==gitbytes,n;checks.append({'path':n,'bytes':len(gitbytes),'matches_pushed_root0281':True})
archives=[]
for step,archive in [('step-0279-20261103T122418+0000','qualified-original-raw-source.tar.gz'),('step-0280-20261103T131855+0000','new-qualified-raw-source.tar.gz'),('step-0281-20261103T141838+0000','qualified-auxiliary-raw-source.tar.gz')]:
 p=r/'docs/tmp/build-and-evaluate'/step/'experiment-001'/archive;count=size=0
 with tarfile.open(p,'r:gz')as tar:
  for m in tar:
   if m.isfile():
    data=tar.extractfile(m).read();assert len(data)==m.size;size+=len(data);count+=1
 with gzip.open(p,'rb')as f:
  while f.read(1024*1024):pass
 archives.append({'path':str(p),'compressed_bytes':p.stat().st_size,'members_read':count,'payload_bytes_read':size,'gzip_to_EOF':True})
for p in prior.rglob('*.gz'):
 if p.name.endswith('.tar.gz'):continue
 with gzip.open(p,'rb')as f:
  while f.read(1024*1024):pass
j={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pod':os.uname().nodename,'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'uptime':Path('/proc/uptime').read_text().strip(),'branch':'main','tracked_dirty':dirty.splitlines(),'completed_root0281_files':checks,'retained_recent_archives':archives,'root_analysis_seconds':time.monotonic()-start,'root_analysis_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'new_native_runs':0}
(e/'integrity-recheck.json').write_text(json.dumps(j,indent=2)+'\n')
words="【Claude 通知：phobos-vt 已恢复，接着干】phobos-vt 在约 14:38 UTC 掉线，主机 14:48 UTC 重启（uptime 确认，原因未知），14:50 UTC Ready。Workspace 已回到 phobos-vt（Pod 6qph8），volume healthy，唯一副本 r-50a43bb5 在 phobos-vt 上，PVC 数据都在，工作盘 73%，privileged 还在。\n重启杀掉了 Workspace 里的全部进程，现在没有任何测量在跑，P 核锁是空的。掉线时正在跑的运行一律记为\"被主机重启中断\"，不计入成本或删失，也不能用作完整样本；已完成的记录要先核对完整性（重启可能截断最后写入的文件）再续跑。不要重复已完成的工作。如果掉线再次发生，不要改调度或做恢复操作，保留现场等我处理。\n仓库里有 9 个已修改未提交的文件，只动自己路径下的；推送失败就等一下重试，不要 stash 或覆盖别人的改动。连接继续用 Cloudflare 跳板：Import-Module ./scripts/fleet.psm1; & (Get-Module fleet) { $script:SshOptions += @('-J','ssh.yunwei37.com') }\n\n【主线程这一轮】先核对并提交你那部分未提交的文件。把 M 线已有的墙钟分解记为待写入：8P 的约 299 秒里，串行回退 115 秒、依赖和上下文审查 31 秒、规划 11 秒、并行波次 123 秒、未归因约 18 秒；这个分解还没有修正版重测，写进论文时标为\"部分\"。论文的方法学里写明：被主机重启打断的运行不计入任何成本数字。"
p=r/'docs/user-instruction.md';t=p.read_text();assert words not in t;p.write_text(t+'\n\n## 2026-11-03 UTC — verbatim host-reboot recovery and measurement exclusion\n\n'+words+'\n')
print('STEP',s);print('INTEGRITY',json.dumps({k:v for k,v in j.items()if k not in ['completed_root0281_files','tracked_dirty']}));print('ROOT_FILES_MATCH',len(checks))
