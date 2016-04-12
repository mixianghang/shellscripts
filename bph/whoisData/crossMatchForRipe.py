#!/usr/bin/python
import sys
import os
import time

if len(sys.argv) < 6:
  print "Usage: keyDir uniformDir oldDate initDate newFile"
  sys.exit(1)

keyDir = sys.argv[1]
uniformDir = sys.argv[2]
oldDate = sys.argv[3]
initDate = sys.argv[4]
newFilePath  = sys.argv[5]

oldFilePath = os.path.join(uniformDir, oldDate, "inetnum_ripe")
initFilePath = os.path.join(uniformDir, initDate, "inetnum_ripe")
if not os.path.exists(oldFilePath):
  print "file path doesn't exits, quit the program: {0}".format(oldFilePath)
  sys.exit(1)
if not os.path.exists(initFilePath):
  print "file path doesn't exits, quit the program: {0}".format(initFilePath)
  sys.exit(1)

oldFileFd = open(oldFilePath, "r")
initFileFd = open(initFilePath, "r")
newFileFd  = open(newFilePath, "a")

keyMap = {}
appendKwFilePath = os.path.join(keyDir, initDate, "inetnum_kwlist_appended")
appendKwFilePath1 = os.path.join(keyDir, initDate, "inet6num_kwlist_appended")
deleteKwFilePath = os.path.join(keyDir, initDate, "inetnum_kwlist_deleted")
deleteKwFilePath1 = os.path.join(keyDir, initDate, "inet6num_kwlist_deleted")
fileList = [appendKwFilePath, appendKwFilePath1, deleteKwFilePath, deleteKwFilePath1]

for filePath in fileList:
  if not os.path.exists(filePath):
    print "path doesn't exist: {0}".format(filePath)
    continue
  with open(filePath, "r") as f:
    keyList = f.read().splitlines()
    for key in keyList:
      keyMap[key] = 1

print "retreive {0} changed and deleted keys".format(len(keyMap))

lineNum = 0
acceptedNum = 0
for line in oldFileFd:
  lineNum += 1
  if lineNum == 1:
    newFileFd.write(line)
    continue
  if lineNum % 1000000 == 0:
    print "process {0} lines with {1} accepted from file {2}".format(lineNum, acceptedNum, oldFilePath)
  attrList = line.split("\t")
  if len(attrList) <= 2:
    print "error when process new line from old file :{0}".format(line)
    continue
  key = attrList[1] 
  key = key.strip(" \t\n\r")
  if keyMap.has_key(key) and keyMap[key] == 1:
    newFileFd.write(line)
    acceptedNum += 1
    keyMap[key] = 2
    continue

print "process {0} lines with {1} accepted from file {2}".format(lineNum, acceptedNum, oldFilePath)
  
lineNum = 0
acceptedNum = 0
for line in initFileFd:
  lineNum += 1
  if lineNum == 1:
    continue
  if lineNum % 1000000 == 0:
    print "process {0} lines with {1} accepted from file {2}".format(lineNum, acceptedNum, initFilePath)
  attrList = line.split("\t")
  if len(attrList) <= 2:
    print "error when process new line from old file :{0}".format(line)
    continue
  key = attrList[1] 
  key = key.strip(" \t\n\r")
  if not keyMap.has_key(key):
    newFileFd.write(line)
    acceptedNum += 1
    continue

print "process {0} lines with {1} accepted from file {2}".format(lineNum, acceptedNum, initFilePath)
