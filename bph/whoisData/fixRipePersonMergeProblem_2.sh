#!/bin/bash
lastDate=20160520

apiDataDir="/data/salrwais/BPH/Whois/API/RIPE/Data"
sizeLimit=400000000
#generate changed key list and save into $keyDir


today=20160227
yesterday=20160226
cd $apiDataDir
while [ $today  -le $lastDate ]
do 
  startSec=$(date +"%s")
  echo $today
  personFile=$today/person
  compressedFile=${today}.7z
  if [ ! -e $compressedFile ];then
	echo "$compressedFile doesn't exist"
	exit 1
  fi
  7z u $compressedFile $personFile
  if [ $? -ne 0 ];then
	echo "update 7z file $compressedFile failed"
	exit 1
  fi
  rm $personFile
  compressedSize=$(wc -c <$compressedFile)
  if [ $compressedSize -le $sizeLimit ];then
	echo "the result size is below threshold"
	exit 1
  fi
  endSec=$(date +"%s")
  echo "time cost for $today is $(($endSec - $startSec))"
  yesterday=$today
  today=$(date -d "$today +1day" +"%Y%m%d")
done
