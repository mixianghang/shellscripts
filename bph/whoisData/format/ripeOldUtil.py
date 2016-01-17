#!/usr/bin/python
import os
import sys
from Exceptions import *
import re
from pprint import pprint
from  uniformUtil import *

class BaseConverter(object):
  def __init__(self, resultFilePath, configParser, name):
    self.columnSep = "\t"
    self.valueSep  = "|"
    self.optionSep = "|"
    self.kwRe=re.compile("([-\w/]+):[ \t]*(.*)", re.I)
    self.valueRe=re.compile("[ \t]*([^:]+)", re.I)
    self.commentRe=re.compile("^#", re.I)
    self.stripRe = re.compile("[\|#\t\n \r]+", re.I)
    self.inetnumRe = re.compile("^inetnum:[ \t]+([^ \t\n-]+)[ \t-]+([^ \t\n-]+)")
    self.resultDict = {}
    self.objectNum = 0
    self.options = []
    self.mappedOptions = []
    self.resultFilePath = resultFilePath
    self.resultFileFd = open(resultFilePath, "a")
    if self.resultFileFd is None:
      raise OpenFileFailure("open file failed: {0}".format(resultFilePath))
    #create regular expression
    self.ip4RangeRe= re.compile("([\d\.]+)[\t \|-]+([\d\.]+)", re.I)
    self.name = name
    self.type = name
    self.readConfig(configParser, self.name)
    self.resultFileFd.write(self.columnSep.join(self.mappedOptions) + "\n")
    self.lastKey = ""
    self.cidrAsnMap = {}
  def init(self):
    return 0
  def refreshCidrAsnMap(self,newMap):
    self.cidrAsnMap = newMap
  def refreshType(self,type):
    self.type = type
  #retrieve key and value
  def processNewLine(self, line):
    if self.commentRe.match(line):
      return 0
    matchObject = self.kwRe.match(line)
    if matchObject is None:
      matchObject = self.valueRe.match(line)
      if matchObject is None:
        print "parse error for line {0}".format(line)
        sys.stderr.write("parse error for {1} line: {0}".format(line, lineNum))
        return -1
      else:
        key = self.lastKey
        value = matchObject.group(1)
    else:
      kv = matchObject.groups()
      key = kv[0]
      value = kv[1]
    value = value.strip(" \n\r\t")
    value = self.stripRe.sub(" ", value)
    if key == "inetnum":
      matchObj = self.inetnumRe.match(line)
      if matchObj is not None:
        startIp = matchObj.group(1)
        endIp   = matchObj.group(2)
        try:
          response = findMappedCidrForRange(startIp, endIp, self.cidrAsnMap)
          if response['code'] == 0:
            cidrKey = response['key']
            self.resultDict['asn'] = self.cidrAsnMap[cidrKey]
        except Exception as e:
          print repr(e)
          print startIp, endIp
          print line
          sys.exit(1)
    if key == "inet6num":
      response = findMappedCidrForCidr(value, self.cidrAsnMap)
      if response['code'] == 0:
        cidrKey = response['key']
        self.resultDict['asn'] = self.cidrAsnMap[cidrKey]
    if self.resultDict.has_key(key):
      self.resultDict[key] = self.valueSep.join([self.resultDict[key], value])
    else:
      self.resultDict[key] = value
    self.lastKey = key
    return 0
  def writeAndClear(self):
    if len(self.resultDict) <= 0:
      return 0
    resultList=[]
    index = 0
    #the first column is type
    resultList.append(self.type)
    index += 1

    keys = self.resultDict.keys()
    #choose result
    while index < len(self.options):
      option = self.options[index]
      subOptions = option.split(self.optionSep)
      subList = []
      for subOption in subOptions:
        if subOption in keys:
          subList.append(self.resultDict[subOption].strip(" \n\r\t"))
        else:
          continue
      if len(subList) > 0:
        resultList.append(self.valueSep.join(subList).strip(" \n\r\t"))
        #if option == "NetHandle":#convert to cidr and ip range
        #  value = inetDict[option]
        #  ips = ip4RangeRe.match(value)
        #  if ips is None:
        #    sys.stderr.write("parse ip range failed for range {0}".format(value))
        #    sys.exit(1)
        #  startIp = ips.group(1)
        #  endIp   = ips.group(2)
        #  cidrs = iprange_to_cidrs(startIp, endIp)
        #  cidrStr = []
        #  for cidr in cidrs:
        #    cidrStr.append(str(cidr))
        #  resultList.append(value)
        #  resultList.append(valueSep.join(cidrStr))
        #  option1 = next(iterOptions)
        #  option2 = next(iterOptions)
      else:
        resultList.append("")
      index += 1
    self.resultFileFd.write((self.columnSep.join(resultList)) + "\n")
    self.resultDict.clear()
    self.objectNum += 1
    if self.objectNum % 10000 == 0 and self.objectNum > 0:
      print "finish {0} objects of type {1} and name {2}".format(self.objectNum, self.type, self.name)
    return 0
  def finishAndClean(self):
    self.resultFileFd.close()
    print "finish {0} with {1} objects".format(self.name, self.objectNum)
  def readConfig(self, configParser, sectionName):
    items=configParser.items(sectionName)
    for item in items:
      self.mappedOptions.append(item[0])
      self.options.append(item[1])
    del items
    return 0

class NetnumConverter(BaseConverter):
  inited = 0
  def __init__(self, resultFilePath, configParser, name):
    super(NetnumConverter, self).__init__()
    self.resultFilePath = resultFilePath
    self.resultFileFd = open(resultFilePath, "a")
    if self.resultFileFd is None:
      raise OpenFileFailure("open file failed: {0}".format(resultFilePath))
    #create regular expression
    self.ip4RangeRe= re.compile("([\d\.]+)[\t \|-]+([\d\.]+)", re.I)
    self.name = name
    self.readConfig(configParser, self.name)
    if NetnumConverter.inited == 0:
      self.resultFileFd.write(self.columnSep.join(self.mappedOptions) + "\n")
      NetnumConverter.inited = 1
    self.lastKey = ""
  def init(self):
    return 0
  def processNewLine(self, line):
    if self.commentRe.match(line):
      return 0
    matchObject = self.kwRe.match(line)
    if matchObject is None:
      matchObject = self.valueRe.match(line)
      if matchObject is None:
        print "parse error for line {0}".format(line)
        sys.stderr.write("parse error for {1} line: {0}".format(line, lineNum))
        return -1
      else:
        key = self.lastKey
        value = matchObject.group(1)
    else:
      kv = matchObject.groups()
      key = kv[0]
      value = kv[1]
    value = value.strip(" \n\r\t")
    value = self.stripRe.sub(" ", value)
    if self.resultDict.has_key(key):
      self.resultDict[key] = self.valueSep.join([self.resultDict[key], value])
    else:
      self.resultDict[key] = value
    self.lastKey = key
    return 0
  def writeAndClear(self):
    if len(self.resultDict) <= 0:
      return 0
    resultList=[]
    keys = self.resultDict.keys()
    #choose result
    iterOptions = iter(self.options)
    for option in iterOptions:
      subOptions = option.split(self.optionSep)
      for subOption in subOptions:
        if subOption in keys:
          option = subOption
          break
        else:
          continue
      if option in keys:
        resultList.append(self.resultDict[option].strip(" \n\r\t"))
        #if option == "NetHandle":#convert to cidr and ip range
        #  value = inetDict[option]
        #  ips = ip4RangeRe.match(value)
        #  if ips is None:
        #    sys.stderr.write("parse ip range failed for range {0}".format(value))
        #    sys.exit(1)
        #  startIp = ips.group(1)
        #  endIp   = ips.group(2)
        #  cidrs = iprange_to_cidrs(startIp, endIp)
        #  cidrStr = []
        #  for cidr in cidrs:
        #    cidrStr.append(str(cidr))
        #  resultList.append(value)
        #  resultList.append(valueSep.join(cidrStr))
        #  option1 = next(iterOptions)
        #  option2 = next(iterOptions)
      else:
        resultList.append("NULL")
    self.resultFileFd.write((self.columnSep.join(resultList)) + "\n")
    self.resultDict.clear()
    self.objectNum += 1
    if self.objectNum % 10000 == 0 and self.objectNum > 0:
      print "finish {0} objects of type {1}".format(self.objectNum, self.name)
    return 0
  def finishAndClean(self):
    self.resultFileFd.close()

def main():
  object = NetnumConverter(sys.argv[1])
if __name__ == "__main__":
  main()
