#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:41:59 2022

@author: inf-29-2021
"""
#Produce the query and top target is any target is present
#Ran as such: python oneTargetBlastParset.py input output
#open input and output file
import sys
with open(sys.argv[1], 'r') as blastfile, open(sys.argv[2], 'w') as outfile:
    #read input file file
    line=blastfile.readline()
    #Set query flag as false
    Q=False
    #loop while lines remain unread in input file
    while line:
        line=blastfile.readline()
        #Store query names if line is a query line
        if line.startswith('Query='):
            query=line.strip('\n').split(' ')
            #set query flag to true since query is found
            Q=True
        #Store target name from target lines
        if line.startswith('>') and Q==True:
            target=line.replace('>', '')
            #Create output line from data collected thusfar
            outline=query[1]+'\t'+target.strip('\n')
            #Write output line into output file
            outfile.write(outline+'\n')
            #Query flag is set to false since a target was found 
            Q=False
