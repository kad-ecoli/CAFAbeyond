#!/usr/bin/env python
import matplotlib
matplotlib.use("agg")
from matplotlib import pyplot as plt
import numpy as np
import os
from os.path import dirname, basename, abspath
resultdir=dirname(abspath(__file__))
rootdir=dirname(resultdir)

method_list=[
    ("naive_1"        ,"naive1"        ),
    ("naive_2"        ,"naive2"        ),
    ("goa_1"          ,"uniprot\ngoa"  ),
    ("blastevalue_1"  ,"blast\nevalue" ),
    ("blastlocalID_1" ,"blast\nlocal"  ),
    ("blastbitscore_1","blast\nscore1" ),
    ("blastbitscore_2","blast\nscore2" ),
    ("blastbitscore_3","blast\nscore3" ),
    ("blastglobalID_1","blast\nglobal1"),
    ("blastglobalID_2","blast\nglobal2"),
    ("blastglobalID_3","blast\nglobal3"),
    ("blastrank_1"    ,"blast\nrank"   ),
    ("blastfreq_1"    ,"blast\nfreq"   ),
    ("blastmetago_1"  ,"blast\nmetago" ),
    ("blastnetgo_1"   ,"blast\nnetgo"  ),
    ]
method_list=[(method,xtick) for method,xtick in method_list if os.path.isfile(
    "%s/%s_all_results.txt"%(resultdir,method))]
fontsize      =9
width         =0.3
color_list    =["black", "grey","white"]
xticks=[xtick for method,xtick in method_list]

for s,metric in enumerate(["Fmax","Smin","wFmax"]):
    plt.figure(figsize=(7.87,4))
    for a,Aspect in enumerate(["mf","bp","cc"]):
        ymax=0
        for k,Knowledge in enumerate(["NK","LK","PK"]):
            ax=plt.subplot(3,1,a+1)

            score_list=[]
            for m,(method,xtick) in enumerate(method_list):
                infile="%s/%s_all_results.txt"%(resultdir,method)
                score=0
                if os.path.isfile(infile):
                    fp=open(infile,'r')
                    for line in fp.read().splitlines():
                        if line.startswith("%so\t%s\tfull"%(Aspect,Knowledge)):
                            if metric=="Fmax":
                                score=float(line.split()[3])
                            elif metric=="Smin":
                                score=float(line.split()[5])
                            elif metric=="wFmax":
                                score=float(line.split()[7])
                    fp.close()
                score_list.append(score)
                plt.text(m+(k-1)*0.3,score+0.01,("%.3f"%score).lstrip('0')[:4],
                    rotation=90,fontsize=fontsize,va="bottom",ha="center")
            plt.bar(np.arange(len(score_list))+(k-1)*width,
                score_list,align="center",width=width,label=Knowledge,
                color=color_list[k],edgecolor='k')
            ymax=max((ymax,max(score_list)))
        plt.ylabel("%s %s"%(Aspect.upper(),metric
             ), labelpad=0,fontsize=fontsize)
        yticks=np.arange(0.1,1.1,0.1) if a<2 else np.arange(0,1.1,0.1)
        yticks_label=["%.1f"%y for y in yticks]
        if metric=="Smin":
            yticks=np.arange(2,20,2) if a<2 else np.arange(0,20,1)
            yticks_label=["%d"%y for y in yticks]
        plt.yticks(yticks,yticks_label,fontsize=fontsize)
        plt.xticks([])
        if a==2:
            plt.xticks(np.arange(len(score_list)),xticks,fontsize=fontsize)
        plt.axis([-0.5,len(method_list)-0.5,0,ymax*1.4])
        ax.tick_params('x',length=0)
        ax.tick_params('y',length=3)
        ax.tick_params('both',pad=0)
        if a==0:
            plt.legend(handlelength=1,ncol=3,loc="upper center",
                borderpad=0.1,handletextpad=0.2,borderaxespad=0.1,
                columnspacing=0.5,fontsize=fontsize)
    plt.tight_layout(pad=0.1,h_pad=0,w_pad=0)
    plt.savefig(metric+"_full.png",dpi=300)
