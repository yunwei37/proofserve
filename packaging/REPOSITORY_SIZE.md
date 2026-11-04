# Repository size for the operator decision

Snapshot **83f4143fb607fc9e75c9dcc7850bc3f31d1a5187**,2026-11-04UTC. No existing files were
moved, removed or rewritten. This is an E8–9 delivery observation, not a final
verification benchmark. A disposable measurement clone remains outside the
development checkout; it was not used for development.

| Quantity | Bytes | GiB |
|---|---:|---:|
| HEAD tracked file contents (30088paths) | 3902471177 | 3.634 |
| Full main-ancestor history: uncompressed blobs | 4642875887 | 4.324 |
| Existing live .git allocated storage | 3131965440 | 2.917 |
| Actual depth-one clone, complete checkout and .git | 7030562816 | 6.548 |
| Depth-one clone .git | 3030827008 | 2.823 |

The literal command was **git clone --depth 1 https://github.com/yunwei37/proofserve.git DESTINATION**
against the public proofserve repository, with a normal full checkout.
Observed wall time **1477.831s (24.63min)**.
This one network/server/CPU observation is not a promised download time.
The actual command array and clone commit are in repository-size.json.
Both clone and history inventory resolve to the same83f4143f snapshot.

Git blob bytes are logical/uncompressed; .git figures are allocated disk, not
network byte counts. The existing .git may include objects beyond the measured
main ancestry. A shallow clone still downloads the large current tree.

## Largest current-tree components

| Component | Tracked logical bytes |
|---|---:|
| artifacts | 3098680466 |
| docs | 743766571 |
| research | 27444848 |
| workloads | 24317502 |
| tools | 4512639 |
| bench | 1868227 |

Largest tracked subdirectories:

- artifacts/linarith-oracle-2026-10-17: 1463064986bytes
- docs/tmp: 733900853bytes
- artifacts/autoverus-native-2026-10-09: 468379502bytes
- artifacts/lean-parallel-verification-2026-10-12: 221683664bytes
- artifacts/leanpolish-native-2026-10-09: 195508411bytes
- artifacts/lean-gpu-checking-2026-10-13: 133639222bytes

The live artifacts directory is larger than tracked HEAD because it includes
retained untracked/dirty experimental data. Those are different measurements;
they were left untouched. Rust crates are only about0.71MB of tracked source.
Released archives and images exclude the research checkout.

## Options, not changes

- Keep the user's current decision to retain research data in this repository:
  recommend the standalone package/container; depth-one clone alone saves little.
- If that decision changes, the large raw artifacts and docs/tmp historical
  capture/log bundles are the first candidates for a separately versioned data
  archive. Retain source pins, small CSVs, analysis and stable links in the repo.
- Removing data only from a future HEAD reduces a new depth-one clone, not the
  existing full history. History rewriting or a separate repository is another
  operator decision; neither was done or prepared here.
- Generated untracked outputs do not affect clone size. Their lifecycle can be
  reviewed separately by their owners; this report is not permission to delete.

No repository settings, Git history, research files, tags or publication changed.

## Coordinator decision — 2026-11-04

Coordinator **Claude** decided to retain the research data in this repository,
following the user's earlier retention decision: **no repository slimming and
no Git history changes**. This records the coordinator's decision, not a new
direct user quote. Ordinary users should install the prepared standalone
release archive or container once published; cloning the research checkout is
not the installation requirement. The historical size measurements above
remain pinned observations, not newly measured values.

Cleaning O-owned, unreferenced Docker caches and expanded preview copies on
the PVC is separate from repository retention. It does not move/delete tracked
research data, alter Git history, or change the cited measurements.
