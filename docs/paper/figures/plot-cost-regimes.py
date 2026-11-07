"""Plot Figure 1 (checking cost relative to compilation) from the committed CSVs.

Usage: python3 plot-cost-regimes.py FIGURE_DIR OUTPUT_PDF
Reads cost-regimes-cpu.csv (31 module process pairs) and
cost-regimes-target-wall.csv (four single-module re-check windows).
"""
import csv
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

d, out = sys.argv[1], sys.argv[2]
cpu = list(csv.DictReader(open(os.path.join(d, 'cost-regimes-cpu.csv'), encoding='utf-8')))
wall = list(csv.DictReader(open(os.path.join(d, 'cost-regimes-target-wall.csv'), encoding='utf-8')))
blue, orange = '#1f5fa8', '#d06a1a'

plt.rcParams.update({'font.size': 7, 'font.family': 'serif', 'axes.linewidth': 0.5})
fig, (a, b) = plt.subplots(1, 2, figsize=(3.4, 1.75), constrained_layout=True,
                           gridspec_kw={'width_ratios': [1, 1.15]})
lo, hi = 0.5, 300
a.plot([lo, hi], [lo, hi], color='#888888', lw=0.6, ls='--', label='equal cost')
for marked, color, marker, label in (('0', blue, 'o', 'no decide +kernel'), ('1', orange, '^', 'decide +kernel')):
    g = [r for r in cpu if r['proxy'] == marked]
    a.scatter([float(r['source_cpu_s']) for r in g], [float(r['check_cpu_s']) for r in g],
              s=9, color=color, marker=marker, lw=0, label=f'{label} ({len(g)})')
a.set_xscale('log'); a.set_yscale('log'); a.set_xlim(lo, hi); a.set_ylim(0.3, 400)
a.set_xlabel('Compile CPU (s)'); a.set_ylabel('Check CPU (s)')
a.set_title('(a) 31 modules', fontsize=7)
handles, labels = a.get_legend_handles_labels()

names = {'Mathlib.Data.Nat.Basic': 'Nat.Basic', 'OAI.Analysis.PlanarPacking.Grid': 'Grid',
         'OAI.Analysis.PlanarPacking.Certificate.Amplitudes': 'Amplitudes',
         'OAI.MeasureTheory.Falconer.Estimates.NearPinDeletion': 'NearPin'}
rows = sorted(wall, key=lambda r: float(r['ratio_percent']))
ys = range(len(rows))
vals = [float(r['ratio_percent']) for r in rows]
b.barh(list(ys), vals, color=[orange if r['proxy'] == '1' else blue for r in rows], height=0.6)
for y, v in zip(ys, vals):
    b.text(v + 2, y, f'{v:.1f}%', va='center', fontsize=6)
b.set_yticks(list(ys)); b.set_yticklabels([names[r['module']] for r in rows])
b.set_xlim(0, 112); b.set_xticks([0, 50, 100]); b.set_xlabel('Re-check / compile (%)')
b.set_title('(b) Four modules', fontsize=7)
fig.legend(handles, ['equal cost (a)', 'no decide +kernel (a, 14)', 'decide +kernel (a, 17)'],
           loc='outside lower center', ncol=3, frameon=False, fontsize=5.5,
           handletextpad=0.2, columnspacing=0.8)
fig.savefig(out, dpi=300)
