#!/usr/bin/env python
docstring='''
This script checks if inclusion of GO:0005515 "protein binding" is appropriate
'''
import sys
import os
curdir=os.path.dirname(os.path.abspath(__file__))
rootdir=os.path.dirname(curdir)
datadir=os.path.join(rootdir,"data")

def make_target(oldfile,newfile):
    #### read file ####
    target_old_list=[]
    fp=open(oldfile,'r')
    for line in fp.read().splitlines():
        target,GOterms=line.split()
        target_old_list.append(target)
    fp.close()
    target_old_set=set(target_old_list)

    protein_binding_only_list=[]
    non_protein_binding_dict=dict()
    fp=open(newfile,'r')
    for line in fp.read().splitlines():
        target,GOterms=line.split()
        if target in target_old_set:
            continue
        if GOterms=="GO:0003674,GO:0005488,GO:0005515":
            protein_binding_only_list.append(target)
        else:
            non_protein_binding_dict[target]=GOterms.split(',')
    fp.close()
    return protein_binding_only_list,non_protein_binding_dict

def read_ic(naive_file):
    ic_dict=dict()
    fp=open(naive_file,'r')
    for line in fp.read().splitlines():
        items =line.split('\t')
        GOterm=items[0]
        ic    =items[3]
        ic_dict[GOterm]=float(ic)
    return ic_dict

if __name__=="__main__":
    oldfile=datadir+"/goa_uniprot_all.F.is_a.198"
    newfile=datadir+"/goa_uniprot_all.F.is_a.203"
    protein_binding_only_list,non_protein_binding_dict=make_target(
        oldfile,newfile)
    ic_dict=read_ic(datadir+"/naive.F.with_GO:0005515")

    print("#### NK/LK MF targets with GO:0005515 as the only leaf term ####")
    print("Number of targets: %d"%(len(protein_binding_only_list)))
    ic_per_target=ic_dict["GO:0003674"]+ic_dict["GO:0005488"]+ \
                  ic_dict["GO:0005515"]
    print("IC per target: %.6f"%ic_per_target)
    print("Total IC: %.6f"%(ic_per_target*len(protein_binding_only_list)))
    
    print("#### NK/LK MF targets with at least 1 non-GO:0005515 leaf term ####")
    print("Number of targets: %d"%(len(non_protein_binding_dict)))
    total_ic=0
    missing_term=[]
    for target in non_protein_binding_dict:
        for GOterm in non_protein_binding_dict[target]:
            if GOterm in ic_dict:
                total_ic+=ic_dict[GOterm]
            elif not GOterm in missing_term:
                sys.stderr.write("No IC for term %s\n"%GOterm)
                missing_term.append(GOterm)
    print("IC per target: %.6f"%(total_ic/len(non_protein_binding_dict)))
    print("Total IC: %.6f"%total_ic)
