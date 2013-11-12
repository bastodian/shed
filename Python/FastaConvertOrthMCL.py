#!/usr/bin/env python

import screed, sys

infile = sys.argv[1]
outfile = sys.argv[2]
tag = sys.argv[3]

with open(outfile, 'w') as out:
    for n, record in enumerate(screed.open(infile)):
        out.write('>%s|%s\n%s\n' % (tag, record['name'], record['sequence']))
