#!/usr/bin/env python
docstring='''predict_ppi.py target.list ppi_1_all.txt
    use PPI from STRING database to to predict GO terms for input file target.list,
    output predictions to ppi_1_all.txt
'''
import sys
from os.path import dirname, basename, abspath
import gzip
bindir=dirname(abspath(__file__))
rootdir=dirname(bindir)
datdir=rootdir+"/data"

def read_target_list(infile):
    fp=open(infile,'r')
    target_list=fp.read().splitlines()
    fp.close()
    return target_list

def read_annotation():
    annotation_dict=dict()
    template_list=[]
    for Aspect in "FPC":
        annotation_dict[Aspect]=dict()
        filename=datdir+"/uniprot_sprot_exp."+Aspect
        fp=open(filename,'r')
        for line in fp.read().splitlines():
            target,GOterm_list=line.split('\t')
            annotation_dict[Aspect][target]=GOterm_list.split(',')
            template_list.append(target)
        fp.close()
    template_set=set(template_list)
    return annotation_dict,template_set

def read_ppi(target_set,template_set):
    ppi_dict=dict()
    fp=gzip.open(datdir+"/uniprot.links.gz",'r')
    for line in fp:
        target,template,score=line.split('\t')
        if not target in target_set or not template in template_set:
            continue
        if not target in ppi_dict:
            ppi_dict[target]=dict()
        ppi_dict[target][template]=int(score)/1000.
    return ppi_dict
    
def write_output(target_list,annotation_dict,ppi_dict,outfile):
    txt ="AUTHOR ppi\n"
    txt+="MODEL 1\n"
    txt+="KEYWORDS protein interactions.\n"
    for target in target_list:
        if not target in ppi_dict:
            continue
        for Aspect in "FPC":
            predict_dict=dict()
            denominator=0
            for template,score in ppi_dict[target].items():
                if not template in annotation_dict[Aspect]:
                    continue
                denominator+=score
                for GOterm in annotation_dict[Aspect][template]:
                    if not GOterm in predict_dict:
                        predict_dict[GOterm]=0
                    predict_dict[GOterm]+=score
            for GOterm in predict_dict:
                predict_dict[GOterm]/=denominator
            for cscore,GOterm in sorted([(predict_dict[GOterm],GOterm
                ) for GOterm in predict_dict],reverse=True):
                cscore="%.2f"%cscore
                if cscore=="0.00":
                    break
                txt+="%s\t%s\t%s\n"%(target,GOterm,cscore)
    txt+="END\n"
    fp=open(outfile,'w')
    fp.write(txt)
    return

if __name__=="__main__":
    if len(sys.argv)!=3:
        sys.stderr.write(docstring)
        exit()

    infile              =sys.argv[1]
    outfile             =sys.argv[2]
    target_list         =read_target_list(infile)
    annotation_dict,template_set=read_annotation()
    ppi_dict            =read_ppi(set(target_list),template_set)
    write_output(target_list,annotation_dict,ppi_dict,outfile)
