#!/usr/bin/env python
docstring='''
subset_mapping.py target.list GeneIDmapping.tsv outputmapping.tsv
'''
import sys

def read_target_list(infile):
    fp=open(infile,'r')
    target_list=fp.read().splitlines()
    fp.close()
    return target_list

def read_mapping(mapfile,target_set):
    map_dict=dict()
    fp=open(mapfile,'r')
    for line in fp.read().splitlines():
        items=line.split('\t')
        target=items[0]
        GeneID=items[-1]
        if not target in target_set:
            continue
        map_dict[target]=GeneID
    fp.close()
    return map_dict

def write_map(target_list,map_dict,outfile):
    txt=''
    for target in target_list:
        if target in map_dict:
            txt+="%s\t%s\n"%(target,map_dict[target])
    fp=open(outfile,'w')
    fp.write(txt)
    fp.close()
    return

if __name__=="__main__":
    if len(sys.argv)!=4:
        sys.stderr.write(docstring)
        exit()

    infile =sys.argv[1]
    mapfile=sys.argv[2]
    outfile=sys.argv[3]
    target_list=read_target_list(infile)
    map_dict   =read_mapping(mapfile,set(target_list))
    write_map(target_list,map_dict,outfile)
