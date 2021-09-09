#!/usr/bin/env python
docstring='''predict_goa.py target.list target.is_a goa_1_all.txt
    use UniProt-GOA annotations to predict GO terms for input file target.list,
    output predictions to goa_1_all.txt
'''
import sys
from os.path import dirname, basename, abspath
bindir=dirname(abspath(__file__))
rootdir=dirname(bindir)
datdir=rootdir+"/data"

def read_precision_by_evidence():
    evidence2cscore_dict=dict()
    fp=open(datdir+"/precision_by_evidence.txt",'r')
    for line in fp.read().splitlines():
        if line.startswith('#'):
            continue
        evidence,cscore=line.split()
        evidence2cscore_dict[evidence]=float(cscore)
    fp.close()
    return evidence2cscore_dict

def read_target_list(infile):
    fp=open(infile,'r')
    target_list=fp.read().splitlines()
    fp.close()
    return target_list

def read_goa_isa(target_list,annfile,evidence2cscore_dict):
    target_set=set(target_list)
    annotation_dict=dict()
    fp=open(annfile,'r')
    for line in fp.read().splitlines():
        target,Aspect,GOterm,evidence_list=line.split('\t')
        if not target in target_set:
            continue
        cscore=0
        for evidence in evidence_list.split(','):
            if evidence2cscore_dict[evidence]>cscore:
                cscore=evidence2cscore_dict[evidence]
        if not target in annotation_dict:
            annotation_dict[target]=[]
        annotation_dict[target].append((cscore,GOterm))
    fp.close()
    return annotation_dict

def write_output(target_list,annotation_dict,outfile):
    txt ="AUTHOR iea\n"
    txt+="MODEL 1\n"
    txt+="KEYWORDS de novo prediction.\n"
    for target in target_list:
        if not target in annotation_dict:
            continue
        for cscore,GOterm in annotation_dict[target]:
            txt+="%s\t%s\t%.2f\n"%(target,GOterm,cscore)
    txt+="END\n"
    fp=open(outfile,'w')
    fp.write(txt)
    return

if __name__=="__main__":
    if len(sys.argv)!=4:
        sys.stderr.write(docstring)
        exit()

    infile              =sys.argv[1]
    annfile             =sys.argv[2]
    outfile             =sys.argv[3]
    evidence2cscore_dict=read_precision_by_evidence()
    target_list         =read_target_list(infile)
    annotation_dict     =read_goa_isa(target_list,annfile,evidence2cscore_dict)
    write_output(target_list,annotation_dict,outfile)
