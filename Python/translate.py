#!/usr/bin/env python

'''
   Script to translate the sequences in an input Fasta file using all
   6 reading frames (this includes the reverse complement strand). 
'''

from sys import argv
from sys import stdout
from Bio import SeqIO, Seq
from Bio.Alphabet import generic_dna

InFile = argv[1]

with open(InFile, 'rU') as FastaFile:
    for record in SeqIO.parse(FastaFile, "fasta"):
        ReadFrame = -1
        RevComp = Seq.Seq(str(record.seq), generic_dna).reverse_complement() 
        while ReadFrame <= 1:
            ReadFrame += 1
            stdout.write('>%s_RF:%s\n%s\n' % (str(record.name), str(ReadFrame), \
                    Seq.Seq(str(record.seq[ReadFrame:]), generic_dna).translate()))
            stdout.write('>%s_revCompRF:%s\n%s\n' % (str(record.name), str(ReadFrame), \
                    Seq.Seq(str(RevComp[ReadFrame:]), generic_dna).translate()))
