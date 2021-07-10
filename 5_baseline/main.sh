#!/bin/bash
FILE=`readlink -e $0`
curdir=`dirname $FILE`
rootdir=`dirname $curdir`
datadir="$rootdir/data"
inputdir="$rootdir/input"
bindir="$rootdir/bin"

cd $curdir/
$curdir/curate.sh
$curdir/predict.sh
$curdir/assess.sh
./plot.py
