import ChunkBase
import Lean
set_option maxHeartbeats 2000000
set_option maxRecDepth 20000
open Lean Elab Command Meta

@[extern "ck_cpu_ns"] opaque cpuNs : IO UInt64
@[extern "ck_thread_cpu_ns"] opaque threadCpuNs : IO UInt64

/-- No unchecked declaration insertion: only the stock checking API. -/
def checkDecl (env : Environment) (decl : Declaration) : IO Environment := do
  match env.addDeclCore 2000000000 20000 decl none with
  | .ok checked => pure checked
  | .error _ => throw <| IO.userError "original C++ kernel rejected declaration"

elab "chunked_kernel_run" : command => do
  if (← IO.getEnv "CK_PREPARE") == some "1" then return
  let k := ((← IO.getEnv "CK_K").getD "1").toNat!
  let some root ← IO.getEnv "CK_OUT" | throwError "CK_OUT is required"
  unless k == 0 || [1, 2, 4, 8].contains k do throwError "unsupported k"
  unless !(← getOptions).getBool `debug.skipKernelTC false do throwError "kernel checking disabled"
  let env ← getEnv
  let some base := env.importEnv? | throwError "missing import environment"
  let some (.defnInfo rootDef) := base.find? `ChunkBase.rootGoal | throwError "missing root"
  let mut decls := #[]
  let setupWall ← IO.monoNanosNow
  let setupCPU ← cpuNs
  if k == 0 then
    let pf ← liftTermElabM <| mkDecideProof rootDef.value
    let name := `ChunkOriginal.result
    let decl := Declaration.thmDecl {name, levelParams := [], type := rootDef.value, value := pf, all := [name]}
    let before ← IO.monoNanosNow
    let cpuBefore ← cpuNs
    let kt0 ← IO.monoNanosNow
    let kc0 ← threadCpuNs
    let checked ← checkDecl (base.setMainModule (Name.mkSimple "ChunkOriginal")) decl
    let kc1 ← threadCpuNs
    let kt1 ← IO.monoNanosNow
    writeModule checked (System.FilePath.mk root / "ChunkOriginal.olean") (writeIR := false)
    logInfo m!"CK_KERNEL 0 {kt0} {kt1} {kc1-kc0}"
    let after ← IO.monoNanosNow
    let cpuAfter ← cpuNs
    let axs ← liftTermElabM <| withEnv checked <| collectAxioms name
    logInfo m!"CK_ORIGINAL_AXIOMS {axs}"
    IO.FS.writeFile (System.FilePath.mk root / "original-type.txt") (toString rootDef.value)
    logInfo m!"CK_RESULT original {after-before} {cpuAfter-cpuBefore} 0 0"
    return
  for i in [:k] do
    let modName := Name.mkSimple s!"ChunkK{k}Part{i}"
    let goal := Name.str `ChunkBase s!"goal_{k}_{i}"
    let some (.defnInfo d) := base.find? goal | throwError "missing group {goal}"
    let proposition := if (← IO.getEnv "CK_NEGATIVE") == some "1" && i == 0 then mkConst (Name.mkSimple "False") else d.value
    let pf ← liftTermElabM <| mkDecideProof proposition
    unless !pf.hasSorry && !pf.hasMVar && !pf.hasFVar do throwError "nonclosed/sorry chunk"
    let name := Name.str modName "proof"
    decls := decls.push (modName, Declaration.thmDecl {name, levelParams := [], type := proposition, value := pf, all := [name]})
  let preparedWall ← IO.monoNanosNow
  let preparedCPU ← cpuNs
  let before ← IO.monoNanosNow
  let cpuBefore ← cpuNs
  let mut tasks := #[]
  for (modName, decl) in decls do
    let job : IO (Nat × Nat × UInt64) := do
      let kt0 ← IO.monoNanosNow
      let kc0 ← threadCpuNs
      let checked ← checkDecl (base.setMainModule modName) decl
      let kc1 ← threadCpuNs
      let kt1 ← IO.monoNanosNow
      writeModule checked (System.FilePath.mk root / s!"{modName}.olean") (writeIR := false)
      pure (kt0, kt1, kc1-kc0)
    tasks := tasks.push (← IO.asTask job)
  for i in [:tasks.size] do
    match tasks[i]!.get with
    | .error e => throwError "chunk failure: {e}"
    | .ok (kt0,kt1,kcpu) => IO.println s!"CK_KERNEL {i} {kt0} {kt1} {kcpu}"
  let after ← IO.monoNanosNow
  let cpuAfter ← cpuNs
  -- Ordinary .olean import: each new file was produced after original kernel success.
  let imports := decls.map fun (modName, _) => ({ module := modName } : Import)
  let mergeStart ← IO.monoNanosNow
  let mergeCPU ← cpuNs
  unsafe enableInitializersExecution
  let imported ← importModules imports {} (loadExts := true)
  let importStop ← IO.monoNanosNow
  let rootName := `ChunkCombined.result
  let values := decls.map fun (_, decl) => mkConst decl.getNames.head!
  let value := mkAppN (mkConst (Name.str `ChunkBase s!"merge_{k}")) values
  let combined ← checkDecl (imported.setMainModule `ChunkCombined)
    (.thmDecl {name := rootName, levelParams := [], type := rootDef.value, value, all := [rootName]})
  let finalCheckStop ← IO.monoNanosNow
  let axs ← liftTermElabM <| withEnv combined <| collectAxioms rootName
  unless axs.toList == [Name.mkSimple "propext"] do throwError "axioms differ from qualified original: {axs}"
  let some (.thmInfo done) := combined.find? rootName | throwError "final theorem absent"
  unless !done.value.hasSorry do throwError "sorry in final proof"
  unless done.type == rootDef.value do throwError "final statement changed"
  let auditStop ← IO.monoNanosNow
  writeModule combined (System.FilePath.mk root / "ChunkCombined.olean") (writeIR := false)
  let merged ← IO.monoNanosNow
  let mergedCPU ← cpuNs
  logInfo m!"CK_MERGE_PARTS {importStop-mergeStart} {finalCheckStop-importStop} {auditStop-finalCheckStop} {merged-auditStop}"
  logInfo m!"CK_RESULT chunks {after-before} {cpuAfter-cpuBefore} {merged-mergeStart} {mergedCPU-mergeCPU}"
  logInfo m!"CK_SETUP {preparedWall-setupWall} {preparedCPU-setupCPU}"
  logInfo m!"CK_VALID k={k} target_identical=true axioms=[propext] new_axioms=0 sorry=false children={decls.size}"
chunked_kernel_run
