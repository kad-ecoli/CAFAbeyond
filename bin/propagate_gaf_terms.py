#!/usr/bin/env python
docstring='''
propagate_gaf_term.py go-basic.obo goa_uniprot_all.gaf.gz goa_uniprot_all.F.is_a goa_uniprot_all.P.is_a goa_uniprot_all.C.is_a
    propagate parent GO terms for GAF format GO annotation from 
    goa_uniprot_all.gaf.gz output full sets of GO term to 
    goa_uniprot_all.F.is_a, goa_uniprot_all.P.is_a, goa_uniprot_all.C.is_a
'''
import sys
import obo2csv # parsing GO hierachy
import gzip

def propagate_gaf_term(obo_dict,infile,outfile_dict):
    allterm_dict=dict(F=dict(),P=dict(),C=dict())
    missing_GO_list=[]
    
    if infile.endswith(".gz"):
        fp=gzip.open(infile,'r')
    else:
        fp=open(infile,'r')
    lines=fp.read().splitlines()
    fp.close()
    for line in lines:
        items=line.split('\t')
        DB_Object_ID=items[1]
        GO_ID=items[4]
        Aspect=items[8]
        if not GO_ID in obo_dict[Aspect]["Term"]:
            if not GO_ID in missing_GO_list:
                sys.stderr.write("ERROR! Cannot find GO Term %s\n"%GO_ID)
                missing_GO_list.append(GO_ID)
            continue
        if not DB_Object_ID in allterm_dict[Aspect]:
            allterm_dict[Aspect][DB_Object_ID]=[]
        if not GO_ID in allterm_dict[Aspect][DB_Object_ID]:
            allterm_dict[Aspect][DB_Object_ID].append(GO_ID)

        for parent_GO in obo_dict.is_a(Term_id=GO_ID, direct=False,
            name=True, number=False).split('\t'):
            GO_ID,name=parent_GO.split(" ! ")
            if not GO_ID in allterm_dict[Aspect][DB_Object_ID]:
                allterm_dict[Aspect][DB_Object_ID].append(GO_ID)

    for Aspect in "FPC":
        outfile=outfile_dict[Aspect]
        print("writing "+outfile)
        txt=''
        for DB_Object_ID in allterm_dict[Aspect]:
            txt+="%s\t%s\n"%(DB_Object_ID,
                ','.join(sorted(allterm_dict[Aspect][DB_Object_ID])))
        fp=open(outfile,'w')
        fp.write(txt)
        fp.close()
    return

if __name__=="__main__":
    if len(sys.argv)!=6:
        sys.stderr.write(docstring)
        exit()

    obo_file         =sys.argv[1]
    infile           =sys.argv[2]
    outfile_dict     =dict()
    outfile_dict['F']=sys.argv[3]
    outfile_dict['P']=sys.argv[4]
    outfile_dict['C']=sys.argv[5]

    obo_dict=obo2csv.parse_obo_file(obo_file)
    propagate_gaf_term(obo_dict,infile,outfile_dict)
