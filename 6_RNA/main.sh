#!/bin/bash
FILE=`readlink -e $0`
curdir=`dirname $FILE`
rootdir=`dirname $curdir`
datadir="$rootdir/data"
downloaddir="$rootdir/download"
bindir="$rootdir/bin"

old=198
new=203
for version in `echo $old $new`;do
    zcat $datadir/goa_uniprot_all.gaf.$version.gz|grep '^RNAcentral' |grep -P "(\tEXP\t)|(\tIDA\t)|(\tIPI\t)|(\tIMP\t)|(\tIGI\t)|(\tIEP\t)|(\tTAS\t)|(\tIC\t)|(\tHTP\t)|(\tHDA\t)|(\tHMP\t)|(\tHGI\t)|(\tHEP\t)" | gzip - > $curdir/goa_rnacentral_all.gaf.${version}.gz
    $bindir/curate_GAF.py -db=RNAcentral                  \
	    $curdir/goa_rnacentral_all.gaf.${version}.gz  \
	    $curdir/goa_rnacentral_all.EXP.${version}     \
	    $curdir/goa_rnacentral_all.EXP.NOT.${version} \
	    $curdir/goa_rnacentral_all.HTP.${version}     \
	    $curdir/goa_rnacentral_all.HTP.NOT.${version} \
	    $curdir/goa_rnacentral_all.species.${version}
	
    gzip -f $curdir/goa_rnacentral_all.EXP.${version}
    gzip -f $curdir/goa_rnacentral_all.EXP.NOT.${version}
    gzip -f $curdir/goa_rnacentral_all.HTP.${version}
    gzip -f $curdir/goa_rnacentral_all.HTP.NOT.${version}

    $bindir/propagate_gaf_terms.py $datadir/go-basic.obo \
	    $curdir/goa_rnacentral_all.EXP.${version}.gz \
	    $curdir/goa_rnacentral_all.F.is_a.$version   \
	    $curdir/goa_rnacentral_all.P.is_a.$version   \
	    $curdir/goa_rnacentral_all.C.is_a.$version
done

cat $curdir/goa_rnacentral_all.species.* |cut -f1|sort|uniq > $curdir/goa_rnacentral_all.species

$bindir/calculate_ic.py $datadir/go-basic.obo $curdir/goa_rnacentral_all.F.is_a.$old $curdir/naive.F
$bindir/calculate_ic.py $datadir/go-basic.obo $curdir/goa_rnacentral_all.P.is_a.$old $curdir/naive.P
$bindir/calculate_ic.py $datadir/go-basic.obo $curdir/goa_rnacentral_all.C.is_a.$old $curdir/naive.C

$bindir/make_target.py -exclude= \
    $curdir/goa_rnacentral_all.F.is_a.$old \
    $curdir/goa_rnacentral_all.P.is_a.$old \
    $curdir/goa_rnacentral_all.C.is_a.$old \
    $curdir/goa_rnacentral_all.F.is_a.$new \
    $curdir/goa_rnacentral_all.P.is_a.$new \
    $curdir/goa_rnacentral_all.C.is_a.$new \
    $curdir/NK.F $curdir/NK.P $curdir/NK.C \
    $curdir/LK.F $curdir/LK.P $curdir/LK.C \
    $curdir/PK.F $curdir/PK.P $curdir/PK.C


$rootdir/2_target_type/main.py -datadir=$curdir > $curdir/readme.md
