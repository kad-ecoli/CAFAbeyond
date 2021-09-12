#!/bin/bash
FILE=`readlink -e $0`
curdir=`dirname $FILE`
resultdir=$curdir/result
mkdir -p $resultdir
cd $resultdir

$curdir/bin/predict_blast.py     $curdir/input/target.fasta _all.txt 
$curdir/bin/predict_naive.py     $curdir/input/target.species _all.txt 
$curdir/bin/predict_posterior.py $curdir/input/target.list $curdir/input/target.PK naive_3_all.txt
$curdir/bin/predict_goa.py       $curdir/input/target.list $curdir/input/target.is_a goa_1_all.txt
$curdir/bin/predict_metago.py    $curdir/input/target.blastp $curdir/input/target.psiblast _all.txt
$curdir/bin/predict_ppi.py       $curdir/input/target.list ppi_1_all.txt
$curdir/bin/predict_tmalign.py   $curdir/input/target.tm _all.txt

$curdir/bin/predict_coxpres.py $curdir/input/target.list $curdir/data/coxpres_r.gz coxpres_3_all.txt
$curdir/bin/predict_coxpres.py $curdir/input/target.list $curdir/data/coxpres_m.gz coxpres_2_all.txt
$curdir/bin/predict_coxpres.py $curdir/input/target.list $curdir/data/coxpres_u.gz coxpres_1_all.txt
