#!/bin/bash
FILE=`readlink -e $0`
curdir=`dirname $FILE`
cd $curdir
wget https://ndownloader.figshare.com/files/17519846 -O supplementary_data.tar.gz
tar -xvf supplementary_data.tar.gz supplementary_data/cafa3/sheets/*o_all_type*_mode1_all_fmax_sheet.csv
tar -xvf supplementary_data.tar.gz supplementary_data/cafa3/sheets/*o_all_type*_mode1_all_wfmax_sheet.csv
tar -xvf supplementary_data.tar.gz supplementary_data/cafa3/sheets/*o_all_type*_mode1_all_smin_sheet.csv

$curdir/check_cutoff.py
