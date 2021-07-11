#!/usr/bin/env python
docstring='''assess_result.py blastlocalID_1_all.txt blastlocalID_1_all_results.txt
    calculate Fmax, coverage and Smin by full mode for prediction 
    blastlocalID_1_all.txt. output result to blastlocalID_1_all_results.txt
'''
import sys
import obo2csv # parsing GO hierachy
from os.path import dirname, basename, abspath
from math import sqrt
bindir=dirname(abspath(__file__))
rootdir=dirname(bindir)
datdir=rootdir+"/data"
root_terms={ "GO:0005575", "GO:0003674", "GO:0008150"}
root_dict =dict(F=set("GO:0003674"), P=set("GO:0008150"), C=set("GO:0005575"))
target_type_list=["NK","LK","PK"]

def read_label():
    label_dict=dict()
    for target_type in target_type_list:
        label_dict[target_type]=dict(F=dict(),P=dict(),C=dict())
        for Aspect in "FPC":
            filename="%s/%s.%s"%(datdir,target_type,Aspect)
            fp=open(filename,'r')
            lines=fp.read().splitlines()
            fp.close()
            for line in lines:
                items=line.split('\t')
                target=items[0]
                oldterms=root_dict[Aspect]
                if target_type=="PK":
                    oldterms=set([GOterm for GOterm in items[2].split(',')])
                GOterms=set([GOterm for GOterm in items[1].split(','
                               ) if not GOterm in oldterms])
                label_dict[target_type][Aspect][target]=(GOterms,oldterms)
    return label_dict

def read_information_content():
    ic_dict=dict()
    for Aspect in "FPC":
        filename=datdir+"/naive."+Aspect
        fp=open(filename,'r')
        for line in fp.read().splitlines():
            items=line.split('\t')
            GOterm=items[0]
            ic=float(items[3])
            ic_dict[GOterm]=ic
        fp.close()
    return ic_dict

def read_prediction(obo_dict,infile,label_dict):
    predict_dict=dict(NK=dict(F=dict(),P=dict(),C=dict()),
                      LK=dict(F=dict(),P=dict(),C=dict()),
                      PK=dict(F=dict(),P=dict(),C=dict()))
    fp=open(infile,'r')
    lines=fp.read().splitlines()
    fp.close()
    for line in lines:
        items=line.split('\t')
        if len(items)!=3:
            continue
        target,GOterm,cscore=items
        Aspect=''
        for a in "FPC":
            if GOterm in obo_dict[a]["Term"]:
                Aspect=a
                break
        if Aspect=='':
            print("ERROR! Unknow GO term "+GOterm)
            continue
        target_type=''
        for t in target_type_list:
            if target in label_dict[t][Aspect]:
                target_type=t
                break
        if target_type=='':
            #print("skip target %s for Aspect %s"%(target,Aspect))
            continue
        if GOterm in label_dict[target_type][Aspect][target][1]:
            #print("skip pre-existing GO term %s for Aspect %s of target %s"%(GOterm,Aspect,target))
            continue
        if not target in predict_dict[target_type][Aspect]:
            predict_dict[target_type][Aspect][target]=[]
        predict_dict[target_type][Aspect][target].append((GOterm,float(cscore)))
    return predict_dict

def sum_ic(GOterm_list,ic_dict):
    return sum([ic_dict[GOterm] for GOterm in GOterm_list if GOterm in ic_dict])
    
def dot_product(list1,list2):
    if len(list1)!=len(list2):
        sys.stderr.write("ERROR! unequal list length\n")
        exit(1)
    return sum([list1[i]*list2[i] for i in range(len(list1))])

def assess_result(label_dict,ic_dict,predict_dict,outfile):
    txt="Aspect\tType\tMode\tFmax\tCutoff\tSmin\tCutoff\twFmax\tCutoff\tF'max\tCutoff\tS'min\tCutoff\twF'max\tCutoff\tCoverage\n"
    aspect_dict=dict(F="mfo",P="bpo",C="cco")
    for Aspect in "FPC":
        ontology=aspect_dict[Aspect]
        for target_type in target_type_list:
            Fmax=0
            Cutoff_F=0
            Smin=0
            Cutoff_S=1
            wFmax=0
            Cutoff_wF=0
            Fpmax=0
            Cutoff_Fp=0
            Spmin=0
            Cutoff_Sp=1
            wFpmax=0
            Cutoff_wFp=0
            total_label=len(label_dict[target_type][Aspect])
            Coverage=1.*len(predict_dict[target_type][Aspect])/total_label
            cscore_list=[]
            label_ic_dict=dict()
            target_ic_list=[]
            for target in label_dict[target_type][Aspect]:
                label_ic_dict[target]=sum_ic(
                    label_dict[target_type][Aspect][target][0],ic_dict)
                target_ic_list.append(label_ic_dict[target])
            sum_target_ic=sum(target_ic_list)
            Smin=sum_target_ic/total_label
            Spmin=dot_product(target_ic_list,target_ic_list)/sum_target_ic
            target_weight_list=[target_ic/sum_target_ic for target_ic in target_ic_list]
            for target,GOterms in predict_dict[target_type][Aspect].items():
                cscore_list+=[cscore for GOterm,cscore in GOterms]
            cscore_list=sorted(set(cscore_list))
            for cutoff in cscore_list:
                total_precision_list=[]
                total_recall_list=[]
                total_predict=0
                total_wprecision_list=[]
                total_wrecall_list=[]
                total_ru_list=[]
                total_mi_list=[]
                for target in label_dict[target_type][Aspect]:
                    if not target in predict_dict[target_type][Aspect]:
                        total_precision_list.append(0)
                        total_recall_list.append(0)
                        total_wprecision_list.append(0)
                        total_wrecall_list.append(0)
                        total_ru_list.append(label_ic_dict[target])
                        total_mi_list.append(0)
                        continue
                    predict_list=[GOterm for GOterm,cscore in predict_dict[
                        target_type][Aspect][target] if cscore>=cutoff]
                    if len(predict_list)==0:
                        total_precision_list.append(0)
                        total_recall_list.append(0)
                        total_wprecision_list.append(0)
                        total_wrecall_list.append(0)
                        total_ru_list.append(label_ic_dict[target])
                        total_mi_list.append(0)
                        continue
                    label_set=label_dict[target_type][Aspect][target][0]
                    total_predict+=1
                    wpredict=sum_ic(predict_list,ic_dict)
                    tp=label_set.intersection(predict_list)
                    wtp=sum_ic(tp,ic_dict)
                    precision=1.*len(tp)/len(predict_list)
                    wprecision=0 if wpredict==0 else wtp/wpredict
                    recall=1.*len(tp)/len(label_set)
                    wrecall=0 if label_ic_dict[target]==0 else wtp/label_ic_dict[target]
                    total_precision_list.append(precision)
                    total_recall_list.append(recall)
                    total_wprecision_list.append(wprecision)
                    total_wrecall_list.append(wrecall)
                    total_mi=0
                    for GOterm in predict_list:
                        if GOterm in ic_dict and not GOterm in label_set:
                            total_mi+=ic_dict[GOterm]
                    total_mi_list.append(total_mi)
                    total_ru=0
                    for GOterm in label_set:
                        if GOterm in ic_dict and not GOterm in predict_list:
                            total_ru+=ic_dict[GOterm]
                    total_ru_list.append(total_ru)
                total_label=len(label_dict[target_type][Aspect])
                precision =0 if total_predict==0 else sum(total_precision_list)/total_predict
                wprecision=0 if total_predict==0 else sum(total_wprecision_list)/total_predict
                recall   =sum(total_recall_list)/total_label
                wrecall  =sum(total_wrecall_list)/total_label
                mi       =sum(total_mi_list)/total_label
                ru       =sum(total_ru_list)/total_label
                precisionp =dot_product(target_weight_list,total_precision_list)
                wprecisionp=dot_product(target_weight_list,total_wprecision_list)
                recallp    =dot_product(target_weight_list,total_recall_list)
                wrecallp   =dot_product(target_weight_list,total_wrecall_list)
                mip        =dot_product(target_weight_list,total_mi_list)
                rup        =dot_product(target_weight_list,total_ru_list)

                F  =0 if  precision * recall ==0 else 2/(1/ precision +1/ recall )
                wF =0 if wprecision *wrecall ==0 else 2/(1/wprecision +1/wrecall )
                S  =sqrt(ru *ru +mi *mi )
                Fp =0 if  precisionp* recallp==0 else 2/(1/ precisionp+1/ recallp)
                wFp=0 if wprecisionp*wrecallp==0 else 2/(1/wprecisionp+1/wrecallp)
                Sp =sqrt(rup*rup+mip*mip)
                if F>=Fmax:
                    Fmax=F
                    Cutoff_F=cutoff
                if S<=Smin:
                    Smin=S
                    Cutoff_S=cutoff
                if wF>=wFmax:
                    wFmax=wF
                    Cutoff_wF=cutoff
                if Fp>=Fpmax:
                    Fpmax=Fp
                    Cutoff_Fp=cutoff
                if Sp<=Spmin:
                    Spmin=Sp
                    Cutoff_Sp=cutoff
                if wFp>=wFpmax:
                    wFpmax=wFp
                    Cutoff_wFp=cutoff
            txt+="%s\t%s\tfull\t%.4f\t%.2f\t%.4f\t%.2f\t%.4f\t%.2f\t"%(
                ontology,target_type.upper(),
                Fmax,Cutoff_F,Smin,Cutoff_S,wFmax,Cutoff_wF
                )+"%.4f\t%.2f\t%.4f\t%.2f\t%.4f\t%.2f\t%.4f\n"%(
                Fpmax,Cutoff_Fp,Spmin,Cutoff_Sp,wFpmax,Cutoff_wFp,Coverage)
    fp=open(outfile,'w')
    fp.write(txt)
    fp.close()
    return

if __name__=="__main__":
    if len(sys.argv)!=3:
        sys.stderr.write(docstring)
        exit()

    infile  =sys.argv[1]
    outfile =sys.argv[2]

    obo_dict=obo2csv.parse_obo_file(datdir+"/go-basic.obo")
    label_dict=read_label()
    ic_dict=read_information_content()
    predict_dict=read_prediction(obo_dict,infile,label_dict)
    assess_result(label_dict,ic_dict,predict_dict,outfile)
