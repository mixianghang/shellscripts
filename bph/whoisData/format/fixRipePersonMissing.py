#!/usr/bin/python
import os
import sys
import re
'''
 This file is used to fix Ripe person missing by merging data generated from appended api data and data from
 yesterday
 1.Newly generated person_ripe for $today
 2.missing_person_key_file
 3.others_ripe file
'''
'''
  select out role|irt|mntner lines from personTodayPath and save them into othersTodayPath
  arguments:
  1.personFilePath othersFilePath
'''
def filterOthers():
  personFilePath = sys.argv[2]
  othersFilePath = sys.argv[3]
  print "filter others with personFile {0} and othersFile {1}".format(personFilePath, othersFilePath)
  typeRe = re.compile("(role|mntner|irt)\t", re.I)
  if not os.path.exists(personFilePath) or os.path.exists(othersFilePath):
    sys.stderr.write("{0} doesn't exist or {1} exists\n".format(personFilePath, othersFilePath))
    sys.exit(1)
  othersFd = open(othersFilePath, "w")
  sep = "\t"
  with open(personFilePath, "r") as personFd:
    objNum = 0
    for line in  personFd:
      if typeRe.match(line) != None:
        othersFd.write(line)
        objNum += 1
    print "select out {0} objects of types(role/mntner/irt)".format(objNum)
    othersFd.close()
    if objNum <= 0:
      sys.exit(1)
'''
filter out unchanged person objects from yesterday's person file
arguments:
1.todayAppendedKeyFile 2. todayDeleteKeyFile 3. yesterdayPersonFile  4. resultFilePath
'''
def filterUnchanged():
  with open(sys.argv[2], "r") as appendedKeyFd:
    appendedKeyList = appendedKeyFd.read().splitlines()
  with open(sys.argv[3], "r") as deletedKeyFd:
    deletedKeyList = deletedKeyFd.read().splitlines()
  exclusiveKeyList = appendedKeyList + deletedKeyList
  exclusiveKeyMap = {}
  for key in exclusiveKeyList:
    exclusiveKeyMap[key] = 1
  print "get {0} exclusiveKeys".format(len(exclusiveKeyList))
  sep = "\t"
  resultKeyMap = {}
  with open(sys.argv[4], "r") as yesterdayPersonFd:
    with open(sys.argv[5], "w") as resultFd:
      objNum = 0;
      lineNum = 0;
      for line in yesterdayPersonFd:
        attrs = line.split(sep)
        if attrs[0] == "person":
          lineNum += 1
          if attrs[1] not in exclusiveKeyMap and attrs[1] not in resultKeyMap:
            resultFd.write(line)
            objNum += 1
            resultKeyMap[attrs[1]] = 1
      print "got {0} objs from {1} with {2} persons".format(objNum, sys.argv[4], lineNum)

'''
generate missing person key list
arguments:
1.todayPersonPath todayKeyPath missingKeyPath
'''
def genMissingKeyList():
  personPath = sys.argv[2]
  keyPath    = sys.argv[3]
  missingKeyPath = sys.argv[4]
  if len(sys.argv) >= 6:
    objName = sys.argv[5].lower()
  else:
    objName = "person"
  keyMap = {}
  with open(keyPath, "r") as keyFd:
    for line in keyFd:
      key = line[:-1].lower()
      keyMap[key] = 1
  allKeyNum = len(keyMap)
  print "retrieve {0} keys from {1}".format(allKeyNum, keyPath)
  with open(personPath, "r") as personFd:
    for line in personFd:
      attrs = line.split("\t")
      if attrs[0] == objName and attrs[1].lower() in keyMap:
        del keyMap[attrs[1].lower()]
  with open(missingKeyPath, "w") as missingKeyFd:
    for key in keyMap:
      missingKeyFd.write(key + "\n")
  print "got {0} missing keys from {1} keys".format(len(keyMap), allKeyNum)

if __name__ == "__main__":
  option = int(sys.argv[1])
  if option == 1:
    #select out role|irt|mntner lines from personTodayPath and save them into othersTodayPath
    filterOthers()
  elif option == 2:
    '''
    filter out unchanged person objects from yesterday's person file
    arguments:
    1.today yesterday uniformDir dataDir keyDir
    '''
    filterUnchanged()
  elif option == 3:
    '''
    generate missing person key list
    arguments:
    1.todayPersonPath todayKeyPath missingKeyPath
    '''
    genMissingKeyList()

