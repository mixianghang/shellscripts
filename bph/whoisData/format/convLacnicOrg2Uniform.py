#!/usr/bin/python
import os
import sys
from ConfigParser import SafeConfigParser
import re
import json
from pprint import pprint

reload(sys)  
sys.setdefaultencoding('utf8')

def parseEntities(entities, resultDict):
  handles = []
  for entity in entities:
    if entity.has_key("handle"):
      handles.append(entity["handle"])
  handleValue = "|".join(handles)
  if resultDict.has_key("handles"):
    resultDict["handles"] = "|".join([resultDict["handles"], handleValue])
  else:
    resultDict["handles"] = handleValue
  return 0
def parseVcardArray(vcardsArray, resultDict):
  if vcardsArray is None or not isinstance(vcardsArray, list):
    return -1
  vcards = vcardsArray[1]
  phoneRe = re.compile("tel:(.*)")
  phoneList = []
  emailList = []
  addressList = []
  nameList = []
  kindList = []
  for vcard in vcards:
    type = vcard[0]
    value = vcard[3]
    if type == "tel":#lacnic tel value is text rather than url in afrinic
      #matchObj = phoneRe.match(value)
      #if matchObj is None:
      #  print "error when parse phone from {0}".format(value)
      #  return -1
      phoneList.append(value)
    elif type == "email":
      emailList.append(value)
    elif type == "adr":
      for i in range(0, len(value)):
        if value[i] is None:
          value[i] = ""
      if isinstance(value, list):
        addressList.append(" ".join(value)) 
    elif type == "fn":
      nameList.append(value)
    elif type == "kind":
      kindList.append(value)
      
  keysDict = {"address":addressList, "email":emailList, "phone":phoneList, "name":nameList, "kind":kindList}
  stripRe = re.compile("[\r\n\t]+")
  for key in keysDict:
    value = "|".join(keysDict[key])
    if resultDict.has_key(key):
      resultDict[key] = "|".join([resultDict[key], value])
    else:
      resultDict[key] = value
    resultDict[key] = stripRe.sub(" ", resultDict[key])
  return 0
def crossMatch(resultDict, configMap):
  keys = resultDict.keys()
  #choose result
  resultList = []
  for key,option in configMap:
    subOptions = option.split("|")
    subList = []
    for subOption in subOptions:
      if subOption in keys:
        subList.append(resultDict[subOption].strip(" \n\r\t"))
      else:
        continue
    if len(subList) > 0:
      resultList.append("|".join(subList).strip(" \n\r\t"))
    else:
      resultList.append("")
  return (1, resultList)
def getOrgInfo(jsonStrList):
  jsonStr = "".join(jsonStrList)
  jsonObj = None
  try:
    jsonObj = json.loads(jsonStr)
  except Exception as e:
    errorMsg = repr(e)
    return (-1, errorMsg)
  orgEntity = None
  if not jsonObj.has_key("entities"):#no org obj
    return (0,)
  entities = jsonObj["entities"]
#select out the org entity
  for entity in entities:
    roles = entity['roles']
    if len(roles) == 1 and roles[0] == "registrant":
      handle = entity['handle']
      if re.match("^[0-9a-z]+-[0-9a-z]+-[0-9a-z]+$", handle, re.I):
        orgEntity = entity
        break
      else:
        print "role match but key pattern doesn't: {0}".format(jsonStrList)
        break
  if orgEntity is  None:
    return (0,)
  inetnumKey = jsonObj['handle']
  orgKey     = orgEntity['handle']
  resultDict = {}
  resultDict['organisation'] = orgKey
  resultDict['type'] = "organisation"
  resultDict["source"] = "lacnic"
  if orgEntity.has_key("entities"):
    parseEntities(orgEntity['entities'], resultDict)
  if orgEntity.has_key("vcardArray"):
    parseVcardArray(orgEntity['vcardArray'], resultDict)
    if resultDict.has_key("kind") and resultDict["kind"] != "org":
      print "role match, key match, kind doesn't match: {0}".format(jsonStr)
      return (0,)
  if orgEntity.has_key("events"):
    for event in orgEntity["events"]:
      if event["eventAction"] == "last changed":
        resultDict["last-modified"] = event["eventDate"]
  return (1, resultDict, inetnumKey, orgKey)

  
def main():
  if len(sys.argv) < 4:
    print "Usage: sourceDir resultDir configFile"
    sys.exit(1)

  sourceDir = sys.argv[1]
  resultDir = sys.argv[2]
  configFile = sys.argv[3]
  inetnumFilePath = os.path.join(sourceDir, "inetnum")
  if not os.path.exists(inetnumFilePath):
    print "{0} doesn't exist".format(inetnumFilePath)
    sys.exit(1)

  orgFilePath = os.path.join(resultDir, "org_lacnic")
  mapFilePath = os.path.join(resultDir, "inetnum_org_lacnic")
  orgFd = open(orgFilePath, "w")
  mapFd = open(mapFilePath, "w")

  onlyStartRe = re.compile("^{\n?$", re.I)
  endStartRe = re.compile("^}{\n?$", re.I)
  onlyEndRe = re.compile("^}\n?$", re.I)

  configParser = SafeConfigParser()
  configParser.read(configFile)
  orgConfig = configParser.items("org")
  keys= []
  for key, option in orgConfig:
    keys.append(key)
  orgFd.write("\t".join(keys) + "\n")

  netOrgMap = {}
  orgKeys = {}
  currObj = None
  currJsonList = []

  orgNum = 0
  objNum = 0
  lineNum = 0
  orgObjNum = 0
  with open(inetnumFilePath, "r") as fd:
    for line in fd:
      lineNum += 1
      if currObj:#current in a json object
        isEnd = False
        isStart = False
        if endStartRe.match(line):#match }{, got a complete  json object
          isEnd = True
          isStart = True
        elif onlyEndRe.match(line):
          isEnd = True
        else:
          currJsonList.append(line)
          continue
        if isEnd:
          currJsonList.append("}")
          objNum += 1
          if objNum % 10000 == 0:
            print "process {0} objects and {1} of them have org".format(objNum, orgNum)
          response = getOrgInfo(currJsonList)
          if response[0] == 1:
            orgNum += 1
            resultDict = response[1]
            netKey = response[2]
            orgKey = response[3]
            if not orgKeys.has_key(orgKey):
              resultDict['type'] = "organisation"
              tempResp = crossMatch(resultDict, orgConfig)
              if tempResp[0] == 1:
                resultList =  tempResp[1]
                orgFd.write("\t".join(resultList) + "\n")
                orgKeys[orgKey] = 1
                orgObjNum += 1
            netOrgMap[response[2]] = response[3]
          else:
            print "{0}".format(currJsonList)
          currObj = None
          currJsonList = []
        if isStart:
          currJsonList = ["{"]
          currObj = 1
          continue
      else:
        if onlyStartRe.match(line):
          currObj = 1
          currJsonList.append("{")
        else:
          print "error process line at {0}: {1}".format(lineNum, line)
          sys.exit(1)

  for netKey in netOrgMap:
    mapFd.write("\t".join([netKey, netOrgMap[netKey]]) + "\n")
  print "finish processing {0} objects and {1} of them have org".format(objNum, orgNum)
  print "find out {0} org objects".format(orgObjNum)
  orgFd.close()
  mapFd.close()

if __name__ == "__main__":
  main()

