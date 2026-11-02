# Whole-library native check: actual progress

Review: 自审. P0–7/shared flock/no Lean -M/external11.5GiB child cgroup/512MiB parent reserve.

- source_modules: 163097
- accepted_source_ids: 36
- accepted_dependency_ids: 7964
- missing_source_ids: 163061
- native_check_attempts: 17
- kernel_wall_s: 1314.61454653088
- kernel_cpu_s: 1313.364439
- kernel_cpu_h: 0.36482345527777776
- kernel_peak_rss_gib: 4.784229278564453
- complete: False

All costs are observed prefixes until every source ID and required native dependency is covered. No claim of validating8.3–41.6CPUh is made from partial data. LatestWsource32 scenarios207.894666–630.701677construction/10.826785–41.839086modeled streamCPUh remain separate. Source production for missing typed inputs is recorded separately. Native snapshots include only successful preceding certification; startup/reload/export/exit are included. Checkpoint frequency does not bound live environment size: failure at12GiB requires partitioning, not merely a smaller quota. Native failures/timeouts/memory events remain raw, not false mathematical verdicts.

- all: kernel_check_progress; source errors/censors=0; blocked=0.
- all: native_incomplete_partition_or_repair_required; source errors/censors=0; blocked=0.

RawPVC: /workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/whole-library-20261102. Commands: whole-library-run.py reduce; queue --cohort all; window --cohort <directory>. See whole-library-plan.md.
