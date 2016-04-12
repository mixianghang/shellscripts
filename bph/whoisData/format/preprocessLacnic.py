#!/usr/bin/python
import os
import sys
import re

def main():
  if len(sys.argv) <= 2:
    print "Usage : sourceDir resultDir"
    sys.exit(1)
  sourceDir = sys.argv[1]
  resultDir = sys.argv[2]

  inetnumFilePath = os.path.join(sourceDir, "inetnum_lacnic")
  netOrgFilePath = os.path.join(sourceDir, "inetnum_org_lacnic")
  resultInetnumFilePath = os.path.join(resultDir, "inetnum_lacnic")
  if not os.path.exists(inetnumFilePath):
    print "{0} doesn't exist".format(inetnumFilePath)
    sys.exit(1)
  if not os.path.exists(netOrgFilePath):
    print "{0} doesn't exist".format(netOrgFilePath)
    sys.exit(1)
  if inetnumFilePath == resultInetnumFilePath:
    print "source and result files are the same, rename source file"
    os.rename(inetnumFilePath, inetnumFilePath + "_bak")
    inetnumFilePath += "_bak"
  netOrgMap = {}
  with open(netOrgFilePath, "r") as fd:
    for line in fd:
      line = line.strip(" \n\r\t")
      parts = line.split("\t")
      if len(parts) != 2:
        print " retrieve org net pair failed at line: {0}".format(line)
        sys.exit(1)
      netOrgMap[parts[0]] = parts[1]
  print "retrieve {0} net-org key pairs".format(len(netOrgMap))
  resultInetnumFd = open(resultInetnumFilePath, "w")
  with open(inetnumFilePath, "r") as fd:
    lineNum = 0
    mapped = 0
    for line in fd:
      lineNum += 1
      line = line[:-1]#strip /n
      if lineNum == 1:
        resultInetnumFd.write(line + "\n")
        continue
      attrs = line.split("\t")
      primaryKey = attrs[1]
      if netOrgMap.has_key(primaryKey):#add org primay key 
        attrs[8] =  netOrgMap[primaryKey]
        mapped += 1
      if attrs[2] != "" and attrs[2]:
        attrs[3] = attrs[2]
        attrs[2] = ""
      resultInetnumFd.write("\t".join(attrs) + "\n")
    print "finish {0} lines with {1} mapped".format(lineNum, mapped)
  resultInetnumFd.close()
if __name__ == "__main__":
  main()
