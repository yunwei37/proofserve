# Ramsey complete-closure measurement: actual progress

Review: 自审.

**Historical whole-library point:2488 /163097accepted source IDs;10744dependencies;0.694505kernelCPUh;32attempts/31successful;9124producer errors/151485blocked. It is partial and retired, not this Ramsey denominator.**

**Ramsey phase source: baseline source coverage 10924/11188 closure nodes (reused 10744, new 180) (180/444targets); kernel accepts 0/444targets and 0dependencies; kernelCPU 0.000000h; current segment 0; at least 23 segments (500 nodes each) remain.**

These are separate experiment costs. No global CPU estimate is formed by adding or rescaling this prefix. Producer uses official SDK/cache Meta/IR; checker consumes exact source-produced terms. Same-capture immutable shared source artifacts and actual compiler costs are charged once per complete closure; newly built targets use -o/-i/-c. This is summed source compiler work, not a fresh parallel Lake wall time. Oracle cost is a separate qualification. All timing uses P0–7/shared flock/no-M,12GiB total allocation. A complete CPU ratio requires full source, stream and original module-local coverage.

- complete: False
- phase: source
- target_modules: 444
- closure_modules: 11188
- source_built: 10924
- reused_source_nodes: 10744
- new_source_nodes_built: 180
- source_targets_built: 180
- source_cpu_s: 40998.65352
- source_reused_cpu_s: 25373.748385
- source_new_cpu_s: 15624.905135
- kernel_accepted_targets: 0
- kernel_accepted_dependencies: 0
- kernel_cpu_s: 0
- kernel_cpu_h: 0.0
- current_segment: 0
- remaining_segments_min: 23
- oracle_qualified: 10744
- kernel_peak_rss_gib: 0.0
- kernel_over_source_cpu: None
