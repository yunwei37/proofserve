# Step021: first corrected full-closure phase; direct accounting and model scope
EXPERIMENT: the corrected source completed P1 on the actual 4,449-module
Barrier closure: native exit0, accepted ID set identical to the original
serial reference, native/cgroup retired, no resource interruption.
Wall655.448141s, CPU647.069201s, peakRSS3028.129MiB.
The same source's P2 is running inside the finite p12 phase, not complete.
A live completed-module snapshot showed original-kernel CPU8.082s onCPU0
and7.764s onCPU1; this confirms actual useful work on both cores, unlike
the retained invalid v1mapping. It is not a whole-run P2result.

P1direct account: read/context31.588236s, graph plan11.125302s, upstream
complex/cycle replay119.093597s, duplicate proof0.035407s, parallel-path
original-kernel wall occupancy474.499789s, joined-batch nonkernel1.571146s,
other residual17.534663s. These seven terms sum to the native wall.
Original-check thread CPU468.391659s and3,283,925,639allocation units cover
237,863ordinary checks. Sum of frontier maximum job CPU93.432557s yields
work/span proxy5.013153, including this scheduler's wave barriers; it is not
the inherent declaration DAGcritical path. Fallback zeros remain unobserved.

WRITE: small interim CSV/native summaries and a primary-source model note.
The result consumer now includes the planned unpinned controls, reads logical
worker counts independently of empty pin lists, excludes unfinished/resource
cells, verifies all per-thread aggregates, and emits signed phase deltas that
must sum to the measured wall delta. This analysis-only change does not touch
the frozen running source, binary or runner. The parser was exercised on the
retained v1finished records as diagnostic input and the actual corrected P1;
v1P2does not become admissible scientific evidence by parsing successfully.
An initial local text-replacement assertion stopped before writing any file;
corrected edit compiled and the real-record analyses completed.

REVIEW 自审: no full fitted serial proportion or E/P conclusion yet. P1timing
differs from historical runs even with identical work; old-source numbers are
not mixed in a fit. Full points are single fixed-order observations, so frequency
and external work remain limitations. Primary model sources were read online;
no prior-work theorem is asserted to apply directly to this scheduler.
Finite foreground series485768/birth771540558remains active, sequential phases
and one native process at a time. No host/network/config change or new agent.
Raw and frozen sources: /workspaces/.agent-state/gpu-smt-captures/parallel-stream-attribution-20261102-v2 .
