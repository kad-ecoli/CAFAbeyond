#!/usr/bin/env python
docstring='''predict_tmalign.py target.9606.tm _9606_go.txt
    use tmalign baseline to predict GO terms for input file target.9606.tm
output:
    tmalignfreq_1_9606_go.txt     - N(GOterm) / N
    tmalignID_3_9606_go.txt       - freq weighted by globalID
    tmalignTM_3_9606_go.txt       - freq weighted by TM-score
    tmalignTMID_3_9606_go.txt     - freq weighted by TM-score * globalID
'''
import sys
from os.path import dirname, basename, abspath, isfile
from subprocess import Popen,PIPE
from math import exp
import gzip
bindir=dirname(abspath(__file__))
rootdir=dirname(bindir)
datdir=rootdir+"/data"

def read_annotation():
    annotation_dict=dict()
    for Aspect in "FPC":
        annotation_dict[Aspect]=dict()
        filename=datdir+"/uniprot_sprot_exp."+Aspect
        fp=open(filename,'r')
        for line in fp.read().splitlines():
            target,GOterm_list=line.split('\t')
            annotation_dict[Aspect][target]=GOterm_list.split(',')
        fp.close()
    return annotation_dict

def read_tmalign(infile):
    tmalign_dict=dict()
    if isfile(infile):
        fp=open(infile,'r')
    else:
        fp=gzip.open(infile+".gz",'r')
    for line in fp.read().splitlines():
        if line.startswith('#'):
            continue
        items=line.split('\t')
        if len(items)!=11:
            continue
        qacc,sacc,TM1,TM2,RMSD,ID1,ID2,IDali,qlen,slen,length=items
        TM1=float(TM1)
        TM2=float(TM2)
        if max((TM1,TM2))<0.5:
            continue
        ID1=float(ID1)
        ID2=float(ID2)
        TM=min((TM1,TM2))
        ID=min((ID1,ID2))
        if not qacc in tmalign_dict:
            print("parsing "+qacc)
            tmalign_dict[qacc]=[]
        tmalign_dict[qacc].append([TM*ID,sacc,
            1.,
            ID,
            TM,
            TM*ID,
            ])
    fp.close()
    for qacc in tmalign_dict: # sort by descending TM-score
        tmalign_dict[qacc]=[items[1:] for items in sorted(tmalign_dict[qacc],reverse=True)]
    return tmalign_dict

def write_output(tmalign_dict,annotation_dict,suffix):
    method_list=[
        "tmalignfreq_1",    # 0 - N(GOterm) / N
        "tmalignID_3",      # 1 - freq weighted by globalID
        "tmalignTM_3",      # 2 - freq weighted by TM-score
        "tmalignTMID_3",    # 3 - freq weighted by TM-score * globalID
    ]
    for m,method in enumerate(method_list):
        outfile=method+suffix
        print("writing "+outfile)
        author,model=method.split('_')
        txt ="AUTHOR %s\n"%author
        txt+="MODEL %s\n"%model
        txt+="KEYWORDS structure alignment.\n"
        for target in sorted(tmalign_dict.keys()):
            print(target+" for "+outfile)
            for Aspect in "FPC":
                predict_dict=dict()
                score_list=[]
                for line in tmalign_dict[target]:
                    sacc=line[0]
                    score=line[m+1]
                    if not sacc in annotation_dict[Aspect]:
                        continue
                    score_list.append(score)
                    for GOterm in annotation_dict[Aspect][sacc]:
                        if not GOterm in predict_dict:
                            predict_dict[GOterm]=0
                        predict_dict[GOterm]+=score
                denominator=sum(score_list)
                if denominator<=0:
                    continue
                for GOterm in predict_dict:
                    nominator=predict_dict[GOterm]
                    predict_dict[GOterm]=nominator/denominator
                for cscore,GOterm in sorted([(predict_dict[GOterm],
                    GOterm) for GOterm in predict_dict],reverse=True):
                    cscore="%.2f"%cscore
                    if cscore=="0.00":
                        break
                    txt+="%s\t%s\t%s\n"%(target,GOterm,cscore)
        txt+="END\n"
        fp=open(outfile,'w')
        fp.write(txt)
        fp.close()
    return

if __name__=="__main__":
    if len(sys.argv)!=3:
        sys.stderr.write(docstring)
        exit()

    infile=sys.argv[1]
    suffix=sys.argv[2]
    annotation_dict=read_annotation()
    tmalign_dict=read_tmalign(infile)
    write_output(tmalign_dict,annotation_dict,suffix)
