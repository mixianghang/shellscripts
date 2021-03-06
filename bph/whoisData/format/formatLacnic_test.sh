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
#for lacnic
  bulkDir=/data/salrwais/BPH/Whois/bulkWhois/LACNIC/20170101/
  apiDir=/data/salrwais/BPH/Whois/API/LACNIC/Data/$date/
  $currDir/convertLacnic2Uniform.py $bulkDir $apiDir $resultDir $configFile 

  rm -rf $tempDir
  date=$(date -d "$date +1day" +"%Y%m%d")
done
