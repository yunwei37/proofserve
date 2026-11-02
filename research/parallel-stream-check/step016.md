# Step016: extend original-kernel streaming beyond eight workers
EXPERIMENT: new user RQ3task. Preserved original v14source; added optional
per-executing-worker counters around a forced noinline original-kernel IO call,
100target sampling, three leaf repeats, checked-payload serialization. Default
expansion cells disable per-target logs. Same original kernel and token commit.
14GiBown sampled/charged guard remains, no-M. P-core lock still serializes timed
tasks; scaling footprints are explicitly8P,8P+4E,8P+8E,8P+16E, not homogeneous
core counts. Native collector accepts only each explicit declared affinity.

Two preparation parser failures (reserved repeat identifier; minimal Prelude
fixture lacking notation) were corrected after processes retired; failed source
and native stdout retained. Successful native short control:1,200observations
over100targets at1/4/8/16workers x3; twelve .olean snapshots byte-identical.
Corrupt original proof rejected at1/16/24workers,4native processes/cgroups retired,
no memory stop. These qualify the adapter and serializer, not the real-module
determinism/scaling result. Build peak within M16GiB, E8-15preparation only.

WRITE: extended-plan.md freezes complete Barrier closure4,449module curve
8/12/16/24, separate original-prefix/resident-leaf100target experiment. Public
snapshot boundary explicit: checked ConstantInfo substitution, original metadata
and upstream unsafe/partial exclusions; not environment-extension validation.

REVIEW 自审: current controls do not fill real curves. New requested affinity
is an authorized experiment-local footprint, no host/security/workspace change.
No O source modified; separate frozen v16PVCcopy. Broader goal remains active.
