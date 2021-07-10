#!/bin/bash
FILE=`readlink -e $0`
curdir=`dirname $FILE`
rootdir=`dirname $curdir`
datadir="$rootdir/data"
inputdir="$rootdir/input"
bindir="$rootdir/bin"

cd $curdir/
$bindir/predict_blastbitscore.py $inputdir/target.fasta _all.txt
$bindir/predict_blast.py $inputdir/target.fasta _all.txt 
$bindir/predict_naive.py $inputdir/target.species _all.txt 
$bindir/predict_goa.py $inputdir/target.list $inputdir/target.is_a goa_1_all.txt
