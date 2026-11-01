import OAI.Analysis.PlanarPacking.Grid
import OAI.Analysis.PlanarPacking.Certificate.UMoments9
import OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41
import Lean
set_option maxHeartbeats 1000000
set_option maxRecDepth 10000
open Lean Elab Command Meta
elab "native_chunk_census" : command => do
  let env ← getEnv
  let mods := [`OAI.Analysis.PlanarPacking.Grid,
    `OAI.Analysis.PlanarPacking.Certificate.UMoments9,
    `OAI.MathematicalPhysics.Transonic.Certificates.BarrierData41]
  let mut counts : Std.HashMap (String × String) Nat := {}
  let mut emitted : Std.HashMap (String × String) Nat := {}
  for (name, ci) in env.constants.toList do
    unless (name.toString.splitOn "_proof_").length > 1 do continue
    unless mods.any (fun mod => env.getModuleIdxFor? name == env.getModuleIdx? mod) do continue
    let .thmInfo thm := ci | continue
    unless thm.value.cleanupAnnotations.getAppFn.isConstOf (Name.mkSimple "of_decide_eq_true") do continue
    for mod in mods do
      unless env.getModuleIdxFor? name == env.getModuleIdx? mod do continue
      let (cat, detail) ← liftTermElabM do
        let mut target ← withReducible <| whnf ci.type
        if target.getAppFn.constName!.toString.endsWith "PointBox.Check" then
          target ← withTransparency .all <| whnf target
        if target.isForall then
          let dom := target.bindingDomain!
          return ("forall", toString dom.getAppFn)
        if target.isAppOfArity `Eq 3 then
          let ty ← withReducible <| whnf target.getAppArgs[0]!
          if let .const n _ := ty.getAppFn then
            if (getStructureInfo? env n).isSome then
              return ("record_equality", toString n)
          return ("atomic_equality", toString ty.getAppFn)
        if target.isAppOf `And then return ("conjunction","And")
        if target.isAppOf `Exists then return ("existential","Exists")
        return ("other",toString target.getAppFn)
      let key := (mod.toString,cat++":"++detail)
      counts := counts.insert key (counts[key]?.getD 0 + 1)
      let n := emitted[key]?.getD 0
      if n < 2 then
        IO.println s!"CK_NATIVE_EXAMPLE {mod} {name} {cat} {detail} {ci.type}"
        emitted := emitted.insert key (n+1)
  for ((mod,cat), n) in counts.toList do
    IO.println s!"CK_NATIVE_COUNT {mod} {cat} {n}"
native_chunk_census
