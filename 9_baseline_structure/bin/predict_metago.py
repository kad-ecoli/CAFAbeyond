#!/usr/bin/env python
docstring='''predict_metago.py target.blast target.psiblast metago_1_9606_go.txt
    use blast and psiblast search result to derive metago sequence based
prediction metago_1_9606.go.txt
output:
    metago_1_9606_go.txt
'''
import sys
from os.path import dirname, basename, abspath
from subprocess import Popen,PIPE
from math import exp
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
    fp=open(infile,'r')
    for line in fp:
        items=line.split('\t')
        if len(items)<8:
            continue
        qacc,qlen,sacc,slen,evalue,bitscore,length,nident=items
        qlen=float(qlen)
        nident=float(nident)
        if not qacc in blast_dict:
            print("parsing %s from %s"%(qacc,infile))
            blast_dict[qacc]=[]
        blast_dict[qacc].append([sacc, nident/qlen])
    fp.close()
    return blast_dict

def write_output(blast_dict,psiblast_dict,annotation_dict,outfile):
    method="metago_1"
    print("writing "+outfile)
    author,model=method.split('_')
    txt ="AUTHOR %s\n"%author
    txt+="MODEL %s\n"%model
    txt+="KEYWORDS sequence alignment.\n"
    for target in sorted(blast_dict.keys()):
        for Aspect in "FPC":
            weight=0
            blast_predict_dict=dict()
            psiblast_predict_dict=dict()

            blast_denominator=0
            for line in blast_dict[target]:
                sacc=line[0]
                score=line[1]
                if not sacc in annotation_dict[Aspect]:
                    continue
                blast_denominator+=score
                for GOterm in annotation_dict[Aspect][sacc]:
                    if not GOterm in blast_predict_dict:
                        blast_predict_dict[GOterm]=0
                    blast_predict_dict[GOterm]+=score
            for GOterm in blast_predict_dict:
                blast_predict_dict[GOterm]/=blast_denominator

            psiblast_denominator=0
            for line in psiblast_dict[target]:
                sacc=line[0]
                score=line[1]
                if not sacc in annotation_dict[Aspect]:
                    continue
                if score>weight:
                    weight=score
                psiblast_denominator+=score
                for GOterm in annotation_dict[Aspect][sacc]:
                    if not GOterm in psiblast_predict_dict:
                        psiblast_predict_dict[GOterm]=0
                    psiblast_predict_dict[GOterm]+=score
            for GOterm in psiblast_predict_dict:
                psiblast_predict_dict[GOterm]/=psiblast_denominator

            predict_dict=dict()
            for GOterm,psiblastscore in psiblast_predict_dict.items():
                blastscore=0
                if GOterm in blast_predict_dict:
                    blastscore=blast_predict_dict[GOterm]
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
    outfile      =sys.argv[3]
    annotation_dict=read_annotation()
    blast_dict=read_blast(blastfile)
    psiblast_dict=read_blast(psiblastfile)
    write_output(blast_dict,psiblast_dict,annotation_dict,outfile)
