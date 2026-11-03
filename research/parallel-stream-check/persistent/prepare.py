# Materialize one same-binary toggle from the frozen fd1e9be sources.
import shutil,json
from pathlib import Path
BASE=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-attribution-20261102-v2')
ROOT=Path('/workspaces/.agent-state/gpu-smt-captures/parallel-stream-persistence-20261103')
HERE=Path(__file__).resolve().parent
def main():
    source=ROOT/'source';source.mkdir(exist_ok=False)
    for name in ['ParallelCore.lean','ParallelStream.lean','checked_commit.c','placement_profile.c']:
        shutil.copyfile(BASE/'source'/name,source/name)
    text=(source/'ParallelCore.lean').read_text()
    anchor='@[extern "ps_cpu_id"] opaque cpuId : IO UInt32\n'
    extra='''
@[extern "ps_persistence_frontier"]
opaque persistenceFrontier (base : Kernel.Environment)
    (probes : @& Array (String × ConstantInfo)) (input : @& Array ConstantInfo) :
    IO Kernel.Environment
@[extern "ps_persistence_ready"] opaque persistenceReady (base : @& Kernel.Environment) : IO Unit
@[extern "ps_persistence_summary"] opaque persistenceSummary : IO String
@[extern "ps_rc_kind"] opaque rcKind {α : Type} (value : @& α) : IO UInt8
'''
    assert text.count(anchor)==1;text=text.replace(anchor,anchor+extra)
    anchor='  let .ok metrics := Json.parse text | throw <| IO.userError "invalid native profile summary"\n'
    extra='''  let persistenceText ← persistenceSummary
  let .ok persistence := Json.parse persistenceText |
    throw <| IO.userError "invalid persistence profile summary"
'''
    assert text.count(anchor)==1;text=text.replace(anchor,anchor+extra)
    anchor='("fallback_cpu_ns",toJson fallbackCpu),("metrics",metrics)]'
    assert text.count(anchor)==1
    text=text.replace(anchor,'("fallback_cpu_ns",toJson fallbackCpu),("metrics",metrics),("persistence",persistence)]')
    anchor='  let hasPins := !((← IO.getEnv "PARALLEL_PIN_CPUS").getD "").isEmpty\n'
    extra='''  -- Before enqueue: all prior frontier tasks joined; no current worker exists.
  let diagnostic := (← IO.getEnv "PARALLEL_PERSIST_DIAGNOSTIC") == some "1"
  let probes := if diagnostic then
    (#["Nat.add","Nat.mul","c0","c1"] : Array String).filterMap fun name =>
      (base.find? name.toName).map fun ci => (name,ci)
    else #[]
  let base ← persistenceFrontier base probes plan.constants
'''
    assert text.count(anchor)==1;text=text.replace(anchor,anchor+extra)
    anchor='  gate.resolve (1 : Nat)\n'
    assert text.count(anchor)==1;text=text.replace(anchor,'  persistenceReady base\n'+anchor)
    (source/'ParallelCore.lean').write_text(text)
    shutil.copyfile(HERE/'persistence.c',source/'persistence.c')
    shutil.copyfile(HERE/'PersistenceProbe.lean',source/'PersistenceProbe.lean')
    for name in ['native.py','attribution.py']:shutil.copyfile(BASE/name,ROOT/name)
    sdk=Path('/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux')
    for name in ['LeanChecker.lean','Lean/Environment.lean','Init/System/IO.lean']:
        shutil.copyfile(sdk/'src/lean'/name,ROOT/'reference-source'/Path(name).name)
    (ROOT/'preparation.json').write_text(json.dumps(dict(base_source='fd1e9be',
      sdk_commit='5045d0056413266e57c625dcd7c365b10e377c52',
      only_intervention='official Runtime.markPersistent before worker enqueue',
      timing='same executable toggle; diagnostics off in primary runs',
      original_stream_unmodified=(source/'ParallelStream.lean').read_bytes()==(BASE/'source/ParallelStream.lean').read_bytes()),indent=2))
    print('PREPARED',ROOT)
if __name__=='__main__':main()
