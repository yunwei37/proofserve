import Lake
open Lake DSL
package proofserveChecker
lean_lib ProofServe
extern_lib libproofserve pkg := do
  let src ← inputTextFile (pkg.dir / "c" / "runtime.c")
  let obj ← buildO (pkg.buildDir / "c" / "runtime.o") src
    #["-I", (← getLeanIncludeDir).toString] #["-fPIC"] "cc"
  buildStaticLib (pkg.staticLibDir / nameToStaticLib "proofserve") #[obj]
@[default_target] lean_exe «proofserve-check» where
  root := `Main
