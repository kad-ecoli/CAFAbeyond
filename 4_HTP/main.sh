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

$bindir/make_target.py \
    EXP.F.is_a.$old EXP.P.is_a.$old EXP.C.is_a.$old \
    EXP.F.is_a.$new EXP.P.is_a.$new EXP.C.is_a.$new \
    EXP_NK.F EXP_NK.P EXP_NK.C \
    EXP_LK.F EXP_LK.P EXP_LK.C \
    EXP_PK.F EXP_PK.P EXP_PK.C

cat EXP_NK.F EXP_LK.F EXP_PK.F > EXP.F
cat EXP_NK.P EXP_LK.P EXP_PK.P > EXP.P
cat EXP_NK.C EXP_LK.C EXP_PK.C > EXP.C

$bindir/make_target.py \
    HTP.F.is_a.$old HTP.P.is_a.$old HTP.C.is_a.$old \
    HTP.F.is_a.$new HTP.P.is_a.$new HTP.C.is_a.$new \
    HTP_NK.F HTP_NK.P HTP_NK.C \
    HTP_LK.F HTP_LK.P HTP_LK.C \
    HTP_PK.F HTP_PK.P HTP_PK.C

cat HTP_NK.F HTP_LK.F HTP_PK.F > HTP.F
cat HTP_NK.P HTP_LK.P HTP_PK.P > HTP.P
cat HTP_NK.C HTP_LK.C HTP_PK.C > HTP.C

$bindir/make_target.py \
    EXP+HTP.F.is_a.$old EXP+HTP.P.is_a.$old EXP+HTP.C.is_a.$old \
    EXP+HTP.F.is_a.$new EXP+HTP.P.is_a.$new EXP+HTP.C.is_a.$new \
    EXP+HTP_NK.F EXP+HTP_NK.P EXP+HTP_NK.C \
    EXP+HTP_LK.F EXP+HTP_LK.P EXP+HTP_LK.C \
    EXP+HTP_PK.F EXP+HTP_PK.P EXP+HTP_PK.C

cat EXP+HTP_NK.F EXP+HTP_LK.F EXP+HTP_PK.F > EXP+HTP.F
cat EXP+HTP_NK.P EXP+HTP_LK.P EXP+HTP_PK.P > EXP+HTP.P
cat EXP+HTP_NK.C EXP+HTP_LK.C EXP+HTP_PK.C > EXP+HTP.C

rm *EXP.*.is_a* *EXP_*K.*
rm *HTP.*.is_a* *HTP_*K.*