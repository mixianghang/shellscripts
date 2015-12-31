#!/usr/bin/python
import sys
import os
import ConfigParser
from pprint import pprint
import time
from retrieveUtil import error
from retrieveUtil import ripeLoopup

#time measurement example
start = time.clock()
#end = time.clock()
#print "time elapsed in seconds:", (end - start)
date=time.strftime("%Y%m%d")

if len(sys.argv) < 2:
  print >>sys.stderr, "Usage: py configFile" 
  sys.exit(1)
#read config file and get a list of configs
configFile=sys.argv[1]
if not os.path.exists(configFile):
  sys.stderr.write("config file doesn't exist: %s" %configFile)
  sys.exit(1)

configParser = ConfigParser.SafeConfigParser()
configParser.read(configFile)
sections = configParser.sections()
if sections is None:
  print >>sys.stderr, "no config items in config file: %s" % (configFile)
  sys.exit(1)
for section in sections:
  print section
  keyList = configParser.get(section, "keylistPath")
  startPosition = configParser.getint(section, "startPos")
  requestUrl = configParser.get(section, "requestUrl")
  resultFile = configParser.get(section,"resultFile")
  print "%s %s %s" %(keyList, requestUrl, resultFile)
  if not os.path.exists(keyList):
	error("keylist file doesn't exist:{0}".format(keyList))
	sys.exit(1)
  if os.path.exists(resultFile):
	try:
	  os.rename(resultFile, resultFile + "_bak_" +date)
	except exception as e:
	  error("rename result file failed: {0}".format(resultFile))
	  sys.exit(1)
  #open keylist file and loop to send http request and save response
  keyListFd = open(keyList, "r")
  resultFileFd  = open(resultFile, "a")
  if keyListFd is None or resultFileFd is None:
	error("open keylist or result file failed")
	sys.exit(1)
  index = 0;
  for kw in keyListFd:
	if index + 1 < startPosition:
	  continue
	kw = kw.strip(" \n\r\t")
	lookupResponse = ripeLoopup(requestUrl, kw)	
	code = int(lookupResponse['code'])
	body = lookupResponse['body']
	if code != 0:
	  error("request error for key {0}, requestUrl {1} with errorMsg {2}".format(kw, requestUrl, body))
	else:
	  resultFileFd.write(body)
	if index % 100 == 0:
	  resultFileFd.flush()
	index += 1
  print "finishing %d kws from %s" %(index, keyList)
#end = time.clock()
#print "time elapsed in seconds:", (end - start)
end = time.clock()
print "time elapsed in seconds:", (end - start)
#loop through configs, for each config, for each config, read key list, for each key, retrieve referenced object and save to file
