#!/bin/bash
sourceBaseDir=/data/seclab/BPH/Uniform/
currDir=/data/seclab/BPH/Xianghang/bulkData/Scripts/format/
startDate=$(date +"%Y%m%d")
endDate=$(date +"%Y%m%d")
if [ $# -ge 2 ];then
  startDate=$1
  endDate=$2
fi
if [ $# -ge 4 ];then
  startDate=$1
  endDate=$2
  sourceBaseDir=$3
  currDir=$4
fi
date=$startDate
while [ $date -le $endDate ]
do
  tempDir=$currDir/temp_preprocessLacnic_$(date +"%Y%m%d-%H%M%S")
  mkdir -p $tempDir
  sourceDir=$sourceBaseDir/$date

  echo "$currDir/preprocessLacnic.py $sourceDir $tempDir"
  $currDir/preprocessLacnic.py $sourceDir $tempDir
  if [ $? -ne 0 ];then
	echo "failed to run $currDir/preprocessLacnic.py $sourceDir $tempDir"
	rm -rf $tempDir
	date=$(date -d "$date +1day" +"%Y%m%d")
	continue
  fi
  cp $tempDir/* $sourceDir/
  rm -rf $tempDir
  date=$(date -d "$date +1day" +"%Y%m%d")
done
