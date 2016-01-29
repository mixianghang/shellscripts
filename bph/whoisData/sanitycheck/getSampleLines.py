#!/usr/bin/python
import os
import sys
import random

if len(sys.argv) < 3:
  print "Usage file sampleSize"
  sys.exit(1)

sourceFile = sys.argv[1]
sampleSize = int(sys.argv[2])

if not os.path.exists(sourceFile):
  print "source file doesn't exist: {0}".format(sourceFile)
  sys.exit(1)

size = 0
with open(sourceFile, "r") as f:
  for line in f:
    size += 1

print "the line num of file {0} is {1}".format(sourceFile, size)
sampleList = random.sample(xrange(2, size + 1), sampleSize)
with open(sourceFile, "r") as f:
  lineNum = 0
  for line in f:
    lineNum += 1
    line = line[:-1]
    if lineNum in sampleList:
      print "lineNum{0}:{1}".format(lineNum, line)
