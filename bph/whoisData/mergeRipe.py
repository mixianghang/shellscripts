#!/usr/bin/python
import sys
import os
import re
import time

def main():
  if len(sys.argv) < 5:
    sys.stderr.write("Usage: keyDir dataDir date1 date2")
    sys.exit(1)
  keyDir  = sys.argv[1]
  dataDir = sys.argv[2]
  oldDate   = sys.argv[3]
  newDate  = sys.argv[4]
  typeList = ["inetnum", "inet6num", "orgnisation", "irt", "mntner", "person", "role", "aut-num", "as-set", "as-block", "domain", "route-set"]
  date = time.strftime("%Y-%m-%d-%H-%M-%S")
  startTime = time.time()
  for type in typeList:
    appendKeyFile = os.path.join(keyDir, newDate, "{0}_kwlist_appended".format(type))
    deleteKeyFile = os.path.join(keyDir, newDate, "{0}_kwlist_deleted".format(type))
    appendDataFile = os.path.join(dataDir, newDate, "{0}_appended".format(type))
    oldDataFile   = os.path.join(dataDir, oldDate, type)
    newDataFile   = os.path.join(dataDir, newDate, type)

    if os.path.exists(newDataFile):
      os.rename(newDataFile, newDataFile + "_bak_" + date)
    newDataFd = open(newDataFile, "a")
    if not os.path.exists(oldDataFile):
      sys.stderr.write("Error: file not exist for type {0}: {1}".format(type, oldDataFile))
      continue
    oldDataFd = open(oldDataFile, "r")

    #define regular expression to match some patterns
    startRe = re.compile("<\?xml version=\"1\.0\" encoding=\"UTF-8\"\?>\n$")
    endRe  = re.compile("</whois-resources>\n$")
    pkStartRe = re.compile("[ \t]*<primary-key>\n$")
    pkRe      = re.compile("[ \t]*<attribute[ \t]+name=\"[^\"]+\"[ \t]+value=\"([^\"]+)\"[ \t]*/>\n$")
    
    #generate key list 
    if os.path.isfile(appendKeyFile):
      with open(appendKeyFile, "r") as f:
        appendKeyList = f.read().splitlines()
    else:
      appendKeyList = []
    if os.path.isfile(deleteKeyFile):
      with open(deleteKeyFile, "r") as f:
        deleteKeyList = f.read().splitlines()
    else:
      deleteKeyList = []
    excludeKeyList = appendKeyList + deleteKeyList
    print "Start type {0} with excludeList {1}".format(type, len(excludeKeyList))
    maxLimit = 10000
    currPK = None
    currObj = []
    lineNum = 0
    added = 0
    excluded = 0
    for line in oldDataFd:
      lineNum += 1
      currObj.append(line)
      if len(currObj) >= maxLimit:
        sys.stderr.write("error to parse old data when reading more than {0} lines at {1} of type {2}".format(maxLimit, lineNum, type))
        break
      if pkStartRe.match(line):
        nextLine = next(oldDataFd)
        lineNum += 1
        currObj.append(nextLine)
        matchObj = pkRe.match(nextLine)
        if matchObj is None:
          sys.stderr.write("parse primary key line failed: at line {0}, type {1} with conent: {2}".format(lineNum, type, nextLine))
          break
        else:
          currPK = matchObj.group(1)
      if endRe.match(line):
        if currPK is None:
          sys.stderr.write("end without primary key at line {0} and type {1}".format(lineNum, type))
          break
        else:
          if currPK not in excludeKeyList:
            newDataFd.write("".join(currObj))
            added += 1
          else:
            excluded += 1
          currObj = []
          currPK  = None
    oldDataFd.close()
    print "finish {0} lines of old files with {1} added objects and {2} excluded objects for type {3}".format(lineNum, added, excluded, type)
    if os.path.exists(appendDataFile):
      with open(appendDataFile, "r") as f:
        print "append data from appendDataFile {0}".format(appendDataFile)
        for line in f:
          newDataFd.write(line)
    newDataFd.close()
  endTime = time.time()
  print "finish all the types with time cost of {0:.2f}".format(endTime - startTime)
    
if __name__ == "__main__":
  main()
