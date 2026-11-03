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
## Corrected-environment directory continuation

Updated 2026-11-03T00:10:49.967144+00:00; review: 自审.

The retired whole-library point is still **2488 / 163097 accepted source
modules**, **10744 certified dependencies**, **0.694505 kernel CPU hours**,
**9124 failed producer calls**, and **151485 blocked source modules**.
No successful result is imputed to the missing or environment-failed nodes.

Current Ramsey phase: **source**. Source **2/444** targets,
kernel **0/444** targets,
**0** freshly checked dependencies;
kernel CPU **0.000000 h**, new target source CPU
**0.001467 h**. The source denominator additionally includes
**7.048263 h** of measured, immutable common dependency construction.
Current check segment **0**, at least
**23** segments remain.
See [Ramsey progress](ramsey-progress.md). The complete ratio remains unavailable.

The corrected producer has passed the four actual controls. It removes the
known environment cause; it does not establish that every released source
will elaborate or fit the experimental task bound. Of the 151485 blocked
nodes, **140950 (93.05%)** have only failed-producer ancestry in the retained
DAG and could become schedulable if those producers succeed. **10535**
still reach missing external providers (273 external-only;10262 mixed).
These are structural opportunities, not 140950 newly accepted proofs.

The next directory selected after Ramsey is **Transonic (466 targets)**:
31 external roots, all outside OAI; no additional OAI subtree is required.
PlanarPacking (562 targets) additionally requires an OAI Triangular module,
so Transonic is the smaller self-contained next comparison. It is prepared
offline only until Ramsey and its reference checks actually finish.
<!-- current-directory-end -->
