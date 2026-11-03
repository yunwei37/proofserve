import ParallelCore
open Lean
def snapshot (label : String) (env : Environment) (input : Array ConstantInfo) : IO Unit := do
  let mut probes := #[]
  for name in (#["Nat.add","Nat.mul","c0","c1"] : Array String) do
    if let some ci := env.toKernelEnv.find? name.toName then
      probes := probes.push <| Json.mkObj [
        ("name",toJson name),("class",toJson (← rcKind ci).toNat)]
  let mut classes := #[0,0,0,0,0]
  for ci in input do
    let k := (← rcKind ci).toNat
    classes := classes.set! k (classes[k]!+1)
  IO.println <| Json.compress <| Json.mkObj [
    ("event",toJson "official_import_snapshot"),("label",toJson label),
    ("environment_wrapper_class",toJson (← rcKind env).toNat),
    ("kernel_base_class",toJson (← rcKind env.toKernelEnv).toNat),
    ("existing_ci",toJson probes),("input_ci_observations",toJson classes)]
unsafe def main (args : List String) : IO UInt32 := do
  initSearchPath (← findSysroot)
  let module := (args.headD "ComputeControl").toName
  let file ← findOLean module
  let mut files := #[file]
  for level in [OLeanLevel.server,OLeanLevel.private] do
    let part := level.adjustFileName file
    if ← part.pathExists then files := files.push part
  let parts ← readModuleDataParts files
  let some (first,_) := parts[0]? | throw <| IO.userError "empty module parts"
  let some (last,_) := parts[parts.size-1]? | throw <| IO.userError "empty module parts"
  let (_,s) ← importModulesCore first.imports |>.run
  let ordinary ← finalizeImport s first.imports {} 0 false false (isModule := true)
  snapshot "stock_finalize_leak_false" ordinary last.constants
  let persistent ← finalizeImport s first.imports {} 0 true false (isModule := true)
  snapshot "same_finalize_leak_true" persistent last.constants
  return 0
