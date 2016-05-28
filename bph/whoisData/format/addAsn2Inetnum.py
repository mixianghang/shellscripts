#!/usr/bin/python
import os
import sys
import time
import re
from uniformUtil import *
from pprint import pprint

#used to format bgp file downloaded from http://bgp.potaroo.net/v6/as2.0/bgptable.txt
def fortmatV6BGP(originFile, formattedFile):
  prefixRe = re.compile("\*>?[ ]+([0-9a-f:]+/[0-9]+)[ \t]*", re.I)
  pathRe   = re.compile("^[ \t]+([0-9][0-9 ]+[0-9])[ ]+", re.I)
  sepPathRe = re.compile("[ \t]+", re.I)
  valueSep = "|"
  with open(formattedFile, "w") as formattedFd:
    with open(originFile, "r") as originFd:
      currObj = 0
      currPrefix = None
      mappedAsns = []
      lineNum = 0
      success = 0
      failed  = 0
      for line in originFd:
        lineNum += 1
        matchObj = prefixRe.match(line)
        if matchObj:
          if currObj == 1:
            if currPrefix and len(mappedAsns) > 0:
              formattedFd.write("{0}\t{1}\n".format(currPrefix, valueSep.join(mappedAsns)))
              success += 1
              if success % 1000 == 0:
                print "finish format {0} bgpV6 records and failed {1}".format(success, failed) 
            else:
              print "parse error for {0} at line {1}".format(currPrefix, lineNum)
              failed += 1
          currObj = 1
          currPrefix = matchObj.group(1) 
          mappedAsns = []
          continue
        matchObj = pathRe.match(line)
        if matchObj:
          if currObj != 1:
            print "parse error failed at lineNum {0}: {1}".format(lineNum, line)
            currObj = 0
            currPrefix = None
            mappedAsns = []
            continue
          asnStr = matchObj.group(1)
          asnStr = asnStr.strip(" \t\n\r")
          asnList = sepPathRe.split(asnStr)
          if len(asnList) > 0:
            originAsn = asnList[-1]
            if originAsn not in mappedAsns:
              mappedAsns.append(originAsn)
          continue
        continue
  response = {"code":0}
  return response

    

def addAsn2Inetnum(formatDir, bgpFile, resultDir, registries):
  date = time.strftime("%Y%m%d_%H%M%S")
  if not os.path.exists(formatDir):
    print "format dir doesn't exist: {0}".format(formatDir)
    return -1
  if not os.path.exists(bgpFile):
    print "bgp file doesn't exist: {0}".format(bgpFile)
    return -1
  if not os.path.exists(resultDir):
    os.makedirs(resultDir)
#retrieve cidr asn mapping from bgpfile
  cidrAsnMap = {}
  splitRe = re.compile("[ \t]+", re.I)
  with open(bgpFile, "r") as bgp:
    lineNum = 0
    failed = 0
    success = 0
    for line in bgp:
      lineNum += 1
      line = line.strip(" \n\t\r")
      splitList = splitRe.split(line)
      if len(splitList) == 2:
        cidir = splitList[0]
        asn   = splitList[1]
        cidrAsnMap[cidir] = asn
        success += 1
      else:
        failed += 1
        print "failed to parse bgp line at {0}: {1}".format(lineNum, line)
    print "finish retrieving bgp file and get {0} cidr-asn mappings and failed {1}".format(success, failed)

  ipRangeRe = re.compile("[ ]*([0-9a-z\.:]+)[ ]+-[ ]+([0-9a-z\.:]+)", re.I)
  asSubRe = re.compile("(as)+", re.I)
  asRe = re.compile("[0-9\|,]*as", re.I)
  for registry in registries:
    inetnumFilePath = os.path.join(formatDir, "inetnum_{0}".format(registry))
    if not os.path.exists(inetnumFilePath):
      sys.stderr.write("inetnum file for type {0} doesn't exist".format(inetnumFilePath))
      continue
    resultFilePath = os.path.join(resultDir, "inetnum_{0}".format(registry))
    if os.path.exists(resultFilePath):
      print "result file exists, bak it ".format(inetnumFilePath)
      os.rename(resultFilePath, resultFilePath + "_bak_" + date)
    inetnumFd = open(inetnumFilePath, "r")
    resultFd  = open(resultFilePath, "w")
    print "start to process file:{0}".format(inetnumFilePath)
    added = 0
    lineNum = 0
    ipv6Added = 0
    for line in inetnumFd:
      lineNum += 1
      if lineNum == 1:
        resultFd.write(line)
        continue
      attrs = line.split("\t")
      if len(attrs) < 3:
        print "split line failed:{0}".format(line) 
        continue
      if registry == "arin":
        primaryKey = attrs[2]
      else:
        primaryKey = attrs[1]
      response = None
      if "/" in primaryKey:#key is cidr
        response = findMappedCidrForCidr(primaryKey, cidrAsnMap)
      else:
        matchedIps = ipRangeRe.match(primaryKey)
        if matchedIps:
          startIp = matchedIps.group(1)
          endIp   = matchedIps.group(2)
          response = findMappedCidrForRange(startIp, endIp, cidrAsnMap)
        else:
          print "parse ip range failed for line: {0}".format(line)
      if response and response['code'] == 0:
        asnList = response['body']
        attrs[6] = "|".join(asnList)
        added += 1
        if ":" in primaryKey:
          ipv6Added += 1
        if added %  1000 ==0:
          print "add asn to {0} inetnums from registry {1}, among them, {2} are ipv6".format(added, registry, ipv6Added)
      matchObj = asRe.match(attrs[6])
      if matchObj:
        attrs[6] = asSubRe.sub("", attrs[6])
      resultFd.write("\t".join(attrs))
    print "complement asn for {0} ({3} are ipv6) out of {1} inetnum objects from {2} registry".format(added, lineNum, registry, ipv6Added)
    resultFd.close()
    inetnumFd.close()

if __name__ == "__main__":
  if len(sys.argv) < 5:
    print "usage: formatDir, bgpFile, resultFile registry"
    sys.exit(1)
  date = time.strftime("%Y%m%d_%H%M%S")
  formatDir = sys.argv[1]
  bgpFile   = sys.argv[2]
  resultDir = sys.argv[3]
  registry  = sys.argv[4]
  bgpDir = os.path.dirname(bgpFile)
  bgpIpV4 = os.path.join(bgpDir, "bgpTable_ipv4")
  bgpIpV6 = os.path.join(bgpDir, "bgpTable_ipv6")
  formattedBgpIpV6 = os.path.join(bgpDir, "bgpTable_ipv6_formatted")
  if not os.path.exists(bgpFile) or not os.path.exists(formattedBgpIpV6):
    #download bgp files for both ipv4 and v6 prefixes
    urlForIpV4 = "http://thyme.apnic.net/current/data-raw-table"
    urlForIpV6 = "http://bgp.potaroo.net/v6/as2.0/bgptable.txt"
    if not os.path.exists(bgpIpV4):
      response = downloadFile(urlForIpV4, bgpIpV4)
      if response['code'] != 0:
        print "donwload bgp file {0} failed with error msg: {1}".format(bgpIpV4, response['body'])
        sys.exit(1)
      else:
        print "succeed in downloading bgp table for ipV4: {0}".format(bgpIpV4)
    if not os.path.exists(bgpIpV6):
      response = downloadFile(urlForIpV6, bgpIpV6)
      if response['code'] != 0:
        print "donwload bgp file {0} failed with error msg: {1}".format(bgpIpV6, response['body'])
        sys.exit(1)
      else:
        print "succeed in downloading bgp table for ipV6: {0}".format(bgpIpV6)
    #process ipv6 bgp file to the standard format with every line containing only prefix and mapped origin asn 
    #values, when there are multiple asn values, they will be separated by |
    if not os.path.exists(formattedBgpIpV6):
      response = fortmatV6BGP(bgpIpV6, formattedBgpIpV6)
      if response['code'] == 0:
        print "finish formatting bgpV6 file:{0}".format(bgpIpV6)
      else:
        print "error happened when formatting bgp file:{0}".format(bgpIpV6)
        sys.exit(1)
    #concatenate v4 and v6 bgp file to one file
    bgpFileList = [bgpIpV4, formattedBgpIpV6]
    with open(bgpFile, "w") as bgpFd:
      for bgpPartFile in bgpFileList:
        with open(bgpPartFile, "r") as bgpPartFd:
          for line in bgpPartFd:
            bgpFd.write(line)
   
  addAsn2Inetnum(formatDir, bgpFile, resultDir, [registry])
  
  

