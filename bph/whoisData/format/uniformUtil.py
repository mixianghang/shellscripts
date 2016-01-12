#!/usr/bin/python
import os
import netaddr
import sys
from pprint import pprint
import re
def findMappedCidrForCidr(cidrStr, cidrAsnMap):
  response = {}
  cidr = netaddr.IPNetwork(cidrStr)
  if cidr is None:
    print "error when convert cidr str to cidr for cidrStr {0}".format(cidrStr)
    #print cidrs
    response["code"] = -1
    return response
  cidrLen = cidr.prefixlen
  while cidr.prefixlen > 0:
    cidrStr = str(cidr.cidr)
    if cidrAsnMap.has_key(cidrStr):
      response['code'] = 0
      response['key']  = cidrStr
      return response
    else:
      cidr.prefixlen -= 1
      continue
  response['code'] = -1
  return response
def findMappedCidrForRange(startIp, endIp, cidrAsnMap):
  response = {}
  cidrs = netaddr.iprange_to_cidrs(startIp, endIp)
  if len(cidrs) > 1 or len(cidrs) < 1:
    #print "error when convert ip range to cidrs for start ip {0} and {1}".format(startIp, endIp)
    #print cidrs
    response["code"] = -1
    return response
  cidr = cidrs[0]
  cidrLen = cidr.prefixlen
  while cidr.prefixlen > 0:
    cidrStr = str(cidr.cidr)
    if cidrAsnMap.has_key(cidrStr):
      response['code'] = 0
      response['key']  = cidrStr
      return response
    else:
      cidr.prefixlen -= 1
      continue
  response['code'] = -1
  return response
def findAsnForInetnum(inetnumFile, asnMap, inetnumRe = None):
  if not os.path.exists(inetnumFile):
    print "inetnum file doesn't exist:{0}".format(inetnumFile)
    return -1
  inetnumFd = open(inetnumFile,"r")
  if inetnumRe is None:
    inetnumRe = re.compile("^inet?num:[ \t]+([^ \t\n-]+)[ \t-]+([^ \t\n-]+)")
  splitRe = re.compile("[ \t-]+")
  lineNum = 0
  for line in inetnumFd:
    lineNum += 1
    if lineNum % 10000 == 0:
      print "current line number is {0}".format(lineNum)
      sys.exit(1)
    matchObj = inetnumRe.match(line)
    if matchObj is None:
      continue
    else:
      startIp = matchObj.group(1)
      endIp   = matchObj.group(2)
      response = findMappedCidrForRange(startIp, endIp, asnMap)
      if response['code'] == 0:
        print startIp, endIp, response['key'], asnMap[response['key']]
def createCidrAsnMap(routeFile, mapDict, routeRe = None, originRe = None):
  if not os.path.exists(routeFile):
    print "route file doesn't exist:{0}".format(routeFile)
    return -1
  routeFileFd = open(routeFile, "r")
  if routeRe is None:
    routeRe = re.compile("^route6?:[ \t]+([^ \t\n]+)")
  if originRe is None:
    originRe = re.compile("^origin:[ \t]+([^ \t\n]+)")
  preCidr = None
  lineNum = 0
  for line in routeFileFd:
    lineNum += 1
    matchObj = routeRe.match(line)
    if matchObj:
      preCidr = matchObj.group(1)
      continue
    matchObj = originRe.match(line)
    if matchObj:
      if preCidr is None:
        print "no cidr before origin as for line {0}:{1}".format(lineNum, line)
        return -1
      mapDict[preCidr] = matchObj.group(1)
      preCidr = None
  print "finish {0} lines and get {1} maps for file {2}".format(lineNum, len(mapDict), routeFile)
  routeFileFd.close()
  return 0

if __name__ == "__main__":
  routeFile = sys.argv[1]
  inetnumFile = sys.argv[2]
  mapDict = {}
  createCidrAsnMap(routeFile, mapDict)
  mapkeys = mapDict.keys()
  findAsnForInetnum(inetnumFile, mapDict)
#  for key in mapDict:
#    print key, mapDict[key]

