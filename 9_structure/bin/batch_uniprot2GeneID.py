#!/usr/bin/env python
docstring='''
batch_uniprot2GeneID.py target.list uniprot_sprot_exp.GeneID.tsv coxpres_m/ coxpres_m.tsv

input:
    target.list - list of target files to be parsed
    uniprot_sprot_exp.GeneID.tsv - mapping of template uniprot ID to entrez Gene ID
    coxpres_m/  - folder of coexpression

output:
    coxpres_m.tsv - combined coexpression data
'''
import os, sys
import gzip

def read_target_list(infile):
    target_list=[]
    fp=open(infile,'r')
    for line in fp.read().splitlines():
        items=line.split('\t')
        target_list.append(items[0])
    fp.close()
    return target_list

def read_mapping(mapfile):
    map_dict=dict()
    fp=open(mapfile,'r')
    for line in fp.read().splitlines():
        items=line.split('\t')
        template=items[0]
        GeneID=items[-1]
        map_dict[GeneID]=template
    fp.close()
    return map_dict

def combine_coxpres(target_list,map_dict,datadir,outfile):
    txt=''
    filename_list=[]
    for target in target_list:
        filename=os.path.join(datadir,target)
        if not os.path.isfile(filename):
            continue
        filename_list.append(filename)
        if len(filename_list)%100==0:
            print(filename)
        fp=open(filename,'r')
        for line in fp.read().splitlines():
            GeneID,score=line.split('\t')
            if not GeneID in map_dict:
                continue
            txt+="%s\t%s\t%s\n"%(target,map_dict[GeneID],score)
        fp.close()
    if outfile.endswith(".gz"):
        fp=gzip.open(outfile,'w')
    else:
        fp=open(outfile,'w')
    fp.write(txt)
    fp.close()
    return

if __name__=="__main__":
    if len(sys.argv)!=5:
        sys.stderr.write(docstring)
        exit()

    infile =sys.argv[1]
    mapfile=sys.argv[2]
    datadir=sys.argv[3]
    outfile=sys.argv[4]
    target_list=read_target_list(infile)
    map_dict   =read_mapping(mapfile)
    combine_coxpres(target_list,map_dict,datadir,outfile)
