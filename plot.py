from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent
figures = root / 'figures'
figures.mkdir(exist_ok=True)
r = pd.read_csv(root/'data/round_comparison.csv')
topics = pd.read_csv(root/'data/topic_comparison.csv')
metrics = ['Theory', 'Observation', 'Overall']
fig,axes=plt.subplots(1,2,figsize=(10,4.8),sharey=True)
colors=['#116b73','#ae5219']
for ax,scope in zip(axes,['All published','Bronze and HM']):
    for i,event in enumerate(['Senior','Junior']):
        a=r[(r.event==event)&(r['sample']==scope)].set_index('component').loc[metrics]
        bars=ax.bar(np.arange(3)+(i-.5)*.36,a.percentile,width=.34,color=colors[i],label=f'{event} (n={a.Bangladesh_n.iloc[0]})')
        ax.bar_label(bars,fmt='%.1f',padding=3,fontsize=9)
    ax.set(ylim=(0,100),xticks=range(3),xticklabels=metrics,title=scope)
    ax.axhline(50,color='#626669',ls=':',lw=1)
    ax.legend(frameon=False,fontsize=9)
    ax.spines[['top','right']].set_visible(False)
axes[0].set_ylabel('Mean percentile against other contestants')
fig.suptitle('Bangladesh at IOAA 2026',fontsize=18,fontweight='bold')
fig.text(.5,.025,'Each panel uses peers from the same event and award sample. Junior scores cover 2 of 5 Bangladesh entrants.',ha='center',fontsize=9)
fig.tight_layout(rect=(0,.07,1,.95))
fig.savefig(figures/'rounds.png',dpi=180)
plt.close(fig)
fig,ax=plt.subplots(figsize=(9,4.8))
ax.barh(topics.topic,topics.gap_pp,color=[colors[0] if x>=0 else colors[1] for x in topics.gap_pp])
ax.axvline(0,color='black',lw=.8)
ax.set_xlabel('Bangladesh minus other disclosed contestants (percentage points of available marks)')
ax.set_title('Junior topic results • 2 Bangladesh and 65 other scorecards')
ax.spines[['top','right']].set_visible(False)
fig.tight_layout()
fig.savefig(figures/'topics.png',dpi=180)
