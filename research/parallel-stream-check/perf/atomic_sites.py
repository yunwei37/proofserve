# Static atomic-opcode locations in the exact measured binary, not a timing.
import subprocess,re,json,csv,sys
from pathlib import Path
def collect(binary,out):
 out.mkdir(parents=True,exist_ok=True)
 raw=subprocess.check_output(['nm','-S','-n','-C','--defined-only',str(binary)],text=True)
 selected=[]
 for line in raw.splitlines():
  x=line.split(None,3)
  if len(x)!=4 or x[2] not in ['t','T']:continue
  start=int(x[0],16);size=int(x[1],16);name=x[3]
  if ('lean::type_checker::' in name or 'lean::instantiate' in name or
   name in ['lean_dec_ref_cold','lean_inc_ref_huge_n']):
   selected.append((start,start+size,name))
 regions=[]
 for a,b,_ in sorted(selected):
  if regions and a-regions[-1][1]<4096:regions[-1][1]=max(regions[-1][1],b)
  else:regions.append([a,b])
 sites=[];alltext=[]
 for a,b in regions:
  text=subprocess.check_output(['objdump','-d','--no-show-raw-insn','--demangle',
   '--start-address='+hex(a),'--stop-address='+hex(b),str(binary)],text=True)
  alltext.append(text);current='';begin=0
  for line in text.splitlines():
   m=re.match(r'^([0-9a-f]+) <(.+)>:$',line)
   if m:begin=int(m[1],16);current=m[2];continue
   m=re.match(r'^\s*([0-9a-f]+):\s+(.*)$',line)
   if m and 'lock ' in m[2]:
    sites.append(dict(file_address=hex(int(m[1],16)),symbol=current,symbol_offset=hex(int(m[1],16)-begin),
     opcode=m[2],known_RC_function=current in ['lean_dec_ref_cold','lean_inc_ref_huge_n']))
 (out/'selected-disassembly.txt').write_text(chr(10).join(alltext))
 with (out/'atomic-sites.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['file_address','symbol','symbol_offset','opcode','known_RC_function'])
  w.writeheader();w.writerows(sites)
 (out/'static-sites.json').write_text(json.dumps(dict(binary=str(binary),selected_symbols=len(selected),
  regions=len(regions),atomic_sites=len(sites),scope='static opcode sites; no execution or cycle claim',
  caveat='atomic opcode inside type checker is not automatically classified as RC'),indent=2))
 return len(sites)
if __name__=='__main__':print(collect(Path(sys.argv[1]),Path(sys.argv[2])))
