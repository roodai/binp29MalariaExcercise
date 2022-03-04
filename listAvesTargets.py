#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 13:52:47 2022

@author: inf-29-2021
"""

#produces list of blastp targets of avian origin
#Ran as such: python noAvesParser.py input.blastp reference.fasta taxonomy.dat output

import sys
blids=list()
geneids=[]
osids={}
with open (sys.argv[1], 'r') as blin, open(sys.argv[2], 'r') as protin:
    blinVariable=blin.readlines()
    for line in blinVariable:
        #extract target ids from lines, append them to their list
        if line.split('\t')[1] != '':
            geneids.append(line.split('\t')[0])
            blids.append(line.split('|')[1])

    for line in protin:
        if line.startswith('>'):
                #extract target id and species origin from reference file if they are present in the target id list derived from the input file
            if line.split('|')[1] in blids:
                OS=line.split('=')[1]
                OX=line.split('=')[2]
                OX=OX[:len(OX)-3]
                OS=OS[:len(OS)-3]
                osids[OS]=line.split('|')[1]
                osids[line.split('|')[1]]=OS

aves_found = False
SN = ''
SNset = set()
targetAves = list()
with open(sys.argv[3], "r") as T1, open (sys.argv[4], 'w') as blout:
    for line in T1:
        # Ensuring we are in the "birds" section of the taxonomy file.
        if aves_found == True:
            # We want to keep the name from "SCIENTIFIC NAME" row
            if line.startswith("SCIENTIFIC"):
                if SN:
                    SNset.add(SN)
                SN = line.rstrip().split(":")[-1][1:]

            elif line.startswith("BLAST"):
                aves_found = False
                break
        # This part here will set the aves_found to True, when the BLAST NAME "birds" is found in the taxonomy file.
        # All rows below will be species belonging to bird, until next "BLAST NAME" is found.
        elif line.startswith("BLAST NAME"):
            line = line.split(":")[1]
            if "birds" in line:
                aves_found = True
    
    #compare set of birds found in the taxonomy file to species extracted from the input file
    for i in osids:
        if osids[i] in SNset:
            # if species from input file are present in the set of birds add the target and gene id to a list
            blout.write(geneids[blids.index(i)]+'\n')
            