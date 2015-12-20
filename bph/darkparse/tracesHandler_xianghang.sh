#!/bin/bash
# this shell script takes 2 parameters, date and compressedFileDir, extractFlag
# tracesLocation="seclab@seclab.soic.indiana.edu:/home/infraTracer/traces"
day=$1
cacheDir="cache/"
currDir=$(pwd)
echo "current dir is " $currDir
dataDir="${currDir}/${2}"
mkdir extracted_${day}
tracesLocation="${dataDir}/*linux*.7z"
for f in $tracesLocation
do
	echo "Working on"
	echo "$f"
	if [ "$3" -eq "1" ] #all
	then
	   echo "extract all files from $f"
	   7z x "$f" -y -o${currDir}/extracted_${day}/*  >&/dev/null
	elif [ "$3" -eq "2" ] # only cache
			then
		   7z x "$f" -y -o${currDir}/extracted_${day}/*  $cacheDir  >&/dev/null
			else
	   7z x "$f" -y -o${currDir}/extracted_${day}/* props.txt alltraces.txt listname.txt agent.txt torip.txt lastlocation.txt visitedlist.ini cachelist.txt >&/dev/null
			fi
	#7z x "$f" -y -o/data/seclab/BHP/traces/${day}_new/* props.txt alltraces.txt listname.txt agent.txt torip.txt lastlocation.txt visitedlist.ini cachelist.txt >&/dev/null
done
echo "done.."
