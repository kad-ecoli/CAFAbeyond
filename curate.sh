#!/bin/bash
FILE=`readlink -e $0`
rootdir=`dirname $FILE`
datadir="$rootdir/data"
downloaddir="$rootdir/download"
bindir="$rootdir/bin"

cut -f2 -d_ $downloaddir/uniref50.list > $datadir/uniref50.list
cut -f2 -d_ $downloaddir/uniref90.list > $datadir/uniref90.list
for version in `echo 198 203`;do
    zcat $downloaddir/goa_uniprot_all.gaf.$version.gz |grep -P "(\tEXP\t)|(\tIDA\t)|(\tIPI\t)|(\tIMP\t)|(\tIGI\t)|(\tIEP\t)|(\tTAS\t)|(\tIC\t)|(\tHTP\t)|(\tHDA\t)|(\tHMP\t)|(\tHGI\t)|(\tHEP\t)" | gzip - > $datadir/goa_uniprot_all.gaf.${version}.gz
    $bindir/curate_GAF.py \
         $datadir/goa_uniprot_all.gaf.${version}.gz \
         $datadir/goa_uniprot_all.EXP.${version} \
         $datadir/goa_uniprot_all.EXP.NOT.${version} \
         $datadir/goa_uniprot_all.HTP.${version} \
         $datadir/goa_uniprot_all.HTP.NOT.${version} \
         $datadir/goa_uniprot_all.species.${version}
        
    gzip $datadir/goa_uniprot_all.EXP.${version}
    gzip $datadir/goa_uniprot_all.EXP.NOT.${version}
    gzip $datadir/goa_uniprot_all.HTP.${version}
    gzip $datadir/goa_uniprot_all.HTP.NOT.${version}

    $bindir/propagate_gaf_terms.py $datadir/go-basic.obo $datadir/goa_uniprot_all.EXP.${version}.gz $datadir/goa_uniprot_all.F.is_a.$version $datadir/goa_uniprot_all.P.is_a.$version data/goa_uniprot_all.C.is_a.$version

done


cat $datadir/goa_uniprot_all.species.* |cut -f1|sort|uniq > $datadir/goa_uniprot_all.species

for listfile in `echo swissprot.list uniref50.list uniref90.list reference_proteome.list`;do
    cat $datadir/goa_uniprot_all.species $datadir/$listfile |sort|uniq -c|grep -F " 2 "|grep -ohP "\S+$" > $datadir/${listfile}.overlap
done

version=198
$bindir/calculate_ic.py $datadir/go-basic.obo  $datadir/goa_uniprot_all.F.is_a.$version   $datadir/naive.F.with_GO:0005515
$bindir/calculate_ic.py $datadir/go-basic.obo  $datadir/goa_uniprot_all.P.is_a.$version   $datadir/naive.P
$bindir/calculate_ic.py $datadir/go-basic.obo  $datadir/goa_uniprot_all.C.is_a.$version   $datadir/naive.C
grep -vP "\tGO:0003674,GO:0005488,GO:0005515$" $datadir/goa_uniprot_all.F.is_a.$version > $datadir/no_GO:0005515.F.is_a.$version 
$bindir/calculate_ic.py $datadir/go-basic.obo  $datadir/no_GO:0005515.F.is_a.$version     $datadir/naive.F
