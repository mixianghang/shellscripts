#!/usr/bin/python
################################################
#
#Filename: retrieveUtil.py
#
#@author: Xianghang Mi
#@email: mixianghang@outlook.com
#@description: ---
#Create: 2015-12-31 11:27:40
# Last Modified: 2015-12-31 21:05:45
################################################
import urllib2
import urllib
import json
from pprint import pprint
import sys
import time
import requests
def error(errMsg):
  sys.stderr.write(errMsg)
def ripeLoopupThroughRequests(requestUrl, key, format="json"):
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
  try:
	httpResponse = requests.get(url, params=getValues)
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
	#response["body"] = "some unexpected error"
  else:
	#print httpResponse.status_code
	if httpResponse.status_code >= 400:
	  response["code"] = -1
	  response["body"] = "return status codes that cannot be handled:{}".format(httpResponse.status_code)
	else:
	  response['code'] = 0
	  response['body'] = httpResponse.text
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

if len(sys.argv) < 4:
  print "Usage num kwlistFile isUrlLib"
  sys.exit(1)
main(sys.argv[1], sys.argv[2], sys.argv[3])

#pprint(response)

