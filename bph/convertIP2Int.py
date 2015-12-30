#!/usr/bin/python
import sys
import util
import os
#parse and convert ips in delegated file`
delegatedFilePath = sys.argv[1]
if not os.path.isfile(delegatedFilePath):
  print "%s is not a valid file" %(delegatedFilePath)
  sys.exit(1)
delegatedFile = open(delegatedFilePath, "r")
if not delegatedFile:
  print "open file %s failed" %(delegatedFile)
  sys.exit(1)
previousStartIpInt = -1
previousEndIpInt = -1
previousStartIpStr = ""
previousEndIpStr = ""
delegatedResultPath = os.path.join(os.path.dirname(delegatedFilePath), "delegated_converted")
if os.path.exists(delegatedResultPath):
  os.remove(delegatedResultPath)
delegatedResult = open(delegatedResultPath, "a+")
ipv4Num = 0
for line in delegatedFile:
  if ":" in line:
	print "don't process IPv6 right now %s" %(line)
	break
  ipv4Num += 1
  lineParts = line.split(" ")
  if len(lineParts) != 2:
	print "line format is wrong %s" %(line)
	sys.exit(1)
  startIpInt = util.convertIP2Int(lineParts[0])
  if startIpInt == -1:
	print "convert IP failed %s" %(ipInt)
	sys.exit(1)
  endIpInt = startIpInt + int(lineParts[1])
  if startIpInt >= previousStartIpInt and endIpInt <= previousEndIpInt:
	continue
  if (startIpInt != previousEndIpInt):
	if previousEndIpInt != -1:
	  previousStartIpStr = util.convertIP2Str(previousStartIpInt)
	  previousEndIpStr   = util.convertIP2Str(previousEndIpInt)
	  delegatedResult.write("%s %s %s %s\n" %(previousStartIpInt, previousEndIpInt, previousStartIpStr, previousEndIpStr))
	previousEndIpInt = endIpInt
	previousStartIpInt = startIpInt
	continue
  else:
	previousEndIpInt = endIpInt
	continue
if (previousStartIpInt != -1):
  previousStartIpStr = util.convertIP2Str(previousStartIpInt)
  previousEndIpStr   = util.convertIP2Str(previousEndIpInt)
  delegatedResult.write("%s %s %s %s\n" %(previousStartIpInt, previousEndIpInt, previousStartIpStr, previousEndIpStr))
print "convert %d ipv4 numbers" %(ipv4Num)
delegatedResult.close()
delegatedFile.close()


#parse and convert IP in inetnum
inetnumFilePath   = sys.argv[2]
inet6numFilePath  = sys.argv[3]
if not os.path.isfile(inetnumFilePath):
  print "%s is not a valid file" %(inetnumFilePath)
  sys.exit(1)
inetnumFile = open(inetnumFilePath, "r")
if not inetnumFile:
  print "open file %s failed" %(inetnumFile)
  sys.exit(1)
previousStartIpInt = -1
previousEndIpInt = -1
previousStartIpStr = ""
previousEndIpStr = ""
inetnumResultPath = os.path.join(os.path.dirname(inetnumFilePath), "inetnum_converted")
if os.path.exists(inetnumResultPath):
  os.remove(inetnumResultPath)
inetnumResult = open(inetnumResultPath, "a+")
ipv4Num = 0
for line in inetnumFile:
  if ":" in line:
	print "don't process IPv6 right now %s" %(line)
	break
  ipv4Num += 1
  lineParts = line.split(" ")
  if len(lineParts) != 2:
	print "line format is wrong %s" %(line)
	sys.exit(1)
  startIpInt = util.convertIP2Int(lineParts[0])
  if startIpInt == -1:
	print "convert IP failed %s" %(ipInt)
	sys.exit(1)
  endIpInt = startIpInt + int(lineParts[1])
  if startIpInt >= previousStartIpInt and endIpInt <= previousEndIpInt:
	continue
  if (startIpInt != previousEndIpInt):
	if previousEndIpInt != -1:
	  previousStartIpStr = util.convertIP2Str(previousStartIpInt)
	  previousEndIpStr   = util.convertIP2Str(previousEndIpInt)
	  inetnumResult.write("%s %s %s %s\n" %(previousStartIpInt, previousEndIpInt, previousStartIpStr, previousEndIpStr))
	previousEndIpInt = endIpInt
	previousStartIpInt = startIpInt
	continue
  else:
	previousEndIpInt = endIpInt
	continue
if (previousStartIpInt != -1):
  previousStartIpStr = util.convertIP2Str(previousStartIpInt)
  previousEndIpStr   = util.convertIP2Str(previousEndIpInt)
  inetnumResult.write("%s %s %s %s\n" %(previousStartIpInt, previousEndIpInt, previousStartIpStr, previousEndIpStr))
print "convert %d ipv4 numbers" %(ipv4Num)
inetnumResult.close()
inetnumFile.close()
