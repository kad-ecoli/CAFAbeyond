#!/bin/bash
FILE=`readlink -e $0`
curdir=`dirname $FILE`
rootdir=`dirname $curdir`
datadir="$rootdir/data"
downloaddir="$rootdir/download"
bindir="$rootdir/bin"

$curdir/main.py $datadir/goa_uniprot_all.species.203 $datadir 
