#!/usr/bin/env python
import sys, os
import matplotlib
matplotlib.use("agg")
from matplotlib import pyplot as plt
import numpy as np

metric_list=["Fmax","wFmax","Smin"]
aspect_list=["MF","BP","CC"]
color_list=["black","darkgrey","lightgrey"]
curdir=os.path.dirname(os.path.abspath(__file__))
plt.figure(figsize=(7.87,2.63))
fontsize=10
width=0.4
for a,aspect in enumerate(aspect_list):
    plt.subplot(1,3,a+1)
    for t,knowledge in enumerate(["NK","LK"]):
        data_dict=dict()
        for m,metric in enumerate(metric_list):
            data_dict[metric]=[]
            filename="%s/supplementary_data/cafa3/sheets/%s_all_type%d_mode1_all_%s_sheet.csv"%(
                curdir,aspect.lower()+'o',t+1,metric.lower())
            fp=open(filename,'r')
            for line in fp.read().splitlines()[1:]:
                items=line.split(',')
                Coverage=float(items[1])
                Threshold=float(items[3])
                if Coverage>=0.9:
                    data_dict[metric].append(Threshold)
            fp.close()
            data_dict[metric]=np.array(data_dict[metric])
            mean=data_dict[metric].mean()
            print(os.path.basename(filename),len(data_dict[metric]),mean)
            plt.text(m+width*(t-0.5),mean,"%.2f"%mean,va='center',ha='center',fontsize=fontsize)
        color=color_list[t]
        plt.boxplot([data_dict[metric] for metric in metric_list],
            notch=True,positions=np.arange(len(metric_list))+width*(t-0.5),
            boxprops=dict(color=color),
            capprops=dict(color=color), 
            whiskerprops=dict(color=color,linestyle='-'),
            flierprops=dict(color=color, markeredgecolor=color),
            medianprops=dict(color=color),
            )
        plt.bar(-2,-2,edgecolor=color,facecolor='white',label=knowledge,lw=1.5)
        print("Delta %s = %.2f"%(aspect,data_dict['Smin'].mean()-data_dict['wFmax'].mean()))
    plt.ylabel("Cutoff for %s prediction"%aspect,fontsize=fontsize)
    plt.xticks(range(len(metric_list)),metric_list,fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    if True:#a==0:
        plt.legend(loc="lower right",fontsize=fontsize,ncol=len(metric_list),
            borderpad=0.1, handlelength=1, handletextpad=0.2, #borderaxespad=0.1,
            columnspacing=0.2)
    plt.axis([-0.5,len(metric_list)-0.5,-0.01,1.01])

plt.tight_layout(pad=0.1,h_pad=0.1,w_pad=0.1)
plt.savefig("check_cutoff.png",dpi=300)
