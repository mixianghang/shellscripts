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
#generate changed key list and save into $keyDir


today=$startDate
cd $apiDataDir
while [ $today  -le $lastDate ]
do 
  startSec=$(date +"%s")
  echo $today
  newFile=$today/$objName
  compressedFile=${today}.7z
  if [ ! -e $compressedFile ];then
	echo "$compressedFile doesn't exist"
	exit 1
  fi
  7z u $compressedFile $newFile
  if [ $? -ne 0 ];then
	echo "update 7z file $compressedFile failed"
	exit 1
  fi
  endSec=$(date +"%s")
  compressedSize=$(wc -c <$compressedFile)
  if [ $compressedSize -le $sizeLimit ];then
	echo "the result size is below threshold"
	exit 1
  fi
  rm -r $today
  echo "size of result file is $compressedSize"
  echo "time cost for $today is $(($endSec - $startSec))"
  today=$(date -d "$today +1day" +"%Y%m%d")
done
