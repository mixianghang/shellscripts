#!/usr/bin/python
import sys
import os
import re
import time

#filter out failed keys and damaged objects, so that to retry requests
if len(sys.argv) < 4:
  sys.stderr.write("Usage: keyFile, oldDataFile  failedKeyFile")
  sys.exit(1)
keyFile  = sys.argv[1]
dataFile = sys.argv[2]
failedKeyFile = sys.argv[3]
date = time.strftime("%Y%m%d-%H%M%S")
if not os.path.exists(keyFile) :
  print "keyfile doesn't exist:{0}".format(keyFile)
  sys.exit(1)
if not os.path.exists(dataFile) :
  print "datafile doesn't exist:{0}".format(dataFile)
  sys.exit(1)
if os.path.exists(failedKeyFile):
  print "result file exists, rename and bak it"
  os.rename(failedKeyFile, failedKeyFile + "_bak_" + date)
startTime = time.time()
keyFd = open(keyFile, "r")
dataFd = open(dataFile, "r")
failedKeyFd = open(failedKeyFile, "a")
keyMap = {}
for line in keyFd:
  line = line.strip(" \t\n")
  keyMap[line] = 1
print "retrieve {0} keys from keyfile {1}".format(len(keyMap), keyFile)
keyRe = re.compile("[ \t]*\"handle\"[ \t]+:[ \t]+\"([^\"]+)\"")
for line in dataFd:
  matchObj = keyRe.match(line)
  if matchObj:
    key = matchObj.group(1)
    keyMap.pop(key, None)
for key in keyMap:
  failedKeyFd.write(key + "\n")
keyFd.close()
dataFd.close()
failedKeyFd.close()
print "filter out {0} failed keys".format(len(keyMap))
endTime = time.time()
print "time cost is {0:.2f}".format(endTime - startTime)

