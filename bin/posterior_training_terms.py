#!/usr/bin/env python
docstring='''posterior_training_terms.py go-basic.obo uniprot_sprot_exp.F posterior.F
    calculate the posterior probability of child GO terms given parent terms
'''
import sys
import obo2csv # parsing GO hierachy
import gzip

def posterior_training_terms(obo_dict,infile,outfile):
    allterm_dict=dict()
    if infile.endswith(".gz"):
        fp=gzip.open(infile,'r')
    else:
        fp=open(infile,'r')
    lines=fp.read().splitlines()
    fp.close()

    allterm_list=[]
    for line in lines: 
        items=line.split('\t')
        target=items[0]
        GOterms=items[1].split(',')
        allterm_dict[target]=set(GOterms)
        allterm_list+=GOterms
    allterm_list=sorted(list(set(allterm_list)))
    print("%d terms for %s"%(len(allterm_list),outfile))

    GOterm_count_dict=dict()
    for GOterm in allterm_list:
        GOterm_count_dict[GOterm]=1.+sum([GOterm in allterm_dict[target] \
            for target in allterm_dict])
    print("%d proteins"%(max(GOterm_count_dict.values())))

    prob_dict=dict() # key is child; value is parent
    for GOterm in allterm_list:
        prob_dict[GOterm]=dict()
        for parent_GO in obo_dict.is_a(Term_id=GOterm, direct=False,
            name=True, number=False).split('\t'):
            parent_GO,name=parent_GO.split(" ! ")
            if parent_GO==GOterm:
                continue
            prob=(1.+GOterm_count_dict[GOterm])/(
                  1.+GOterm_count_dict[parent_GO])
            if ("%.3f"%prob)!="0.000":
                prob_dict[GOterm][parent_GO]=prob
        #print("%d parents for %s"%(len(prob_dict[GOterm]),GOterm))

    posterior_dict=dict() # key is parent, value is child
    for parent_GO in allterm_list:
        posterior_dict[parent_GO]=[]
        for GOterm in prob_dict:
            if parent_GO in prob_dict[GOterm]:
                prob=prob_dict[GOterm][parent_GO]
                posterior_dict[parent_GO].append((prob,GOterm))
        posterior_dict[parent_GO].sort(reverse=True)
    
    txt=''
    for GOterm in allterm_list:
        if len(posterior_dict[GOterm])==0:
            continue
        txt+=GOterm+'\t'+','.join([parent_GO+'_%.3f'%posterior for \
            posterior,parent_GO in posterior_dict[GOterm]])+'\n'
    fp=open(outfile,'w')
    fp.write(txt)
    fp.close()
    return

if __name__=="__main__":
    if len(sys.argv)!=4:
        sys.stderr.write(docstring)
        exit()

    obo_file=sys.argv[1]
    infile  =sys.argv[2]
    outfile =sys.argv[3]

    obo_dict=obo2csv.parse_obo_file(obo_file)
    posterior_training_terms(obo_dict,infile,outfile)
