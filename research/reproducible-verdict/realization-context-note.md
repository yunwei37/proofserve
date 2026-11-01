# Prepared import realization-context correction
2026-11-01UTC,self-review; source inspection, runtime qualification pending.
v3run_tac controls fail before their intended branch. SDK4.34.1
Environment.importModules saves an earlier import environment in its realization
context; Meta.evalExprCore may switch to importEnv? when references are imported.
setMainModule also updates that saved environment. This standalone harness did
not set a main module after import as the usual frontend setup does.

Preparedv7sets fixed ReproCandidate after import. It changes the module context;
old captures/heartbeat vectors remain separate and unchanged. This is an adapter
correction, not an upstream kernel/runtime patch. No unsupported control counted
as success. Compile/native qualification awaits current collection retirement.
