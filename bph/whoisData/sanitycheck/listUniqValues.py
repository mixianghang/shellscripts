#!/usr/bin/python
import sys
import os
sourceFile=sys.argv[1]
indexStr=sys.argv[2]
indexList=indexStr.split(",")
if len(indexList) <= 0:
  print "no index"
  sys.exit(1)

mapList = []
for i in range(0, len(indexList)):
  mapList.append({})
if not os.path.exists(sourceFile):
  print "file doesn't exist: {0}".format(sourceFile)
  sys.exit(1)
lineSep = "\t"
attrNameStr = ""
with open(sourceFile, "r") as fd:
  lineNum = 0
  for line in fd:
    lineNum += 1
    line = line[:-1]
    if lineNum == 1:#the first line is title
      attrNameStr = line
      print attrNameStr
      continue
    attrs = line.split(lineSep)
    indexNum = 0
    for indexNum, index in enumerate(indexList):
      if len(attrs) < int(index):
        print "line don't have this index: {0}: {1}".format(lineNum, line)
        continue
      value = attrs[int(index) - 1] if attrs[int(index) - 1] != "" and attrs[int(index) - 1] is not None else\
       "NULL"
      if mapList[indexNum].has_key(value):
        mapList[indexNum][value] += 1
      else:
        mapList[indexNum][value] = 1
#output 
  attrNameList = attrNameStr.split(lineSep)
  for indexNum, indexStr in enumerate(indexList):
     index = int(indexStr)
     attributeName = attrNameList[index - 1]
     print "possible values for attribute {0} at {1} are as below:".format(attributeName, index)
     valueMap = mapList[indexNum]
     for key in valueMap:
       print "{0}:{1}:{2}".format(attributeName, key, valueMap[key])
