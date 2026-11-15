"""Plot published delegation means for each 2026 competition."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parent
rows = pd.read_csv(ROOT / 'data/overall_standings.csv')
plt.rcParams.update({'svg.fonttype': 'none', 'font.family': 'DejaVu Sans'})
green, blue, light = '#006853', '#426586', '#b3c4d1'
for event in ['Senior','Junior']:
    senior = event == 'Senior'
    field = rows[rows.event.eq(event)]
    ranked = field.dropna(subset=['observed_rank']).sort_values('observed_rank')
    groups = [ranked.iloc[:33],ranked.iloc[33:]] if senior else [ranked]
    fig, axes = plt.subplots(1,len(groups),figsize=(12,10) if senior else (9,7),squeeze=False)
    fig.subplots_adjust(left=.19 if senior else .31,right=.965,top=.89,bottom=.08 if senior else .18,wspace=.72)
    for ax, group in zip(axes.flat,groups):
        for pos, row in enumerate(group.itertuples()):
            home = row.team == 'Bangladesh'
            color = green if home else blue
            if home:
                ax.axhspan(pos-.47,pos+.47,color='#dff2e9',zorder=0)
            if pd.notna(row.mean):
                ax.hlines(pos,0,row.mean,color=light,lw=1)
                ax.scatter(row.mean,pos,s=52 if home else 28,facecolor=color if row.listed==row.scored else 'white',edgecolor=color,linewidth=1.5,zorder=3)
                ax.annotate(f'{row.mean:.1f}',(row.mean,pos),xytext=(6,0),textcoords='offset points',va='center',fontsize=8,color=color,weight='bold' if home else 'normal')
            else:
                ax.text(2,pos,'Single score • mean withheld',va='center',fontsize=8,color='#555')
        labels=[f'{int(r.observed_rank):2}   {r.team}'+('' if senior else f'   {r.scored}/{r.listed}') for r in group.itertuples()]
        ax.set_yticks(range(len(group)),labels,fontsize=9)
        for tick,team in zip(ax.get_yticklabels(),group.team):
            if team=='Bangladesh':
                tick.set_color(green)
                tick.set_weight('bold')
        ax.set_ylim(len(group)-.5,-.5)
        ax.set_xlim(0,510 if senior else 65)
        ax.set_xlabel('Mean overall score (points)')
        ax.grid(axis='x',alpha=.18)
        ax.spines[['left','right','top']].set_visible(False)
        ax.tick_params(axis='y',length=0)
    fig.suptitle(f'Bangladesh among the {event} delegations',fontsize=20,weight='bold',y=.98)
    fig.text(.5,.926,'Hanoi  •  307 scores across 65 delegation codes' if senior else 'Thailand  •  67 of 104 scores disclosed  •  labels show scored / listed',ha='center',fontsize=11)
    if senior:
        fig.text(.5,.017,'Ordered by mean overall score. Each delegation is counted once, including the second Vietnam team.',ha='center',fontsize=10)
    else:
        handles=[Line2D([],[],marker='o',linestyle='',markeredgecolor=blue,markerfacecolor=face,label=name) for face,name in [(blue,'Complete delegation'),('white','Partial disclosure')]]
        fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.069),ncol=2,frameon=False)
        missing=', '.join(f'{x.team} (0/{x.listed})' for x in field[field.scored.eq(0)].itertuples())
        fig.text(.5,.045,'No disclosed scores: '+missing,ha='center',fontsize=9)
        fig.text(.5,.014,'Positions describe available scorecards. The full-team ranking is unknown.',ha='center',fontsize=9)
    path=ROOT/'figures'/f'{event.lower()}-country-standings.svg'
    fig.savefig(path)
    plt.close(fig)
