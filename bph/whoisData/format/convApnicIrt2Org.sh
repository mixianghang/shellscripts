#!/bin/bash
uniformBaseDir=/data/seclab/BPH/Uniform/
formatScriptDir=/data/seclab/BPH/Xianghang/bulkData/Scripts/format
if [ $# -lt 2 ];then
  echo "Usage: startDate endDate"
  exit 1
fi
startDate=$1
endDate=$2
today=$startDate
while [ $today -le $endDate ]
do
  startSec=$(date +"%s")
  echo $today
  personFile=$uniformBaseDir/$today/person_apnic
  orgFile=$uniformBaseDir/$today/org_apnic
  if [ ! -e $personFile ];then
	echo "$personFile doesn't exist"
	exit 1
  fi
  if [ -e $orgFile ];then
	echo "$orgFile exists, remove it"
	rm $orgFile
  fi
  #select out  others types
  $formatScriptDir/convApnicIrt2Org.py $personFile $orgFile
  if [ $? -ne 0 ];then
	echo "conv irt 2 org  failed"
	exit 1
  fi
  endSec=$(date +"%s")
  echo "time cost for $today $yesterday is $(($endSec - $startSec))"
  today=$(date -d "$today +1day" +"%Y%m%d")
done
