#!/bin/bash
FILE=`readlink -e $0`
curdir=`dirname $FILE`
rootdir=`dirname $curdir`
datadir="$rootdir/data"
downloaddir="$rootdir/download"
inputdir="$rootdir/input"
bindir="$rootdir/bin"

cd $curdir/
wget http://ftp.ebi.ac.uk/pub/databases/alphafold/sequences.fasta -O sequences.fasta
grep '>' sequences.fasta |cut -f2 -d- > sequences.list
cat $datadir/uniprot_sprot_exp.list $inputdir/target.list|sort |uniq > all.list
$curdir/bin/batch_retrieval.py all.list sequences.list structure.list
$curdir/bin/batch_retrieval.py structure.list $datadir/uniprot_sprot_exp.list $curdir/data/uniprot_sprot_exp.list
$curdir/bin/batch_retrieval.py structure.list $inputdir/target.list $curdir/input/target.list
rm all.list sequences.list sequences.fasta structure.list

cp $datadir/go-basic.obo $curdir/data/ 
cp $datadir/precision_by_evidence.txt  $curdir/data/ 
$curdir/bin/batch_retrieval.py $curdir/input/target.list $inputdir/target.PK $curdir/input/target.PK
$curdir/bin/batch_retrieval.py $curdir/input/target.list $inputdir/target.fasta $curdir/input/target.fasta
$curdir/bin/batch_retrieval.py $curdir/input/target.list $inputdir/target.is_a $curdir/input/target.is_a
$curdir/bin/batch_retrieval.py $curdir/input/target.list $inputdir/target.species $curdir/input/target.species
$curdir/bin/batch_retrieval.py $curdir/data/uniprot_sprot_exp.list $datadir/uniprot_sprot_exp.fasta $curdir/data/uniprot_sprot_exp.fasta
$curdir/bin/batch_retrieval.py $curdir/data/uniprot_sprot_exp.list $datadir/uniprot_sprot_exp.F $curdir/data/uniprot_sprot_exp.F
$curdir/bin/batch_retrieval.py $curdir/data/uniprot_sprot_exp.list $datadir/uniprot_sprot_exp.P $curdir/data/uniprot_sprot_exp.P
$curdir/bin/batch_retrieval.py $curdir/data/uniprot_sprot_exp.list $datadir/uniprot_sprot_exp.C $curdir/data/uniprot_sprot_exp.C
$curdir/bin/batch_retrieval.py $curdir/data/uniprot_sprot_exp.list $datadir/uniprot_sprot_exp.species $curdir/data/uniprot_sprot_exp.species
$curdir/bin/batch_retrieval.py $curdir/input/target.list $datadir/LK.F $curdir/data/LK.F
$curdir/bin/batch_retrieval.py $curdir/input/target.list $datadir/LK.P $curdir/data/LK.P
$curdir/bin/batch_retrieval.py $curdir/input/target.list $datadir/LK.C $curdir/data/LK.C
$curdir/bin/batch_retrieval.py $curdir/input/target.list $datadir/NK.F $curdir/data/NK.F
$curdir/bin/batch_retrieval.py $curdir/input/target.list $datadir/NK.P $curdir/data/NK.P
$curdir/bin/batch_retrieval.py $curdir/input/target.list $datadir/NK.C $curdir/data/NK.C
$curdir/bin/batch_retrieval.py $curdir/input/target.list $datadir/PK.F $curdir/data/PK.F
$curdir/bin/batch_retrieval.py $curdir/input/target.list $datadir/PK.P $curdir/data/PK.P
$curdir/bin/batch_retrieval.py $curdir/input/target.list $datadir/PK.C $curdir/data/PK.C
$bindir/calculate_ic.py $curdir/data/go-basic.obo  $curdir/data/uniprot_sprot_exp.F   $curdir/data/naive.F
$bindir/calculate_ic.py $curdir/data/go-basic.obo  $curdir/data/uniprot_sprot_exp.C   $curdir/data/naive.C
$bindir/calculate_ic.py $curdir/data/go-basic.obo  $curdir/data/uniprot_sprot_exp.P   $curdir/data/naive.P
$bindir/makeblastdb -in $curdir/data/uniprot_sprot_exp.fasta -dbtype prot -parse_seqids
$bindir/posterior_training_terms.py $curdir/data/go-basic.obo $curdir/data/uniprot_sprot_exp.F $curdir/data/posterior.F
$bindir/posterior_training_terms.py $curdir/data/go-basic.obo $curdir/data/uniprot_sprot_exp.P $curdir/data/posterior.P
$bindir/posterior_training_terms.py $curdir/data/go-basic.obo $curdir/data/uniprot_sprot_exp.C $curdir/data/posterior.C

curl -s ftp://ftp.ebi.ac.uk/pub/databases/alphafold/|grep -ohP "\w+_\d+_\w+\.tar"|uniq > tar.list
mkdir -p $curdir/input/pdb
mkdir -p $curdir/data/pdb
for tar in `cat tar.list`;do
    wget ftp://ftp.ebi.ac.uk/pub/databases/alphafold/$tar -O $tar
    tar -xf $tar *.pdb.gz
    rm $tar
    ls AF-*-F*-model_v*.pdb.gz|cut -f2 -d- > AF.pdb.list
    $curdir/bin/batch_retrieval.py $curdir/input/target.list AF.pdb.list AF.pdb.list.overlap
    for target in `cat AF.pdb.list.overlap`;do
        if [ -s "$curdir/input/pdb/$target.pdb.gz" ];then
	    continue
	fi
        filename=`ls AF-$target-F*-model_v*.pdb.gz |tail -1`
        zcat $filename |grep -F " CA "|cut -c1-54|gzip - > $curdir/input/pdb/$target.pdb.gz
    done

    $curdir/bin/batch_retrieval.py $curdir/data/uniprot_sprot_exp.list AF.pdb.list AF.pdb.list.overlap
    for target in `cat AF.pdb.list.overlap`;do
        if [ -s "$curdir/data/pdb/$target.pdb.gz" ];then
	    continue
	fi
        filename=`ls AF-$target-F*-model_v*.pdb.gz |tail -1 `
        zcat $filename |grep -F " CA "|cut -c1-54|gzip - > $curdir/data/pdb/$target.pdb.gz
    done
    rm AF-*-F*-model_v*.gz AF.pdb.list*
done
rm tar.list

#$curdir/bin/pdb2xyz -dir $curdir/input/pdb/ $curdir/input/target.list -suffix .pdb.gz > $curdir/input/target.xyz
#$curdir/bin/xyz_sfetch $curdir/input/target.xyz
mkdir -p $curdir/data/xyz
cut -c3 $curdir/data/uniprot_sprot_exp.list |sort|uniq > $curdir/data/xyz/list
for C in `cat $curdir/data/xyz/list`;do
    echo "^[A-Z][0-9]$C"
    grep -P "^\w{2}$C" $curdir/data/uniprot_sprot_exp.list > $curdir/data/xyz/$C.list
    $curdir/bin/pdb2xyz -dir $curdir/data/pdb/ $curdir/data/xyz/$C.list -suffix .pdb.gz | gzip - > $curdir/data/xyz/$C.xyz.gz 
done
rm -rf $curdir/data/pdb
