#!/usr/bin/python
import sys
import os
import re
from ConfigParser import SafeConfigParser
from netaddr import *
import time

reload(sys)  
sys.setdefaultencoding('utf8')

if len(sys.argv) < 4:
  print "Usage: sourceDir resultDir configFile"
  print len(sys.argv)
  sys.exit(0)

sourceDir=sys.argv[1]
resultDir=sys.argv[2]
configFile=sys.argv[3]

#source file
inetFile=os.path.join(sourceDir, "split", "apnic.db.inetnum")
inet6File=os.path.join(sourceDir, "split", "apnic.db.inet6num")
personFile=os.path.join(sourceDir, "split", "apnic.db.person")
roleFile=os.path.join(sourceDir, "split", "apnic.db.role")
mntnerFile=os.path.join(sourceDir, "split", "apnic.db.mntner")

#result file
inetResultFile=os.path.join(resultDir, "inetnum_apnic")

if not os.path.exists(inetFile):
  print "inetnum file doesn't exist"
  sys.exit(1)

#open source file and result file
inetFileFd = open(inetFile, "r")
inetResultFd = open(inetResultFile,"a")

#create regular expression
kwRe=re.compile("([\w-]+):[ \t]*(.*)", re.I)
valueRe=re.compile("[ \t]*([^:]+)", re.I)
commentRe=re.compile("^#", re.I)
ip4RangeRe= re.compile("([\d\.]+)[\t \|-]+([\d\.]+)", re.I)
stripRe = re.compile("[\|#\t\n \r]+", re.I)

#read config file
configParser = SafeConfigParser()
configParser.read(configFile)
netItems=configParser.items("inetnum")
netMappedOptions = []
netOptions = []
for item in netItems:
  netMappedOptions.append(item[0])
  netOptions.append(item[1])
del netItems

valueSep = "|"
columnSep ="\t"
inetResultFd.write(columnSep.join(netMappedOptions) + "\n")
inetDict={}
lineNum = 0
lastKey = ""
objectNum = 0
startTime=time.time()
for line in inetFileFd:
  lineNum += 1
  if commentRe.match(line):
    continue
  if line == "\n":
    if len(inetDict) > 0:
      resultList=[]
      keys = inetDict.keys()
      #choose result
      iterOptions = iter(netOptions)
      for option in iterOptions:
        if option in keys:
          resultList.append(inetDict[option].strip(" \n\r\t"))
          if option == "inetnum":#convert to cidr and ip range
            value = inetDict[option]
            ips = ip4RangeRe.match(value)
            if ips is None:
              sys.stderr.write("parse ip range failed for range {0}".format(value))
              sys.exit(1)
            startIp = ips.group(1)
            endIp   = ips.group(2)
            cidrs = iprange_to_cidrs(startIp, endIp)
            cidrStr = []
            for cidr in cidrs:
              cidrStr.append(str(cidr))
            resultList.append(value)
            resultList.append(valueSep.join(cidrStr))
            option1 = next(iterOptions)
            option2 = next(iterOptions)
        else:
          resultList.append("NULL")
      inetResultFd.write((columnSep.join(resultList)) + "\n")
      inetDict.clear()
      objectNum += 1
      if objectNum % 10000 == 0 and objectNum > 0:
        print "finish {0} objects".format(objectNum)
      continue
    #have retrieve a whole inetnum object
    else:
      continue
  matchObject = kwRe.match(line)
  if matchObject is None:
    matchObject = valueRe.match(line)
    if matchObject is None:
      print "parse error for line {0}".format(line)
      sys.stderr.write("parse error for {1} line: {0}".format(line, lineNum))
      sys.exit(1)
    else:
      key = lastKey
      value = matchObject.group(1)
  else:
    kv = kwRe.match(line).groups()
    key = kv[0]
    value = kv[1]
  value = value.strip(" \n\r\t")
  value = stripRe.sub(" ", value)
  if inetDict.has_key(key):
    inetDict[key] = valueSep.join([inetDict[key], value])
  else:
    inetDict[key] = value
  lastKey = key

endTime=time.time()
print "retrieve {0} lines, get {1} objects with timeCost {2:.2f}".format(lineNum, objectNum, endTime - startTime)
inetFileFd.close()
inetResultFd.close()
