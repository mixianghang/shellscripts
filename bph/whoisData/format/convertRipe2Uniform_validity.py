#!/usr/bin/python
import sys
import os
import re
from ConfigParser import SafeConfigParser
from netaddr import *
import time
from ripeUtil import *
from pprint import pprint
from uniformUtil import *

reload(sys)  
sys.setdefaultencoding('utf8')

def main():
  #check and assign cl args to variables
  if len(sys.argv) < 4:
    print "Usage: sourceDir resultDir configFile bulkDir"
    print len(sys.argv)
    sys.exit(0)

  sourceDir=sys.argv[1]
  resultDir=sys.argv[2]
  configFile=sys.argv[3]
  #bulkDir = sys.argv[4]

  #create cidrAsnMap
  cidrAsnMap = {}
  #routeFile = os.path.join(bulkDir, "ripe.db.route")
  #route6File = os.path.join(bulkDir, "ripe.db.route6")
  #createCidrAsnMap(routeFile, cidrAsnMap)
  #createCidrAsnMap(route6File, cidrAsnMap)
  print "retrieve {0} cidr asn mappings".format(len(cidrAsnMap))

#source file
  objList = [("inetnum", "inetnum"), ("inetnum", "inet6num"), ("person", "person"), ("person", "role"),
  ("person", "irt"), ("person", "mntner"),("asn", "aut-num"),("org","organisation")]
  #objList = [("person", "person")]
  convDict = {}

#read config file
  classes = {}
  configParser = SafeConfigParser()
  configParser.read(configFile)


  lineNum = 0
  startTime=time.time()
  for obj in objList:
    name = obj[0]
    type = obj[1]
    if not convDict.has_key(name):
      resultFilePath = os.path.join(resultDir, "{0}_formatted_missing".format(name))
      print "create obj for name {0} and type {1}".format(name, type)
      convObj = BaseConverter(resultFilePath, configParser, name)
      convObj.refreshType(type)
      convDict[name] = convObj
      if name == "inetnum":
        convObj.refreshCidrAsnMap(cidrAsnMap)
    else:
      convObj = convDict[name]
      convObj.refreshType(type)
    sourceFilePath = os.path.join(sourceDir, "{0}_missing".format(type))
    if not os.path.exists(sourceFilePath):
      print "file doestn't exist: {0}".format(sourceFilePath)
      continue
    sourceFileFd = open(sourceFilePath, "r")
    kwRe = re.compile("([\w/-]+):[ \t]*(.*)", re.I)
    startRe = re.compile("[ \t\n\r]+<attributes>", re.I)
    endRe = re.compile("[ \t\n\r]+</attributes>", re.I)
    lineNum = 0
    currObj = 0
    for line in sourceFileFd:
      lineNum += 1
      if currObj == 1:
        if endRe.match(line) is None:
          if convObj.processNewLine(line) != 0:
            print "error when process new line {0} for {1} at {2}".format(line, type, lineNum)
        else:
          convObj.writeAndClear()
          currObj = 0
      else:
        if startRe.match(line) is None:
          continue
        else:
          currObj = 1

  for key in convDict:
    obj = convDict[key]
    obj.finishAndClean()
  endTime=time.time()
  print "time cost is {0:.2f}".format(endTime - startTime)
if __name__ == "__main__":
  main()
