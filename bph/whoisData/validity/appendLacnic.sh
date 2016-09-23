#!/bin/bash
#append missing objects and generate missing keys for lacnic
uniformBaseDir=/data/seclab/BPH/Uniform/
missDirName=missed/lacnic
apiKeyDir=/data/salrwais/BPH/Whois/API/LACNIC/Keys
apiDataDir=/data/salrwais/BPH/Whois/API/LACNIC/Data
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
  missDir=$uniformBaseDir/$today/missing/lacnic
  dataDir=$uniformBaseDir/$today
  if [ ! -e $missDir ];then
	mkdir -p $missDir
  fi
  awk -F"\"|\t" '{print $1}' $apiKeyDir/$today/${type}_kwlist_appended > $missDir/${type}_kwlist_appended
  awk -F"\"|\t" '{print $1}' $apiKeyDir/$today/${type}_kwlist_deleted  > $missDir/${type}_kwlist_deleted
  awk -F"\"|\t" '{print $1}' $apiKeyDir/$today/${type}_kwlist  > $missDir/${type}_kwlist
  exclusiveKwFile=$missDir/${type}_kwlist_exclusive
  missKwFile=$missDir/${type}_kwlist_missing
  kwFile=$missDir/${type}_kwlist
  cat $missDir/${type}_kwlist_appended $missDir/${type}_kwlist_deleted > $exclusiveKwFile
  oldDataPath=$uniformBaseDir/$yesterday/${type}_lacnic
  newDataPath=$uniformBaseDir/$today/${type}_lacnic
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
