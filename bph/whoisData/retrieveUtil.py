#!/usr/bin/python
################################################
#
#Filename: retrieveUtil.py
#
#@author: Xianghang Mi
#@email: mixianghang@outlook.com
#@description: ---
#Create: 2015-12-31 11:27:40
# Last Modified: 2015-12-31 20:31:58
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
def main(num):
  url = "http://rest.db.ripe.net/ripe/inetnum"
  key = "79.107.0.0 - 79.107.255.255"
  success = 0
  failed = 0
  startTime = time.time()
  print "start at ", time.strftime("%H-%M-%S")
  for i in range(0,int(num)):
    response = ripeLoopup(url, key)
    if response['code'] != 0:
        failed += 1
    else:
        success +=1
	#pprint(decodedDict)
  print "end at ", time.strftime("%H-%M-%S")
  endTime = time.time()
  print "success: {0}, failed: {1}, timecost: {2}".format(success, failed, endTime - startTime)
main(sys.argv[1])

#pprint(response)

