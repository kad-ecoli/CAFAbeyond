#!/bin/bash
FILE=`readlink -e $0`
curdir=`dirname $FILE`
rootdir=`dirname $curdir`
datadir="$rootdir/data"
inputdir="$rootdir/input"
bindir="$rootdir/bin"

cd $curdir/result

method_list="
naive_1
naive_2
naive_3
goa_1
blastlocalID_1
blastglobalID_1
blastglobalID_2
blastglobalID_3
blastevalue_1
blastrank_1
blastfreq_1
blastmetago_1
blastnetgo_1
metago_1
metago_2
tmalignfreq_1
tmalignID_3
tmalignTM_3
tmalignTMID_3
ppi_1
coxpres_1
coxpres_2
coxpres_3
"

for method in $method_list;do
    if [ ! -s "${method}_all.txt" ];then
        continue
    fi
    echo assessing $method
    $curdir/bin/assess_result.py ${method}_all.txt ${method}_all_results.txt
done
