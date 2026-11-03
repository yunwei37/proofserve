from pathlib import Path
import os,json,gzip,re,shutil,tarfile
os.sched_setaffinity(0,{22,23});r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-grid-source39-root-step.txt').read_text().strip());e=s/'experiment-001'
m=json.loads((e/'reanalysis.json').read_text());w=json.loads((e/'source39-reanalysis.json').read_text())
w['scenario_missing_check_four_times_source_CPU_h']=3*w['scenario_missing_check_twice_source_CPU_h']-2*w['scenario_missing_check_equals_source_CPU_h']
w['scenario_missing_check_twelve_times_source_CPU_h']=11*w['scenario_missing_check_twice_source_CPU_h']-10*w['scenario_missing_check_equals_source_CPU_h']
(e/'source39-reanalysis.json').write_text(json.dumps(w,indent=2)+'\n')
raw=Path(w['new_originals'][0]['raw']);assert not(raw/'native.log').read_bytes()
cmd=json.loads((raw/'command.json').read_text());assert cmd['self_wall_s']==1200
for archive in ['source39-raw-source.tar.gz']:
 count=size=0
 with tarfile.open(e/archive,'r:gz')as tf:
  for z in tf:
   if z.isfile():data=tf.extractfile(z).read();assert len(data)==z.size;count+=1;size+=len(data)
 with gzip.open(e/archive,'rb')as f:
  while f.read(1024*1024):pass
 (e/'source39-archive-integrity.json').write_text(json.dumps(dict(archive=archive,compressed_B=(e/archive).stat().st_size,members=count,payload_B=size,gzip_EOF=True))+'\n')
for name in ['grid','source39']:
 shutil.copy2('/workspaces/.agent-state/gpu-smt-paper-recovery-20261030/step0284-'+name+'-recompute.py',e/('step0284-'+name+'-recompute.py'))
sid=s.name.removeprefix('step-');tag=r'\expref{'+sid+r'}{0284}'
p=r/'docs/paper/main.tex';t=p.read_text()
t=t.replace('Source-frame coverage is now 38/42 with 19 complete strata and 4 missing','Source-frame coverage is now 39/42 with 19 complete strata and 3 missing')
t=t.replace('The 38 completed no-'+r'\texttt{-M}'+' random source targets sum to 554.806 seconds\nof native wall intervals and 867.533 user-plus-system CPU seconds.','The 39 completed no-'+r'\texttt{-M}'+' random source targets sum to 634.212 seconds\nof native wall intervals and 954.511 user-plus-system CPU seconds.')
a=t.index(r'\measured{\expref{0276-20261103T062502+0000}{0276}; one further original-frame source cost.}')
b=t.index('\nThese are source-compilation estimates',a)
t=t[:a]+r'''\measured{TAG; one further original-frame source cost.}
AllocatedForecastPrimitiveCapBound completes in 79.406 native elapsed seconds
and 86.978 CPU seconds. Its untimed E-core prerequisites receive no sampling
weight. This is the first observed draw in a 2,023-module ordinary stratum,
so the complete-stratum domain remains 161,034 modules across 19 strata.
On that unchanged domain, stratified compiler CPU remains 57.546 hours
in marked files and 189.317 hours in other files, a conditional marked share
of 23.31\%. All nine marked strata have both draws, covering 5,848 marked
modules; two ordinary strata and 2,063 ordinary modules remain incompletely
observed, with three original costs still missing.'''.replace('TAG',tag)+t[b:]
a=t.index('The two incomplete strata contain');b=t.index('\n\paragraph{Narrow missing-cost scenarios',a)
t=t[:a]+r'''The two incomplete strata contain 2,063 of 163,097 modules (1.26\%),
not necessarily that many unbuilt files. Three original source costs are absent.
The 39 known terms in the eventual complete-sample Horvitz--Thompson point
sum to 271.301 CPU-hours. This subtotal includes one observed draw from an
incomplete stratum and therefore differs from the 246.863-hour complete-stratum
subtotal. Neither is a lower confidence limit or a zero-filled population
estimate. Increasing every missing draw by one CPU second would increase
the eventual point by 0.292 CPU-hours under the fixed original weights.
This sensitivity does not predict missing costs or variance.
'''+t[b:]
a=t.index(r'\paragraph{Whole-frame costs require explicit missing-cost scenarios.}');b=t.index(r'\paragraph{Source features do not establish bounded prediction error.}',a)
t=t[:a]+r'''\paragraph{Whole-frame costs require explicit missing-cost scenarios.}
\partialev{TAG; fixed 39-source sensitivity, not measurements
or confidence limits.}
Preserving 39 known costs and original inclusion weights, assume the three
remaining ordinary-marker draws cost between the observed ordinary minimum
and maximum, 1.204525--86.977989 CPU-s.
Whole-frame construction scenarios then span 271.6--296.8 CPU-hours,
with endpoints rounded outward.
The new ordinary observation exceeds the old 40.791652-second class maximum:
the earlier 38-draw 247.5--270.3-hour scenario was an assumption,
and an additional observation need not merely narrow its range.

A separate transfer model gives 18.3--26.3 checking CPU-hours.
It assigns ordinary modules the complete checkpoint-closure CPU
fractions 0.063124--0.089514 and marked modules the older unsegmented
computation fractions 0.084421--0.084671.
This deliberately mixes protocol-specific anchors; it is neither a measured
matched protocol nor evidence that source markers identify checking cost.
The earlier 16.8--24.0-hour transfer used the 38-cost snapshot.
Neither model is measured whole-library checking cost, a confidence interval
or a guaranteed saving. Their known terms use all 39 observed draws; they
also differ from RQ2's trusted-import target checks and complete selected closures.

The LowBlock15\_1 observation remains 184.589 CPU-s, above the old
31-draw marked-class maximum of 163.846 CPU-s, another demonstration
that observed support is only an assumption.
Without missing-cost assumptions, the completion-cost upper remains unbounded.
Assigning all missing draws ten times the current observed ordinary maximum
raises the source scenario to 525.3 CPU-hours.
At the current class-maximum source scenario, giving missing draws no
checking savings yields 43.8 modeled checking CPU-hours; twice their source
work yields 69.2 and four times yields 120.0, below the 296.7-hour source value.
A separate stress assumption of twelve times their source work yields
323.2 checking CPU-hours, reversing that comparison.
These are different stress assumptions, not measured checking costs.
A subunit factor assigned to unknown modules cannot establish general benefit.
All three unobserved original source costs remain missing in the primary evidence.

'''.replace('TAG',tag)+t[b:]
old='Grid and historical Barrier retests remain incomplete and supply no\nadditional result here. No source-build or production-service speedup follows.'
assert old in t;t=t.replace(old,'The complete Grid retest is reported next; the historical Barrier retest\nremains incomplete. No source-build or production-service speedup follows.')
addition=r'''
\paragraph{The corrected computational closure also scales at a CPU cost.}
\measured{TAG; all twelve Grid processes, three repetitions per arm.}
Using the same default-persistent executable and unprofiled protocol,
the original serial stream and the one-, four- and eight-worker paths
each accept the same ordered 3,793-module closure.
Every run has 382,707 entries and 3,554 upstream unsafe/partial exclusions.
The parallel paths retain 209,672 ordinary jobs in 14,887 waves across
2,676 modules; 1,117 complex/cyclic modules use upstream replay.
No module-local context fallback occurs.

Serial and one/four/eight-worker wall medians are 561.213 and
581.429/264.097/221.614 seconds. The corresponding observed ranges are
555.326--571.886 and 579.775--582.426/263.030--265.476/217.716--223.332 seconds.
Relative to the original serial stream, four workers give 2.125-fold
and eight give 2.532-fold ratios of medians.
Native CPU medians are 558.456 and 579.927/630.129/662.182 seconds:
four and eight workers cost 12.83\% and 18.57\% more CPU than serial.
Moving from four to eight reduces wall time 16.09\% while increasing CPU
5.09\%; the one-worker prototype remains slower than the original baseline.

The new four-worker point matches the configuration family of the historical
1.882-fold Grid comparison; the eight-worker point is an additional
configuration, not a relabeled replacement. Historical raw records and table
values remain. These post-reboot observations use kernel 7.0.0-42;
the old/new difference is not normalized across that boundary or attributed
solely to persistence. The same-executable ablation above remains separate.
All twelve native scopes and the matrix controller retire normally under
the same no-\texttt{-M}, P0--7 and external memory protections.
Profiling and tracing remain off; lease waiting, sampler join and cgroup
deletion are outside the native clock.
The three ordered repeats retain caches and give ranges, not confidence
intervals or a hardware-independent scaling law.
Original mathematical checking remains, with the declared reader,
quiescence and checked-token trust. The selected closure does not establish
source-build, whole-library, service or cluster gains.
'''.replace('TAG',tag)
anchor='\n\paragraph{The complete counter matrix supports the prototype correction.}'
assert t.count(anchor)==1;t=t.replace(anchor,'\n'+addition+anchor)
p.write_text(t)
print('EDIT_PAPER',len(t),w['scenario_missing_check_four_times_source_CPU_h'],w['scenario_missing_check_twelve_times_source_CPU_h'])
