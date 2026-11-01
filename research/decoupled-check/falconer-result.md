# Complete Falconer project extension: observed status

Self-review.

- closure_modules: 13205
- successful_source_nodes: 5079
- construction_complete: False
- reused_same_capture_nodes: 5077
- source_compiler_wall_s: 5641.356517917477
- matched_stream_wall_s: None
- acceptance_parity_complete: False
- finalized_check_over_source_ratio: None
- module_local_fallbacks: None
- status: partial
- failure: {'operation': 'source_construction', 'module': 'Std.Data.DHashMap', 'key': 'build-04183'}

Only complete exit0 cells and the full per-module acceptance comparison finalize a ratio. The numerator consumes exact newly constructed artifacts. Common dependency nodes reuse actual successful compiler cells and immutable artifacts from this same pinned experiment; their work is charged once per complete dependency closure. This is summed native compiler work, not parallel Lake wall time, a whole AI source-verification speedup, or a fresh reconstruction of shared nodes. Source failure, missing typed inputs, resource/timeout and graph mismatch stay explicit. A nonzero module-local fallback count means context segmentation, not one global environment. Memory checkpoints belong to a separate profiling pass; primary timing has them disabled.
