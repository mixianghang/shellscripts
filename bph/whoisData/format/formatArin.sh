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
  tempDir=$currDir/temp_formatArin_$(date +"%Y%m%d-%H%M%S")
  mkdir -p $tempDir
  mkdir -p $resultBaseDir/$date
  resultDir=$resultBaseDir/$date

#for arin
#copy and unzip to temp
  if [ ! -e "/data/salrwais/BPH/Whois/bulkWhois/ARIN/$date/arin.zip" ];then
	echo "/data/salrwais/BPH/Whois/bulkWhois/ARIN/$date/arin.zip doesn't exist"
    date=$(date -d "$date +1day" +"%Y%m%d")
	continue
  fi
  unzip -x /data/salrwais/BPH/Whois/bulkWhois/ARIN/$date/arin.zip -d $tempDir/arin
#run unformat script
  $currDir/convertArin2Uniform.py $tempDir/arin $resultDir $configFile
  $currDir/addAsn2InetnumForOneRegistry.sh $date $date arin

  rm -rf $tempDir
  date=$(date -d "$date +1day" +"%Y%m%d")
done
