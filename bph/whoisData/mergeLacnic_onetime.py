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
  #typeList = ["person", "inetnum"]
  typeList = ["inetnum"]
  date = time.strftime("%Y-%m-%d-%H-%M-%S")
  startTime = time.time()
  for type in typeList:
    appendKeyFile = os.path.join(keyDir, newDate, "{0}_kwlist_appended".format(type))
    deleteKeyFile = os.path.join(keyDir, newDate, "{0}_kwlist_deleted".format(type))
    newKeyFile = os.path.join(keyDir, newDate, "{0}_kwlist".format(type))
    appendDataFile = os.path.join(dataDir, newDate, "{0}_appended".format(type))
    oldDataFile   = os.path.join(dataDir, oldDate, type)
    newDataFile   = os.path.join(dataDir, newDate, type)

    if os.path.exists(newDataFile):
      print "newDate file exists, so remove it"
      os.remove(newDataFile)
    newDataFd = open(newDataFile, "a")
    if not os.path.exists(oldDataFile):
      sys.stderr.write("Error: file not exist for type {0}: {1}".format(type, oldDataFile))
      continue
    oldDataFd = open(oldDataFile, "r")

    
    #generate key list 
    newKeyDict = {}
    if os.path.isfile(newKeyFile):
      with open(newKeyFile, "r") as f:
        newKeyList = f.read().splitlines()
        for key in newKeyList:
          newKeyDict[key] = 1
    else:
      print "{0} doesn't exist ".format(newKeyFile)
      sys.exit(1)
    if os.path.isfile(appendKeyFile):
      with open(appendKeyFile, "r") as f:
        appendKeyList = f.read().splitlines()
    else:
      print "{0} doesn't exist ".format(appendKeyFile)
      sys.exit(1)
    if os.path.isfile(deleteKeyFile):
      with open(deleteKeyFile, "r") as f:
        deleteKeyList = f.read().splitlines()
    else:
      print "{0} doesn't exist ".format(deleteKeyFile)
      sys.exit(1)
    excludeKeyList = appendKeyList + deleteKeyList
    print "Start type {0} with newkey List {2} and excludeList {1}".format(type, len(excludeKeyList), len(newKeyDict))
    maxLimit = 10000
    currPK = None
    isObj  = 0
    currObj = []
    lineNum = 0
    added = 0
    excluded = 0
    #define regular expression to match some patterns
    startRe = re.compile("^[ \t]*{[ \t]*\n?$")
    closeStartRe = re.compile("^[ \t]*}{[ \t]*\n?$")
    closeRe =   re.compile("^[ \t]*}[ \t]*\n?$")
    if type == "inetnum":
      pkRe = re.compile("[ \t]*\"handle\"[ \t]+:[ \t]+\"([0-9a-f:\.]+/[0-9]+)\"")
    else:
      pkRe = re.compile("[ \t]*\"handle\"[ \t]+:[ \t]+\"([^\"]+)\"")
    for line in oldDataFd:
      lineNum += 1
      startMatch = startRe.match(line)
      if startMatch:
        currObj = []
        isObj = 1
        currObj.append(line)
        continue
      closeStartMatch = closeStartRe.match(line)
      if closeStartMatch:
        if isObj == 1 and currPK and currPK not in excludeKeyList and newKeyDict.has_key(currPK):
          currObj.append("}\n")
          newDataFd.write("".join(currObj))
          added += 1
        if currPK and currPK in  excludeKeyList:
          excluded += 1
        currObj = []
        currPK = None
        currObj.append("{\n")
        isObj = 1
        continue
      closeMatch = closeRe.match(line)
      if closeMatch:
        if isObj == 1 and currPK and currPK not in excludeKeyList and newKeyDict.has_key(currPK):
          currObj.append("}\n")
          newDataFd.write("".join(currObj))
          added += 1
        if currPK and currPK in  excludeKeyList:
          excluded += 1
        currObj = []
        currPK = None
        isObj = 0
        continue
      pkMatch = pkRe.match(line)
      if pkMatch:
        if isObj == 1:
          currPK = pkMatch.group(1)
          currObj.append(line)
        else:
          currObj = []
          isObj = 0
          pkMatch = None
        continue
      currObj.append(line)
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
