#!/usr/bin/python
import sys
import os
if __name__ == "__main__":
  if len(sys.argv) < 7:
    print "Usage: type newPath oldPath eclusiveKwPath, keyPath, missKeyPath"
    print sys.argv
    sys.exit(1)
  type = sys.argv[1].lower();#person/role/irt/mntner/organisation/
  newPath = sys.argv[2];
  oldPath = sys.argv[3];
  exclusivePath = sys.argv[4];
  keyPath = sys.argv[5];
  missKeyPath = sys.argv[6]
#generateg exclusive key list and map
  exclusiveList = []
  exclusiveMap = {}
  with open(exclusivePath, "r") as exclusiveFd:
    exclusiveList = exclusiveFd.read().splitlines()
    for line in  exclusiveList:
      exclusiveMap[line.lower()] = 1
#generate kw list and map
  keyList = []
  keyMap = {}
  with open(keyPath, "r") as keyFd:
    keyList = keyFd.read().splitlines()
    for line in keyList:
      keyMap[line.lower()] = 1
  print "get {0} exclusive kws and {1} kws".format(len(exclusiveList), len(keyList))
  if len(keyList) <= 0:
    sys.stderr.write("key list cannnot be empty: {0}\n".format(keyPath))
    sys.exit(1)

#generate existing kw list by searching the obj file
  existKeyMap = {}
  with open(newPath, "r") as newFd:
    for line in newFd:
      attrs = line.split("\t")
      if attrs[0].lower() == type:
        existKeyMap[attrs[1].lower()] = 1
#generate appendKeyMap and appended lines
  appendKeyMap = {}
  appendLines = []
  with open(oldPath, "r") as oldFd:
    for line in oldFd:
      attrs = line.split("\t")
      if attrs[0].lower() == type:
        key = attrs[1].lower()
        if (key in keyMap) and \
           key not in existKeyMap and \
           key not in exclusiveMap:
          if key not in appendKeyMap:
            appendLines.append(line)
            appendKeyMap[key] = 1
#append lines to newPath
  with open(newPath, "a") as newFd:  
    for line in appendLines:
      newFd.write(line)
  print "append {0} lines from {1} to {2}".format(len(appendLines), oldPath, newPath)
#generate missingKeyList
  missingKeyList = []
  for key in keyMap:
    if key not in existKeyMap and key not in appendKeyMap:
      missingKeyList.append(key)
  print "still {0} missing keys for {1}".format(len(missingKeyList), newPath)
#write missing keyes to missKeyPath
  with open(missKeyPath, "w") as missFd:
    if len(missingKeyList) > 0:
      missFd.write("\n".join(missingKeyList))

