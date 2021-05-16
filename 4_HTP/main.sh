#!/bin/bash
FILE=`readlink -e $0`
curdir=`dirname $FILE`
rootdir=`dirname $curdir`
datadir="$rootdir/data"
downloaddir="$rootdir/download"
bindir="$rootdir/bin"

cd $curdir

old=198
new=203
for version in `echo $old $new`;do
    $bindir/propagate_gaf_terms.py $datadir/go-basic.obo \
	    $datadir/goa_uniprot_all.EXP.${version}.gz   \
	    EXP.F.is_a.$version EXP.P.is_a.$version EXP.C.is_a.$version
    $bindir/propagate_gaf_terms.py $datadir/go-basic.obo \
	$datadir/goa_uniprot_all.HTP.${version}.gz       \
	HTP.F.is_a.$version HTP.P.is_a.$version HTP.C.is_a.$version
    zcat $datadir/goa_uniprot_all.EXP.${version}.gz      \
	 $datadir/goa_uniprot_all.HTP.${version}.gz |gzip - > EXP+HTP.${version}.gz
    $bindir/propagate_gaf_terms.py $datadir/go-basic.obo \
	EXP+HTP.${version}.gz \
	EXP+HTP.F.is_a.$version EXP+HTP.P.is_a.$version EXP+HTP.C.is_a.$version
    rm  EXP+HTP.${version}.gz
done

for evidence in `echo EXP HTP EXP+HTP`;do
    $bindir/make_target.py \
	${evidence}.F.is_a.$old ${evidence}.P.is_a.$old ${evidence}.C.is_a.$old \
	${evidence}.F.is_a.$new ${evidence}.P.is_a.$new ${evidence}.C.is_a.$new \
	${evidence}_NK.F        ${evidence}_NK.P        ${evidence}_NK.C \
	${evidence}_LK.F        ${evidence}_LK.P        ${evidence}_LK.C \
	${evidence}_PK.F        ${evidence}_PK.P        ${evidence}_PK.C
    cat ${evidence}_NK.F ${evidence}_LK.F ${evidence}_PK.F > ${evidence}.F
    cat ${evidence}_NK.P ${evidence}_LK.P ${evidence}_PK.P > ${evidence}.P
    cat ${evidence}_NK.C ${evidence}_LK.C ${evidence}_PK.C > ${evidence}.C
    rm ${evidence}.*.is_a* ${evidence}_*K.*
done

echo "| evidence | MF targets | BP targets | CC targets |" >  readme.md
echo "| :--:     | :--:       | :--:       | :--:       |" >> readme.md
for evidence in `echo EXP HTP EXP+HTP`;do
    echo "| $evidence    |" `cat $evidence.F|wc -l` "      |" `cat $evidence.P|wc -l` "      |" `cat $evidence.C|wc -l` "      |" >> readme.md
done
