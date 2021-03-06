#!/usr/bin/python
from __future__ import unicode_literals
import sys
import os
import re
from ConfigParser import SafeConfigParser
from netaddr import *
import time
from pprint import pprint
from lacnicUtil import *
from uniformUtil import *

reload(sys)  
sys.setdefaultencoding('utf8')

def readFromBulk(sourceDir, resultDir,configFile):
  #read inetnum inetnum6 mnter aut-num from the same file
  sourceFile1 = os.path.join(sourceDir, "lacnic.dp")
  if not os.path.exists(sourceFile1):
    print "lacnic source file doesn't exist {0}".format(sourceFile1)
    return -1

  sourceFileFd = open(sourceFile1, "r")
  netResultFile = os.path.join(resultDir, "inetnum_lacnic")
  asnResultFile = os.path.join(resultDir, "asn_lacnic")
  orgResultFile = os.path.join(resultDir, "org_lacnic")
  personResultFile = os.path.join(resultDir, "person_lacnic")

  #create cidrAsnMap
  cidrAsnMap = {}
#  createCidrAsnMap(sourceFile1, cidrAsnMap)
  #print "retrieve {0} cidr asn mappings".format(len(cidrAsnMap))

  configParser = SafeConfigParser()
  configParser.read(configFile)
#create converter
  inetnumConv = BaseConverter(netResultFile, configParser, "inetnum")
  asnConv = BaseConverter(asnResultFile, configParser, "asn")

  convDict = {"inetnum":inetnumConv, "inet6num":inetnumConv, "aut-num":asnConv}

  lineNum = 0
  startTime=time.time()
  curObj = None
  type = ""
  startRe = re.compile("^[ \t\r\n]+$", re.I)
  kvRe = re.compile("([\w/-]+):[ \t]+(.*)", re.I)
  endRe   = startRe
  commentRe = re.compile("^%.*", re.I)
  for line in sourceFileFd:
    lineNum += 1
    if commentRe.match(line):
      continue
    if curObj is not None:
      if endRe.match(line):
        curObj.writeAndClear()
        curObj = None
      else:
        if curObj.processNewLine(line) != 0:
          print "process new line failed for line {0} and type {1} :{2}".format(lineNum, type, line)
    else:#try to find qualified object
      matchObj =kvRe.match(line)
      if matchObj is None:
        continue
      else:
        key = matchObj.group(1)
        value = matchObj.group(2)
        if convDict.has_key(key):
          curObj = convDict[key]
          curObj.refreshType(key)
          type = key
          if curObj.processNewLine(line) != 0:
            print "process new line failed for line {0} and type {1} :{2}".format(lineNum, type, line)
        else:
          continue

def readFromApiData(sourceDir, resultDir, configFile):
  configParser = SafeConfigParser()
  configParser.read(configFile)
  personResultFile = os.path.join(resultDir, "person_lacnic")
  personConv = PersonConverter(personResultFile, configParser, "person")
  objList = [("person", "person", "person", personConv)]
  #objList = [("person", "person/role", "person_role", personConv),("person", "irt", "irt", personConv)]
  for obj in objList:
    name = obj[0]
    type = obj[1]
    fileName = obj[2]
    convObj = obj[3]
    convObj.refreshType(type)
    sourceFilePath = os.path.join(sourceDir, "{0}".format(fileName))
    if not os.path.exists(sourceFilePath):
      print "file doesn't exist:{0}".format(sourceFilePath)
      continue
    sourceFileFd = open(sourceFilePath, "r")
    kwRe = re.compile("([\w/-]+):[ \t]*(.*)", re.I)
    startRe = re.compile("^}?{\n$", re.I)
    endRe = re.compile("^}{?[\n]?$", re.I)
    onlyEndRe = re.compile("^}[\n]?$", re.I)
    lineNum = 0
    currObj = 0
    print "name {0}, type {1}, file{2}".format(name, type, fileName)
    for line in sourceFileFd:
      lineNum += 1
      if currObj == 1:
        if endRe.match(line) is None:
          if convObj.storeNewLine(line) != 0:
            print "error when process new line {0} for {1} at {2}".format(line, type, lineNum)
        else:
          convObj.end()
          if onlyEndRe.match(line):
            currObj = 0
          else:
            currObj = 1
            convObj.newStart()
      else:
        if startRe.match(line) is None:
          continue
        else:
          currObj = 1
          convObj.newStart()
  personConv.finishAndClean()
def main():
  #check and assign cl args to variables
  if len(sys.argv) < 5:
    print "Usage: sourceDir1 sourceDir2 resultDir configFile"
    print len(sys.argv)
    sys.exit(0)

  bulkDir = sys.argv[1]
  apiDir  = sys.argv[2]
  resultDir= sys.argv[3]
  configFile= sys.argv[4]

  startTime = time.time()
  if os.path.exists(bulkDir):
    readFromBulk(bulkDir, resultDir, configFile)
  else:
    sys.stderr.write("skip read from bulk since bulk data doesn't exist:{0}".format(bulkDir))
  if os.path.exists(apiDir):
    readFromApiData(apiDir, resultDir, configFile)
  else:
    sys.stderr.write("skip read from api since bulk data doesn't exist:{0}".format(apiDir))

  endTime=time.time()
  print "time cost is {0:.2f}".format(endTime - startTime)
if __name__ == "__main__":
  main()
