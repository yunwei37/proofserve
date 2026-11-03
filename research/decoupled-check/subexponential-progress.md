# SubexponentialSAT complete-closure measurement: actual progress

Review: 自审.

**Historical whole-library point:2488 /163097accepted source IDs;10744dependencies;0.694505kernelCPUh;32attempts/31successful;9124producer errors/151485blocked. It is partial and retired, not this SubexponentialSAT denominator.**

**SubexponentialSAT phase oracle: baseline source coverage 14721/14721 closure nodes (reused 10744, new 3977) (3977/3977targets); kernel accepts 3977/3977targets and 10744dependencies; kernelCPU 0.944251h; current segment 30; at least 0 segments (500 nodes each) remain.**

These are separate experiment costs. No global CPU estimate is formed by adding or rescaling this prefix. Producer uses official SDK/cache Meta/IR; checker consumes exact source-produced terms. Same-capture immutable shared source artifacts and actual compiler costs are charged once per complete closure; newly built targets use -o/-i/-c. This is summed source compiler work, not a fresh parallel Lake wall time. Oracle cost is a separate qualification. All timing uses P0–7/shared flock/no-M,12GiB total allocation. A complete CPU ratio requires full source, stream and original module-local coverage.

- complete: False
- phase: oracle
- target_modules: 3977
- closure_modules: 14721
- source_built: 14721
- reused_source_nodes: 10744
- new_source_nodes_built: 3977
- source_targets_built: 3977
- source_cpu_s: 46905.836649
- source_reused_cpu_s: 25373.748385
- source_new_cpu_s: 21532.088263999998
- kernel_accepted_targets: 3977
- kernel_accepted_dependencies: 10744
- kernel_cpu_s: 3399.302946
- kernel_cpu_h: 0.9442508183333332
- current_segment: 30
- remaining_segments_min: 0
- oracle_qualified: 10808
- kernel_peak_rss_gib: 14.73128890991211
- kernel_over_source_cpu: None
