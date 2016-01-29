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
  7z x /data/salrwais/BPH/Whois/bulkWhois/ARIN/$date/arin.zip -o$tempDir/arin arin_db.txt
  if [ -e $resultDir/org_arin ];then
	mv $resultDir/org_arin  $resultDir/org_arin_bak
  fi
#run unformat script
  $currDir/convertArin2Uniform_onetime.py $tempDir/arin $resultDir $configFile
  if [ $? -ne 0 ];then
	mv $resultDir/org_arin_bak  $resultDir/org_arin
  else
	rm $resultDir/org_arin_bak
  fi

  rm -rf $tempDir
  date=$(date -d "$date +1day" +"%Y%m%d")
done
