#!/usr/bin/env python

'''
   Script to select sequences of minimum length.

'''

import screed, sys

infile = sys.argv[1]
outfile = sys.argv[2]
minlen = sys.argv[3]

with open(outfile, 'w') as out:
    for n, record in enumerate(screed.open(infile)):
        if len(record['sequence']) >= int(minlen):
            out.write('>%s\n%s\n' % \
                (record['name'],\
                record['sequence']))
