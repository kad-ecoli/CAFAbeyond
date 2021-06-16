#!/usr/bin/env python
docstring='''
evaluate_HTP.py goa_uniprot_all.HTP.198.gz
    evaluate the accuracy of HTP annotations
'''

import os
import sys
import obo2csv
from propagate_gaf_terms import propagate_gaf_terms

bindir=os.path.dirname(os.path.abspath(__file__))
rootdir=os.path.dirname(bindir)
datadir=rootdir+"/data"

def read_ic():
    ic_dict=dict()
    for Aspect in "FPC":
        fp=open(datadir+"/naive."+Aspect,'r')
        for line in fp.readlines():
            items=line.split('\t')
            GOterm=items[0]
            ic=items[3]
            ic_dict[GOterm]=float(ic)
        fp.close()
    return ic_dict

def read_propagate_file(infile):
    ann_dict=dict()
    fp=open(infile,'r')
    for line in fp.read().splitlines():
        items=line.split('\t')
        target=items[0]
        newGOterms=items[1].split(',')
        oldGOterms=[]
        if len(items)>2:
            oldGOterms=items[2].split(',')
        ann_dict[target]=[newGOterms,oldGOterms]
    fp.close()
    return ann_dict

def sum_ic(GOterm_list,ic_dict):
    return sum([ic_dict[GOterm] for GOterm in GOterm_list if GOterm in ic_dict])

def evaluate_HTP(HTPfile_dict,EXPfile_dict,ic_dict):
    print("| Aspect | targets | Precision | Recall | F    | wPrecision | wRecall | wF   |")
    print("| :--:   | :--:    | :--:      | :--:   | :--: | :--:       | :--:    | :--: |")
    for Aspect in "FPC":
        htp_dict=read_propagate_file(HTPfile_dict[Aspect])
        exp_dict=read_propagate_file(EXPfile_dict[Aspect])
        target_set=set(htp_dict.keys()).intersection(exp_dict.keys())
        target_list=list(target_set)
        precision_list=[]
        recall_list=[]
        wprecision_list=[]
        wrecall_list=[]
        for target in target_list:
            htp_terms=htp_dict[target][0]
            exp_new_terms=exp_dict[target][0]
            exp_old_terms=set(exp_dict[target][1])
            htp_terms=[GOterm for GOterm in htp_terms if not GOterm in exp_old_terms]
            TP_terms=set(htp_terms).intersection(exp_new_terms)
            wTP_terms=sum_ic(TP_terms,ic_dict)
            whtp_terms=sum_ic(htp_terms,ic_dict)
            wexp_terms=sum_ic(exp_new_terms,ic_dict)
            precision=0
            if len(htp_terms):
                precision=1.*len(TP_terms)/len(htp_terms)
            recall=1.*len(TP_terms)/len(exp_new_terms)
            precision_list.append(precision)
            recall_list.append(recall)
            wprecision=0
            if whtp_terms>0:
                wprecision=wTP_terms/whtp_terms
            wrecall=wTP_terms/wexp_terms
            wprecision_list.append(wprecision)
            wrecall_list.append(wrecall)
        precision=sum(precision_list)/len(precision_list)
        recall=sum(recall_list)/len(recall_list)
        F=2./(1./precision+1./recall)
        wprecision=sum(wprecision_list)/len(wprecision_list)
        wrecall=sum(wrecall_list)/len(wrecall_list)
        wF=2./(1./wprecision+1./wrecall)
        print("| %s | %d | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f |"%(
            Aspect,len(target_list),precision,recall,F,wprecision,wrecall,wF))
    return

if __name__=="__main__":
    if len(sys.argv)!=2:
        sys.stderr.write(docstring)
        exit()
    obo_file=datadir+"/go-basic.obo"
    HTP_gaf=sys.argv[1]

    HTPfile_dict=dict()
    HTPfile_dict['F']="preHTP.F"
    HTPfile_dict['P']="preHTP.P"
    HTPfile_dict['C']="preHTP.C"
    obo_dict=obo2csv.parse_obo_file(obo_file)
    propagate_gaf_terms(obo_dict,HTP_gaf,HTPfile_dict)

    EXPfile_dict=dict()
    EXPfile_dict['F']="EXP.F"
    EXPfile_dict['P']="EXP.P"
    EXPfile_dict['C']="EXP.C"

    ic_dict=read_ic()
    evaluate_HTP(HTPfile_dict,EXPfile_dict,ic_dict)
