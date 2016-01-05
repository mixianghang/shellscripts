#!/usr/bin/python
import os
import sys
import time
if len(sys.argv) < 4:
    print "Usage : sourceFile unitLineNum resultDir"
    sys.exit(1)
else:
    sourceFile = sys.argv[1]
    unit = int(sys.argv[2])
    resultDir = sys.argv[3]
date = time.strftime("%Y-%m-%d-%H-%M")
if not os.path.exists(resultDir):
    #os.rename(resultDir, resultDir + "_bak_" + date)
    os.makedirs(resultDir)
if not os.path.exists(sourceFile):
    print "source file doesn't exist"

fileFd = open(sourceFile, "r")
lines = fileFd.readlines()
lineNum = len(lines)
index = 0
sourceFileName = os.path.basename(sourceFile)
i = 0
while index < lineNum:
    i += 1
    if (index + unit) >= lineNum:
        partLines = lines[index:]
    else:
        partLines = lines[index:index+unit]
    partFileName = "_".join([sourceFileName, str(i), str(index + 1), str(index + unit)])
    partFile = open(os.path.join(resultDir, partFileName), "w")
    partFile.write("".join(partLines))
    partFile.close()
    index += len(partLines)
print "finish splitting the file into {0} parts".format(i)

    
