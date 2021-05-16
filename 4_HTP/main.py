#!/usr/bin/env python
docstring='''
This script compares EXP and HTP annotations
'''
import sys
import os
curdir =os.path.dirname(os.path.abspath(__file__))
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

def read_target_dict(goa_file_list):
    target_list=[]
    GOterm_dict=dict()
    for goa_file in goa_file_list:
        fp=open(goa_file)
        for line in fp.read().splitlines():
            items      =line.split('\t')
            target     =items[0]
            GOterm_list=items[1].split(',')
            if len(items)>2:
                oldGOterm_set=set(items[2].split(','))
                GOterm_list=[GOterm for GOterm in GOterm_list \
                      if not GOterm in oldGOterm_set]
            target_list.append(target)
            for GOterm in GOterm_list:
                if not GOterm in GOterm_dict:
                    GOterm_dict[GOterm]=[target]
                else:
                    GOterm_dict[GOterm].append(target)
        fp.close()
    target_set=set(target_list)
    for GOterm in GOterm_dict:
        GOterm_dict[GOterm]=len(GOterm_dict[GOterm])
    return target_set,GOterm_dict

if __name__=="__main__":
    ic_dict=read_ic((datadir+"/naive.F", datadir+"/naive.P",
                     datadir+"/naive.C"))
    print("| Evidence | MF targets | BP targets | CC targets |")
    print("| :--:     | :--:       | :--:       | :--:                      |")
    for evidence in ["EXP","HTP","EXP+HTP"]:
        target_set,GOterm_dict=read_target_dict(
            ["%s/%s.%s"%(curdir,evidence,Aspect) for Aspect in "FPC"])
        terms_ge10 =sum([num>=10 for num in GOterm_dict.values()])
        terms_ge100=sum([num>=100 for num in GOterm_dict.values()])
        total_ic=sum([ic_dict[GOterm]*num for GOterm,num in GOterm_dict.items() if GOterm in ic_dict])
        mean_ic=total_ic/sum(GOterm_dict.values())
        print("| %s | %d | %d | %d | %d | %.3f |"%(
            evidence, len(target_set), len(GOterm_dict), terms_ge10, terms_ge100, mean_ic))
