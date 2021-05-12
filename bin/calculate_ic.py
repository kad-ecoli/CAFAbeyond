#!/usr/bin/env python
docstring='''
calculate_ic.py go-basic.obo goa_uniprot_all.F.is_a naive.F
    calculate the naive probability and information content of GO terms
'''
import sys
import obo2csv # parsing GO hierachy
from math import log

def calculate_ic(obo_dict,infile,outfile):
    allterm_dict=dict()
    fp=open(infile,'r')
    lines=fp.read().splitlines()
    fp.close()
    for line in lines:
        DB_Object_ID,GOterms=line.split()
        allterm_dict[DB_Object_ID]=GOterms.split(',')

    GO_ID_list=[]
    for DB_Object_ID in allterm_dict:
        GO_ID_list+=allterm_dict[DB_Object_ID]
    naive_list=[]
    ic_dict=dict()
    # a pseudo-count of 1 is added according to
    # https://github.com/yuxjiang/CAFA2/blob/master/matlab/pfp_eia.m
    # natural log instead of log2 was used
    for GO_ID in sorted(set(GO_ID_list)):
        num_with_child=sum([GO_ID in allterm_dict[DB_Object_ID] \
            for DB_Object_ID in allterm_dict])
        prob=(1.+num_with_child)/(1.+len(allterm_dict))
        name=obo_dict.short(GO_ID).split(' ! ')[1]
        ic=-log(prob)
        parent_GO_list=[]
        for parent_GO in obo_dict.is_a(Term_id=GO_ID, direct=True,
            name=True, number=False).split('\t'):
            parent_GO=parent_GO.split(' ! ')[0]
            if parent_GO!=GO_ID:
                parent_GO_list.append(parent_GO)
        num_with_parent=0
        for DB_Object_ID in allterm_dict:
            with_parent_terms=sum([parent_GO in allterm_dict[
                DB_Object_ID] for parent_GO in parent_GO_list])
            num_with_parent+=(with_parent_terms==len(parent_GO_list))
        ic_condition=-log(1+num_with_child)+log(1+num_with_parent)
        naive_list.append((GO_ID,prob,ic,ic_condition,name))
    
    naive_list.sort(key = lambda x: x[3])
    naive_list.sort(key = lambda x: x[1],reverse=True)

    txt=''
    for GO_ID,prob,ic,parent_ic,name in naive_list:
        txt+="%s\t%.6f\t%.6f\t%.6f\t%s"%(GO_ID,prob,ic,parent_ic,name)
    fp=open(outfile,'w')
    fp.write(txt.replace("\t-0.000000","\t0.000000"))
    fp.close()
    return

if __name__=="__main__":
    if len(sys.argv)!=4:
        sys.stderr.write(docstring)
        exit()

    obo_file=sys.argv[1]
    infile  =sys.argv[2]
    outfile =sys.argv[3]

    obo_dict=obo2csv.parse_obo_file(obo_file)
    calculate_ic(obo_dict,infile,outfile)
