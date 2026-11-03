# W115: Packet cost and updated sampling uncertainty
Date:2026-11-03UTC. Review:自审.
## EXPERIMENT_GATE
Original PacketLocality compile_ok24.167262native CPU/16.947552elapsed s.
P0–7/shared lock,j8,no-M,authoredHB,3facets; raw/cleanup checked; source exact,
native retired,cgroup removed,no memory events. Published9bc03030.
Its cell90-99;101+;0 now closes with Allocated:20/21cells,40/42draws,
163057/163097modules. The missing40module cell remains unestimated.
## WRITE_GATE
Current scenario278.1052–279.0582CPUh; serial18.7807–24.7010 and
parallel25.5469–33.6134 transferred CPUh. Computation proxy20.6217–20.6923%.
These are missing-draw/calibration scenarios, not statistical confidence.
Covered20-cell HT point278.0918 and nominal t95%94.1480–462.0355CPUh,
df2.60858; missing40,heavy-tail approximation and calibration uncertainty
explicit. Two fixed precision cells now80.0456% variance. Updated small table,
README/status and exact native return; paper root-owned.
## REVIEW_GATE — 自审
Native CPU differs from elapsed; queue/setup/cleanup245.05s excluded.
Partial frame is not full-corpus CI, even with99.9755% module coverage.
No selective replacement/new weighting; old38values unchanged by driver.
## Outer audit — 自审
This changes both cost and uncertainty. Ground E29873/birth1096083 actually
launched next under master8141. Two originals remain, then fixed6+6panels.
No competing WLean, new node action, or inference from a launch to completion.
