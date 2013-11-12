#!/usr/bin/env python

'''
  Script to remove line-breaks in sequences from fasta or fastq files.  
'''

import sys
import screed

def fixseqs(filein, fileout):

    fw = open(fileout, 'w')
    fi = open(filein, 'r')
    line1 = fi.readline()
    
    #Does line 1 correspond to FASTA?
    if line1[0] == '>':
        for n, record in enumerate(screed.open(filein)):
            name = record['name']
            sequence = record['sequence']
            fw.write('>%s\n%s\n' % (name, sequence))
            #print name, "\n", sequence
    #Does line 1 correspond to FASTQ?
    elif line1[0] == '@':
        for n, record in enumerate(screed.open(filein)):
            if 'N' in record['annotations']:
                name = record['name'] + ' ' + record['annotations']
                sequence = record['sequence']
                accuracy = record['accuracy']
                fw.write('@%s\n%s\n+\n%s\n' % (name, sequence, accuracy))
    #No FASTA or FASTQ file provided
    else:
        print 'Neither fasta nor fastq input. Do your headers start with\n\
                > (fasta) or @ (fastq)?'
    fw.close()

if __name__ == '__main__':
    fixseqs(sys.argv[1], sys.argv[2])
