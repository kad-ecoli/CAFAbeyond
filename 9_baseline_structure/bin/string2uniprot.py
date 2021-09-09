#!/usr/bin/python2
docstring='''string2uniprot.py 10090.protein.links.v11.0.txt.gz 10090.uniprot_2_string.tsv 10090.uniprot.links

Input:
    10090.protein.links.v11.0.txt.gz - string format protein link file
    10090.uniprot_2_string.tsv       - two column table for uniprot accession and string
Output:
    10090.uniprot.links              - stringID replaced by uniprot
'''
import gzip
import sys

def string2uniprot(linkfile,mapfile,outfile):
    map_dict=dict()
    fp=open(mapfile,'r')
    for line in fp.read().splitlines():
        accession,stringID=line.split('\t')
        map_dict[stringID]=accession
    fp.close()

    txt=''
    fp=gzip.open(linkfile,'r')
    for line in fp.read().splitlines():
        items=line.split(' ')
        stringID1,stringID2,score=items
        if not stringID1 in map_dict or not stringID2 in map_dict:
            continue
        txt+="%s\t%s\t%s\n"%(map_dict[stringID1],map_dict[stringID2],score)
    fp.close()

    fp=open(outfile,'w')
    fp.write(txt)
    fp.close()
    return

if __name__=="__main__":
    if len(sys.argv)!=4:
        sys.stderr.write(docstring)
        exit()

    linkfile=sys.argv[1]
    mapfile =sys.argv[2]
    outfile =sys.argv[3]
    string2uniprot(linkfile,mapfile,outfile)
