#!/usr/bin/python
import sys
import os
if len(sys.argv) < 3:
  print "Usage sourceFile, indexStr"
  sys.exit(1)
sourceFile=sys.argv[1]
indexStr=sys.argv[2]
indexList=indexStr.split(",")
onlyShowResult = False
if len(sys.argv) > 3:
  onlyShowResult = True
if not os.path.exists(sourceFile):
  print "file doesn't exist: {0}".format(sourceFile)
  sys.exit(1)
lineSep = "\t"
with open(sourceFile, "r") as fd:
  lineNum = 0
  failed = 0
  attrNameList = []
  for line in fd:
    line = line[:-1]
    lineNum += 1
    if lineNum == 1:#the first line is title
      attrNameList = line.split(lineSep)
      print "check the following attributes"
      for index in indexList:
        indexInt = int(index)
        if len(attrNameList) >= indexInt:
          print "{0} {1}".format(indexInt, attrNameList[indexInt - 1])
      continue
    attrs = line.split(lineSep)
    for index in indexList:
      if len(attrs) < int(index):
        print "line don't have this index: {0}: {1}".format(lineNum, line)
        failed += 1
        continue
      if attrs[int(index) - 1] == "" or attrs[int(index) -1] is None:
        if not onlyShowResult:
          print "attribute {0} {3} is NULL for line {1}: {2}".format(index, lineNum, line, attrNameList[int(index) - 1])
        failed += 1
  print "process {0} lines with {1} failed the check".format(lineNum, failed)
      
