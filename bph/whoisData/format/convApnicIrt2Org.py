#!/usr/bin/python
import os
import sys
import re
'''
this file is used to select out irt from person file and conv it into an org file
  arguments:
  personFilePath orgFilePath
'''
def convIrt2Org():
  personFilePath = sys.argv[1]
  orgFilePath = sys.argv[2]
  typeRe = re.compile("^irt\t", re.I)
  if not os.path.exists(personFilePath) or os.path.exists(orgFilePath):
    sys.stderr.write("{0} doesn't exist or {1} exists\n".format(personFilePath, orgFilePath))
    sys.exit(1)
  orgFd = open(orgFilePath, "w")
  sep = "\t"
  irtOrgMap={
    1:1,
    2:2,
    3:3,
    5:4,
    6:6,
    7:7,
    8:5,
    10:8,
    11:9,
    12:10,
    13:11,
    14:12,
    15:13,
    16:14,
    17:15,
    18:16,
    19:17,
    20:18,
    21:19,
    22:20
  }
  with open(personFilePath, "r") as personFd:
    objNum = 0
    for line in  personFd:
      if typeRe.match(line) != None:
        line = line[:-1]
        irtAttrs = line.split("\t")
        if len(irtAttrs) != 20:
          sys.stderr.write("data validity error: {0}\n".format(line))
          sys.exit(1)
        orgList = []
        for i in range(1, 23):
          if i == 1:
            orgList.append("organisation")
          elif i in irtOrgMap:
            index = irtOrgMap[i]
            orgList.append(irtAttrs[index - 1])
          else:
            orgList.append("")
        orgFd.write("\t".join(orgList) + "\n")
        objNum += 1
    print "select out {0} objects of types irt".format(objNum)
    orgFd.close()
    if objNum <= 0:
      sys.exit(1)

if __name__ == "__main__":
  convIrt2Org()
