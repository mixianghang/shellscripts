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
parentDir=/data/seclab/BPH/Xianghang/bulkData/Scripts/
while [ $date -le $endDate ]
do
  tempDir=$currDir/temp
  mkdir -p $tempDir
  mkdir -p $resultBaseDir/$date
  resultDir=$resultBaseDir/$date

#for ripe
  sourceRipe=/data/salrwais/BPH/Whois/API/RIPE/Data/$date
  bulkRipe=/data/salrwais/BPH/Whois/bulkWhois/RIPE/$date
  if [ ! -e "$sourceRipe" ];then
	echo "$sourceRipe doesn't exist"
	((date++))
	continue
  fi
  #if [ ! -e "$bulkRipe" ];then
  #  echo "$bulkRipe doesn't exist"
  #  date=$(date -d "$date +1day" +"%Y%m%d")
  #  continue
  #fi
  #cp -r /data/salrwais/BPH/Whois/bulkWhois/RIPE/$date $tempDir/ripe
  #gzip -d $tempDir/ripe/*.gz
#run unformat script
  $currDir/convertRipe2Uniform.py $sourceRipe $resultDir $configFile  $tempDir/ripe
  $currDir/addAsn2InetnumForOneRegistry.sh $date $date ripe

  yesterday=$(date -d "$date -1day" +"%Y%m%d")
  echo "compress $yesterday"
  $parentDir/compress.sh $yesterday $yesterday "RIPE"
  rm -rf $tempDir
  date=$(date -d "$date +1day" +"%Y%m%d")
done
