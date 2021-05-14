#!/usr/bin/env python
docstring='''
This script counts the number of targets per database
'''
import sys
import os
curdir=os.path.dirname(os.path.abspath(__file__))
rootdir=os.path.dirname(curdir)
datadir=os.path.join(rootdir,"data")

def read_species_dict(speciesfile_list):
    species_dict=dict()
    for speciesfile in speciesfile_list:
        fp=open(speciesfile,'r')
        for line in fp.read().splitlines():
            target,species=line.split()
            species_dict[target]=species
        fp.close()
    return species_dict

def read_target_list(listfile):
    fp=open(listfile,'r')
    target_list=fp.read().splitlines()
    fp.close()
    return target_list

def read_cafa_list(cafa_species_file,species_dict,swissprot_list):
    cafa_species_set=set(read_target_list(cafa_species_file))
    cafa_list=[]
    for target in swissprot_list:
        if species_dict[target] in cafa_species_set:
            cafa_list.append(target)
    return cafa_list

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

def get_target_type_stat(dataset,species_dict,target_type_dict):
    proteins_list=[]
    species_list=[]
    target_num_dict=dict()
    for target_type in ["NK","LK","PK"]:
        target_num_dict[target_type]=0
        for Aspect in "FPC":
            for target in target_type_dict[target_type][Aspect]:
                if not target in dataset:
                    continue
                proteins_list.append(target)
                species_list.append(species_dict[target])
                target_num_dict[target_type]+=1
    species_num=len(set(species_list))
    proteins_num=len(set(proteins_list))
    return proteins_num,species_num,target_num_dict

if __name__=="__main__":
    species_dict  =read_species_dict([datadir+"/goa_uniprot_all.species.198",
                                      datadir+"/goa_uniprot_all.species.203"])
    swissprot_list=read_target_list(datadir+"/swissprot.list.overlap")
    uniref50_list =read_target_list(datadir+"/uniref50.list.overlap")
    reference_proteome_list=read_target_list(
                   datadir+"/reference_proteome.list.overlap")
    uniref90_list =read_target_list(datadir+"/uniref90.list.overlap")
    cafa_list     =read_cafa_list(
                   curdir+"/CAFA4.species.list",species_dict,swissprot_list)
    uniprot_list  =species_dict.keys()
    target_type_dict=read_target_type_dict(datadir)

    database_list=[
        ("UniProt"   ,set(uniprot_list)),
        ("UniRef90"  ,set(uniref90_list)),
        ("Reference" ,set(reference_proteome_list)),
        ("UniRef50"  ,set(uniref50_list)),
        ("SwissProt" ,set(swissprot_list)),
        ("CAFA4"     ,set(cafa_list)),
    ]
    lines=[]
    total_proteins_num=0
    total_species_num=0
    total_target_num_dict=dict(NK=0,LK=0,PK=0)
    for name,dataset in database_list:
        proteins_num,species_num,target_num_dict=get_target_type_stat(
            dataset,species_dict,target_type_dict)
        if total_proteins_num==0:
            total_proteins_num=proteins_num
            total_species_num=species_num
            for target_type in target_num_dict:
                total_target_num_dict[target_type]=target_num_dict[target_type]
        lines.append("| %s | %d (%.0f%%) | %d (%.0f%%) | %d (%.0f%%) | %d (%.0f%%) | %d (%.0f%%) |\n"%(
            name,
            proteins_num,100.*proteins_num/total_proteins_num,
            species_num,100.*species_num/total_species_num,
            target_num_dict["NK"],100.*target_num_dict["NK"]/total_target_num_dict["NK"],
            target_num_dict["LK"],100.*target_num_dict["LK"]/total_target_num_dict["LK"],
            target_num_dict["PK"],100.*target_num_dict["PK"]/total_target_num_dict["PK"]))
    lines.append("| :--:     | :--:      | :--:     | :--:      | :--:      | :--:      |\n")
    lines.append("| Database | Proteins  | Species  | NK        | LK        | PK        |\n")
    print(''.join(lines[::-1]))
