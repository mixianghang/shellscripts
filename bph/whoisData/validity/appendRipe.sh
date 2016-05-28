#!/bin/bash
#append missing objects and generate missing keys
uniformBaseDir=/data/seclab/BPH/Uniform/
missDirName=missed/ripe
apiKeyDir=/data/salrwais/BPH/Whois/API/RIPE/Keys
apiDataDir=/data/salrwais/BPH/Whois/API/RIPE/Data
scriptDir=/data/seclab/BPH/Xianghang/bulkData/Scripts/validity
if [ $# -lt 3 ];then
  echo "Usage: startDate endDate type"
  exit 1
fi
startDate=$1
endDate=$2
type=$3

today=$startDate
yesterday=$(date -d "$today -1day" +"%Y%m%d")
while [ $today -le $endDate ]
do
  startSec=$(date +"%s")
  echo $today $yesterday
  missDir=$uniformBaseDir/$today/missing/ripe
  dataDir=$uniformBaseDir/$today
  if [ ! -e $missDir ];then
	mkdir -p $missDir
  fi
  awk -F"\"" '{print $1}' $apiKeyDir/$today/${type}_kwlist_appended > $missDir/${type}_kwlist_appended
  awk -F"\"" '{print $1}' $apiKeyDir/$today/${type}_kwlist_deleted  > $missDir/${type}_kwlist_deleted
  awk -F"\"" '{print $1}' $apiKeyDir/$today/${type}_kwlist  > $missDir/${type}_kwlist
  exclusiveKwFile=$missDir/exclusive_$type
  missKwFile=$missDir/missing_$type
  kwFile=$missDir/${type}_kwlist
  cat $missDir/${type}_kwlist_appended $missDir/${type}_kwlist_deleted > $exclusiveKwFile
  oldDataPath=$uniformBaseDir/$yesterday/${type}_ripe
  newDataPath=$uniformBaseDir/$today/${type}_ripe
  $scriptDir/appendFromOld.py $type  $newDataPath $oldDataPath  $exclusiveKwFile $kwFile $missKwFile
  if [ $?  -ne 0 ];then
	echo "error for $today"
	exit 1
  fi
  endSec=$(date +"%s")
  echo "time cost for $today is $(($endSec - $startSec))"
  yesterday=$today
  today=$(date -d "$today +1day" +"%Y%m%d")
done
