#!/usr/bin/env python
docstring='''predict_metago.py target.blast target.psiblast _9606_go.txt
    use blast and psiblast search result to derive metago sequence based
prediction metago_1_9606.go.txt
output:
    metago_1_9606_go.txt
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

def read_blast(infile):
    blast_dict=dict()
    if isfile(infile):
        fp=open(infile,'r')
    else:
        fp=gzip.open(infile+".gz",'r')
    for line in fp:
        items=line.split('\t')
        if len(items)<8:
            continue
        qacc,qlen,sacc,slen,evalue,bitscore,length,nident=items
        qlen=float(qlen)
        slen=float(slen)
        bitscore=float(bitscore)
        nident=float(nident)
        if not qacc in blast_dict:
            if len(blast_dict) % 100 ==0:
                print("parsing %s from %s"%(qacc,infile))
            blast_dict[qacc]=[]
        blast_dict[qacc].append([sacc, 
            nident/qlen,
            nident/max((qlen,slen)),
            bitscore,
            ])
    fp.close()
    return blast_dict

def write_output(blast_dict,psiblast_dict,annotation_dict,outfile):
    target_list=[]
    target_list+=[target for target in blast_dict.keys()]
    target_list+=[target for target in psiblast_dict.keys()]
    target_list=sorted(set(target_list))
    method_list=[
        "metago_1",
        "metago_2",
        ]
    for m,method in enumerate(method_list):
        outfile=method+suffix
        print("writing "+outfile)
        author,model=method.split('_')
        txt ="AUTHOR %s\n"%author
        txt+="MODEL %s\n"%model
        txt+="KEYWORDS sequence alignment.\n"
        for t,target in enumerate(target_list):
            if t % 100==0: # do not print every target
                print("predicting "+target)
            for Aspect in "FPC":
                weight_list=[]
                blast_predict_dict=dict()
                psiblast_predict_dict=dict()
                GOterm_list=[]
                
                if target in blast_dict:
                    blast_denominator=0
                    for line in blast_dict[target]:
                        sacc=line[0]
                        score=line[1] if m==0 else line[-1]
                        if not sacc in annotation_dict[Aspect]:
                            continue
                        if m>=1:
                            weight_list.append(line[2])
                        blast_denominator+=score
                        for GOterm in annotation_dict[Aspect][sacc]:
                            if not GOterm in blast_predict_dict:
                                blast_predict_dict[GOterm]=0
                            blast_predict_dict[GOterm]+=score
                    for GOterm in blast_predict_dict:
                        blast_predict_dict[GOterm]/=blast_denominator
                        GOterm_list.append(GOterm)

                if target in psiblast_dict:
                    psiblast_denominator=0
                    for line in psiblast_dict[target]:
                        sacc=line[0]
                        score=line[1] if m==0 else line[3]
                        if not sacc in annotation_dict[Aspect]:
                            continue
                        if m==0:
                            weight_list.append(line[1])
                        psiblast_denominator+=score
                        for GOterm in annotation_dict[Aspect][sacc]:
                            if not GOterm in psiblast_predict_dict:
                                psiblast_predict_dict[GOterm]=0
                            psiblast_predict_dict[GOterm]+=score
                    for GOterm in psiblast_predict_dict:
                        psiblast_predict_dict[GOterm]/=psiblast_denominator
                        GOterm_list.append(GOterm)

                weight=0
                if len(weight_list):
                    if m==0:
                        weight=max(weight_list)
                    else:
                        weight=1
                        for w in weight_list:
                            weight*=(1.-w)
                        weight=1-weight
                predict_dict=dict()
                GOterm_list=list(set(GOterm_list))
                for GOterm in GOterm_list:
                    blastscore=0
                    psiblastscore=0
                    if GOterm in blast_predict_dict:
                        blastscore=blast_predict_dict[GOterm]
                    if GOterm in psiblast_predict_dict:
                        psiblastscore=psiblast_predict_dict[GOterm]
                    predict_dict[GOterm]=weight*blastscore+(1-weight)*psiblastscore

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
    if len(sys.argv)!=4:
        sys.stderr.write(docstring)
        exit()

    blastfile   =sys.argv[1]
    psiblastfile=sys.argv[2]
    suffix      =sys.argv[3]
    annotation_dict=read_annotation()
    blast_dict   =read_blast(blastfile)
    psiblast_dict=read_blast(psiblastfile)
    write_output(blast_dict,psiblast_dict,annotation_dict,suffix)
