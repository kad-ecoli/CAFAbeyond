#!/usr/bin/env python
docstring='''
main.py ../data/goa_uniprot_all.species.203 ../data
    check species diversity of high IC target subset
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

def parse_uniprot_species(uniprotspecies):
    accession_species_dict=dict()
    fp=open(uniprotspecies,'r')
    for line in fp.read().splitlines():
        accession,taxid=line.split('\t')
        accession_species_dict[accession]=taxid
    fp.close()
    return accession_species_dict

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
    return per_target_ic_dict

def subset_ic(per_target_ic_dict,accession_species_dict,portion=1.0):
    target_list=[]
    for target in per_target_ic_dict:
        if not target in accession_species_dict or not target in accession_species_dict:
            continue
        species=accession_species_dict[target]
        ic=per_target_ic_dict[target]
        target_list.append((ic,species,target))
    target_num=int(len(target_list)*portion)
    if portion>1:
        target_num=int(portion)
    if target_num>len(target_list):
        target_num=len(target_list)
    target_list=sorted(target_list,reverse=True)
    target_list=target_list[:target_num]
    species_list=[]
    for ic,species,target in target_list:
        species_list.append(species)
    return len(set(species_list))

if __name__=="__main__":
    if len(sys.argv)!=3:
        sys.stderr.write(docstring)
        exit(0)
    uniprotspecies=sys.argv[1]
    datadir       =sys.argv[2]

    ic_dict=read_ic((datadir+"/naive.F", datadir+"/naive.P",
                     datadir+"/naive.C"))
    accession_species_dict=parse_uniprot_species(uniprotspecies)
    all_target_ic_dict=dict(F=dict(),P=dict(),C=dict())
    print("# species diversity among the subset of targets with highest IC #")
    print("| target type | GO aspect | target | species | species for top 1000 targets | species for top 500 targets | species for top 300 targets | species for 100 targets |")
    print("| :--:        | :--:      | :--:   | :--:    | :--:                         | :--:                        | :--:                        | :--:                    |")
    for target_type in ["NK","LK","PK"]:
        for Aspect in "FPC":
            filename=datadir+"/"+target_type+"."+Aspect
            if target_type =="All":
                filename=[datadir+"/NK."+Aspect,
                          datadir+"/LK."+Aspect,
                          datadir+"/PK."+Aspect]
            all_target_ic_dict[Aspect][target_type]=calculate_target_ic(
                filename,ic_dict)
            species_all=subset_ic(all_target_ic_dict[Aspect][target_type],
                accession_species_dict,1)
            species_1000=subset_ic(all_target_ic_dict[Aspect][target_type],
                accession_species_dict,1000)
            species_500=subset_ic(all_target_ic_dict[Aspect][target_type],
                accession_species_dict,500)
            species_300=subset_ic(all_target_ic_dict[Aspect][target_type],
                accession_species_dict,300)
            species_100=subset_ic(all_target_ic_dict[Aspect][target_type],
                accession_species_dict,100)
            print("| %s | %s | %d | %d | %d | %d | %d | %d|"%(target_type,Aspect,
                len(all_target_ic_dict[Aspect][target_type]),
                species_all,species_1000,species_500,species_300,species_100))
