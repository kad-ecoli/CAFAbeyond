#!/usr/bin/env python
docstring='''
This script counts the number of targets per target type
'''
import sys
import os
curdir=os.path.dirname(os.path.abspath(__file__))
rootdir=os.path.dirname(curdir)
datadir=os.path.join(rootdir,"data")

def read_ic(naive_file_list):
    ic_dict=dict()
    for naive_file in naive_file_list:
        fp=open(naive_file,'r')
        for line in fp.read().splitlines():
            items =line.split('\t')
            GOterm=items[0]
            ic    =items[3]
            ic_dict[GOterm]=float(ic)
        fp.close()
    return ic_dict

def calculate_target_ic(infile,ic_dict):
    per_target_ic_dict=dict()
    lines=[]
    filename_list=[infile]
    if isinstance(infile,list):
        filename_list=infile
    for filename in filename_list:
        fp=open(filename,'r')
        lines+=fp.read().splitlines()
        fp.close()
    for line in lines:
        items=line.split('\t')
        target=items[0]
        newGOterms=items[1].split(',')
        if len(items)==3:
            oldGOterms=set(items[2].split(','))
            newGOterms=[GOterm for GOterm in newGOterms if not GOterm in oldGOterms]
        per_target_ic_dict[target]=sum([ic_dict[GOterm] for GOterm in newGOterms if GOterm in ic_dict])
    target_num=len(per_target_ic_dict)
    total_ic=sum(per_target_ic_dict.values())
    return target_num,total_ic/target_num

if __name__=="__main__":
    ic_dict=read_ic((datadir+"/naive.F", datadir+"/naive.P",
                     datadir+"/naive.C"))
    all_target_ic_dict=dict(F=dict(),P=dict(),C=dict())
    for Aspect in "FPC":
        for target_type in ["NK","LK","PK","All"]:
            filename=datadir+"/"+target_type+"."+Aspect
            if target_type =="All":
                filename=[datadir+"/NK."+Aspect,
                          datadir+"/LK."+Aspect,
                          datadir+"/PK."+Aspect]
            all_target_ic_dict[Aspect][target_type]=calculate_target_ic(
                filename,ic_dict)

    print("## Number of proteins (average IC per protein) ##")
    print("| Type |      NK         |       LK       |        PK       |        All      |")
    print("| :--: |     :--:        |      :--:      |       :--:      |       :--:      |")
    for Aspect in "FPC":
        line="|   %s  |"%Aspect
        for target_type in ["NK","LK","PK","All"]:
            target_num,average_ic=all_target_ic_dict[Aspect][target_type]
            line+=" %d (%.6f) |"%(target_num,average_ic)
        print(line)
    line="|  All |"
    for target_type in ["NK","LK","PK","All"]:
        total_target_num=0
        total_average_ic=0
        for Aspect in "FPC":
           target_num,average_ic=all_target_ic_dict[Aspect][target_type]
           total_target_num+=target_num
           total_average_ic+=target_num*average_ic
        total_average_ic/=total_target_num
        line+=" %d (%.6f) |"%(total_target_num,total_average_ic)
    print(line)
