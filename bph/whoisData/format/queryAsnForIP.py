#!/usr/bin/python
import os
import sys
import netaddr
from pprint import pprint
import re
import requests
import time
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
    print "error when convert ip range to cidrs for start ip {0} and {1}".format(startIp, endIp)
    print cidrs
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

def retrieveBgpMap(bgpFile, cidrAsnMap):
  if not os.path.exists(bgpFile):
    print "bgp file doesn't exist: {0}".format(bgpFile)
    return -1
#retrieve cidr asn mapping from bgpfile
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

def main():
  netStr = sys.argv[1]
  bgpFile = sys.argv[2]
  cidrAsnMap = {}
  retrieveBgpMap(bgpFile, cidrAsnMap)
  if len(cidrAsnMap) < 1:
    print "retrieve bgp table failed {0}".format(bgpFile)
    sys.exit(1)
  print "retrieve {0} bgp records".format(len(cidrAsnMap))
  netStr = netStr.stip(" \n\r\t")
  if "/" in netStr:
    response = findMappedCidrForCidr(netStr, cidrAsnMap)
  else:
    netRe = re.compile("^([0-9a-z:\.]+)[ \t]+-[ \t]+([0-9a-z:\.]+)", re.I)
    matchObj = netRe.match(netStr)
    if matchObj is None:
      print "parse ip range failed:{0}".format(netStr)
      sys.exit(1)
    else:
      startIP = matchObj.group(1)
      endIP  = matchObj.group(2)
      response = findMappedCidrForRange(startIP, endIP, cidrAsnMap)
    if response['code'] == 0:
      print "asn for {0} is {1}".format(netStr, cidrAsnMap[response['key']])
    else:
      print "parse error for {0}".format(netStr)
  
