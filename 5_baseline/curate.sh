#!/bin/bash
FILE=`readlink -e $0`
curdir=`dirname $FILE`
rootdir=`dirname $curdir`
datadir="$rootdir/data"
downloaddir="$rootdir/download"
inputdir="$rootdir/input"
bindir="$rootdir/bin"

cd $datadir/

$bindir/propagate_training_terms.py go-basic.obo goa_uniprot_all.EXP.198.gz uniprot_sprot_exp.
cat uniprot_sprot_exp.F uniprot_sprot_exp.P uniprot_sprot_exp.C|cut -f1|sort|uniq > uniprot_sprot_exp.list
$bindir/batch_retrieval.pl uniprot_sprot_exp.list |sed 's/>sp|/>/g'|sed 's/>tr|/>/g'|cut -f1 -d'|' > uniprot_sprot_exp.fasta


$bindir/makeblastdb -in uniprot_sprot_exp.fasta -dbtype prot -parse_seqids
$bindir/SelfScore uniprot_sprot_exp.fasta|grep -v '^#'|cut -f1,3 > uniprot_sprot_exp.fasta.SelfScore_nw
$bindir/blastSelfScore.py uniprot_sprot_exp.fasta uniprot_sprot_exp.fasta.SelfScore_blast
cat $datadir/*K.*|cut -f1 |sort|uniq> $inputdir/target.list
$bindir/batch_retrieval.pl $inputdir/target.list |sed 's/>sp|/>/g'|sed 's/>tr|/>/g'|cut -f1 -d'|' > $inputdir/target.fasta

zcat $downloaddir/goa_uniprot_all.gaf.198.gz |grep -E `cat $inputdir/target.list|paste -sd'|'` > $downloaddir/goa_uniprot_all.gaf.198.clean
$bindir/cull_IEA.py $datadir/go-basic.obo $inputdir/target.list $downloaddir/goa_uniprot_all.gaf.198.clean $inputdir/target.is_a 
rm $downloaddir/goa_uniprot_all.gaf.198.clean
zcat $datadir/goa_uniprot_all.EXP.198.gz |cut -f2,13|cut -f1 -d'|'|sort|uniq|sed 's/taxon://g' > $datadir/uniprot_sprot_exp.species
zcat $datadir/goa_uniprot_all.EXP.203.gz |grep -E `cat $inputdir/target.list|paste -sd'|'`|cut -f2,13|cut -f1 -d'|'|sort|uniq|sed 's/taxon://g' > $inputdir/target.species
for target in `cat $inputdir/target.list`;do
    grep -P "^$target\t" $inputdir/target.species
done > $inputdir/target.species.tmp
mv $inputdir/target.species.tmp $inputdir/target.species
$bindir/posterior_training_terms.py $datadir/go-basic.obo $datadir/uniprot_sprot_exp.F $datadir/posterior.F
$bindir/posterior_training_terms.py $datadir/go-basic.obo $datadir/uniprot_sprot_exp.P $datadir/posterior.P
$bindir/posterior_training_terms.py $datadir/go-basic.obo $datadir/uniprot_sprot_exp.C $datadir/posterior.C
for target in `cut -f1 $datadir/PK.*|sort|uniq`;do
    GOterms=`grep -P "^$target\t" $datadir/PK.*|cut -f3|paste -sd,`
    echo $target $GOterms
done | sed 's/ /\t/g' > $inputdir/target.PK
