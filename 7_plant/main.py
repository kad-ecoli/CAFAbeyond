#!/usr/bin/env python
docstring='''
main.py fullnamelineage.plant.dmp goa_uniprot_all.species.203 datadir
    statistics on plant species among targets
'''
import sys

def parse_taxid_name(fullnamedmp):
    taxid_name_dict=dict()
    fp=open(fullnamedmp,'r')
    for line in fp.read().splitlines():
        taxid,name=line.rstrip().split('\t|\t')
        taxid_name_dict[taxid]=name
    fp.close()
    return taxid_name_dict

def parse_uniprot_species(uniprotspecies,taxid_name_dict):
    accession_species_dict=dict()
    fp=open(uniprotspecies,'r')
    for line in fp.read().splitlines():
        accession,taxid=line.split('\t')
        if not taxid in taxid_name_dict:
            continue
        accession_species_dict[accession]=taxid
    fp.close()
    return accession_species_dict

def species_target_stat(datadir,accession_species_dict,taxid_name_dict):
    txt="# plant targets #\n"
    for target_type in ["NK","LK","PK"]:
        for Aspect in "FPC":
            filename="%s/%s.%s"%(datadir,target_type,Aspect)
            stat_dict=dict()
            fp=open(filename,'r')
            for line in fp.read().splitlines():
                accession=line.split('\t')[0]
                if not accession in accession_species_dict:
                    continue
                taxid=accession_species_dict[accession]
                if not taxid in stat_dict:
                    stat_dict[taxid]=[]
                stat_dict[taxid].append(accession)
            fp.close()
            stat_list=[]
            for taxid in stat_dict:
                stat_dict[taxid]=len(stat_dict[taxid])
                stat_list.append((stat_dict[taxid],taxid))
            stat_list.sort(reverse=True)
            txt+="* %s target %s aspect: %d targets;\t%d from %s (%s)"%(
                target_type,Aspect,
                sum(stat_dict.values()),stat_list[0][0],
                taxid_name_dict[stat_list[0][1]],stat_list[0][1])
            if len(stat_list)>1:
                txt+=";\t%d from %s (%s)"%(stat_list[1][0],
                    taxid_name_dict[stat_list[1][1]],stat_list[1][1])
            txt+='\n'
    fp=open("readme.md",'w')
    fp.write(txt)
    fp.close()
    return

if __name__=="__main__":
    if len(sys.argv)!=4:
        sys.stderr.write(docstring)
        exit()

    fullnamedmp   =sys.argv[1]
    uniprotspecies=sys.argv[2]
    datadir       =sys.argv[3]

    taxid_name_dict=parse_taxid_name(fullnamedmp)
    accession_species_dict=parse_uniprot_species(uniprotspecies,taxid_name_dict)
    species_target_stat(datadir,accession_species_dict,taxid_name_dict) 
