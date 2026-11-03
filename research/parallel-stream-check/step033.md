# Step033: full P4 stat returns; immediate per-cell foreground collection
EXPERIMENT_GATE: previous goal turn was progress: real controls/first full
native and sources were committed. Current P4stat completes same4,449accepted
IDs,237,863ordinary checks/3,283,925,639allocation units; all seven PMUs100%
running. Whole-command user cycles1,821,258,323,442;instructions3,339,686,815,722;
IPC1.833725;retiredL3miss loads523,881,148;lockedloads5,811,018,482;
L3HITM531,789,977;RFOHITM344,815,349. Nativewall350.946s/CPU655.014s,
CkernelCPU471.631s. This is not the later P8comparison.

Latest direct user requires decode after each returned cell and stay online.
Paused only the original controller waiting in q.wait, not its active native
or lock child. Retired unused childless after-all waiter524740. New finite
foreground collector526238/birth772873509owns actual pidfdexit waits, collects
each native, immediately decodes records, then allows original frozen controller
to spawn its next cell. Pauses again only its waiting parent. Frozen native
binary/commands/order unchanged; no second Lean, no restarted cell.
P4record526242/birth772873573really queues behind existing foreign lock.
Parent SIGSTOP is deliberate, not a deadlock or stalled native.

WRITE_GATE: small actual fullstat/timing tables/identities archived.2/16complete.
No perf-overhead estimate from just before/plain versus stat: after/plain still
missing, run drift/order can reverse signs. Native and cgroupCPU remain distinct
columns; user cycles exclude OSsystemCPU and are not yet call-scoped.

REVIEW_GATE 自审: PIDbirth, native retirement, actual counts/counter coverage
checked. Same reference work, unknown future values remain missing. All failed
qualification data preserved. Offline decode serial relative to own native,
14GiBnative guard/1GiBdecode guard on existing permitted CPUs. No Lean/sysctl
change. Foreign files/locks untouched. Full study remains active until16returns
or actual failure; do not mark resource/cause/goal complete at this boundary.
