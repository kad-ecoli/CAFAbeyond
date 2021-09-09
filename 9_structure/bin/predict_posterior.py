#!/usr/bin/env python
docstring='''predict_posterior.py target.list target.PK naive_3_all.txt 
    use posterior probability of prior existing GO terms to predict GO terms

Input:
    target.list - list of targets
    target.PK   - prior existing GO terms

Ouput:
    naive_3_all.txt 
'''
import sys
from os.path import dirname, basename, abspath, isfile
bindir=dirname(abspath(__file__))
rootdir=dirname(bindir)
datdir=rootdir+"/data"

def read_target_list(infile):
    fp=open(infile,'r')
    target_list=fp.read().splitlines()
    fp.close()
    return target_list

def read_posterior():
    posterior_dict=dict()
    for Aspect in "FPC":
        filename=datdir+"/posterior."+Aspect
        fp=open(filename,'r')
        for line in fp.read().splitlines():
            parent_GO,childern_GOterms=line.split('\t')
            posterior_dict[parent_GO]=dict()
            for child_GO in childern_GOterms.split(','):
                GOterm,cscore=child_GO.split('_')
                posterior_dict[parent_GO][GOterm]=float(cscore)
        fp.close()
    return posterior_dict

def read_prior_annotation(target_list,PK_file):
    prior_dict=dict()
    for target in target_list:
        prior_dict[target]=["GO:0005575","GO:0003674","GO:0008150"]
    fp=open(PK_file,'r')
    for line in fp.read().splitlines():
        target,GOterms=line.split('\t')
        prior_dict[target]=list(set(prior_dict[target]+GOterms.split(',')))
    fp.close()
    return prior_dict

def propagate_child_terms(posterior_dict,prior_dict):
    predict_dict=dict()
    for target,parent_GO_list in prior_dict.items():
        predict_dict[target]=dict()
        for parent_GO in parent_GO_list:
            predict_dict[target][parent_GO]=1.000
            if not parent_GO in posterior_dict:
                continue
            for GOterm,cscore in posterior_dict[parent_GO].items():
                if GOterm in predict_dict[target]:
                    predict_dict[target][GOterm]=max(
                   (predict_dict[target][GOterm],cscore))
                else:
                    predict_dict[target][GOterm]=cscore
    return predict_dict

def write_output(target_list,predict_dict,outfile):
    txt ="AUTHOR naive\n"
    txt+="MODEL 3\n"
    txt+="KEYWORDS de novo prediction.\n"
    for target in target_list:
        GOterm_list=[(cscore,GOterm) for GOterm,cscore in predict_dict[target].items()]
        for cscore,GOterm in sorted(GOterm_list,reverse=True):
            if "%.2f"%cscore!="0.00":
                txt+="%s\t%s\t%.2f\n"%(target,GOterm,cscore)
    txt+="END\n"
    fp=open(outfile,'w')
    fp.write(txt)
    fp.close()
    return

if __name__=="__main__":
    if len(sys.argv)!=4:
        sys.stderr.write(docstring)
        exit()

    infile =sys.argv[1]
    PK_file=sys.argv[2]
    outfile=sys.argv[3]

    target_list=read_target_list(infile)
    posterior_dict=read_posterior()
    prior_dict=read_prior_annotation(target_list,PK_file)
    predict_dict=propagate_child_terms(posterior_dict,prior_dict)
    write_output(target_list,predict_dict,outfile)
