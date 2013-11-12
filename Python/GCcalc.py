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

    # Adjust mononucleotides in S to account for rev comp sequence S*:
    # F*mononucleotide = 1/2(fA + fT) or 1/2(fG + fC)
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

    Contigs[ID]['GC'] = (Sequence.count('G') + Sequence.count('C')) / fMononucl
    Contigs[ID]['AT'] = (Sequence.count('A') + Sequence.count('T')) / fMononucl

# Write the column labels out
count = 0
Labels = []
for Contig, Dinucleotide in Contigs.iteritems():
    count += 1
    if count < 2:
        for Label in Dinucleotide:
            Labels.append(Label)
    else:
        break
sys.stdout.write('ID,%s\n' % ','.join(Labels))

# Write odds ratios for each dinucleotide plus the contig ID to stdout
for Contig, Dinucleotide in Contigs.iteritems():
    DinuclList = []
    DinuclList.append(Contig)
    for i in Dinucleotide:
        DinuclList.append(str(Dinucleotide[i]))
    sys.stdout.write('%s\n' % ','.join(DinuclList))
