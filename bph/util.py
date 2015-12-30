#!/usr/bin/python
def convertIP2Int(ipStr):
  ipParts = ipStr.split(".")
  if len(ipParts) != 4:
	return -1
  resultInt = (int(ipParts[0]) << 24) + (int(ipParts[1]) << 16) + (int(ipParts[2]) << 8) + (int(ipParts[3]))
  return resultInt
def convertIP2Str(ipInt):
  ipParts = [(ipInt >> 24) % 256, (ipInt >> 16) % 256, (ipInt >> 8) % 256, (ipInt) % 256]
  return "%d.%d.%d.%d" %(ipParts[0], ipParts[1], ipParts[2], ipParts[3])

    
