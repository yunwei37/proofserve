# Step022: matched complete P1/P2 result and frontier-cost distribution
EXPERIMENT: corrected p12phase finished at2026-11-02T23:58:31Z, wall1089.594s.
Both full native points completed4,449reference IDs and retired all own native
processes/cgroups. P1wall655.448s/CPU647.069s; P2wall433.980s/CPU625.008s.
Actual P2uses both physical cores; no within-check migrations. Native14GiB
guards did not fire. No fixed whole-closure serial fraction is fitted from two
points. The complete signed accounting and same-work counters are in p12.md/CSV.

P1ordinary work/span proxy5.013and its distribution show wave-constrained
parallelism;33.69%ordinary-check CPU belongs to modules with proxy below4.
Ordinary per-module allocation sums match P1/P2in3,055observed modules,
not a claim about every unobserved declaration/fallback. CPUcost falls with
two cores despite stable allocation sums. This cautions against treating
allocation units or a single E/Pcalibration as universal time estimates.

WRITE: standalone interim table, small complete native/resource summaries,
phase delta tables, per-core/TIDplacement, top-span/module delta tables.
Offline analyzer now also checks actual emitted leaf bytes against the original
input and computes matched helper-specific P/Ecosts when det24finishes.
That pending analysis path is not an executed50-target result. Plan's raw v2path
now matches the retained actual point. Running source and binary untouched.

REVIEW 自审: direct read/context/plan/fallback terms are implementation serial
windows, not necessary dependency lower bounds. Occupancy is not CPU. The
frontier-max proxy is not inherent critical path. Single ordered full points
have no replication CI, and old timings are not pooled. All required raw and
failed v1records retained. Only owned paths; other lane dirty work preserved.
The real series progressed to p48controller487457/birth771649525, which held
the P lock at23:59:00UTC. This is verified ownership, not a scheduling promise.
Remaining phases use their existing finite sequence, one native process at a
time. Overall task remains active; no host setting, service or agent added.
