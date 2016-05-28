#!/bin/bash
if [ $# -le 3 ];then
  echo "Usage: objName startDate endDate sizeLimit"
  exit 1
fi
objName=$1
startDate=$2
lastDate=$3
sizeLimit=$4
#aut-num:148000000
#person: 400000000

apiDataDir="/data/salrwais/BPH/Whois/API/RIPE/Data"
apiKeyDir="/data/salrwais/BPH/Whois/API/RIPE/Keys"
bulkDataDir="/data/salrwais/BPH/Whois/bulkWhois/RIPE"
scriptDir="/data/seclab/BPH/Xianghang/bulkData/Scripts"
tempDir=temp_$(date +"%H%M%S")
mkdir -p $tempDir
#generate changed key list and save into $keyDir


today=$startDate
yesterday=$(date -d "$startDate -1day" +"%Y%m%d")
while [ $today  -le $lastDate ]
do 
  startSec=$(date +"%s")
  echo $today $yesterday
  oldFile=$apiDataDir/$yesterday/$objName
  newAppendedFile=$apiDataDir/$today/${objName}_appended
  newFile=$apiDataDir/$today/$objName
  #uncompress old date file
  if [ ! -e $oldFile ];then
	7z x $apiDataDir/${yesterday}.7z -o$apiDataDir ${yesterday}/$objName
	if [ $? -ne 0 ];then
	  echo "uncompress old file failed: 7z x $apiDataDir/${yesterday}.7z -o$apiDataDir ${yesterday}/$objName"
	  exit 1
	fi
  fi
  if [ ! -e $newAppendedFile ];then
	7z x $apiDataDir/${today}.7z -o$apiDataDir ${today}/${objName}_appended 
	if [ $? -ne 0 ];then
	  echo "uncompress failed: 7z x $apiDataDir/${today}.7z -o$apiDataDir ${today}/${objName}_appended"
	  exit 1
	fi
  fi
  if [ -e $newFile ];then
	echo "$newFile exist before merging, rm it"
	rm $newFile
  fi
  #merge person obj
  $scriptDir/mergeRipe.py $apiKeyDir $apiDataDir $yesterday $today  3 $objName
  sizeOfNew=$(wc -c <$newFile)
  if [ $sizeOfNew -le $sizeLimit ];then
	echo "the result size is less than expectation: $newFile $sizeOfNew"
	exit 1
  fi
  endSec=$(date +"%s")
  echo "size of result file is $sizeOfNew"
  echo "time cost for $today $yesterday is $(($endSec - $startSec))"
  yesterday=$today
  today=$(date -d "$today +1day" +"%Y%m%d")
done
