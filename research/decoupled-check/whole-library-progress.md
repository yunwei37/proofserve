# Whole-library native check: actual progress

Review: 自审. P0–7/shared flock/no Lean -M/external11.5GiB child cgroup/512MiB parent reserve.

**Accepted source: 2488 / 163097; certified dependencies: 10744; kernel CPU: 0.694505 h; current check: all-check-00031 (attempt 32, successful 31); remaining: at least 322 source-equivalent500-module segments.**

Missing typed inputs, new dependencies, resource failures and repeated work prevent a credible total-segment or ETA point estimate. The322-type number is only a source-count lower bound, not an extrapolated completion promise.

- source_modules: 163097
- accepted_source_ids: 2488
- accepted_dependency_ids: 10744
- missing_source_ids: 160609
- native_check_attempts: 32
- kernel_wall_s: 2509.761405901052
- kernel_cpu_s: 2500.217912
- kernel_cpu_h: 0.6945049755555556
- kernel_peak_rss_gib: 10.033504486083984
- complete: False

- source_failures_or_censors: 9124
- dependency_blocked_source_modules: 151485

## Source error classification (all retained logs)

- interpreter_unknown_declaration: 4697
- missing_native_external_implementation: 4421
- missing_module_data_file: 4
- compiler_IR_missing_executable_code_unqualified_environment: 1
- interpreter_missing_IR: 1
These are producer/import configuration and data-layout errors, not qualified proof rejections. See whole-library-source-errors.md.

All costs are observed prefixes until every source ID and required native dependency is covered. No claim of validating8.3–41.6CPUh is made from partial data. LatestWsource32 scenarios207.894666–630.701677construction/10.826785–41.839086modeled streamCPUh remain separate. Source production for missing typed inputs is recorded separately. Native snapshots include only successful preceding certification; startup/reload/export/exit are included. Checkpoint frequency does not bound live environment size: failure at12GiB requires partitioning, not merely a smaller quota. Native failures/timeouts/memory events remain raw, not false mathematical verdicts.

- all: incomplete_missing_typed_inputs; source errors/censors=9124; blocked=151485.

RawPVC: /workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/whole-library-20261102. Commands: whole-library-run.py reduce; queue --cohort all; window --cohort <directory>. See whole-library-plan.md.


<!-- current-directory-start -->
## Corrected-environment Ramsey window

Review: 自审. Historical whole-library point remains **2488 / 163097**
accepted source modules, **10744 certified dependencies**, **0.694505 kernel
CPU hours**, **9124 producer errors**, **151485 blocked source modules**.
That partial run is retired; none of these counts is silently repaired.

Current Ramsey: **source**; source **190/444**,
kernel **0/444**, freshly checked dependencies
**0**; source CPU
**13.199957 h** (new targets
**6.151694 h**), kernel CPU
**0.000000 h**; segment **0**;
at least **23** check segments remain.
Complete: **False**. [Full progress](ramsey-progress.md).

The environment fix could remove failed-producer-only ancestry blocking for
**140950 / 151485 nodes (93.05%)**, conditional on those producers actually
compiling. **10535** blocked nodes still reach missing external providers:
273 external-only and10262 mixed. These are static scheduling opportunities,
not newly accepted proofs or a global validation cost.
Next is Transonic:466 targets,5115 dependency nodes in the retained native
header DAG, pending actual full native set equality; no extra OAI subtree.
<!-- current-directory-end -->

### Ramsey complete-directory route cancelled

Ramsey producer retired at190/444targets; no Ramsey lock request remains. Full stream coverage0/444 and kernelCPU0 remain unchanged. Module-local sampling will use retained outputs; next complete directory is SubexponentialSAT, conditional on the explicit12h planning estimate. Historical whole-library counts remain2488/163097accepted,10744certified dependencies,0.694505kernelCPUh,9124producer errors/151485blocked. See [Ramsey stop](ramsey-progress.md).

<!-- retained-prefix-sample -->
Production stopped190/444; full stream0/444,0CPUh. Size sample **20/20 accepted**, **0 failures**, **0.226578 referenceCPUh**. [Sample](ramsey-sample-result.md).

<!-- subexponential-current -->
## SubexponentialSAT complete-directory attempt

Source **3400/3977**; native stream **0/3977** and **0** dependencies; new sourceCPU **5.110824h**, streamCPU **0.000000h**, segment **0**; complete **False**. [Directory progress](subexponential-progress.md).
Historical whole-library accepted2488/163097; certified dependencies10744; kernelCPU0.694505h; source errors9124/blocked151485 stay unchanged. Ramsey190/444 production is cancelled. Directory costs are not a global full-library measurement.
