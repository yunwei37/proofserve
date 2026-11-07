"""Figure 1: time for a model to write each file versus Lean's time to check it.

Usage: python3 plot-gen-vs-check.py MODULES_CSV_GZ TOKENS_CSV_GZ OUTPUT [SAMPLE_CSV]
MODULES_CSV_GZ: data/openai-math-4eaee875/census/modules.csv.gz (first-check CPU time per completed module)
TOKENS_CSV_GZ:  data/generation-vs-checking/tokens.csv.gz (o200k_base tokens per module)
SAMPLE_CSV:     optional re-check sample with columns module, check_cpu_s (data/generation-vs-checking/sample.csv) (drawn as dark points)
OUTPUT:         .pdf for the paper, .png for the blog
"""
import csv
import gzip
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

mod_path, tok_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
sample_path = sys.argv[4] if len(sys.argv) > 4 else None
tokens = {r['module']: int(r['tokens']) for r in csv.DictReader(gzip.open(tok_path, 'rt', encoding='utf-8'))}
rows = [r for r in csv.DictReader(gzip.open(mod_path, 'rt', encoding='utf-8'))
        if r['status'] == 'completed' and r['module'] in tokens]
xs = [tokens[r['module']] for r in rows]
ys = [float(r['cpu_s']) for r in rows]

blog = out.endswith('.png')
plt.rcParams.update({'font.size': 11 if blog else 7, 'font.family': 'serif', 'axes.linewidth': 0.6})
fig, ax = plt.subplots(figsize=(7.0, 4.4) if blog else (3.4, 2.3), constrained_layout=True)
ax.scatter(xs, ys, s=1.5 if blog else 0.4, color='#5b7fb0', alpha=0.25, lw=0, rasterized=True,
           label='Lean, first check of each file')
if sample_path:
    sample = list(csv.DictReader(open(sample_path, encoding='utf-8')))
    ax.scatter([tokens[r['module']] for r in sample], [float(r['check_cpu_s']) for r in sample],
               s=12 if blog else 4, color='#1b2a49', lw=0, label='Lean, re-check (sample)')
lo, hi = 10, 3e6
rates = ((100, ':'), (1000, '--'), (10000, '-'))
for rate, style in rates:
    ax.plot([lo, hi], [lo / rate, hi / rate], color='#c0392b', lw=1.2 if blog else 0.8, ls=style)
u = 'OAI.Analysis.FreeWords.UltraExpectationFull'
ur = next(r for r in rows if r['module'] == u)
ax.annotate('the 450-line file:\n2.6 CPU-hours', (tokens[u], float(ur['cpu_s'])),
            xytext=(tokens[u] * 12, float(ur['cpu_s']) * 0.8), fontsize=9 if blog else 5.5,
            arrowprops=dict(arrowstyle='->', lw=0.6, color='#333333'), va='center')
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlim(lo, hi); ax.set_ylim(1e-3, 3e4)
import math
fig.canvas.draw()
for rate, style in rates:
    x0 = 25
    a = ax.transData.transform((x0, x0 / rate)); b = ax.transData.transform((x0 * 10, x0 * 10 / rate))
    angle = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    ax.text(x0, x0 / rate * 1.35, f'model writing {rate:,} tokens/s', color='#c0392b',
            fontsize=9 if blog else 5.5, ha='left', va='bottom', rotation=angle, rotation_mode='anchor')
ax.set_xlabel('Length of the file (tokens)')
ax.set_ylabel('Time (seconds)')
from matplotlib.lines import Line2D
handles = [Line2D([], [], ls='', marker='o', ms=6 if blog else 3, color='#5b7fb0', alpha=0.6,
                  label='Lean, first check of each file')]
if sample_path:
    handles.append(Line2D([], [], ls='', marker='o', ms=6 if blog else 3, color='#1b2a49',
                          label='Lean, re-check of a stored proof (sample)'))
ax.legend(handles=handles, loc='lower right', frameon=False, fontsize=9 if blog else 5.5)
fig.savefig(out, dpi=220 if blog else 300)
