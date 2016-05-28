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
#for lacnic
  bulkDir=/data/salrwais/BPH/Whois/bulkWhois/LACNIC/$date/
  apiDir=/data/salrwais/BPH/Whois/API/LACNIC/Data/$date/
  apiFile=/data/salrwais/BPH/Whois/API/LACNIC/Data/${date}.7z
  if [ -f $apiFile ] && [ ! -e $apiDir ];then
	echo "try to uncompress"
	$parentDir/uncompress.sh $date $date lacnic
  fi
  if [ ! -e "$bulkDir" ];then
	echo "$bulkDir doesn't exist"
    date=$(date -d "$date +1day" +"%Y%m%d")
	continue
  fi
  $currDir/convertLacnic2Uniform.py $bulkDir $apiDir $resultDir $configFile 
  $currDir/convLacnicOrg2Uniform.py $apiDir $resultDir $configFile
  echo "$currDir/preprocessLacnic.sh"
  $currDir/preprocessLacnic.sh $date $date
  $currDir/addAsn2InetnumForOneRegistry.sh $date $date lacnic

  rm -rf $tempDir
  if [ -f $apiFile ] && [  -e $apiDir ];then
	rm -r $apiDir
  fi
  date=$(date -d "$date +1day" +"%Y%m%d")
done
