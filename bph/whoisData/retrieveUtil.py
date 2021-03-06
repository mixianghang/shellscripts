#!/usr/bin/python
################################################
#
#Filename: retrieveUtil.py
#
#@author: Xianghang Mi
#@email: mixianghang@outlook.com
#@description: ---
#Create: 2015-12-31 11:27:40
# Last Modified: 2016-01-06 17:02:57
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
import types
class RetrieveThread(threading.Thread):
  requestCount = 0
  partCount = 0
  errorIndicate = 0
  errorCount = 0
  partErrorCount = 0
  errorNumOf429 = 0
  def __init__(self, threadId, kwList, url, resultFile, session=None):
    threading.Thread.__init__(self)
    self.threadId = threadId
    self.kwList = kwList
    self.url = url
    self.resultFile = resultFile
    if not session is None:
        self.session = session
    else:
        self.session =  requests.Session()
  def run(self):
    session = self.session
    date = time.strftime("%Y-%m-%d-%H-%M-%S")
    #if os.path.exists(self.resultFile):
    #    try:
    #      os.rename(self.resultFile, self.resultFile + "_bak_" +date)
    #    except Exception as e:
    #      error("thread{1}:rename result file failed: {0}".format(self.resultFile, self.threadId))
    #      sys.exit(1)
    #  #open keylist file and loop to send http request and save response
    resultFileFd  = open(self.resultFile, "a")
    kwNum = len(self.kwList)
    startTime = time.time()
    index = 0
    while index < kwNum:
      if RetrieveThread.errorIndicate != 0:
        time.sleep(10)
        continue
      kw = self.kwList[index]
      kw = kw.strip(" \n\r\t")
      lookupResponse = ripeLookupThroughRequests(self.url, kw, session=session, format="xml")    
      code = int(lookupResponse['code'])
      body = lookupResponse['body']
      RetrieveThread.requestCount += 1
      RetrieveThread.partCount += 1
      if code != 0:
        RetrieveThread.errorCount += 1
        RetrieveThread.partErrorCount += 1
        if code == -1:
          error("thread{3}:request error for key {0}, requestUrl {1} with errorMsg {2}".format(kw, self.url, body, self.threadId))
        # ripe 429 request limit
        if code == -2:
            RetrieveThread.requestCount -= 1
            RetrieveThread.partCount -= 1
            RetrieveThread.errorIndicate = 1
            #error("thread{3}:request error for key {0}, requestUrl {1} with errorMsg {2}".format(kw, self.url, body, self.threadId))
            print "got 429 error code"
            if RetrieveThread.errorNumOf429 >= 100:
              error("got so many 429 errors, we may be blocked again, bad luck!!")
              sys.exit(1)
            time.sleep(30)
            RetrieveThread.errorNumOf429 += 1
            continue
            #while True:
            #    if RetrieveThread.errorIndicate != 0:
            #        time.sleep(30)
            #        continue
            #    else:
            #        break
            #continue# continue to request for this key
      else:
        resultFileFd.write(body)
        #convRes = convRipeLookupJson2Text(body)
        #if convRes['code'] == 0:
        #    resultFileFd.write(convRes['body'])
        #else:
        #    error("thread{3}:request error for key {0}, requestUrl {1} with errorMsg {2}".format(kw, self.requestUrl,convRes['body'], self.threadId))

      if index % 100 ==0:
        resultFileFd.flush()
      if index >= 100 and index % 100 == 0:
        curTime = time.time()
        print "thread{1}: finish {0} kws of {2}".format(index,self.threadId, kwNum)
        print "thread{1}: finish 100 requests within {0}seconds".format(curTime - startTime, self.threadId)
        startTime = curTime
      index += 1
    print "thread%d: finishing %d kws of %d" %(self.threadId, index + 1, kwNum)
    resultFileFd.flush()
    resultFileFd.close()
    
def error(errMsg):
  date = time.strftime("%Y-%m-%d-%H-%M-%S")
  sys.stderr.write("{0} at date {1}\n".format(errMsg, date))
def joinStr(*arglist):
  args = []
  for item in arglist:
      args.append(item)
  if len(args) >= 1:
      name = args[0]
      name = name + ":"
      if len(name) < 15:
          name = name + (15 - len(name)) * " "
      args[0] = name
  return "  ".join(args)
def convRipeLookupJson2Text(jsonData):
  response = {}
  lines = [""]
  decoded = json.loads(jsonData);
  object = decoded["objects"]["object"][0];
  if not isinstance(object, dict):
      response['code'] = -1
      response['body'] = "parse error"
      return response
  source = object['source'];
  primaryKey = joinStr("primary-key", object['primary-key']['attribute'][0]['name'], object['primary-key']['attribute'][0]['value'])
  lines.append(primaryKey)
  #lines.append(joinStr("link", object['link']['href']))
  attributes = object["attributes"]["attribute"]
  for attribute in attributes:
      name = attribute['name']
      value = attribute['value']
      type = attribute["referenced-type"] if "referenced-type" in attribute.keys() else ""
      comment = attribute['comment'] if "comment" in attribute.keys() else ""
      line = joinStr(name, value, type, comment)
      lines.append(line)
  lines.append("")
  response['code'] = 0
  response['body'] = "\n".join(lines)
  return response

def ripeLookupThroughRequests(requestUrl, key, session, format="json"):
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
    if httpResponse.status_code == 429:
      response["code"] = -2
      response["body"] = "return status codes that cannot be handled:{0}".format(httpResponse.status_code)
    elif httpResponse.status_code == 404:
      response["code"] = -3
      response["body"] = "return status codes that cannot be handled:{0}".format(httpResponse.status_code)
    elif httpResponse.status_code >= 400:
      response["code"] = -1
      response["body"] = "return status codes that cannot be handled:{0}".format(httpResponse.status_code)
    else:
      response['code'] = 0
      response['body'] = httpResponse.content
  return response
def ripeLookupThroughUrllib2(requestUrl, key, format="json"):
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
def ripeLookup(requestUrl, key, format="json"):
  #return ripeLookupThroughRequests(requestUrl, key, format="json")
  return ripeLookupThroughUrllib2(requestUrl, key, format="json")
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
      response = ripeLookupThroughUrllib2(url, kw)
      if index % 20 == 0:
        print "urllib finish ", index, "of ", num
    else:
      response = ripeLookupThroughRequests(url, kw)
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
      i = -1
      for i, l in enumerate(fileFd):
          pass
      return i + 1

def lacnicLookupThroughRequests(requestUrl, key, session):
  response = {}
  url = requestUrl+"/" + urllib.quote(key)
  #getValues= {"unfiltered":""}
  #getData = urllib.urlencode(getValues)
  #fullUrl = url + "?" + getData
  fullUrl = url
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
    response["body"] = "some unexpected error {0}".format(repr(e))
  else:
    #print httpResponse.status_code
    if httpResponse.status_code >= 400:
      response["code"] = -1
      response["body"] = "return status codes that cannot be handled:{0}".format(httpResponse.status_code)
    else:
      response['code'] = 0
      response['body'] = httpResponse.content
  return response
def initSession(session):
  if not isinstance(session, requests.Session):
      print "cannot init a object that is not a Session"
      return -1
  headers={
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
      "Upgrade-Insecure-Requests": 1,
      "UserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
      "Accept-Encoding": "gzip, deflate, sdch",
      "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4"
  }
  cookies={
      "cookies-accepted": "accepted"
  }
  session.headers.update(headers)
  session.cookies.update(cookies)
  return 0

#session = requests.Session()
#initSession(session)
#pprint(session.get("http://rdap.db.ripe.net/entity/GK617-RIPE?unfiltered"))

#print lineCount(sys.argv[1])
#sys.exit(0)
#session = requests.Session()
#if len(sys.argv) < 4:
#  print "Usage num kwlistFile isUrlLib"
#  sys.exit(1)
#main(sys.argv[1], sys.argv[2], sys.argv[3])

#pprint(response)
#decide data types
#list1 = [1,2,3,4]
#dict1 = {"nihao":2, "wohao":1} 
#str1 = "wohao"
#if isinstance(dict1, dict):
#    print "I am  a dict"
#if isinstance(list1, list):
#    print "i am a list"
#if isinstance(str1, str):
#    print "I am a str"
#if isinstance(list1, str):
#    print "I am a str"

#test str.join
#print "a".join(['12', "","", '13'])

#assign by reference
#str1 = 4*"23"
#list = [str1]
#str2 = list[0]
#str2 = str2 + "54"
#print str1
#if str1 is str2:
#    print "we are the same"

#test json2text
#url = "http://rest.db.ripe.net/ripe/person"
#key = "GK617-RIPE"
#session = requests.Session()
#response = ripeLookupThroughRequests(url, key, session)
#if response['code'] != 0:
#    print "reques error:", response['body']
#convRes = convRipeLookupJson2Text(response['body'])
#print convRes['body']

