#!/usr/bin/env python
docstring='''cull_IEA.py go-basic.obo target.list goa_uniprot_all.gaf target.is_a
    remove proteins and terms unrelated to target dataset from goa_uniprot_all.gaf.
    save remaining annotations to target.is_a
'''
import sys
import obo2csv # parsing GO hierachy
import gzip

def read_map_file(map_file):
    fp=open(map_file,'r')
    accession_list=fp.read().splitlines()
    fp.close()
    return accession_list

def isa_IEA(obo_dict,GOterm_list,accession_list,gaf_file,isa_file):
    annotation_dict=dict()
    GOterm_set=set(GOterm_list)
    if gaf_file.endswith(".gz"):
        fp=gzip.open(gaf_file,'r')
    else:
        fp=open(gaf_file,'r')
    for line in fp:
        if not line.startswith('UniProtKB'):
            continue
        items=line.split('\t')
        accession=items[1]
        qualifier=items[3]
        GOterm=items[4]
        evidence=items[6]
        Aspect=items[8]
        if  not accession in accession_list or \
            qualifier.startswith("NOT") or \
            not GOterm in GOterm_set or evidence=="ND":
            continue
        key='\t'.join([accession,Aspect,GOterm])
        if not key in annotation_dict:
            annotation_dict[key]=[]
        elif evidence in annotation_dict[key]:
            continue
        annotation_dict[key].append(evidence)
    fp.close()
    for key,evidence_list in annotation_dict.items():
        accession,Aspect,GOterm=key.split('\t')
        for parent_GO in obo_dict.is_a(Term_id=GOterm, direct=False,
            name=True, number=False).split('\t'):
            GO_ID,name=parent_GO.split(" ! ")
            key='\t'.join([accession,Aspect,GO_ID])
            if not key in annotation_dict:
                annotation_dict[key]=evidence_list
            else:
                annotation_dict[key]+=evidence_list
    for key in annotation_dict:
        annotation_dict[key]=sorted(set(annotation_dict[key]))
    txt=''
    for key in sorted(annotation_dict.keys()):
        txt+=key+'\t'+','.join(annotation_dict[key])+'\n'
    fp=open(isa_file,'w')
    fp.write(txt)
    fp.close()
    return

if __name__=="__main__":
    if len(sys.argv)!=5:
        sys.stderr.write(docstring)
        exit()

    obo_file=sys.argv[1]
    map_file=sys.argv[2]
    gaf_file=sys.argv[3]
    isa_file=sys.argv[4]

    obo_dict=obo2csv.parse_obo_file(obo_file)
    accession_list=read_map_file(map_file)
    GOterm_list=obo_dict['F']['Term'].keys()+ \
                obo_dict['P']['Term'].keys()+ \
                obo_dict['C']['Term'].keys()
    isa_IEA(obo_dict,GOterm_list,accession_list,gaf_file,isa_file)
