"""Post-hoc instruction localization in the exact frozen fd1e9be fixture."""
import csv,gzip,collections,sys
from pathlib import Path
roles={
 'lean_environment_find':{
  0xc:'inner_RC_header_load',0xe:'after_inner_RC_header_load',
  0x1a:'environment_RC_header_load',0x1c:'after_environment_RC_header_load',
  0x72:'inner_RC_header_load_at_release',0x74:'after_inner_RC_header_load_at_release',
  0xcf:'inner_atomic_RC_update',0xd2:'after_inner_atomic_RC_update'},
 'lean::environment::find(lean::name const&) const':{
  0xd:'receiver_RC_header_load',0xf:'after_receiver_RC_header_load',
  0x20:'name_RC_header_load',0x22:'after_name_RC_header_load',
  0x46:'receiver_atomic_RC_update',0x49:'after_receiver_atomic_RC_update',
  0x55:'name_atomic_RC_update',0x58:'after_name_atomic_RC_update'},
 'lean_dec_ref_cold':{
  0:'outer_RC_header_load',2:'after_outer_RC_header_load',
  0xe:'outer_atomic_RC_update',0x11:'after_outer_atomic_RC_update',
  0x67:'child_RC_header_load',0x69:'after_child_RC_header_load',
  0x8e:'child_atomic_RC_update',0x91:'after_child_atomic_RC_update'}}
def main():
 root=Path(sys.argv[1]);out=Path(sys.argv[2]);counts=collections.Counter()
 for d in sorted(root.glob('decode-full-record-P*-r1')):
  p=d/'address-periods.csv.gz'
  if not p.exists():continue
  key=d.name.removeprefix('decode-')
  with gzip.open(p,'rt') as f:
   for x in csv.DictReader(f):
    fn=x['leaf_symbol']
    if fn not in roles:continue
    off=int(x['symbol_offset'])if x['symbol_offset']else None
    role=roles[fn].get(off,'other_or_unknown_instruction')
    counts[(key,x['scope'],fn,off,role)]+=int(x['sampled_period'])
 with out.open('w',newline='') as f:
  w=csv.writer(f,lineterminator=chr(10));w.writerow(['key','scope','function','symbol_offset','instruction_role','estimated_sampled_cycles'])
  for k,v in counts.items():w.writerow([*k,v])
if __name__=='__main__':main()
