#!/bin/bash
if [ $# -lt 2 ];then
  echo "usage startDate endDate"
  exit 1
fi

startDate=$1
endDate=$2
currDir=$(pwd)
sourceDir=/data/salrwais/BPH/Whois/API/RIPE/Data
scriptDir=/data/seclab/BPH/Xianghang/bulkData/Scripts

if [ $# -ge 3 ];then
  sourceDir=$3
fi
if [ $# -ge 4 ];then
  currDir=$4
fi
if [ $# -ge 5 ];then
  scriptDir=$5
fi
tempDir=$currDir/temp
mkdir -p $tempDir
date=$startDate
while [ $date -le $endDate ]
do
  sourceFile=$sourceDir/$date/person
  resultFile=$tempDir/person_$date
  $scriptDir/cleanRipe.py $sourceFile $resultFile
  mv $resultFile $sourceFile
  date=$(date -d "$date +1day" +"%Y%m%d")
done
