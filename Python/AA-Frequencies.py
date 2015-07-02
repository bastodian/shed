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
    Mononucl['C'] = Sequence.count('C')
    Mononucl['D'] = Sequence.count('D')
    Mononucl['E'] = Sequence.count('E')
    Mononucl['F'] = Sequence.count('F')
    Mononucl['G'] = Sequence.count('G')
    Mononucl['H'] = Sequence.count('H')
    Mononucl['I'] = Sequence.count('I')
    Mononucl['K'] = Sequence.count('K')
    Mononucl['L'] = Sequence.count('L')
    Mononucl['M'] = Sequence.count('M')
    Mononucl['N'] = Sequence.count('N')
    Mononucl['P'] = Sequence.count('P')
    Mononucl['Q'] = Sequence.count('Q')
    Mononucl['R'] = Sequence.count('R')
    Mononucl['S'] = Sequence.count('S')
    Mononucl['T'] = Sequence.count('T')
    Mononucl['V'] = Sequence.count('V')
    Mononucl['W'] = Sequence.count('W')
    Mononucl['Y'] = Sequence.count('Y')

    # Create a dictionary with all Dinculeotide Counts for each contig
    ### VERIFY THE MATH HERE 
    Contigs[ID] = {}
    Nucleotides = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']
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
