#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 14:03:54 2022

@author: inf-29-2021
"""
#uses a list of geneids to produce scaffold names from a genemark file and remove them from a fasta
#Ran as such: python removeFromFasta geneids input.gtf input.fasta output.fasta
import sys

rids=[]
with open (sys.argv[1], 'r') as removeids:
    #extract ids from input file
    for line in removeids:
        rids.append(line.strip('\n'))
        
rScaffolds=set()
with open(sys.argv[2], 'r') as gffin:
    #extract gene ids from input genemark file
    for line in gffin:
        geneid=line.split('\t')[8].split('"')[1]
        if geneid in rids:
            #if gene ids in the genemark file are present in ids to be removed add the corresponding scaffold
            #name to the set of scaffold names that are to be removed
            rScaffolds.add(line.split(' ')[0])

with open(sys.argv[3], 'r') as fastain, open(sys.argv[4], 'w') as fastaout:
    for line in fastain:
        if line.startswith('>'):
            #extract the scaffold name from the input fasta header lines
            scaffold=line.split()[0].strip('>')
            if scaffold in rScaffolds:
                #if the scaffold name is in the to be removed set notify 
                print('Scaffold to be removed:'+ ' '+scaffold)
            else:
                #if the scaffold is not in the set write the header line and the next sequence line into the output
                fastaout.write(line+'\n')
                seqline=next(fastain)
                fastaout.write(seqline+'\n')           