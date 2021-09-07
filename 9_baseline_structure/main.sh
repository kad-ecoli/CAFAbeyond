#!/bin/bash
FILE=`readlink -e $0`
curdir=`dirname $FILE`
cd $curdir

$curdir/curate.sh
$curdir/search.sh
$curdir/predict.sh
$curdir/assess.sh
