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
  threadNum  = configParser.getint(section,"threadNum")
  print "%s %s %s" %(keyList, requestUrl, resultFile)
  if not os.path.exists(keyList):
	error("keylist file doesn't exist:{0}".format(keyList))
	sys.exit(1)
  if os.path.exists(resultFile):
	try:
	  os.rename(resultFile, resultFile + "_bak_" +date)
	except Exception as e:
	  error("rename result file failed: {0}".format(resultFile))
	  sys.exit(1)
  if not os.path.exists(os.path.dirname(resultFile)):
      os.makedirs(os.path.dirname(resultFile))
  #open keylist file and loop to send http request and save response
  keyListFd = open(keyList, "r")
  kwNum = lineCount(keyList)
  kwPartNum = (kwNum - startPos) / threadNum if threadNum != 0 else (kwNum - startPos)
  kwList = keyListFd.readlines()
  keyListFd.close()
  threads = []
  partFiles = []
  for i in range(0, threadNum):
      partResultFile = "{0}_part{1}".format(resultFile, i + 1)
      partFiles.append(partResultFile)
      if (i + 1) != threadNum:
          newThread = RetrieveThread(i + 1, kwList[startPos : startPos + kwPartNum], requestUrl, partResultFile)
      else:
          newThread = RetrieveThread(i + 1, kwList[startPos:], requestUrl, partResultFile)
      newThread.start()
      threads.append(newThread)
      startPos += kwPartNum
  for thread in threads:
      thread.join()
  command = "cat {0} > {1}".format(" ".join(partFiles), resultFile)
  call(command, shell=True)
  for partFile in partFiles:
      os.remove(partFile)
#end = time.clock()
#print "time elapsed in seconds:", (end - start)
#end = time.clock()
#print "time elapsed in seconds:", (end - start)
#loop through configs, for each config, for each config, read key list, for each key, retrieve referenced object and save to file
