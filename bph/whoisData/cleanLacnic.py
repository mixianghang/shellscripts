#!/usr/bin/python

import os
import sys
import re
import time

date = time.strftime("%Y%m%d")
if len(sys.argv) < 3:
  print "Usage: sourceFile resultFile"
  sys.exit(1)
sourceFile = sys.argv[1]
resultFile = sys.argv[2]

#check file existance
if not os.path.exists(sourceFile):
  print "source File doesn't exist: {0}".format(sourceFile)
  sys.exit(1)

if os.path.exists(resultFile):
  os.rename(resultFile, resultFile + "_bak_" + date)

sourceFd = open(sourceFile, "r")
resultFd = open(resultFile, "a")

startRe = re.compile("^[ \t]*{[ \t]*\n$")
closeStartRe = re.compile("^[ \t]*}{[ \t]*\n$")
closeRe = re.compile("^[ \t]*}[ \t]*\n$")
startTime = time.time()
currLevel = -1
damaged   = 0
success   = 0
tempList = []
lineNum = 0
for line in sourceFd:
  lineNum += 1
  startMatch = startRe.match(line)
  if startMatch:
    currLevel = 0
    tempList = []
    tempList.append(line)
    continue
  closeStartMatch = closeStartRe.match(line)
  if closeStartMatch:
    if currLevel == 0:
      tempList.append("}\n")
      resultFd.write("".join(tempList))
      success += 1
      if success % 1000 == 0:
        print "success: {0} and damaged: {1}".format(success, damaged)
    else:
      damaged += 1
    currLevel = 0
    tempList = []
    tempList.append("{\n")
    continue
  closeMatch = closeRe.match(line)
  if closeMatch:
      if currLevel == 0:
        tempList.append("}\n")
        resultFd.write("".join(tempList))
        success += 1
        if success % 1000 == 0:
          print "success: {0} and damaged: {1}".format(success, damaged)
      else:
        damaged += 1
      currLevel = -1
      tempList = []
      continue
  tempList.append(line)

endTime = time.time()
print "finish with time cost {0:.2f}, {1} successes and {2} damaged".format(endTime - startTime, success, damaged)
sourceFd.close()
resultFd.close()
