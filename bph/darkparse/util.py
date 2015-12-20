#!/usr/bin/python
################################################
#
#Filename: util.py
#
#@author: Xianghang Mi
#@email: mixianghang@outlook.com
#@description: ---
#Create: 2015-12-12 21:48:40
# Last Modified: 2015-12-13 19:09:31
################################################
import os
import re
def readKwFromFile (kwFileName, kwList):
  kwFile = open(kwFileName, "r") 
  if kwFile is None:
	return False
  for line in kwFile:
	kwList.append(line[:-1])
  kwFile.close()
  return True

def getSubdirs (parentDir, subDirs) :
  if not os.path.isdir(parentDir):
	return False
  subs = os.listdir(parentDir)
  for name in subs:
	if os.path.isdir(os.path.join(parentDir, name)):
	  subDirs.append(name)
  return True

def patternMatch(sourceStr, kwList):
  matchedKw = []
  for kw in kwList:
	result = re.search(kw, sourceStr,re.I)
	if result != None:
	  matchedKw.append(kw)
  return matchedKw
