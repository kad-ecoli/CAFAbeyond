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

#### download structurer data ####

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

#### download PPI data ####

cd $curdir/
wget https://version-11-0.string-db.org/mapping_files/uniprot/all_organisms.uniprot_2_string.2018.tsv.gz -O all_organisms.uniprot_2_string.2018.tsv.gz 
for species in `cat $curdir/data/uniprot_sprot_exp.species |cut -f2 |sort|uniq`;do
    echo $species
    wget https://stringdb-static.org/download/protein.links.v11.0/$species.protein.links.v11.0.txt.gz -O $species.protein.links.v11.0.txt.gz
    zgrep -P "^$species\t" all_organisms.uniprot_2_string.2018.tsv.gz |sed 's/|/\t/g'|cut -f2,4 > $species.uniprot_2_string.tsv
    $curdir/bin/string2uniprot.py $species.protein.links.v11.0.txt.gz $species.uniprot_2_string.tsv $species.uniprot.links
    rm $species.protein.links.v11.0.txt.gz $species.uniprot_2_string.tsv
done
rm all_organisms.uniprot_2_string.2018.tsv.gz 

cmd="cat "
for species in `cat $curdir/data/uniprot_sprot_exp.species |cut -f2 |sort|uniq`;do
    filename=$species.uniprot.links
    if [ -s "$filename" ];then
        cmd="$cmd $filename"
    fi
done
$cmd |gzip - > $curdir/data/uniprot.links.gz
rm *.uniprot.links

#### download coexpression data ####

cd $curdir
wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/idmapping.dat.gz -O idmapping.dat.gz
zcat idmapping.dat.gz |grep "\sGeneID\s" |cut -f1,3 > GeneIDmapping.tsv
rm idmapping.dat.gz
$curdir/bin/subset_mapping.py $curdir/input/target.list GeneIDmapping.tsv target.GeneID.tsv
$curdir/bin/subset_mapping.py $curdir/data/uniprot_sprot_exp.list GeneIDmapping.tsv uniprot_sprot_exp.GeneID.tsv
rm GeneIDmapping.tsv
wget https://coxpresdb.jp/download/ -O coxpresdb.html
wget https://atted.jp/download/     -O atted.html
for link in `grep -ohP "\/download\/\S+d.zip" coxpresdb.html |cut -f1 -d'"'|grep -P "(-[mcu]\.)"|grep -P "\/$"`;do
    target=`echo $link|cut -f3 -d/`
    wget "https://coxpresdb.jp$link" -O $target.zip
done
for link in `grep -ohP "\/download\/\S+?\/coex\/\S+?d.zip" atted.html`;do
    target=`echo $link|cut -f3 -d/`
    wget "https://atted.jp$link" -O $target.zip
done
for filename in `ls *zip`;do
    prefix=`echo $filename|cut -f1 -d.`
    unzip $filename
    folder="coxpres_"`echo $prefix|cut -f2 -d-`
    if [ ! -d "$folder" ];then
	mkdir $folder
    fi
    for line in `sed 's/\t/@/g' target.GeneID.tsv`;do
	accession=`echo $line|cut -f1 -d@`
	GeneID=`echo $line|cut -f2 -d@`
	target=`ls $prefix.*.d/$GeneID 2>/dev/null`
	if [ ! -z "$target" ];then
	    mv $target $folder/$accession
	fi
    done
    rm -rf $prefix\.*\.d
done
rm *.zip
for suffix in `echo r u m`;do
    $curdir/bin/batch_uniprot2GeneID.py target.GeneID.tsv uniprot_sprot_exp.GeneID.tsv coxpres_$suffix/ $curdir/data/coxpres_$suffix.gz
done
rm atted.html coxpresdb.html target.GeneID.tsv uniprot_sprot_exp.GeneID.tsv
rm -rf coxpres_m coxpres_r coxpres_u
