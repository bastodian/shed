#!/usr/bin/env python
'''
q-trim.py

Improved quality trimming. 

You can obtain screed at github by running
   git clone git://github.com/ctb/screed.git

Then, install by running
   python setup.py install
in the newly created screed directory.

Once completed, you should be able to run this script as is.

Author: Jason Pell (pelljaso@cse.msu.edu) & GED Lab

QSCORE: The highest score to trim.
INTERCRAP: After initial trimming, we count the number of 
           remaining bases below the quality score. If it is 
           above the INTERCRAP threshold, then we trim 
           at the first base with the subpar QC score.
MINLENGTH: After all of the trimming, we throw out any read 
           that is below this length.
'''
import sys
import screed

filein = sys.argv[1]
fileout = sys.argv[2]

fw = open(fileout, 'w')

QSCORE = '6'
INTERCRAP = 5
MINLENGTH = 70

# walk through each read using screed
for n, record in enumerate(screed.open(filein)):
   name = record['name'] + ' ' + record['annotations']
   sequence = record['sequence']
   accuracy = record['accuracy']

   sequence = sequence.rstrip('N')
   accuracy = accuracy[:len(sequence)]

   if 'N' in sequence:
      continue

   # trim from the 3' end of the read until you find a "good-qc" base
   loc = -1
   for i in range(len(accuracy)-1,-1,-1):
      if accuracy[i] > QSCORE:
         loc = i+1
         break

   accuracy = accuracy[0:loc]
   sequence = sequence[0:loc]

   # count the number of remaining bases that are below the QC threshold
   count = 0
   trim = -1
   for i in range(len(accuracy)):
      if accuracy[i] <= QSCORE:
         count += 1
         if trim == -1:
            trim = i

   # if we are over the "intercrap" threshold, do a more brutal trimming
   if count >= INTERCRAP:
      accuracy = accuracy[:trim]
      sequence = sequence[:trim]

   # output sequences as long as we are less than the MINLENGTH
   if len(sequence) >= MINLENGTH:
      fw.write('@%s\n%s\n+\n%s\n' % (name, sequence, accuracy))

#   if n % 1000 == 0:
#      print 'scanning', n

fw.close()
