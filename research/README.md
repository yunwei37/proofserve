# Research result index

Updated2026-11-01UTC. [Current status](../docs/research-status.md) ·
[Plan](../docs/research-plan.md) · [Paper](../docs/paper/main.tex) ·
[Evaluation](../docs/evaluation.md). Research roots and their main
result families are indexed below; plans/code aren't completed measurements.

| Directory | What it did / key evidence | Reports and entry points | Raw PVC root |
|---|---|---|---|
| [mechanisms-2026-10-30](mechanisms-2026-10-30/README.md) | Historical tactic/profile, certificate and resource/scheduling experiments. Old-Mprofiler changes7/200error flags;7+7row proofs accept, old-Mcost rankings not current speed results. | [Profiler](mechanisms-2026-10-30/profiler-heartbeat-methodology.md), [native200](mechanisms-2026-10-30/native-cohort-result.md), [certificate7](mechanisms-2026-10-30/openai-kernel-sample/README.md), [memory](mechanisms-2026-10-30/memory-budget-conclusion.md), [prior work](mechanisms-2026-10-30/prior-work.md) | /workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/ |
| [profile-2026-10-31](profile-2026-10-31/systime/final/README.md) | Guard calibration90cells/3modules: M/noMwall ratios2.03/1.61/1.01, observed output parity. Methodology only. Separate noMstockchecker15targets pass,13short median3.510s, not exclusive kernel cost. | [System calibration](profile-2026-10-31/systime/final/README.md), [startup/replay](profile-2026-10-31/startup-replay/README.md), [repaired replay](profile-2026-10-31/startup-replay/repaired-replay-analysis.md) | /workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/ |
| [chunked-kernel-check](chunked-kernel-check/README.md) | Grain31artifacts complete. Barrier15cell/99stage localmodule replay46.992s directstock vs14.127s/8workers,3.326x/CPU+27.8%, exact3425typedconstants. Safeacyclic forms/trustedimports; notsource/library throughput. Envelope15cells: kernel6.292x but prepared-runtime1.096x, CPU+53.6%, one repeat0.949x; imports/merging absorb gain. BothsmallGridpartition points remain whole-pathnegative. | [Envelope](chunked-kernel-check/envelope-result.md), [Barrier](chunked-kernel-check/parallel-result.md), [grain](chunked-kernel-check/step-006-report.md), [flat](chunked-kernel-check/v3-result.md) | /workspaces/.agent-state/gpu-smt-captures/chunked-kernel-check/parallel-barrier-v1; declaration-distribution-v1/; envelope-curve-v3/ |
| [decoupled-check](decoupled-check/README.md) | Fourcomplete selectedclosures share5085unique sourcebuilds and161oraclechunks: Mathlib10.56%, NearPin6.76%, Grid14.52%, Amplitudes14.55%check/sourcework. Targetread-map-replay ratios6.54/0.46/80.28/82.35%are components, notlatencies. Osourcepeak7.57GiB exceedsO4share, actualcap11.875GiB; sharedcontext qualification unresolved. | [Allcohorts](decoupled-check/results.md), [components](decoupled-check/root-components.csv), [originalMathlib](decoupled-check/math-closed-result.md), [rootaudit](../docs/tmp/build-and-evaluate/step-0235-20261101T041713+0000/step-report.md) | /workspaces/.agent-state/gpu-smt-captures/decoupled-check-20261031/ |
| [parallel-stream-check](parallel-stream-check/README.md) | Combined in-memory prototype: v4accepts malformed cyclicTrueproofdata aftersiblingbinding; samebinary module-localpath rejects. Repaired1/8reject,20controls/22native receipts;18cellv4curve stayshistorical; freshv14complete18cell/1330modulepairing68.605→45.050s,1.523x/CPU+36.3%, fixed-order3reps. Coordinator/Cinsertion add implementationTCB. Repairedv14Grid leaf8=65.856s vs265.010serial,4.024x/CPU+97.76%, oneorderedobservation; earlierunderfilledv12historical. Actualfullpairs:Barrier474.851→304.862s/uniform4=1.558x/CPU+24.6%; Grid557.568→296.293s=1.882x/CPU+33.6%, referencepreservedacrosscontrollerrepairgap. Onepair/closure; fullnativeclockendswait4. V14Barrier4449closure:target53.960→10.186s/8requestedworkers,5.297x/CPU+48.6%, oneorderedobservation; differentfromoldfragmentpipeline. All10Envelopehelpers/80children/10merges kernelqualified plus2negativecontrols, importedprefixtrusted; v14coldprefix10752modules+9leaftrials complete:chunk8vsdecl8=1.319x/CPU+5.2%,oneobservation; no completed fullsinglemode/serialclosure pair; separateoriginalserialattempt rc124at1680.158s/10744completeaccepts of10752plus222bytepartialrecord,nomathreject/RSSstop/OOM; rootstep0245. SampledRSS13.971GiBvswait4peak14.019GiB;v10failure retained. | [Full Barrier pair](parallel-stream-check/full-barrier-results.md), [Full Grid pair](parallel-stream-check/full-grid-results.md), [Repaired Grid](parallel-stream-check/grid-repaired-results.md), [Envelope cold-prefix target sequence](parallel-stream-check/envelope-stream-results.md), [Repaired matrix](parallel-stream-check/v14-math-results.md), [Version boundary](parallel-stream-check/math-results.md), [protocol](parallel-stream-check/protocol.md), [repair](parallel-stream-check/step004.md) | /workspaces/.agent-state/gpu-smt-captures/parallel-stream-check-v4/ and parallel-stream-check-v10/; parallel-stream-check-v12/; parallel-stream-check-v14/ |

## Workload evidence outside research/
- [W current state](../workloads/W-status.md) owns actual capture/retirement status.
- [openai/math](../workloads/openai-math/README.md):163097modules/1.354Mlexical
  decide+kernel, not executions or cost weights.
- [Fresh noM31](../workloads/openai-math/noM-standard-artifacts-a/README.md):
  Rootstep0238collectsW48:46deps+2draws;31/42random costs/14complete strata.
- [Conditional marked-file costs](../workloads/openai-math/cost-regimes-noM/README.md):
  17.1434%markedcompilationCPU estimate only within103468modules/14complete strata;
  59629modules/1164marked missing; no finiteglobalCPUestimate/informativeglobalshare.
- [NoM26dependency prefix](../workloads/openai-math/noM-original-c-prefix26/README.md):
  successful prerequisites, no new random endpoint, yielded lock.
- [Generated software](../workloads/ai-verification-software/README.md):
  Vero, released Vericoding outputs and LKVfixtures differ in provenance/trust.

W raw captures: /workspaces/.agent-state/gpu-smt-captures/workloads/
Pinned sources/toolchains: /workspaces/.agent-state/gpu-smt-workloads/
Small derived tables/reports are committed. Original commands/artifacts,
failed/partial data retain recorded PVC paths. Old-Mfigures are historical,
not currentcost inputs. Reviews are **自审**, not independent acceptance.

## Root source comparison and paper integration
[Step0231](../docs/tmp/build-and-evaluate/step-0231-20261101T001556+0000/step-report.md):
freshsame-maskMathlib/openaicomparison7/4vs1354379/5848,10668.32xsites/MB;
3.5856%positivegeneratedfiles, notCPUshare. Rawfixedarchive andsourcecensus:
/workspaces/.agent-state/gpu-smt-captures/step-0231-20261101T001556+0000-static/source.tar.gz. Two scans agree; no-M31results independentlyaudited.
Old8/5Mathlibfigureincludesadocumentationcomment. Nativeweights remainopen.

[Collected W48/current original-frame reduction](../docs/tmp/build-and-evaluate/step-0238-20261101T061522+0000/step-report.md): complete48processes, not48draws. Small per-draw andstratum tables in thatstep; fullraw /workspaces/.agent-state/gpu-smt-captures/workloads/openai4341-noM-original-c-suffix48-prepared-20261101/.

[Rootstep0239 failed combined-stream capture](../docs/tmp/build-and-evaluate/step-0239-20261101T062456+0000/step-report.md): Envelope-stream-r1 return-9 after1313.600s/sample15,697,940,480B vs14GiBsampledstop; charged9,738,059,776B. No kernelOOMevent. Allsampled native identities/controller nowretired; initialcgroupcleanup-pending record retained, cgroup nowabsent. TotalnativeCPUunknown (timeout-parent wait4nearzero is not descendantCPU). Notmathematicalrejection/completecurve/speedup. No automaticrerun or budgetincrease; originalsmallEnvelopev3curve unaffected.

[Envelope full-reference timeout](../docs/tmp/build-and-evaluate/step-0245-20261101T111249+0000/step-report.md): raw parallel-stream-check-v14/runs/envelope-full-reference1-r1; incomplete accepted-record set is not a completed-input parity counterexample or speedup.
