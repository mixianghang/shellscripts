#!/usr/bin/python
import sys
import os
import re
if len(sys.argv) < 4:
  print "Usage sourcefile, index, pattern"
  sys.exit(1)
sourceFile=sys.argv[1]
index = int(sys.argv[2])
patternRe = re.compile(sys.argv[3], re.I)
if not os.path.exists(sourceFile):
  print "file doesn't exist: {0}".format(sourceFile)
  sys.exit(1)
lineSep = "\t"
attrNameList = []
with open(sourceFile, "r") as fd:
  lineNum = 0
  for line in fd:
    lineNum += 1
    line = line[:-1]
    if lineNum == 1:#the first line is title
      attrNameList = line.split(lineSep)
      print line
      continue
    attrs = line.split(lineSep)
    if len(attrs) < index:
      print "pattern match error for {0} : {1}".format(lineNum, line)
      continue
    if patternRe.match(attrs[index - 1]) is None:
      print "pattern match error for {2} {3} at line {0} : {1}".format(index, attrNameList[index -1], lineNum, line)

