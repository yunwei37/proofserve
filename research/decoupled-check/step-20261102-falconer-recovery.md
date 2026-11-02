# O step: Falconer closure recovery

Self-review. Source work is complete, not the old11,679-node checkpoint:
8,128 new +5,077 exact common=13,205 successful nodes; one recovered source
overlay fault remains0.053097s. Successful compiler wall sum22,077.770248s.

The old full primary hit1500.210998s (rc124), leaving8942 complete accepts
and a truncated JSON line; parsing that line crashed window14 and coordinator.
The independent cached-visibility attempt also hit1500.204755s (9040 accepts).
Neither yields a complete cost ratio or measured performance gain.

Implemented durable checkpointed original-kernel checking, qualified on five
native cases across18 fresh processes, including both bad-proof rejections
after restore. Untimed preparation is E-core work, not the P-core numerator.
Snapshots contain already checked terms plus pure audit metadata; delta
snapshots import only the preceding certified delta. This is a private
immutable-capture chain, not an API for trusting arbitrary submitted snapshots.

Timed work is now <=500-new-module segments, finite1400/1740s guards,
no-M, external11.75GiB child cgroup plus small parents, P0–7 FIFO flock.
Each segment independently records and commits results; no native proof
process has to live across windows. The optional queue/finalizer is not
required to resume a completed prefix. All old failures and partial stdout
remain on PVC. No source build is restarted.

Original module-local qualification is independently split into<=512-module
chunks with the frozen original checker. Exact common qualification can be
reused. Full acceptance comparison is pending. The finalizer waits on actual
queue exit events, then measures matched Mathlib checkpoint segments, and
reduces complete observed results. It never treats a queue exit as completion.

The all-stream+upper17 versus classified+upper14.33 control is reconciled:
both keep FIFO and type-conditioned upper admission; serial Grid CPU557.350
is below parallel Grid744.406, explaining the better completion count.
It is not evidence for the checker-switching mechanism or native throughput.

Current remaining limitation: P-core queue wait and native full checking.
No reliable wall ETA follows from partial counts and heterogeneous kernel
work. There is zero remaining source-construction gap. Reports/CSV contain
only observed results; complete AI/matched-Mathlib ratio remains pending.
