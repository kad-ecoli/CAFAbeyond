#!/usr/bin/env python
docstring='''
make_target.py goa_old.F.is_a goa_old.P.is_a goa_old.C.is_a goa_new.F.is_a goa_new.P.is_a goa_new.C.is_a NK.F NK.P NK.C LK.F LK.P LK.C PK.F PK.P PK.C
    compare annotations in goa_old.*.is_a and goa_new.*.is_a
    output the set of no knowledge (NK), limited knowledge (LK) and 
    prior knowledge (PK) targets in the following format:
    accession	new_terms	old_terms

Option:
    -exclude="GO:0003674,GO:0005488,GO:0005515"   - GO terms to exclude. Default is "protein binding".
'''
import sys

def make_target(oldfile_dict,newfile_dict,outfile_dict,exclude):
    #### read file ####
    goa_old_dict=dict(F=dict(),P=dict(),C=dict())
    goa_new_dict=dict(F=dict(),P=dict(),C=dict())
    for Aspect in "FPC":
        filename=oldfile_dict[Aspect]
        fp=open(filename,'r')
        for line in fp.read().splitlines():
            target,GOterms=line.split()
            if GOterms==exclude:
                continue
            goa_old_dict[Aspect][target]=GOterms
        fp.close()

        filename=newfile_dict[Aspect]
        fp=open(filename,'r')
        for line in fp.read().splitlines():
            target,GOterms=line.split()
            if GOterms==exclude:
                continue
            goa_new_dict[Aspect][target]=GOterms
        fp.close()
    target_old_set=set(list(goa_old_dict['F'].keys())+ \
                       list(goa_old_dict['P'].keys())+ \
                       list(goa_old_dict['C'].keys()))

    #### make NK target ####
    NK_target_list=[]
    for Aspect in "FPC":
        txt=''
        for target in goa_new_dict[Aspect]:
            if target in target_old_set:
                continue
            txt+="%s\t%s\n"%(target,goa_new_dict[Aspect][target])
            NK_target_list.append(target)
        filename=outfile_dict[Aspect]['NK']
        fp=open(filename,'w')
        fp.write(txt)
        fp.close()
    NK_target_set =set(NK_target_list)
        
    #### make LK target ####
    for Aspect in "FPC":
        txt=''
        for target in goa_new_dict[Aspect]:
            if target in NK_target_set or target in goa_old_dict[Aspect]:
                continue
            txt+="%s\t%s\n"%(target,goa_new_dict[Aspect][target])
        filename=outfile_dict[Aspect]['LK']
        fp=open(filename,'w')
        fp.write(txt)
        fp.close()
    
    #### make PK target ####
    for Aspect in "FPC":
        txt=''
        for target in goa_new_dict[Aspect]:
            if not target in goa_old_dict[Aspect]:
                continue
            goa_old=goa_old_dict[Aspect][target]
            goa_new=goa_new_dict[Aspect][target]
            goa_old_set=set(goa_old.split(','))
            goa_new_set=set(goa_new.split(','))
            if len(goa_new_set.intersection(goa_old_set))==len(goa_new_set):
                continue
            txt+="%s\t%s\t%s\n"%(target,goa_new,goa_old)
        filename=outfile_dict[Aspect]['PK']
        fp=open(filename,'w')
        fp.write(txt)
        fp.close()
    return

if __name__=="__main__":
    exclude="GO:0003674,GO:0005488,GO:0005515"
    args=[]
    for arg in sys.argv[1:]:
        if arg.startswith('-exclude='):
            exclude=arg[len('-exclude='):]
        elif arg.startswith('-'):
            sys.stderr.write('ERROR! No such option %s\n'%arg)
            exit()
        else:
            args.append(arg)
    if len(args)!=15:
        sys.stderr.write(docstring)
        exit()

    oldfile_dict=dict()
    newfile_dict=dict()
    outfile_dict=dict(F=dict(),P=dict(),C=dict())
    oldfile_dict['F']      =args[0]
    oldfile_dict['P']      =args[1]
    oldfile_dict['C']      =args[2]
    newfile_dict['F']      =args[3]
    newfile_dict['P']      =args[4]
    newfile_dict['C']      =args[5]
    outfile_dict['F']['NK']=args[6]
    outfile_dict['P']['NK']=args[7]
    outfile_dict['C']['NK']=args[8]
    outfile_dict['F']['LK']=args[9]
    outfile_dict['P']['LK']=args[10]
    outfile_dict['C']['LK']=args[11]
    outfile_dict['F']['PK']=args[12]
    outfile_dict['P']['PK']=args[13]
    outfile_dict['C']['PK']=args[14]
    make_target(oldfile_dict,newfile_dict,outfile_dict,exclude)
