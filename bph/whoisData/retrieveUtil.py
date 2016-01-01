#!/usr/bin/python
################################################
#
#Filename: retrieveUtil.py
#
#@author: Xianghang Mi
#@email: mixianghang@outlook.com
#@description: ---
#Create: 2015-12-31 11:27:40
# Last Modified: 2016-01-01 01:00:44
################################################
import urllib2
import urllib
import json
from pprint import pprint
import sys
import os
import time
import requests
import threading
class RetrieveThread(threading.Thread):
  def __init__(self, threadId, kwList, url, resultFile):
    threading.Thread.__init__(self)
    self.threadId = threadId
    self.kwList = kwList
    self.url = url
    self.resultFile = resultFile
  def run(self):
    session = requests.Session()
    date = time.strftime("%Y-%m-%d-%H-%M-%S")
    if os.path.exists(self.resultFile):
        try:
          os.rename(self.resultFile, self.resultFile + "_bak_" +date)
        except Exception as e:
		  error("thread{1}:rename result file failed: {0}".format(self.resultFile, self.threadId))
		  sys.exit(1)
	  #open keylist file and loop to send http request and save response
    resultFileFd  = open(self.resultFile, "a")
    kwNum = len(self.kwList)
    startTime = time.time()
    for index, kw in enumerate(self.kwList):
      kw = kw.strip(" \n\r\t")
      lookupResponse = ripeLoopupThroughRequests(self.url, kw, session=session)	
      code = int(lookupResponse['code'])
      body = lookupResponse['body']
      if code != 0:
        error("thread{3}:request error for key {0}, requestUrl {1} with errorMsg {2}".format(kw, self.requestUrl, body, self.threadId))
      else:
        resultFileFd.write(body)
      if index % 100 ==0:
        resultFileFd.flush()
      if index >= 100 and index % 100 == 0:
        curTime = time.time()
        print "thread{1}: finish {0} kws of {2}".format(index,self.threadId, kwNum)
        print "thread{1}: finish 100 requests within {0}seconds".format(curTime - startTime, self.threadId)
        startTime = curTime
    print "thread%d: finishing %d kws of %d" %(self.threadId, index + 1, keyNum)
    resultFileFd.close()
    
def error(errMsg):
  sys.stderr.write("{}\n".format(errMsg))
def ripeLoopupThroughRequests(requestUrl, key, session, format="json"):
  response = {}
  if format == "json":
	url = requestUrl+"/" + urllib.quote(key) + ".json"
  elif format == "xml":
	url = requestUrl+"/" + urllib.quote(key)
  else:
	response["code"] = -1
	response["body"] = "'format' argument is wrong"
	return response
  getValues= {"unfiltered":""}
  getData = urllib.urlencode(getValues)
  fullUrl = url + "?" + getData
  try:
	#httpResponse = requests.get(url, params=getValues)
	httpResponse = session.get(fullUrl)
	#print httpResponse.url
  except urllib2.HTTPError as e:
    #print "http response error:{0}".format(e.code)
	response["code"] = -1
	response["body"] = "http response error:{0} for url {1}".format(e.code, fullUrl)
	#print "http error page: %s", (e.read())
  except urllib2.URLError as e:
    #print "failed to connect to server with reason:{0}".format(e.reason)
	response["code"] = -1
	response["body"] = "failed to connect to server {1} with reason:{0}".format(e.reason, fullUrl)
  except Exception as e:
    response["code"] = -1
    response["body"] = "some unexpected error"
  else:
	#print httpResponse.status_code
	if httpResponse.status_code >= 400:
	  response["code"] = -1
	  response["body"] = "return status codes that cannot be handled:{}".format(httpResponse.status_code)
	else:
	  response['code'] = 0
	  response['body'] = httpResponse.content
  return response
def ripeLoopupThroughUrllib2(requestUrl, key, format="json"):
  response = {}
  if format == "json":
	url = requestUrl+"/" + urllib.quote(key) + ".json"
  elif format == "xml":
	url = requestUrl+"/" + urllib.quote(key)
  else:
	response["code"] = -1
	response["body"] = "'format' argument is wrong"
	return response
  getValues= {"unfiltered":""}
  getData = urllib.urlencode(getValues)
  fullUrl = url + "?" + getData
  try:
	httpResponse = urllib2.urlopen(fullUrl)
  except urllib2.HTTPError as e:
    #print "http response error:{0}".format(e.code)
	response["code"] = -1
	response["body"] = "http response error:{0} for url {1}".format(e.code, fullUrl)
	#print "http error page: %s", (e.read())
  except urllib2.URLError as e:
    #print "failed to connect to server with reason:{0}".format(e.reason)
	response["code"] = -1
	response["body"] = "failed to connect to server {1} with reason:{0}".format(e.reason, fullUrl)
  else:
	#http request
	response['code'] = 0
	response['body'] = httpResponse.read()
  return response
def ripeLoopup(requestUrl, key, format="json"):
  #return ripeLoopupThroughRequests(requestUrl, key, format="json")
  return ripeLoopupThroughUrllib2(requestUrl, key, format="json")
def main(num, kwFile, isUrlLib):
  success = 0
  failed = 0
  startTime = time.time()
  url = "http://rest.db.ripe.net/ripe/inetnum"
  print "start at ", time.strftime("%H-%M-%S")
  print num, kwFile, isUrlLib
  kwFd = open(kwFile)
  index = 0
  responseSize = 0
  for kw in kwFd:
	kw = kw.strip(" \n\r\t")
	if isUrlLib == '1':
	  response = ripeLoopupThroughUrllib2(url, kw)
	  if index % 20 == 0:
		print "urllib finish ", index, "of ", num
	else:
	  response = ripeLoopupThroughRequests(url, kw)
	  if index % 20 == 0:
		print "requests finish ", index, "of ", num
	if response['code'] != 0:
	  failed += 1
	else:
	  success +=1
	  responseSize += len(response['body'])
	index += 1
	if index >= int(num):
	  break
	#pprint(decodedDict)
  print "end at ", time.strftime("%H-%M-%S")
  endTime = time.time()
  print "success: {0}, failed: {1}, timecost: {2}, responseSize: {3}".format(success, failed, endTime - startTime, responseSize)
  kwFd.close()

def lineCount(filePath):
  if not os.path.exists(filePath):
	  return -1
  with open(filePath) as fileFd:
      for i, l in enumerate(fileFd):
		  pass
      return i + 1

#print lineCount(sys.argv[1])
#sys.exit(0)
#session = requests.Session()
#if len(sys.argv) < 4:
#  print "Usage num kwlistFile isUrlLib"
#  sys.exit(1)
#main(sys.argv[1], sys.argv[2], sys.argv[3])

#pprint(response)

