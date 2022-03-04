#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 11:30:56 2022

@author: inf-29-2021
"""
import sys
buscids=[]
geneids=[]
for i in range (1,(int((len(sys.argv)+1)/2))):   #first half of inputs are busco files
    ids=[]
    with open(sys.argv[i],'r') as curbusc:
        buscid=[]
        geneid=[]
        ngenes=0
        for line in curbusc:
            if not line.startswith('#'):       
                ngenes +=1
                if line.split()[1]=='Complete':
                    buscid.append(line.split()[0])
                    geneid.append(line.split()[2])
                if line.split()[1]=='Duplicated':
                    buscid.append(line.split()[0])
                    geneid.append(line.split()[2])
                    next(curbusc)
        geneids.append(geneid)
        buscids.append(buscid)
    completionratio=len(geneid)/ngenes
    print(completionratio)
        
sharedBusc=set.intersection(*[set(list) for list in buscids])  #Produce intersections between all lists in list of lists, aka items common to all lists
print(len(sharedBusc))


#produce indices of shared buscos form listed list of all buscos, then use the indexes to prduce gene ids
sharedIndices=[]
for ids in buscids:
    indices=[]
    for bus in sharedBusc:
        if bus in ids:
            indices.append(ids.index(bus))
    sharedIndices.append(indices)

#use produced idices to index gene ids listed list to rpoduce gene ids that correspond to the shared buscos
correspondingGenes=[]
for k in range(0,len(geneids)):
    correspondingGene=[]
    for index in sharedIndices[k]:
        correspondingGene.append(geneids[k][index])
    correspondingGenes.append(correspondingGene)
    
    
aafastas=[]
protFileNumber=-1
for j in range(int((len(sys.argv)/2)+1),len(sys.argv)): #second half of inputs are .faa files corresponding to busco files in order
    protFileNumber+=1
    #open .faa files and create a dictionary with gene ids as keys and sequences as values
    with open(sys.argv[j]) as curprot:
        aafasta={}
        for line in curprot:
            if line.startswith('>') and line.split()[0].strip('>') in correspondingGenes[protFileNumber]:
                aafasta[line.split()[0].strip('>')]=next(curprot)
                    #sort the dictionary based on gene id order in the correspondingGenes entry
            propaa=[(key, aafasta[key]) for key in correspondingGenes[protFileNumber] if key in aafasta]
        aafastas.append(propaa)
