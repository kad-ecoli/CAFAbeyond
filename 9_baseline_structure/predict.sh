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
$curdir/bin/predict_metago.py    $curdir/input/target.blastp $curdir/input/target.psiblast metago_1_all.txt

for c in `cut -c3 $curdir/input/target.list|sort|uniq`;do
    if [ -s "$resultdir/tmalignTMID_3_$c.txt" ];then
	continue
    fi
    echo "combine tmalign for xx$c"
    grep -P "^\w\w$c" $curdir/input/target.list > target.$c.list
    rm target.$c.tm
    for target in `cat target.$c.list`;do
	    if [ ! -s "$curdir/tmalign/$target.tm" ];then
	    continue
	fi
	grep -v '#' $curdir/tmalign/$target.tm >> target.$c.tm 
    done
    echo "predict_tmalign for xx$c"
    $curdir/bin/predict_tmalign.py  target.$c.tm _$c.txt
    rm target.$c.tm target.$c.list
done

method_list="tmalignfreq_1
tmalignID_3
tmalignTM_3
tmalignTMID_3"
for method in $method_list;do
    outfile=$resultdir/${method}_all.txt
    head -3 `ls $resultdir/${method}_*.txt|grep -P "${method}_\w.txt"|head -1` > $outfile
    for infile in `ls $resultdir/${method}_*.txt|grep -P "${method}_\w.txt"`;do
	grep -P "GO:\d{7}" $infile >> $outfile
    done
    echo END >> $outfile
done
