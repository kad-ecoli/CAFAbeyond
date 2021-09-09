#!/bin/bash
FILE=`readlink -e $0`
curdir=`dirname $FILE`
rootdir=`dirname $curdir`
datadir="$rootdir/data"
downloaddir="$rootdir/download"
inputdir="$rootdir/input"
bindir="$rootdir/bin"

cd $curdir/
$curdir/bin/blastp -db $curdir/data/uniprot_sprot_exp.fasta -outfmt '6 qacc qlen sacc slen evalue bitscore length nident' -query $curdir/input/target.fasta -out $curdir/input/target.blastp
$curdir/bin/psiblast -db $curdir/data/uniprot_sprot_exp.fasta -outfmt '6 qacc qlen sacc slen evalue bitscore length nident' -query $curdir/input/target.fasta -out $curdir/input/target.psiblast -num_iterations 3

cd $curdir/input/pdb
mkdir -p $curdir/tmalign
for target in `cat $curdir/input/target.list`;do
    $curdir/bin/TMalign $target.pdb.gz -dir2 $curdir/data/xyz/ $curdir/data/xyz/list -suffix .xyz.gz -infmt2 2 -outfmt 2 -fast |sed 's/.pdb.gz//g' |sed 's/[A-Z0-9].xyz.gz://g' > $curdir/tmalign/$target.tm
done

cat  $curdir/tmalign/*.tm | grep -P "(\t1\.0000\t)|(\t0\.[5-9]\d{3}\t)" > $curdir/input/target.tm
