# SubexponentialSAT complete-closure measurement: actual progress

Review: 自审.

**Historical whole-library point:2488 /163097accepted source IDs;10744dependencies;0.694505kernelCPUh;32attempts/31successful;9124producer errors/151485blocked. It is partial and retired, not this SubexponentialSAT denominator.**

**SubexponentialSAT phase source: baseline source coverage 12169/14721 closure nodes (reused 10744, new 1425) (1425/3977targets); kernel accepts 0/3977targets and 0dependencies; kernelCPU 0.000000h; current segment 0; at least 30 segments (500 nodes each) remain.**

These are separate experiment costs. No global CPU estimate is formed by adding or rescaling this prefix. Producer uses official SDK/cache Meta/IR; checker consumes exact source-produced terms. Same-capture immutable shared source artifacts and actual compiler costs are charged once per complete closure; newly built targets use -o/-i/-c. This is summed source compiler work, not a fresh parallel Lake wall time. Oracle cost is a separate qualification. All timing uses P0–7/shared flock/no-M,12GiB total allocation. A complete CPU ratio requires full source, stream and original module-local coverage.

- complete: False
- phase: source
- target_modules: 3977
- closure_modules: 14721
- source_built: 12169
- reused_source_nodes: 10744
- new_source_nodes_built: 1425
- source_targets_built: 1425
- source_cpu_s: 33350.440086
- source_reused_cpu_s: 25373.748385
- source_new_cpu_s: 7976.691701
- kernel_accepted_targets: 0
- kernel_accepted_dependencies: 0
- kernel_cpu_s: 0
- kernel_cpu_h: 0.0
- current_segment: 0
- remaining_segments_min: 30
- oracle_qualified: 10744
- kernel_peak_rss_gib: 0.0
- kernel_over_source_cpu: None
