#!/usr/bin/python
import sys
import os
import re
import time

#filter out failed keys and damaged objects, so that to retry requests
def main():
  if len(sys.argv) < 5:
    sys.stderr.write("Usage: keyFile, oldDataFile, newDataFile newKeyFile")
    sys.exit(1)
  keyFile  = sys.argv[1]
  oldDataFile = sys.argv[2]
  newDataFile = sys.argv[3]
  newKeyFile = sys.argv[4]

  date = time.strftime("%Y-%m-%d-%H-%M-%S")
  startTime = time.time()

  if os.path.exists(newDataFile):
    os.rename(newDataFile, newDataFile + "_bak_" + date)
  newDataFd = open(newDataFile, "a")
  if os.path.exists(newKeyFile):
    os.rename(newKeyFile, newKeyFile + "_bak_" + date)
  newKeyFd = open(newKeyFile, "a")
  if not os.path.exists(oldDataFile):
    sys.stderr.write("Error: file not exist: {0}".format(oldDataFile))
    sys.exit(1)
  oldDataFd = open(oldDataFile, "r")

  
  keyMap = {}
  #generate key list 
  if os.path.isfile(keyFile):
    with open(keyFile, "r") as f:
      keyList = f.read().splitlines()
      for line in keyList:
        keyMap[line] = 1
  else:
    sys.stderr.write("Error: key file doesn't exist:{0}".format(keyFile))
    sys.exit(1)
  print "read out {0} keys from keyfile".format(len(keyMap))

  #define regular expression to match some patterns
  startRe = re.compile("<\?xml version=\"1\.0\" encoding=\"UTF-8\"\?>\n$")
  endRe  = re.compile("</whois-resources>\n$")
  pkStartRe = re.compile("[ \t]*<primary-key>\n$")
  pkRe      = re.compile("[ \t]*<attribute[ \t]+name=\"[^\"]+\"[ \t]+value=\"([^\"]+)\"[ \t]*/>\n$")
  maxLimit = 10000
  currPK = None
  currObj = []
  lineNum = 0
  duplicate = 0
  for line in oldDataFd:
    lineNum += 1
    if len(currObj) == 0:
        if startRe.match(line):
          currPK = None
          currObj.append(line)
        continue
    if startRe.match(line):
      currPK = None
      currObj = []
      currObj.append(line)
      continue
    currObj.append(line)
    if len(currObj) >= maxLimit:
      sys.stderr.write("error to parse old data when reading more than {0} lines at {1}".format(maxLimit, lineNum))
      break
    if pkStartRe.match(line):
      nextLine = next(oldDataFd)
      lineNum += 1
      currObj.append(nextLine)
      matchObj = pkRe.match(nextLine)
      if matchObj is None:
        sys.stderr.write("parse primary key line failed: at line {0} with conent: {1}".format(lineNum, nextLine))
        currObj = []
        currPK = None
        continue
      else:
        currPK = matchObj.group(1)
    if endRe.match(line):
      if currPK is None:
        sys.stderr.write("end without primary key at line {0} and type {1}".format(lineNum, type))
        currObj = []
        currPK = None
        continue
      else:
        if keyMap.has_key(currPK) :
          newDataFd.write("".join(currObj))
        else:
          duplicate += 1
        keyMap.pop(currPK, None)
        currObj = []
        currPK  = None
  oldDataFd.close()
  newDataFd.close()
  endTime = time.time()
  for key in keyMap:
    newKeyFd.write(key + "\n")
  newKeyFd.close()
  print "finish with time cost of {0:.2f}".format(endTime - startTime)
  print "find out {0} failed keys and {1} duplicate objects".format(len(keyMap), duplicate)
    
if __name__ == "__main__":
  main()
