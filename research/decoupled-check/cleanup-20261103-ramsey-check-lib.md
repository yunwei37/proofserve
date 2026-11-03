# Retired Ramsey check-lib removal

Review: 自审.

Explicit user-directed cleanup, after a fresh all-process fd/maps/environ/cmdline/cwd/exe check found no use by the final SubexponentialSAT controller or another process. Active checker matrix configurations also contained no exact reference. Removed only the owned Ramsey check-lib tree. Original raw logs, commands, result JSON, ledger, frame, source snapshots,190-target production and20-sample/K10CSV reports remain.

{
  "utc": "2026-11-03T22:28:49.703781+00:00",
  "target": "/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/ramsey-20261102/check-lib",
  "files": 53910,
  "logical_bytes": 10072981160,
  "allocated_bytes": 10205233152,
  "single_link_allocated_bytes": 0,
  "before": {
    "total": 134951424000,
    "used": 113693478912,
    "free": 21241167872
  },
  "after": {
    "total": 134951424000,
    "used": 113686503424,
    "free": 21248143360
  },
  "observed_used_decrease_bytes": 6975488,
  "live_references": [],
  "queued_checker_configs": "no exact target reference",
  "basis": "Latest explicit instruction to remove retired Ramsey check-lib rebuildable outputs.190-target production/20-sample andK10results remain in committedCSV and progress. Entire raw Ramsey ledger/results/stdout/stderr/commands/source snapshots and all other directories retained.",
  "hardlink_limit": "Removing a pathname does not free contents while other capture links remain; observed disk delta is reported separately."
}

## Final aliases and real reclamation

The deleted check-lib contained only hardlinks. Tracing its inodes found190remaining aliases under this same retired Ramsey capture producer-ai tree. These aliases were no longer in use and had become single-link files. Removing them reclaimed the actual owned output data; shared dependency copies in active captures were not touched.

{
  "utc": "2026-11-03T22:31:38.189488+00:00",
  "path": "/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/ramsey-20261102/producer-ai",
  "removed_aliases": 190,
  "logical_bytes": 2455614280,
  "allocated_bytes": 2456064000,
  "before": {
    "total": 134951424000,
    "used": 113779716096,
    "free": 21154930688
  },
  "after": {
    "total": 134951424000,
    "used": 111323652096,
    "free": 23610994688
  },
  "observed_used_decrease_bytes": 2456064000,
  "reason": "The190remaining local aliases of the same retired Ramsey check-lib artifacts; all now single-link, no live process or current checker configuration reference. Common artifacts still linked by active SubexponentialSAT and other captures remain untouched.",
  "raw_manifest": "/workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/ramsey-20261102/cleanup-producer-ai-manifest-20261103.json"
}
