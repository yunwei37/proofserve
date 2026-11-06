from pathlib import Path
import json,os,time,sys,datetime,fcntl,traceback
raw=Path(__file__).resolve().parent
lock=(raw/'.driver.lock').open('a+')
fcntl.flock(lock,fcntl.LOCK_EX)
cfg=json.loads((raw/'config.json').read_text())
rows=json.loads((raw/'completed.json').read_text())
skip=['grid-P8-strict-theorem-bodies-r1','grid-P8-strict-theorem-bodies-r2','grid-P8-strict-theorem-bodies-r3']
remaining=224718.02+21600-time.clock_gettime(time.CLOCK_BOOTTIME)
assert remaining>0
cfg['matrix_limit_s']=sum(r['wall_s']for r in rows)+remaining
cfg['continuation_note']='Skip the retained 1800s strict Grid timeout and its two unattempted repeats; finish other originally planned cells within original six-hour deadline.'
cfg['original_six_hour_deadline_boottime_s']=224718.02+21600
path=raw/'continuation-config.json';path.write_text(json.dumps(cfg,indent=2)+'\n')
original=json.loads((raw/'planned-cells.json').read_text())
(raw/'primary-phase-terminal.json').write_text((raw/'phase-terminal.json').read_text())
identity=dict(pid=os.getpid(),birth=Path('/proc/self/stat').read_text().rsplit(')',1)[1].split()[19],
  utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),native_commit=cfg['commit'],
  original_deadline_boottime_s=cfg['original_six_hour_deadline_boottime_s'],skipped=skip,
  reasons={'grid-P8-strict-theorem-bodies-r1':'retained per-cell timeout, not kernel rejection',
   'grid-P8-strict-theorem-bodies-r2':'not run after first strict point exceeded fixed per-cell cap',
   'grid-P8-strict-theorem-bodies-r3':'not run after first strict point exceeded fixed per-cell cap'})
(raw/'continuation-controller.json').write_text(json.dumps(identity,indent=2)+'\n')
(raw/'phase-terminal.json').write_text(json.dumps(dict(complete=False,status='continuing_remaining_original_cells',phase='matrix',**identity),indent=2)+'\n')
sys.path.insert(0,str(raw/'frozen/bench'))
import matrix
old_cells=matrix.cells
matrix.cells=lambda c:(x for x in old_cells(c)if x['key']not in skip)
old_dump=matrix.dump
def dump(p,value):
 if p==raw/'planned-cells.json':p=raw/'continuation-planned-cells.json'
 elif p==raw/'terminal.json':p=raw/'continuation-terminal.json'
 old_dump(p,value)
matrix.dump=dump
sys.argv=[str(raw/'frozen/bench/matrix.py'),str(path)]
status='returned';error=None
try:matrix.main()
except BaseException as e:
 status='failed';error=repr(e);traceback.print_exc()
finally:
 done=json.loads((raw/'completed.json').read_text())
 by={r['key']:r for r in done}
 missing=[dict(c,reason=identity['reasons'].get(c['key'],'not reached before continuation stopped'))for c in original if c['key']not in by]
 failures=[r for r in done if r['returncode']!=0 and not r.get('manual_interruption')and r['arm']!='bad-control']
 end=dict(complete=False,phase='matrix',status='collection_finished_with_incomplete_cells'if status=='returned'else'collection_failed',
  original_planned_cells=len(original),returned_cells=len(done),failures=failures,unattempted=missing,
  native_commit=cfg['commit'],error=error,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
  handoff_ready=status=='returned',overall_original_matrix_complete=False)
 old_dump(raw/'collection-terminal.json',end);old_dump(raw/'phase-terminal.json',end)
 print('COLLECTION_RETURN',json.dumps(end),flush=True)
if status!='returned':raise SystemExit(1)
