#!/usr/bin/python
################################################
#
#Filename: localParse.py
#
#@author: Xianghang Mi
#@email: mixianghang@outlook.com
#@description: ---
#Create: 2015-12-12 20:53:38
# Last Modified: 2015-12-13 19:24:43
################################################
import sys
import os
from util import *

if len(sys.argv) < 4 :
  print "Usage: dataDir kwFile resultFile\n"
  sys.exit(1)
dataDir        = sys.argv[1] # dir for parse data
kwFileName     = sys.argv[2] # file for keywords, one each line
resultFileName = sys.argv[3] # file name for storing result
kwList = []
#read keywords into kwList
if not readKwFromFile (kwFileName, kwList):
  print "cannot open file %s" %(kwFileName)
  sys.exit(1)

print "successfully read kws"

#read subdirs of dataDir
subDirs = []
if not getSubdirs(dataDir, subDirs):
  print "get subdirs from %s failed" %(dataDir)
  sys.exit(1)
print "read %d subdirs" %(len(subDirs))

scannedCacheFile = 0
unexistCacheFile = 0
matchedCacheFile = 0
#read cache list, for every cacheitem, read the corresponding html or js file, match kwlist
for subdir in subDirs:
  print "start scan dir %s" %(subdir)
  scanned = 0
  unexist = 0
  matched = 0
  cacheDir = os.path.join(dataDir,subdir, "cache")
  cached = len(os.listdir(cacheDir))
  cacheList = open(os.path.join(dataDir,subdir, "cachelist.txt"))
  matchedList = []
  cacheDict = {}
  for cacheItem in cacheList:
	scanned += 1
	cacheItemParts = cacheItem.split("\t")
	if len(cacheItemParts) == 3 :
	  cacheItemParts[2] = cacheItemParts[2].strip('\n')#strip /n
	#print(cacheItemParts)
	cacheFilePath = os.path.join(cacheDir, cacheItemParts[2]);
	if cacheItemParts[2] in cacheDict:
	  cacheDict[cacheItemParts[2]] += 1
	else:
	  cacheDict[cacheItemParts[2]] = 1
	#print cacheFilePath
	if (not os.path.isfile(cacheFilePath)):
	  print "cache file %s not exist" %(cacheFilePath)
	  unexist += 1
	  continue
	maxSize = 1024 * 1024 * 10# maxFileSize is 10 MB
	if os.path.getsize(cacheFilePath) > maxSize:
	  print "cache file %s is too big" %(cacheFilePath)
	  continue
	cacheFile = open(cacheFilePath, "r")
	if cacheFile is None:
	  print "open cache file %s failed" %(cacheFilePath)
	  continue
	fileStr   = cacheFile.read()
	#print "read cacheFile of size %d\n:%s" %(len(fileStr), cacheFilePath)
	cacheFile.close()
	matchedKws = patternMatch(fileStr, kwList)
	if len(matchedKws) > 0:
	  print "get a matched file %s" %(cacheFilePath)
	  matched += 1
	  matchedKwStr = " ".join(matchedKws)
	  matchedStr = "%s	%s	%s	%s\n" %(cacheItemParts[0], cacheItemParts[1], cacheFilePath,matchedKwStr)
	  matchedList.append(matchedStr)
	continue
  for key in cacheDict:
	if cacheDict[key] > 1:
	  print "%s : %u" %(key, cacheDict[key])
  cacheList.close()
  scannedCacheFile += scanned
  unexistCacheFile += unexist
  matchedCacheFile += matched
  if len(matchedList) > 0:#output matched cache list
	resultFile = open(resultFileName, "a")
	if resultFile is None:
	  print "Error:open result file failed: %s" %(resultFileName)
	  sys.exit(1)
	for matchedItem in matchedList:
	  resultFile.write(matchedItem)
	resultFile.close()
  print "finish scanning %s with scanned %u unexist %u matched %u cached %u" %(subdir, scanned, unexist, matched, cached)
print "scan %u subdirs,  %u files, %u don't exist, %u match some keywords" %(len(subDirs), scannedCacheFile, unexistCacheFile, matchedCacheFile)

