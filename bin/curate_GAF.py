#!/usr/bin/env python
docstring='''
curate_GAF.py goa_uniprot_all.gaf.gz goa_uniprot_all.EXP goa_uniprot_all.NOT.EXP goa_uniprot_all.HTP goa_uniprot_all.NOT.HTP goa_uniprot_all.species

Input:
    goa_uniprot_all.gaf.gz  - GAF format GO annotation

Output:
    goa_uniprot_all.EXP     - positive annotation with EXP,IDA,IPI,IMP,IGI,IEP
    goa_uniprot_all.EXP.NOT - negative annotation with EXP,IDA,IPI,IMP,IGI,IEP
    goa_uniprot_all.HTP     - positive annotation with HTP,HDA,HMP,HGI,HEP
    goa_uniprot_all.HTP.NOT - negative annotation with HTP,HDA,HMP,HGI,HEP
    goa_uniprot_all.species - accessions and taxon with the above evidence codes

Option:
    -db=RNAcentral          - parse RNAcentral entry rather than UniProtKB entry
'''

# GAF2.1 files have the suffix .gaf and contain the following columns:
#
# Column  Contents
# 1       DB
# 2       DB_Object_ID
# 3       DB_Object_Symbol
# 4       Qualifier
# 5       GO_ID
# 6       DB:Reference
# 7       Evidence Code
# 8       With (or) From
# 9       Aspect
# 10      DB_Object_Name
# 11      DB_Object_Synonym
# 12      DB_Object_Type
# 13      Taxon and Interacting taxon
# 14      Date
# 15      Assigned_By
# 16      Annotation_Extension
# 17      Gene_Product_Form_ID

import gzip
import sys

def curate_GAF(infile,outfileEXP,outfileEXPnot,outfileHTP,outfileHTPnot,
    outfileSpecies, db="UniProtKB"):
    target_list=[]
    outEXP=''
    outEXPnot=''
    outHTP=''
    outHTPnot=''
    if infile.endswith(".gz"):
        fp=gzip.open(infile,'r')
    else:
        fp=open(infile,'r')
    EXP_set={'EXP','IDA','IPI','IMP','IGI','IEP','TAS','IC'}
    HTP_set={'HTP','HDA',      'HMP','HGI','HEP'}
    for line in fp.read().splitlines():
        if not line.startswith(db):
            continue
        items       =line.split('\t')
        DB_Object_ID=items[1]
        Qualifier   =items[3]
        GO_ID       =items[4]
        EvidenceCode=items[6]
        Taxon       =items[12]
        if not EvidenceCode in EXP_set and not EvidenceCode in HTP_set:
            continue
        target=DB_Object_ID+'\t'+Taxon.split('|')[0].split(':')[1]+'\n'
        target_list.append(target)
        if EvidenceCode in EXP_set:
            if "NOT" in Qualifier:
                outEXPnot+=line+'\n'
            else:
                outEXP   +=line+'\n'
        elif EvidenceCode in HTP_set:
            if "NOT" in Qualifier:
                outHTPnot+=line+'\n'
            else:
                outHTP   +=line+'\n'
    target_list=list(set(target_list))
    fp=open(outfileSpecies,'w')
    fp.write(''.join(target_list))
    fp.close()
    fp=open(outfileEXP,'w')
    fp.write(outEXP)
    fp.close()
    fp=open(outfileEXPnot,'w')
    fp.write(outEXPnot)
    fp.close()
    fp=open(outfileHTP,'w')
    fp.write(outHTP)
    fp.close()
    fp=open(outfileHTPnot,'w')
    fp.write(outHTPnot)
    fp.close()
    return

if __name__=="__main__":
    if len(sys.argv)<7:
        sys.stderr.write(docstring)
        exit()

    db="UniProtKB"
    args=[]
    for arg in sys.argv[1:]:
        if arg.startswith('-db='):
            db=arg[len("-db="):]
        elif arg.startswith('-'):
            sys.stderr.write("ERROR! Unknown option %s\n"%arg)
        else:
            args.append(arg)
    infile,outfileEXP,outfileEXPnot,outfileHTP,outfileHTPnot,outfileSpecies=args
    curate_GAF(infile,outfileEXP,outfileEXPnot,
        outfileHTP,outfileHTPnot,outfileSpecies,db)
