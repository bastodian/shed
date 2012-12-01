#!/usr/bin/env python

'''
    Script to interleave two fastq files and randomly sample sequences from the interkeaved file. 
    
    takes 4 arguments: inFile1, inFile2, outFile, number of seqs to sample
'''

from random import shuffle
import screed, sys, os

def interleave(fname1, fname2, fout):
    f1 = open(fname1, 'r')
    f2 = open(fname2, 'r')
    seqs = 0
    with open(fout, 'w') as outfile:
        while True:
            try:
                header1 = f1.next()
                seq1 = f1.next()
                junk1 = f1.next()
                qual1 = f1.next()
                
                header2 = f2.next()
                seq2 = f2.next()
                junk2 = f2.next()
                qual2 = f2.next()

                outfile.write('%s%s%s%s%s%s%s%s' % \
                        (header1, seq1, junk1, qual1, \
                        header2, seq2, junk2, qual2))
                seqs += 2
            except Exception:
                break
    
    f1.close()
    f2.close()
    return int(seqs)


def RandSampler(fname, random):
    Reverse = ''
    with open(fname + '.fwd','w') as out1:
        with open(fname + '.rev','w') as out2:
            for n, record in enumerate(screed.open(fname)):
                if n in random:
                    out1.write('@%s %s\n%s\n+\n%s\n' % \
                            (record['name'],record['annotations'],\
                            record['sequence'],record['accuracy']))
                    Reverse = '%s %s' %  (record['name'],\
                            record['annotations'].replace('1:','2:')) 
                elif record['name'] in Reverse:
                    out2.write('@%s %s\n%s\n+\n%s\n' % (record['name'],\
                            record['annotations'],record['sequence'],\
                            record['accuracy']))
                else:
                    continue


def main(filein1, filein2, combined, SampleSize):
    SeqCount = interleave(filein1, filein2, combined)
    List = range(0, SeqCount, 2)
    shuffle(List)
    RandSample = List[0:SampleSize]
    RandSet = frozenset(RandSample)
    
    RandSampler(combined, RandSet)
    interleave(filein1, filein2, combined)

    os.system('rm %s' % (combined))


main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
