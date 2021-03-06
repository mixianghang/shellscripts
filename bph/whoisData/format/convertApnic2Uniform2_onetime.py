#!/usr/bin/python
import sys
import os
import re
from ConfigParser import SafeConfigParser
from netaddr import *
import time
from apnicUtil import *
from pprint import pprint
from uniformUtil import *

reload(sys)  
sys.setdefaultencoding('utf8')

def main():
  #check and assign cl args to variables
  if len(sys.argv) < 4:
    print "Usage: sourceDir resultDir configFile"
    print len(sys.argv)
    sys.exit(0)

  sourceDir=sys.argv[1]
  resultDir=sys.argv[2]
  configFile=sys.argv[3]

#source file
  objList = [("inetnum", "inetnum"), ("inetnum", "inet6num"), ("person", "person"), ("person", "role"),
  ("person", "irt"), ("person", "mntner"),("asn", "aut-num")]
  #objList = [("person", "person")]
  convDict = {}

#read config file
  classes = {}
  configParser = SafeConfigParser()
  configParser.read(configFile)

#create cidrAsnMap
  cidrAsnMap = {}
  routeFile = os.path.join(sourceDir, "apnic.db.route")
  route6File = os.path.join(sourceDir, "apnic.db.route6")
  createCidrAsnMap(routeFile, cidrAsnMap)
  createCidrAsnMap(route6File, cidrAsnMap)
  print "retrieve {0} cidr asn mappings".format(len(cidrAsnMap))


  lineNum = 0
  startTime=time.time()
  for obj in objList:
    name = obj[0]
    type = obj[1]
    if not convDict.has_key(name):
      resultFilePath = os.path.join(resultDir, "{0}_apnic".format(name))
      convObj = BaseConverter(resultFilePath, configParser, name)
      convObj.refreshType(type)
      convDict[name] = convObj
      if name == "inetnum":
        convObj.refreshCidrAsnMap(cidrAsnMap)
    else:
      convObj = convDict[name]
      convObj.refreshType(type)
    sourceFilePath = os.path.join(sourceDir, "apnic.db.{0}".format(type))
    if not os.path.exists(sourceFilePath):
      print "source file {0} doesn't exist".format(sourceFilePath)
      continue
    sourceFileFd = open(sourceFilePath, "r")
    kwRe = re.compile("([\w/-]+):[ \t]*(.*)", re.I)
    blankRe = re.compile("^[ \t\n\r]+$", re.I)
    lineNum = 0
    currObj = 0
    for line in sourceFileFd:
      lineNum += 1
      if currObj == 1:
        if blankRe.match(line) is None:
          if convObj.processNewLine(line) != 0:
            print "error when process new line {0} for {1} at {2}".format(line, type, lineNum)
        else:
          convObj.writeAndClear()
          currObj = 0
      else:
        if blankRe.match(line) is not None:
          continue
        else:
          currObj = 1
          if convObj.processNewLine(line) != 0:
              print "error when process new line {0} for {1} at {2}".format(line, type, lineNum)
          continue

  for key in convDict:
    obj = convDict[key]
    obj.finishAndClean()
  endTime=time.time()
  print "time cost is {0:.2f}".format(endTime - startTime)
if __name__ == "__main__":
  main()
