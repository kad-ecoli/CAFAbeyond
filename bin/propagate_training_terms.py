#!/usr/bin/env python
docstring='''propagate_training_term.py go-basic.obo goa_uniprot_all.EXP.198.gz uniprot_sprot_exp.
    propagate parent GO terms for training set "goa_uniprot_all.EXP.198.gz".
    output full sets of GO term to uniprot_sprot_exp.{F,P,C}
'''
import sys
import obo2csv # parsing GO hierachy
import gzip

def propagate_training_term(obo_dict,infile,prefix):
    allterm_dict={'F':dict(),'C':dict(),'P':dict()}
    if infile.endswith(".gz"):
        fp=gzip.open(infile,'r')
    else:
        fp=open(infile,'r')
    lines=fp.read().splitlines()
    fp.close()
    DB_Object_ID_list=[]
    for line in lines:
        items=line.split('\t')
        DB_Object_ID=items[1]
        GO_ID=items[4]
        Aspect=items[8]
        if not DB_Object_ID in DB_Object_ID_list:
            DB_Object_ID_list.append(DB_Object_ID)
        if not GO_ID in obo_dict[Aspect]["Term"]:
            sys.stderr.write("ERROR! Cannot find GO Term %s\n"%GO_ID)
            continue
        if not DB_Object_ID in allterm_dict[Aspect]:
            allterm_dict[Aspect][DB_Object_ID]=[]
        if not GO_ID in allterm_dict[Aspect][DB_Object_ID]:
            allterm_dict[Aspect][DB_Object_ID].append(GO_ID)

    for Aspect in "FPC":
        filename=prefix+Aspect
        print("writing "+filename)
        txt=''
        for DB_Object_ID in DB_Object_ID_list:
            if not DB_Object_ID in allterm_dict[Aspect]:
                continue
            if ','.join(allterm_dict[Aspect][DB_Object_ID])=="GO:0005515":
                continue # remove protein binding only target
            for GO_ID in allterm_dict[Aspect][DB_Object_ID]:
                for parent_GO in obo_dict.is_a(Term_id=GO_ID, direct=False,
                    name=True, number=False).split('\t'):
                    GO_ID,name=parent_GO.split(" ! ")
                    if not GO_ID in allterm_dict[Aspect][DB_Object_ID]:
                        allterm_dict[Aspect][DB_Object_ID].append(GO_ID)
            GOterms=','.join(sorted(allterm_dict[Aspect][DB_Object_ID]))
            txt+="%s\t%s\n"%(DB_Object_ID,GOterms)
        fp=open(filename,'w')
        fp.write(txt)
        fp.close()
    return

if __name__=="__main__":
    if len(sys.argv)!=4:
        sys.stderr.write(docstring)
        exit()

    obo_file=sys.argv[1]
    infile  =sys.argv[2]
    prefix  =sys.argv[3]

    obo_dict=obo2csv.parse_obo_file(obo_file)
    propagate_training_term(obo_dict,infile,prefix)
