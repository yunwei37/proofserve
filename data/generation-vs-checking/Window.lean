import Lean
open Lean
set_option maxHeartbeats 2000000
set_option maxRecDepth 20000
@[extern "ck_cpu_ns"] opaque cpuNs : IO UInt64
def emit (xs : List (String × Json)) : IO Unit := do
  IO.println (Json.mkObj xs).compress
  (← IO.getStdout).flush
unsafe def main (args : List String) : IO UInt32 := do
  let [moduleName, file] := args | throw <| IO.userError "MODULE OLEAN"
  initSearchPath (← findSysroot)
  let rw0 ← IO.monoNanosNow
  let rc0 ← cpuNs
  let target := System.FilePath.mk file
  let mut files := #[target]
  let server := OLeanLevel.server.adjustFileName target
  if ← server.pathExists then
    files := files.push server
    let priv := OLeanLevel.private.adjustFileName target
    if ← priv.pathExists then files := files.push priv
  let parts ← readModuleDataParts files
  let some (first, _) := parts[0]? | throw <| IO.userError "no exported data"
  let some (data, _) := parts[parts.size-1]? | throw <| IO.userError "no module data"
  let rc1 ← cpuNs
  let rw1 ← IO.monoNanosNow
  emit [("event",toJson "read_complete"),("module",toJson moduleName),
    ("read_wall_ns",toJson (rw1-rw0)),("read_cpu_ns",toJson (rc1-rc0))]
  emit [("event",toJson "import_begin"),("module",toJson moduleName)]
  let iw0 ← IO.monoNanosNow
  let ic0 ← cpuNs
  let (_, imported) ← importModulesCore first.imports |>.run
  let env ← finalizeImport imported first.imports {} 0 false false (isModule := true)
  let ic1 ← cpuNs
  let iw1 ← IO.monoNanosNow
  emit [("event",toJson "import_complete"),("module",toJson moduleName),
    ("import_wall_ns",toJson (iw1-iw0)),("import_cpu_ns",toJson (ic1-ic0))]
  let mw0 ← IO.monoNanosNow
  let mc0 ← cpuNs
  let mut constants : Std.HashMap Name ConstantInfo := {}
  let mut eligible := 0
  for ci in data.constants do
    constants := constants.insert ci.name ci
    if !ci.isUnsafe && !ci.isPartial then eligible := eligible + 1
  let mc1 ← cpuNs
  let mw1 ← IO.monoNanosNow
  emit [("event",toJson "map_complete"),("module",toJson moduleName),
    ("map_wall_ns",toJson (mw1-mw0)),("map_cpu_ns",toJson (mc1-mc0))]
  let cw0 ← IO.monoNanosNow
  let cc0 ← cpuNs
  emit [("event",toJson "check_begin"),("module",toJson moduleName),
    ("clock_monotonic_ns",toJson cw0),("process_cpu_ns",toJson cc0)]
  try
    let checked ← env.toKernelEnv.replay constants
    let cc1 ← cpuNs
    let cw1 ← IO.monoNanosNow
    for ci in data.constants do
      if !ci.isUnsafe && !ci.isPartial then
        unless (checked.find? ci.name).isSome do throw <| IO.userError "missing replayed constant"
    emit [("event",toJson "complete"),("module",toJson moduleName),
      ("check_wall_ns",toJson ((rw1-rw0)+(mw1-mw0)+(cw1-cw0))),
      ("check_cpu_ns",toJson ((rc1-rc0)+(mc1-mc0)+(cc1-cc0))),
      ("replay_wall_ns",toJson (cw1-cw0)),("replay_cpu_ns",toJson (cc1-cc0)),
      ("eligible_entries",toJson eligible),("entries",toJson data.constants.size)]
  catch ex =>
    emit [("event",toJson "kernel_reject"),("module",toJson moduleName),("error",toJson ex.toString)]
    throw ex
  env.freeRegions
  return 0
