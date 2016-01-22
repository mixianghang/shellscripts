#!/usr/bin/python
import sys
import os
import re
from ConfigParser import SafeConfigParser
from netaddr import *
import time
from arinUtil import *
from pprint import pprint

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
  sourceFile       = os.path.join(sourceDir, "arin_db.txt")

#define result file name
  inetnumResultFile = os.path.join(resultDir, "inetnum_arin")
  asnResultFile = os.path.join(resultDir, "asn_arin")
  orgResultFile = os.path.join(resultDir, "org_arin")
  personResultFile = os.path.join(resultDir, "person_arin")

#read config file
  classes = {}
  configParser = SafeConfigParser()
  configParser.read(configFile)
  classes['NetHandle'] = BaseConverter(inetnumResultFile, configParser, "inetnum")
  classes['V6NetHandle'] = classes['NetHandle'] 
  classes['OrgID'] = BaseConverter(orgResultFile, configParser, "org")
  classes['ASHandle'] = BaseConverter(asnResultFile, configParser, "asn")
  classes['POCHandle'] = BaseConverter(personResultFile, configParser, "person")

#open source file and result file
  if not os.path.exists(sourceFile):
    print "arin source file doesn't exist {0}".format(sourceFile)
    return -1
  sourceFileFd = open(sourceFile, "r")

  lineNum = 0
  objectNum = 0
  startTime=time.time()
  classKeys = classes.keys()
  currObj = None
  kwRe = re.compile("([\w-]+):[ \t]*(.*)", re.I)
  blankRe = re.compile("^[ \t\n\r]+$", re.I)
  for line in sourceFileFd:
    lineNum += 1
    if currObj is not None:
      if blankRe.match(line) is None:
        if classes[currObj].processNewLine(line) != 0:
          print "error when process new line {0} for {1}".format(line, currObj)
      else:
        classes[currObj].writeAndClear()
        currObj = None
        objectNum += 1
    else:
      if blankRe.match(line) is not None:
        continue
      matchObject = kwRe.match(line)
      if matchObject is not None and matchObject.group(1) in classKeys:
        currObj = matchObject.group(1)
        if currObj == "V6NetHandle":
          classes[currObj].refreshType("inet6num")
        elif currObj == "NetHandle":
          classes[currObj].refreshType("inetnum")
        if classes[currObj].processNewLine(line) != 0:
          print "error when process new line {0} for {1}".format(line, currObj)
        continue
      else:
        print matchObject.groups()
        print "process line error:{0} at {1}".format(line, lineNum)
        pprint(line)
        sys.exit(1)

  endTime=time.time()
  print "retrieve {0} lines, get {1} objects with timeCost {2:.2f}".format(lineNum, objectNum, endTime - startTime)
  sourceFileFd.close()
if __name__ == "__main__":
  main()
