#!/bin/bash
FILE=`readlink -e $0`
rootdir=`dirname $FILE`
datadir="$rootdir/data"
downloaddir="$rootdir/download"

wget http://release.geneontology.org/2020-06-01/ontology/go-basic.obo -O $datadir/go-basic.obo
wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/old/UNIPROT/goa_uniprot_all.gaf.198.gz -O $downloaddir/goa_uniprot_all.gaf.198.gz
wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/old/UNIPROT/goa_uniprot_all.gaf.203.gz -O $downloaddir/goa_uniprot_all.gaf.203.gz
if [ ! -s "$downloaddir/goa_uniprot_all.gaf.203.gz" ];then
    wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/goa_uniprot_all.gaf.gz -O $downloaddir/goa_uniprot_all.gaf.203.gz
fi

wget "https://www.uniprot.org/uniprot/?query=reviewed:yes&format=list" -O $datadir/swissprot.list
wget "https://www.uniprot.org/uniref/?query=&fil=identity:0.5&format=list" -O $downloaddir/uniref50.list
wget "https://www.uniprot.org/uniref/?query=&fil=identity:0.9&format=list" -O $downloaddir/uniref90.list
wget "https://www.uniprot.org/uniprot/?query=proteome:(reference:yes)&format=list" -O $datadir/reference_proteome.list
