#!/usr/bin/python3

# A quick and dirty program
# sys.argv[1] is input fasta file
# sys.argv[2] is the output file

# Run as: GCminlenfilter.py input.genome output.genome
import sys
try:
    fastafile=sys.argv[1]
    outfile=sys.argv[2]
except:
    print("Provide input file to run program")
    sys.exit()
    
gctresh=input('Input GC content threshold' )
minlen=input('Input minimum lenght of sequence' )
seq = {} # A dictionary with ids as keys and their sequences as values
ids = [] # A list of ids to keep the original order

with open(fastafile, 'r') as fin:
    for line in fin:
        line = line.rstrip()
        if line[0] == '>':
            id = line.split(' ')[0] # Keep id up to the first space
            id = id[1:] # Remove the '>'
            seq[id] = '' 
            ids.append(id)
        else:
            seq[id] += line.upper() #If the line is a sequence line append the sequence to the currently iterated id key

with open(outfile, 'w') as fout:
    for id in ids:
        if len(seq[id]) < int(minlen):
            continue
        gcCount = seq[id].count('G') + seq[id].count('C')
        atCount = seq[id].count('A') + seq[id].count('T')
        gc = gcCount / (gcCount + atCount)
        if gc <= float(gctresh) / 100:
            outGC = round(gc, 2)
            print('>' + id + ' GC=' + str(outGC) + ' Length=' + str(len(seq[id])), file=fout)
            print(seq[id], file=fout)
