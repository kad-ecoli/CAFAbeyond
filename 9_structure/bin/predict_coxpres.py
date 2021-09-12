#!/usr/bin/env python
docstring='''predict_coxpres.py target.list coxpres_u.gz coxpres_1_all.txt
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

def read_coxpres(target_set,template_set,coxpresfile):
    coxpres_dict=dict()
    fp=gzip.open(coxpresfile,'r')
    for line in fp:
        target,template,score=line.split('\t')
        if not target in target_set or not template in template_set:
            continue
        if not target in coxpres_dict:
            coxpres_dict[target]=[]
        score=float(score)
        if score<=0:
            continue
        coxpres_dict[target].append((abs(score),template))
    fp.close()
    for target in coxpres_dict:
        coxpres_dict[target].sort(reverse=True)
    return coxpres_dict
    
def write_output(target_list,annotation_dict,coxpres_dict,outfile):
    model='1'
    items=outfile.split('_')
    if len(items)>=3:
        model=items[-2]
    txt ="AUTHOR coxpres_dict\n"
    txt+="MODEL %s\n"%model
    txt+="KEYWORDS gene expression.\n"
    for t,target in enumerate(target_list):
        if not target in coxpres_dict:
            continue
        if t%100==0:
            print(target)
        for Aspect in "FPC":
            predict_dict=dict()
            denominator=0
            #template_num=0
            for score,template in coxpres_dict[target]:
                if not template in annotation_dict[Aspect]:
                    continue
                #template_num+=1
                #if template_num>500:
                    #continue
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
    if len(sys.argv)!=4:
        sys.stderr.write(docstring)
        exit()

    infile              =sys.argv[1]
    coxpresfile         =sys.argv[2]
    outfile             =sys.argv[3]
    target_list         =read_target_list(infile)
    annotation_dict,template_set=read_annotation()
    coxpres_dict        =read_coxpres(set(target_list),template_set,coxpresfile)
    write_output(target_list,annotation_dict,coxpres_dict,outfile)
