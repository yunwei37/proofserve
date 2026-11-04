> Closeout update: source/stream primary costs below are unchanged. Reference parity stopped at14401/14721 after an isolated-root12GiB RSS failure; three malformed bodies produced six explicit rejections. See [current closeout](subexponential-closeout.md). This earlier primary-cost snapshot is retained, not a fully qualified system result.

# SubexponentialSAT primary costs after the disk stop

Review: 自审. This is a closed source/stream cost calculation, **not final qualification**. The original collector failed at disk_ceiling=0.85 after completing all source production and native stream acceptance. The original failure remains preserved. Only missing module-local references and the three bad-proof controls are being completed; no accepted source or stream work is repeated.

All3977targets and10744dependencies (14721modules) are accepted by the stream, exactly matching the measured source frame. 30segments; kernel CPU 3399.302946s (0.944251h).

| Denominator | Source CPU-s | Kernel CPU-s | CPU ratio | Summed native-child wall ratio |
|---|---:|---:|---:|---:|
| Whole closure, actual retained dependencies included |46905.836649|3399.302946|7.2471%|10.4123%|
| Newly produced targets only; same whole-closure checker |21532.088264|3399.302946|15.7871%|19.4699%|

The incremental row removes only already-paid dependency production, not dependency checking. The retained dependency CPU is actual matching-artifact production, not a forecast or a rerun. Native intervals include startup/checkpoint restoration/export. Wall values sum child intervals; they exclude lock waits, Git, reboot gaps and controller stops. Source emits olean/ilean/C, excluding C linking. Module-local qualification and negative controls are separate costs.

Memory limitation: wait4 reports a maximum child RSS of 14.731289GiB, while the largest charged cgroup peak is 10.229065GiB. These are different counters. The historical cgroup cap does not establish a12GiB RSS guarantee. The final supplemental controller separately samples its own complete tree and stops at12GiB.

The complete-frame stream result is established. Full stream/module-local acceptance-set equality and the three actual malformed-proof controls remain pending; do not infer them from the complete primary counts. The final result will explicitly retain the disk failure and [host-reboot interruption](subexponential-reboot-20261103.md). Prototype figures explain the cost regime; published-system evaluation must come from checker/ and the installed CLI.

Native final accounting: {"constants": 913323, "event": "complete", "mode": "audit", "module_local_fallbacks": 64, "modules": 14721, "retained_regions": 250, "skipped_unsafe_partial": 5318, "unique_shared_kernel_declarations": 905617}. Module acceptance follows the existing safe-declaration policy, including original module-local fallbacks; it is not replay of unsafe runtime code. Fallback costs are charged. See the retained protocol audit for source-capture deadline/reserve differences.
