#!/usr/bin/env python
docstring='''
This script compares EXP and HTP annotations
'''
import sys
import os
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

def read_target_type_dict(datadir):
    target_type_dict=dict(NK=dict(),LK=dict(),PK=dict())
    for target_type in target_type_dict:
        for Aspect in "FPC":
            filename="%s/%s.%s"%(datadir,target_type,Aspect)
            fp=open(filename,'r')
            lines=fp.read().splitlines()
            fp.close()
            target_type_dict[target_type][Aspect]=[line.split()[0] for line in lines]
    return target_type_dict

if __name__=="__main__":
    ic_dict=read_ic((datadir+"/naive.F", datadir+"/naive.P",
                     datadir+"/naive.C"))
