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
  echo $date
  tempDir=$currDir/temp_formatApnic_$date
  mkdir -p $tempDir
  mkdir -p $resultBaseDir/$date
  resultDir=$resultBaseDir/$date


#for apnic
  if [ ! -e "/data/salrwais/BPH/Whois/bulkWhois/APNIC/$date" ];then
	echo "/data/salrwais/BPH/Whois/bulkWhois/APNIC/$date doesn't exist"
    date=$(date -d "$date +1day" +"%Y%m%d")
	continue
  fi
  cp -r /data/salrwais/BPH/Whois/bulkWhois/APNIC/$date $tempDir/apnic
  gzip -d $tempDir/apnic/split/*.gz
  rm $resultDir/*_apnic
#run unformat script
  $currDir/convertApnic2Uniform2_onetime.py $tempDir/apnic/split $resultDir $configFile

  rm -rf $tempDir
  date=$(date -d "$date +1day" +"%Y%m%d")
done
