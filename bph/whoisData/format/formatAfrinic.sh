#!/bin/bash
resultBaseDir=/data/seclab/BPH/Uniform/
configFile=/data/seclab/BPH/Xianghang/bulkData/Scripts/format/uniformFormat.cfg
currDir=/data/seclab/BPH/Xianghang/bulkData/Scripts/format/
startDate=$(date +"%Y%m%d")
endDate=$(date +"%Y%m%d")
if [ $# -ge 2 ];then
  startDate=$1
  endDate=$2
fi
if [ $# -ge 5 ];then
  startDate=$1
  endDate=$2
  resultBaseDir=$3
  configFile=$4
  currDir=$5
fi
date=$startDate
while [ $date -le $endDate ]
do
  tempDir=$currDir/temp
  mkdir -p $tempDir
  mkdir -p $resultBaseDir/$date
  resultDir=$resultBaseDir/$date


#for afrinic
  mkdir -p $tempDir/afrinic
  bulkAfrinic=/data/salrwais/BPH/Whois/bulkWhois/AFRINIC/$date/afrinic.db.gz
  apiDir=/data/salrwais/BPH/Whois/API/AFRINIC/Data/$date/
  if [ ! -e "$bulkAfrinic" ];then
	echo "$bulkAfrinic doesn't exist"
    date=$(date -d "$date +1day" +"%Y%m%d")
	continue
  fi
  if [ ! -e "$apiDir" ];then
	echo "$apiDir doesn't exist"
    date=$(date -d "$date +1day" +"%Y%m%d")
	continue
  fi
  cp $bulkAfrinic $tempDir/afrinic/
  gzip -d $tempDir/afrinic/*
  $currDir/convertAfrinic2Uniform.py $tempDir/afrinic/ $apiDir $resultDir $configFile 
  $currDir/addAsn2InetnumForOneRegistry.sh  $date $date afrinic
  rm -rf $tempDir
  date=$(date -d "$date +1day" +"%Y%m%d")
done
