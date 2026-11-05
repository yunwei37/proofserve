import ProofServe.Core
open Lean ProofServe
set_option maxHeartbeats 100000

def addChecked (env : Kernel.Environment) (d : Declaration) : IO Kernel.Environment := do
  match env.addDeclCore 0 0 d (cancelTk? := none) with
  | .ok env => return env
  | .error ex => throw <| IO.userError (← ex.toMessageData {} |>.toString)

def main : IO Unit := do
  let env ← mkEmptyEnvironment
  let p := "BodyCheckP".toName
  let h := "BodyCheckH".toName
  let t := "BodyCheckTheorem".toName
  let env ← addChecked env.toKernelEnv (.axiomDecl {name:=p,levelParams:=[],type:=mkSort .zero,isUnsafe:=false})
  let env ← addChecked env (.axiomDecl {name:=h,levelParams:=[],type:=mkConst p,isUnsafe:=false})
  let v : TheoremVal := {name:=t,levelParams:=[],type:=mkConst p,value:=mkConst h,all:=[t]}
  let env ← addChecked env (.thmDecl v)
  let bad := ConstantInfo.thmInfo {v with value:=.bvar 0}
  let map : Std.HashMap Name ConstantInfo := ({} : Std.HashMap Name ConstantInfo).insert t bad
  let skipped ← env.replay map
  let mut rejected := false
  try
    validateDuplicate skipped bad "BodyCheckBadCopy".toName
  catch _ =>
    rejected := true
  unless rejected do throw <| IO.userError "skipped duplicate body escaped explicit kernel validation"
  validateDuplicate skipped (.thmInfo v) "BodyCheckValidCopy".toName
  IO.println (Json.mkObj [("upstream_skips_duplicate_body",toJson true),
    ("explicit_bad_body_rejected",toJson rejected),("valid_copy_checked",toJson true)]).compress
