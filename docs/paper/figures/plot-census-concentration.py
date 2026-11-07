"""Plot compile-cost concentration and size-vs-cost for the completed census modules.

Usage: python3 plot-census-concentration.py MODULES_CSV_GZ OUTPUT_PDF
Reads data/openai-math-4eaee875/census/modules.csv.gz; P and E pools stay separate.
"""
import csv
import gzip
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

src, out = sys.argv[1], sys.argv[2]
rows = [r for r in csv.DictReader(gzip.open(src, 'rt', encoding='utf-8')) if r['status'] == 'completed']

def ranks(xs):
    order = sorted(range(len(xs)), key=xs.__getitem__)
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2
        i = j + 1
    return r

def spearman(xs, ys):
    rx, ry = ranks(xs), ranks(ys)
    n = len(xs); mx = sum(rx) / n; my = sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx = sum((a - mx) ** 2 for a in rx); vy = sum((b - my) ** 2 for b in ry)
    return cov / (vx * vy) ** 0.5

plt.rcParams.update({'font.size': 7, 'font.family': 'serif', 'axes.linewidth': 0.5})
fig, (a, b) = plt.subplots(1, 2, figsize=(3.4, 1.55), constrained_layout=True)
colors = {'P': '#1f5fa8', 'E': '#d06a1a'}
for pool in 'PE':
    g = [r for r in rows if r['pool'] == pool]
    cpu = sorted((float(r['cpu_s']) for r in g), reverse=True)
    tot = sum(cpu); n = len(cpu)
    acc, xs, ys = 0.0, [], []
    for i, c in enumerate(cpu, 1):
        acc += c
        if i <= 1000 or i % 50 == 0 or i == n:
            xs.append(100 * i / n); ys.append(100 * acc / tot)
    a.plot(xs, ys, color=colors[pool], lw=1, label=f'{pool} cores')
    top1 = sum(cpu[:max(1, n // 100)]) / tot
    print(f'{pool}: n={n} top1%={100*top1:.1f}% median={sorted(cpu)[n//2]:.2f}s '
          f'spearman(size,cpu)={spearman([float(r["source_bytes"]) for r in g], [float(r["cpu_s"]) for r in g]):.3f}')
a.set_xscale('log'); a.set_xlim(0.01, 100); a.set_ylim(0, 100)
a.set_xlabel('Modules, costliest first (%)'); a.set_ylabel('Share of CPU time (%)')
a.legend(frameon=False, loc='upper left', fontsize=6)
for marked, color, label in (('0', '#9a9a9a', 'no decide +kernel'), ('1', '#c0392b', 'decide +kernel')):
    g = [r for r in rows if r['pool'] == 'E' and r['marked'] == marked]
    b.scatter([float(r['source_bytes']) / 1024 for r in g], [float(r['cpu_s']) for r in g],
              s=0.3, color=color, alpha=0.35 if marked == '0' else 0.6, lw=0, rasterized=True, label=label)
b.set_xscale('log'); b.set_yscale('log')
b.set_xlabel('Source size (KiB)'); b.set_ylabel('E-core CPU s')
b.legend(frameon=False, loc='upper left', fontsize=5.5, markerscale=12, handletextpad=0.2)
fig.savefig(out, dpi=300)
