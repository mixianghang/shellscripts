#!/usr/bin/python

import os
import sys
import re
import time

date = time.strftime("%Y%m%d")
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

startRe = re.compile("^<\?xml")
whoisStart   = re.compile("[ \t]*<whois-resources")
whoisEnd     = re.compile("[ \t]*</whois-resources")
objectsStart = re.compile("[ \t]*<objects>")
objectsEnd   = re.compile("[ \t]*</objects>")
objectStart  = re.compile("[ \t]*<object[^s]")
objectEnd    = re.compile("[ \t]*</object>")
attrsStart   = re.compile("[ \t]*<attributes>")
attrsEnd     = re.compile("[ \t]*</attributes>")
startTime = time.time()
currLevel = -1
damaged   = 0
success   = 0
tempList = []
lineNum = 0
for line in sourceFd:
  lineNum += 1
  if currLevel == -1:#wait for the first line of an object
    if startRe.match(line):
      currLevel = 0
      tempList.append(line)
    continue
  if whoisStart.match(line):
    if currLevel != 0:
      print "damaged object at line: {0}".format(lineNum)
      damaged += 1
      currLevel = -1
      tempList = []
      continue
    else:
      currLevel = 1
      tempList.append(line)
      continue
  elif objectsStart.match(line):
    if currLevel != 1:
      print "damaged object at line: {0}".format(lineNum)
      damaged += 1
      currLevel = -1
      tempList = []
      continue
    else:
      currLevel = 2
      tempList.append(line)
      continue
  elif objectStart.match(line):
    if currLevel != 2:
      print "damaged object at line: {0}".format(lineNum)
      damaged += 1
      currLevel = -1
      tempList = []
      continue
    else:
      currLevel = 3
      tempList.append(line)
      continue
  elif attrsStart.match(line):
    if currLevel != 3:
      print "damaged object at line: {0}".format(lineNum)
      damaged += 1
      currLevel = -1
      tempList = []
      continue
    else:
      currLevel = 4
      tempList.append(line)
      continue
  elif attrsEnd.match(line):
    if currLevel != 4:
      print "damaged object at line: {0}".format(lineNum)
      damaged += 1
      currLevel = -1
      tempList = []
      continue
    else:
      currLevel = 5
      tempList.append(line)
      continue
  elif objectEnd.match(line):
    if currLevel != 5:
      print "damaged object at line: {0}".format(lineNum)
      damaged += 1
      currLevel = -1
      tempList = []
      continue
    else:
      currLevel = 6
      tempList.append(line)
      continue
  elif objectsEnd.match(line):
    if currLevel != 6:
      print "damaged object at line: {0}".format(lineNum)
      damaged += 1
      currLevel = -1
      tempList = []
      continue
    else:
      currLevel = 7
      tempList.append(line)
      continue
  elif whoisEnd.match(line):
    if currLevel != 7:
      print "damaged object at line: {0}".format(lineNum)
      damaged += 1
      currLevel = -1
      tempList = []
      continue
    else:
      currLevel = -1
      tempList.append(line)
      resultFd.write("".join(tempList))
      success += 1
      if success % 10000 == 0:
        print "success: {0} and damage: {1}".format(success, damaged)
      tempList = []
      continue
  tempList.append(line)

endTime = time.time()
print "finish with time cost {0:.2f}, {1} successes and {2} damaged".format(endTime - startTime, success, damaged)
sourceFd.close()
resultFd.close()
