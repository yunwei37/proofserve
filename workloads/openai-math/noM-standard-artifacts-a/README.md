# Fresh no-M compiler costs: first31cases

New convention: no Lean -M flag, owned outer15GiB charged-memory cgroup,
P0–7/j8 under shared nonblocking waiter-aware lock, one Lean process.
These are new native runs; no completed memory-pair row or legacy-Mcost is
reused.31/31compile with exact pinned source and no sorry warning. All31native
verdicts match their known legacy-Mpasses; this is a31case differential only.

Original random sample:29/42costs,12/21complete cells,163,097module frame.
The26Aendpoints use authored/defaultHB and .olean/.ilean/.c outputs.
Grid/Amplitudes retain100kHB/.olean-only and are purposefully selected;
they do not enter the original random-frame estimator.
Native process sums include import, elaboration, checking and standard output
emission, excluding Lake driver/cache setup/linking and post-exit snapshots.
No full-library CPU hours,8/24core wall forecast or globalCI is estimable until
the13missing original draws and their dependencies are resolved. No partial
cost, old-Mcost or purposeful heavy module fills a missing sample.

Grid:317.191522wall s,488.711891CPU s; Amplitudes127.044006wall s,
251.582698CPU s. All31native sum811.259308wall s,1342.922151CPU s.
Per-source/scoped sums are in cost-scopes.csv; sums are not parallel makespan.
The cohort's finite group elapsed time remains in the raw group terminal.

All31sources, expected artifacts, native identities and empty/removed
cgroups checked. No cgroupOOMkill. Max native1s sampledRSS8,227,733,504bytes,
native leader HWM8,065,924KiB, max charged cgrouppeak6,572,814,336bytes.
These differ because shared/file-backed pages may be charged outside the
native cgroup. Neither charged-memory peak nor leaderRSS alone is whole-W
aggregateRSS. The sampler includes native+controller, not separately rooted
concurrent E-core static-analysis processes; no hard whole-WRSSclaim.

Old-Mfigures stay historical/methodology only. The estimator now defaults
memory0 and never produces a new population interval for legacy memory>0.
Raw plan, commands, logs, identities, groupterminal, resource samples,
nativeartifacts and collection receipt are on PVC:
workloads/openai4341-noM-standard-a-20261031.
Recompute with estimate_native_build.py --memory-mib0 --threads8
--heartbeat-budget authored_or_native_default --outputs olean_ilean_c
--locked-only and this point's results.jsonl. No other capture input.

Next actual capture:noM original-Csuffix74jobs,72prerequisites plus unchanged
OriginalBlock81/KeySound82random endpoints. It reuses existing compiled
dependencies as compiler inputs, not their old-MCPU costs. New successful
dependencies publish their .olean sidecars only after native retirement;
failure leaves consumers uninvoked. Every new invocation omits-M.

New noM system-CPU fractions: unweighted originalA26 subset17.98%, Grid20.87%,
Amplitudes14.55%. These replace no old results; old-Msystem fractions are
methodology-only. The new proportions are not global/population wall shares
or evidence attributing every system cycle to a particular call.
