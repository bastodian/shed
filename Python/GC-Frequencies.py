#!/usr/bin/env python

'''
   Script to calculate dinculeotide odds ratios from fasta input file
'''

import screed, sys
from itertools import permutations
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna

infile = sys.argv[1]

Contigs = {}
for n, record in enumerate(screed.open(infile)):
    ID = record['name']
    Sequence = record['sequence']

    Mononucl = {}
    Mononucl['A'] = Sequence.count('A')
    Mononucl['T'] = Sequence.count('T')
    Mononucl['G'] = Sequence.count('G')
    Mononucl['C'] = Sequence.count('C')

    # Create a dictionary with all Dinculeotide Counts for each contig
    ### VERIFY THE MATH HERE 
    Contigs[ID] = {}
    Nucleotides = ['A','T','G','C']
    for Nucl in Nucleotides:
        fNucl = float(Sequence.count(Nucl))
        fMononucl = float(Mononucl['A'] + Mononucl['T'] + Mononucl['G'] + Mononucl['C'])
        Contigs[ID][Nucl] = fNucl  / fMononucl

# Write the column labels out
count = 0
Labels = []
for Contig, Nucl in Contigs.iteritems():
    count += 1
    if count < 2:
        for Label in Nucl:
            Labels.append(Label)
    else:
        break
sys.stdout.write('ID,%s\n' % ','.join(Labels))

# Write Nucleotide frequencies out
for Contig, Nucl in Contigs.iteritems():
    NuclList = []
    NuclList.append(Contig)
    for i in Nucl:
        NuclList.append(str(Nucl[i]))
    sys.stdout.write('%s\n' % ','.join(NuclList))
