#!/usr/bin/python
import os
import sys
import re
from pprint import pprint
class UniformChecker(object):
  ERROR = "Error"
  WARN = "Warn"
  INFO  = "Info"
  def __init__(self, uniformFile, registry, logFile):
    self.uniformFile = uniformFile
    self.registry    = registry.lower()
    self.logFile     = logFile
    self.sep = "|"
    self.logSep = ":"
    emailDomain ="[a-z0-9_-]+(?:\.[a-z0-9_-]+)*\.[a-z]+"
    emailName ="[a-z0-9_-]+(?:\.[a-z0-9_-]+)*"
    emailReStr =  "^({0}@{1})(\|{0}@{1})*$".format(emailName, emailDomain)
    self.emailRe = re.compile(emailReStr, re.I)
    self.oneEmailRe = re.compile("{0}@{1}".format(emailName, emailDomain), re.I)
    self.lenLimitMap = {
    }
    self.typeMap = {
    }
    self.typeList = ["ripe", "apnic", "afrinic", "arin", "lacnic"]
    self.emailPos = -1
    self.phonePos = -1
    self.fixNum = 0
  def checkAndFix(self):
    logFd = open(self.logFile, "a")
    if self.registry not in self.typeList:
      msg = "{0} is not a qualified registry type".format(self.registry) 
      logMsg = self.composeLog(self.ERROR, msg)
      logFd.write(logMsg + "\n")
      sys.stderr.write(logMsg + "\n")
    registry = self.registry

    #test number of objects, chec
    numObj =  0
    #print self.typeMap[registry]
    typeRe = re.compile(self.typeMap[registry], re.I)
    uniformBak = self.uniformFile + "_bak"
    os.rename(self.uniformFile, uniformBak)
    lineNum = 0
    uniformFd = open(self.uniformFile, "w")
    with open(uniformBak, "r") as uniformBakFd:
      for objLine in uniformBakFd:
        lineNum += 1
        attrs = objLine[:-1].split("\t")
        if typeRe.match(attrs[0]) is None:
          uniformFd.write(objLine)
          continue
        numObj += 1

        fixResult = self.fixLine(attrs)
        if fixResult != 1:
          errorMsg = "fix error when processing line {0}".format(lineNum)
          logMsg = self.composeLog(self.ERROR, errorMsg)
          logFd.write(logMsg + "\n")
          #sys.stderr.write(logMsg + "\n")

        #check required attributes: primary key , allHandles
        requiredResult = self.checkRequired(self.requiredMap, attrs)
        if len(requiredResult) != 0:
          errorMsg = "the required attrs:{1}:of line:{0}:don't exist:{2}".format(lineNum, self.sep.join(requiredResult), objLine[:-1])
          logMsg = self.composeLog(self.ERROR, errorMsg)
          #logFd.write(logMsg + "\n")
          sys.stderr.write(logMsg + "\n")

        #check format requirement
        formatResult = self.checkFormat(self.formatMap, attrs)
        if len(formatResult) != 0:
          errorMsg = "the attrs :{1}: of line :{0}: don't match format requirement:{2}".format(lineNum, self.sep.join(formatResult), objLine[:-1])
          logMsg = self.composeLog(self.ERROR, errorMsg)
          logFd.write(logMsg + "\n")
          #sys.stderr.write(logMsg + "\n")

        uniformFd.write("\t".join(attrs) + "\n")
    uniformFd.close()
    os.remove(uniformBak)
    if numObj < self.lenLimitMap[registry]:
      logMsg = "\t".join(["ERROR", "{0} only contains {1} objs which is less than the lower bound of {2}".format(self.uniformFile, numObj, self.lenLimitMap[registry])]) 
      logFd.write(logMsg + "\n")
      sys.stderr.write(logMsg + "\n")
    print "fix {0} objects".format(self.fixNum)
  def checkRequired(self, requiredMap, attrs):
    missedKeys = []
    for key in requiredMap:
      attrIds = requiredMap[key].split(self.sep)
      attrLen = 0
      for idStr in attrIds:
        id = int(idStr)
        attrLen += len(attrs[id])
      if attrLen == 0:
        missedKeys.append(key)
    return missedKeys
  def checkFormat(self, formatMap, attrs):
    unformattedList = []
    for key in formatMap:
      formatRe = formatMap[key][0]
      attrStr = formatMap[key][1]
      attrIds = attrStr.split(self.sep)
      for idStr in attrIds:
        id = int(idStr)
        if len(attrs[id]) != 0 and formatRe.match(attrs[id]) is None:
          unformattedList.append(key)
          break
    return unformattedList
  def composeLog(self, errorLevel, errorMsg):
    return self.logSep.join([errorLevel, errorMsg, self.uniformFile])
  def fixLine(self, attrs):
    isFixed = 0
    if self.emailPos >= 0:
      email = attrs[self.emailPos]
#concatenate parts of a phone number
    if self.phonePos >= 0:
      phoneStr = attrs[self.phonePos]
      phoneList = attrs[self.phonePos].split("|")
      phoneFormattedList = []
      for phone in phoneList:
        if len(phone) == 0:
          continue
        formattedPhone = self.phoneSubRe.sub("", phone)
        if len(formattedPhone) > 0:
          phoneFormattedList.append(self.phoneSubRe.sub("", phone))
      attrs[self.phonePos] = "|".join(phoneFormattedList)
      #print phone
      #print phoneParts
      #print phoneValidParts
      #sys.exit(1)
      if attrs[self.phonePos] != phoneStr:
        if isFixed == 0:
          self.fixNum += 1
          isFixed = 1
#fix problem such as "network@marketaxess.com&lt;mailto:network@marketaxess.com&gt;"
    #if self.registry == "ripe":
    #  if len(email) > 0 and self.emailRe.match(email) is None:
    #    emailList = self.oneEmailRe.findall(email)
    #    attrs[10] = "|".join(emailList)
    #    if self.emailRe.match(attrs[10]) is None:
    #      print "original email is {0}".format(email)
    #      print emailList
    #      return -1
    #    else:
    #      if isFixed == 0:
    #        self.fixNum += 1
    #        isFixed = 1
    return 1

class AsnChecker(UniformChecker):
  def __init__(self,uniformFile, registry, logFile):
    super(AsnChecker, self).__init__(uniformFile, registry, logFile)
    self.lenLimitMap = {
      "ripe" : 30000,
      "apnic" : 10000,
      "afrinic" : 1200,
      "arin" : 25000,
      "lacnic" : 5500
    }
    self.typeMap = {
      "ripe" : "^aut-num$",
      "apnic" : "^aut-num$",
      "afrinic" : "^aut-num$",
      "arin" : "^asn$",
      "lacnic" : "^aut-num$"
    }
    self.typeList = ["ripe", "apnic", "afrinic", "arin", "lacnic"]
    self.requiredMap = {
      "primary_key" : "1",
      "allHandles" : "9",
      "created|changed|last-modified" : "12|13|14"
    }
    if self.registry == "arin" or self.registry == "lacnic":
      del self.requiredMap["allHandles"]
    self.attrMap = {
      0: "type",
      1: "primary-key",
      2: "orgid",
      3: "asname",
      4: "asnumber",
      5: "tech-c",
      6: "abuse-c",
      7: "admin-c",
      8: "nochandle",
      9: "allhandles",
      10: "e-mail",
      11: "address",
      12: "created",
      13: "changed",
      14: "last-modified",
      15: "remarks",
      16: "descr",
      17: "source",
      18: "mnt-by"
    }
    self.emailPos = 10
    self.phonePos = -1
    #arin as num can be: 40305 - 40316
    self.asnRe = re.compile("^[0-9 -]+$", re.I)
    self.asnWithASRe = re.compile("^as([0-9 -]+)$", re.I)
    self.formatMap = {
      #"email":(self.emailRe, "10")#attri 10 should conform email format
    }
    self.fixNum = 0
  def fixLine(self, attrs):
    asnNum = attrs[4]
    email = attrs[10]
    isFixed = 0
    if self.asnRe.match(asnNum):
      pass
    else:
      matchObj = self.asnWithASRe.match(asnNum)
      if matchObj:
        attrs[4] = matchObj.group(1)
        if isFixed == 0:
          self.fixNum += 1
          isFixed = 1
      else:
        return -1 
    if self.registry == "arin":
      handleList = []
      for attr in attrs[5:9]:#tech abuse admin noc
        if len(attr) > 0:
          handleList.append(attr)
      if len(handleList) > 0:
        tempStr = "|".join(handleList)
        if tempStr != attrs[9]:
          attrs[9] = tempStr
          print attrs
          print "haha"
          if isFixed == 0:
            self.fixNum += 1
            isFixed = 1
          

#fix problem such as "network@marketaxess.com&lt;mailto:network@marketaxess.com&gt;"
#because ripe has so many email values that doesn't conform the email standard, cancel this fix
    #if self.registry == "ripe":
    #  if len(email) > 0 and self.emailRe.match(email) is None:
    #    emailList = self.oneEmailRe.findall(email)
    #    attrs[10] = "|".join(emailList)
    #    if self.emailRe.match(attrs[10]) is None:
    #      print "original email is {0}".format(email)
    #      print emailList
    #      return -1
    #    else:
    #      if isFixed == 0:
    #        self.fixNum += 1
    #        isFixed = 1
    return 1

class PersonChecker(UniformChecker):
  def __init__(self,uniformFile, registry, logFile):
    super(PersonChecker, self).__init__(uniformFile, registry, logFile)
    self.lenLimitMap = {
      "ripe" : 2150000,
      "apnic" : 440000,
      "afrinic" : 18000,
      "arin" : 609000,
      "lacnic" : 69000
    }
    self.typeMap = {
      "ripe" : "^(person|role|irt|mntner)$",
      "apnic" : "^(person|role|irt|mntner)$",
      "afrinic" : "^(mntner|person\/role)$",
      "arin" : "^person$",
      "lacnic" : "^person$"
    }
    self.typeList = ["ripe", "apnic", "afrinic", "arin", "lacnic"]
    self.requiredMap = {
      "primary_key" : "1",
      "created|changed|last-modified" : "16|17|18"
    }
    if self.registry == "lacnic":
      del self.requiredMap["created|changed|last-modified"]
    if self.registry == "afrinic":
      del self.requiredMap["created|changed|last-modified"]

#head -n 1 ../20160116/./person_arin  | awk -F"\t" '{for (i = 1; i <= NF; i++) {print i-1 "
#:" "\""$i"\"" ","}}'

    self.attrMap = {
      0:"type",
      1:"primary-key",
      2:"personname",
      3:"org",
      4:"admin-c",
      5:"tech-c",
      6:"abuse-c",
      7:"allhandles",
      8:"mnt-by",
      9:"address",
      10:"email",
      11:"fax-no",
      12:"phone",
      13:"country",
      14:"remarks",
      15:"descr",
      16:"created",
      17:"changed",
      18:"last-modified",
      19:"source"
    }
    self.phoneSplitRe = re.compile("[ -]+", re.I)
    self.phoneRe = re.compile("^\d+(\|\d+)*$", re.I)
    self.phoneSubRe = re.compile("[^0-9]+", re.I)
    self.formatMap = {
      #"email":(self.emailRe, "10"),#attri 10 should conform email format
      "phone":(self.phoneRe, "12")
    }
    self.fixNum = 0
    self.emailPos = 10
    self.phonePos = 12

class OrgChecker(UniformChecker):
  def __init__(self,uniformFile, registry, logFile):
    super(OrgChecker, self).__init__(uniformFile, registry, logFile)
    self.lenLimitMap = {
      "ripe" : 100000,
      "apnic" : 11400,
      "afrinic" : 1900,
      "arin" : 3075000,
      "lacnic" : 18800
    }
    self.typeMap = {
      "ripe" : "^(organisation)$",
      "apnic" : "^(organisation)$",
      "afrinic" : "^(organisation)$",
      "arin" : "^org$",
      "lacnic" : "^organisation$"
    }
    self.typeList = ["ripe", "apnic", "afrinic", "arin", "lacnic"]

    self.attrMap = {
      0:"type",
      1:"primary-key",
      2:"orgName",
      3:"orgType",
      4:"org",
      5:"tech-c",
      6:"abuse-c",
      7:"admin-c",
      8:"noHandle",
      9:"allhandles",
      10:"mnt-by",
      11:"address",
      12:"email",
      13:"fax-no",
      14:"phone",
      15:"country",
      16:"remarks",
      17:"descr",
      18:"created",
      19:"changed",
      20:"last-modified",
      21:"source"
    }
    self.requiredMap = {
      "primary_key" : "1",
      "created|changed|last-modified" : "18|19|20"
    }
    if self.registry == "lacnic":
      del self.requiredMap["created|changed|last-modified"]
    if self.registry == "afrinic":
      del self.requiredMap["created|changed|last-modified"]

#head -n 1 ../20160116/./person_arin  | awk -F"\t" '{for (i = 1; i <= NF; i++) {print i-1 "
#:" "\""$i"\"" ","}}'

    self.phoneSplitRe = re.compile("[ -]+", re.I)
    self.phoneRe = re.compile("^\d+(\|\d+)*$", re.I)
    self.phoneSubRe = re.compile("[^0-9]+", re.I)
    self.emailPos = 12
    self.phonePos = 14
    self.formatMap = {
      #"email":(self.emailRe, "12"),#attri 10 should conform email format
      "phone":(self.phoneRe, "14")
    }
    self.fixNum = 0

class InetnumChecker(UniformChecker):
  def __init__(self,uniformFile, registry, logFile):
    super(InetnumChecker, self).__init__(uniformFile, registry, logFile)
    self.lenLimitMap = {
      "afrinic" : 88000,
      "apnic" : 990000,
      "arin" : 2970000,
      "lacnic" : 350000,
      "ripe" : 4430000
    }
    self.typeMap = {
      "ripe" : "^(inet[6]*num)$",
      "apnic" : "^(inet[6]*num)$",
      "afrinic" : "^(inet[6]*num)$",
      "arin" : "^inet[6]*num$",
      "lacnic" : "^inet[6]*num$"
    }
    self.typeList = ["ripe", "apnic", "afrinic", "arin", "lacnic"]
#awk -F"\t" '{i = 0; while(i++ < NF){printf("%d:\"%s\",\n", i - 1, $i);}}'
    self.attrMap = {
      0:"type",
      1:"primary-key",
      2:"netrange",
      3:"netcidr",
      4:"netname",
      5:"status",
      6:"originas",
      7:"parent",
      8:"org",
      9:"admin-c",
      10:"tech-c",
      11:"abuse-c",
      12:"nochandle",
      13:"allhandles",
      14:"mnt-by",
      15:"e-mail",
      16:"country",
      17:"geoloc",
      18:"language",
      19:"create",
      20:"changed",
      21:"last-modified",
      22:"remarks",
      23:"descr",
      24:"source"
    }
    self.requiredMap = {
      "primary_key" : "1",
      "created|changed|last-modified" : "19|20|21"
    }
    if self.registry == "lacnic":
      del self.requiredMap["created|changed|last-modified"]
    if self.registry == "afrinic":
      del self.requiredMap["created|changed|last-modified"]

#head -n 1 ../20160116/./person_arin  | awk -F"\t" '{for (i = 1; i <= NF; i++) {print i-1 "
#:" "\""$i"\"" ","}}'

    self.phoneSplitRe = re.compile("[ -]+", re.I)
    self.phoneRe = re.compile("^\d+(\|\d+)*$", re.I)
    self.phoneSubRe = re.compile("[^0-9]+", re.I)
    self.emailPos = 15
    self.phonePos = -1
    self.formatMap = {
      #"email":(self.emailRe, "12"),#attri 10 should conform email format
      #"phone":(self.phoneRe, "14")
    }
    self.fixNum = 0
    
if __name__ == "__main__":
  if len(sys.argv) <= 4:
    print "Usage uniformFile type registry logFile"
    sys.exit(1)
  uniformFile = sys.argv[1]
  type = sys.argv[2].lower()
  registry = sys.argv[3]
  logFile = sys.argv[4]
  checker = None
  if type == "asn":
    checker = AsnChecker(uniformFile, registry, logFile)
  elif type == "person":
    checker = PersonChecker(uniformFile, registry, logFile)
  elif type == "org":
    checker = OrgChecker(uniformFile, registry, logFile)
  elif type == "inetnum":
    checker = InetnumChecker(uniformFile, registry, logFile)
  if checker is None:
    print "no matched checker for {0} type".format(type)
    sys.exit(1)
  checker.checkAndFix()

  
  
