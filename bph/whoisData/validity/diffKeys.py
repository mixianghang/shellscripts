#!/usr/bin/python
import sys
import os
if __name__ == "__main__":
  if len(sys.argv) <= 3:
	print "Usage existKeysPath fullKeysPath missKeysPath"
	sys.exit(1)
  existKeysPath = sys.argv[1]
  fullKeysPath  = sys.argv[2]
  missKeysPath  = sys.argv[3]
  existKeyMap = {}
  with open(existKeysPath, "r") as existFd:
    for line in existFd:
	  key = line.strip().lower()
	  if len(key) == 0:
		continue
	  existKeyMap[key] = 1
  fullKeyMap = {}
  with open(fullKeysPath, "r") as fullFd:
    for line in fullFd:
	  key = line.strip().lower()
	  if len(key) == 0:
		continue
	  fullKeyMap[key] = 1
  
  missNum = 0
  with open(missKeysPath, "w") as missFd:
	for key in fullKeyMap:
	  if key in existKeyMap:
		continue
	  else:
		missNum += 1
		missFd.write(key + "\n")
  print "got {0} missing keys".format(missNum)

