"""One finite experiment task; uses only this point's frozen code and own cgroup."""
from pathlib import Path
import json,os,sys,time
import native
ROOT=Path(__file__).resolve().parent
def main():
  label=sys.argv[1]
  threads=int(sys.argv[2])
  requests=ROOT/(label+'.json')
  env=native.environment();env['LEAN_NUM_THREADS']=str(threads)
  result=native.run(label,[native.SDK/'bin/lean','-j'+str(threads),
      '--run',ROOT/'Probe.lean',requests],limit=180,measured=True,env=env)
  (ROOT/(label+'-terminal.json')).write_text(json.dumps(result,indent=2))
  return 0 if result.get('returncode')==0 else 1
if __name__=='__main__':raise SystemExit(main())
