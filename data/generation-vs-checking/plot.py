"""One source-size/latency figure; scenario lines are not generator measurements."""
from pathlib import Path
import sys,os,csv,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
out=Path(sys.argv[1]);rows=list(csv.DictReader((out/'sample.csv').open()));s=json.loads((out/'summary.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(11,4.7),sharex=True,sharey=True)
positive=[int(r['tokens'])for r in rows if int(r['tokens'])>0]
x=np.geomspace(max(1,min(positive)*.7),max(positive)*1.5,180)
for ax,metric,title in zip(axes,['check_wall_s','check_plus_import_wall_s'],['Own-module read + map + replay','Including dependency import']):
 for rate,style in [(100,'-'),(1000,'--'),(10000,':')]:
  ax.plot(x,x/rate,color='#666666',ls=style,lw=1,label=f'Source output at {rate:,} token/s')
 for marked,color,label in [('0','#2166ac','No decide +kernel'),('1','#d6604d','Contains decide +kernel')]:
  good=[r for r in rows if r['status']=='accepted'and r['has_decide_plus_kernel']==marked and int(r['tokens'])>0]
  ax.scatter([int(r['tokens'])for r in good],[max(float(r[metric]),1e-7)for r in good],s=23,c=color,alpha=.75,edgecolors='none',label=label)
  lower=metric.removesuffix('_s')+'_observed_lower_s'
  cens=[r for r in rows if r['status']!='accepted'and r['has_decide_plus_kernel']==marked and int(r['tokens'])>0 and float(r[lower])>0]
  for r in cens:
   y=float(r[lower]);xx=int(r['tokens'])
   ax.scatter([xx],[y],marker='^',c=color,s=38)
   ax.annotate('',xy=(xx,y*1.9),xytext=(xx,y),arrowprops={'arrowstyle':'->','color':color,'lw':1})
 ax.set_xscale('log');ax.set_yscale('log');ax.set_title(title);ax.set_xlabel('Complete source file tokens (o200k_base)')
 ax.grid(alpha=.18,which='major');ax.set_ylabel('Wall seconds')
handles,labels=axes[0].get_legend_handles_labels()
fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.5,.045),ncol=3,frameon=False,fontsize=8)
n_ok=sum(r['status']=='accepted'for r in rows);n_cens=sum(r['right_censored']=='True'for r in rows)
fig.suptitle(f'{len(rows)} sampled modules: {n_ok} completed, {n_cens} time-censored; one P core per process',fontsize=11)
fig.text(.5,.015,'Fixed stratified sample, not population prevalence. Source-output lines are scenarios, not measured AI generation.',ha='center',fontsize=7)
fig.subplots_adjust(left=.07,right=.985,bottom=.25,top=.85,wspace=.18)
fig.savefig(out/'generation-vs-checking.png',dpi=180)
fig.savefig(out/'generation-vs-checking.svg')
fig.savefig(out/'generation-vs-checking.pdf')

svg=out/'generation-vs-checking.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
