import Lean
open Lean
def parts (file : System.FilePath) : IO ModuleData := do
  let ps ← readModuleDataParts #[file]
  let some (data,_) := ps[0]? | throw <| IO.userError "empty parts"
  return data
def sameQuotKind (a b : QuotKind) : Bool :=
  match a, b with
  | .type, .type | .ctor, .ctor | .lift, .lift | .ind, .ind => true
  | _, _ => false

/-- Structural comparisons retain actual typed fields, not just a hash. -/
def sameConstant (a b : ConstantInfo) : Bool :=
  match a, b with
  | .axiomInfo a, .axiomInfo b => a == b
  | .defnInfo a, .defnInfo b => a == b
  | .thmInfo a, .thmInfo b => a == b
  | .opaqueInfo a, .opaqueInfo b => a == b
  | .quotInfo a, .quotInfo b =>
    a.name == b.name && a.levelParams == b.levelParams && a.type == b.type &&
    sameQuotKind a.kind b.kind
  | .inductInfo a, .inductInfo b =>
    a.name == b.name && a.levelParams == b.levelParams && a.type == b.type &&
    a.numParams == b.numParams && a.numIndices == b.numIndices &&
    a.all == b.all && a.ctors == b.ctors && a.numNested == b.numNested &&
    a.isRec == b.isRec && a.isUnsafe == b.isUnsafe && a.isReflexive == b.isReflexive
  | .ctorInfo a, .ctorInfo b => a == b
  | .recInfo a, .recInfo b => a == b
  | _, _ => false

unsafe def main (args : List String) : IO UInt32 := do
  let [mode,path] := args | throw <| IO.userError "usage: InspectArtifacts (compare|graph) INPUT"
  if mode == "compare" then
    let js ← IO.ofExcept <| Json.parse (← IO.FS.readFile path)
    for row in ← IO.ofExcept js.getArr? do
      let a ← IO.ofExcept <| row.getObjValAs? String "a"
      let b ← IO.ofExcept <| row.getObjValAs? String "b"
      let aa ← parts a
      let bb ← parts b
      let ma := aa.constants.foldl (fun m ci => m.insert ci.name ci) ({} : Std.HashMap Name ConstantInfo)
      let mb := bb.constants.foldl (fun m ci => m.insert ci.name ci) ({} : Std.HashMap Name ConstantInfo)
      let mut same := ma.size == mb.size
      for (name,ci) in ma do
        unless mb[name]?.any (sameConstant ci) do same := false
      IO.println <| Json.compress <| Json.mkObj [
        ("event",toJson "semantic_compare"),("a",toJson a),("b",toJson b),
        ("same_constants",toJson same),("a_constants",toJson ma.size),("b_constants",toJson mb.size)]
    return 0
  unless mode == "graph" do throw <| IO.userError "invalid mode"
  let data ← parts path
  let localNames := data.constants.foldl (fun s ci => s.insert ci.name) ({} : NameSet)
  for ci in data.constants do
    let kind := match ci with
      | .thmInfo _ => "theorem" | .defnInfo _ => "definition"
      | .opaqueInfo _ => "opaque" | .axiomInfo _ => "axiom"
      | .inductInfo _ => "inductive" | .ctorInfo _ => "constructor"
      | .recInfo _ => "recursor" | .quotInfo _ => "quotient"
    let refs := ci.getUsedConstantsAsSet.toList.filter localNames.contains
    IO.println <| Json.compress <| Json.mkObj [
      ("event",toJson "node"),("name",toJson ci.name.toString),("kind",toJson kind),
      ("refs",toJson <| refs.map Name.toString),("unsafe_or_partial",toJson (ci.isUnsafe || ci.isPartial))]
  return 0
