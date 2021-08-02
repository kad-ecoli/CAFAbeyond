#!/bin/bash
FILE=`readlink -e $0`
curdir=`dirname $FILE`
rootdir=`dirname $curdir`
datadir="$rootdir/data"
downloaddir="$rootdir/download"
bindir="$rootdir/bin"

wget https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.zip -O new_taxdump.zip
unzip -u new_taxdump.zip fullnamelineage.dmp
grep "cellular organisms; Eukaryota; Viridiplantae; " fullnamelineage.dmp |cut -f1,2 -d'|' > fullnamelineage.plant.dmp
$curdir/main.py fullnamelineage.plant.dmp $datadir/goa_uniprot_all.species.203 $datadir 
