#!/usr/bin/env python

'''
   Script to trim sequences in fastq files to a user-speciofied length.

'''

import screed, sys

infile = sys.argv[1]
outfile = sys.argv[2]
trim = sys.argv[3]

with open(outfile, 'w') as out:
    for n, record in enumerate(screed.open(infile)):
        out.write('@%s %s\n%s\n+\n%s\n' % \
            (record['name'],record['annotations'],\
            record['sequence'][0:trim],record['accuracy'][0:trim]))
