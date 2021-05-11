#!/bin/bash
FILE=`readlink -e $0`
rootdir=`dirname $FILE`
datadir="$rootdir/data"
downloaddir="$rootdir/download"

cut -f2 -d_ $downloaddir/uniref50.list > $datadir/uniref50.list
cut -f2 -d_ $downloaddir/uniref90.list > $datadir/uniref90.list
zcat $downloaddir/goa_uniprot_all.gaf.198.gz |grep -P "(\tEXP\t)|(\tIDA\t)|(\tIPI\t)|(\tIMP\t)|(\tIGI\t)|(\tIEP\t)|(\tHTP\t)|(\tHDA\t)|(\tHMP\t)|(\tHGI\t)|(\tHEP\t)" | gzip - > $datadir/goa_uniprot_all.gaf.198.gz
zcat $downloaddir/goa_uniprot_all.gaf.203.gz |grep -P "(\tEXP\t)|(\tIDA\t)|(\tIPI\t)|(\tIMP\t)|(\tIGI\t)|(\tIEP\t)|(\tHTP\t)|(\tHDA\t)|(\tHMP\t)|(\tHGI\t)|(\tHEP\t)" | gzip - > $datadir/goa_uniprot_all.gaf.203.gz
