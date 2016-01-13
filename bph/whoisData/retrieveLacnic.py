#!/usr/bin/python
import sys
import os
import ConfigParser
from pprint import pprint
import time
from retrieveUtil import *
import threading
from subprocess import call

#time measurement example
#start = time.clock()
#end = time.clock()
#print "time elapsed in seconds:", (end - start)
date=time.strftime("%Y-%m-%d-%H-%M-%S")

if len(sys.argv) < 2:
  print >>sys.stderr, "Usage: py configFile" 
  sys.exit(1)
#read config file and get a list of configs
configFile=sys.argv[1]
if not os.path.exists(configFile):
  sys.stderr.write("config file doesn't exist: %s" %configFile)
  sys.exit(1)

configParser = ConfigParser.SafeConfigParser({"startPos": 0, "threadNum": 10})
configParser.read(configFile)
sections = configParser.sections()
if sections is None:
  print >>sys.stderr, "no config items in config file: %s" % (configFile)
  sys.exit(1)
for section in sections:
  print section
  keyList = configParser.get(section, "keylistPath")
  startPos = configParser.getint(section, "startPos")
  requestUrl = configParser.get(section, "requestUrl")
  resultFile = configParser.get(section,"resultFile")
  numPerMinLimit  = configParser.getint(section,"numPerMinLimit")
  timeDelay  = configParser.getint(section,"timeDelay")
  minLenAlarm = configParser.getint(section,"lengthAlarm")
  session = requests.Session()
  date = time.strftime("%Y-%m-%d-%H-%M-%S")
  if os.path.exists(resultFile):
    try:
        print "path exists {0}".format(resultFile)
        os.rename(resultFile, resultFile + "_bak_" +date)
    except Exception as e:
        error("rename result file failed: {0}".format(resultFile))
        print "{0}nihao".format(repr(e))
        sys.exit(1)
  else:
      print "path doesn't exists {0}".format(resultFile)
      #open keylist file and loop to send http request and save response
  if not os.path.exists(os.path.dirname(resultFile)):
      os.makedirs(os.path.dirname(resultFile))
  resultFileFd  = open(resultFile, "a")
  if not os.path.exists(keyList):
    error("keylist file doesn't exist:{0}".format(keyList))
    sys.exit(1)
  #open keylist file and loop to send http request and save response
  keyListFd = open(keyList, "r")
  kwNum = lineCount(keyList)
  kwList = keyListFd.readlines()
  keyListFd.close()
  numPerMin = 0
  index = startPos
  startTime = time.time()
  retryTimes = 0
  print "kw num is {0}, numPerMin is {1}, lenAlarm is {2}".format(kwNum, numPerMinLimit, minLenAlarm)
  requestNum = 0
  failed = 0
  while index < kwNum:
      if numPerMin >= numPerMinLimit:#limit of lacnic rdap is
          print "sleep {0} before sending requests again".format(timeDelay)
          time.sleep(timeDelay)
          numPerMin = 0
      kw = kwList[index]
      kw = kw.strip(" \n\r\t")
      lookupResponse = lacnicLookupThroughRequests(requestUrl, kw, session=session)    
      code = int(lookupResponse['code'])
      body = lookupResponse['body']
      if code != 0:
          retryTimes += 1
          print("request error for key {0}, requestUrl {1} with error msg {2}\n".format(kw, requestUrl, body))
          if retryTimes >= 3:
              error("request error for key {0}, requestUrl {1} with error msg {2}\n".format(kw, requestUrl, body))
              failed += 1
              requestNum += 1
              index += 1
              retryTimes = 0
          numPerMin += 1
          continue
      elif len(body) <= minLenAlarm:
          retryTimes += 1
          print("request error for key {0}, requestUrl {1} with error msg {2}\n".format(kw, requestUrl, body))
          if retryTimes >= 3:
              error("response is too short for key {0}, requestUrl {1} with error msg {2}\n".format(kw, requestUrl, body))
              failed += 1
              requestNum += 1
              index += 1
              retryTimes = 0
          time.sleep(timeDelay)
          numPerMin = 0
          continue
      else:
          print "recv len {0} with requestNum: {1} and failed: {2}".format(len(body), requestNum, failed)
          requestNum += 1
          resultFileFd.write(body)
      if index % 100 ==0:
        resultFileFd.flush()
      if index >= 1000 and index % 1000 == 0:
        curTime = time.time()
        print "finish {0} kws of {1}".format(index, kwNum)
        print "finish 1000 requests within {0}seconds".format(curTime - startTime)
        startTime = curTime
      index += 1
      numPerMin += 1


#end = time.clock()
#print "time elapsed in seconds:", (end - start)
#end = time.clock()
#print "time elapsed in seconds:", (end - start)
#loop through configs, for each config, for each config, read key list, for each key, retrieve referenced object and save to file
