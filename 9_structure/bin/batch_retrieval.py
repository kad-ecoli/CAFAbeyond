#!/usr/bin/env python
docstring='''
batch_retrieval.py input.list input.fasta output.fasta
    extract the subset of targets common between input.list and input.fasta.
    output the common set to output.fasta
'''
import sys

def batch_retrieval(target_list,infile,outfile):
    target_set=set(target_list)
    outtxt=''
    fp=open(infile,'r')
    txt=fp.read()
    fp.close()
    if txt.startswith('>'): # fasta format
        blocks=('\n'+txt).split('\n>')
        for block in blocks:
            lines=block.splitlines()
            if len(lines)<2:
                continue
            target=lines[0].split()[0]
            if not target in target_set:
                continue
            outtxt+='>'+block.strip()+'\n'
    else:
        for line in txt.splitlines():
            target=line.split()[0]
            if not target in target_set:
                continue
            outtxt+=line+'\n'
    fp=open(outfile,'w')
    fp.write(outtxt)
    fp.close()
    return

if __name__=="__main__":
    if len(sys.argv)!=4:
        sys.stderr.write(docstring)
        exit()

    listfile=sys.argv[1]
    infile  =sys.argv[2]
    outfile =sys.argv[3]

    fp=open(listfile,'r')
    target_list=fp.read().splitlines()
    fp.close()

    batch_retrieval(target_list,infile,outfile)
