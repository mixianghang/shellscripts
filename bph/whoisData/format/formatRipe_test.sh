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
  startSec=$(date +"%s")
  echo $date
  tempDir=$currDir/temp_formatRipe_$(date +"%Y%m%d-%H%M%S")
  mkdir -p $tempDir
  mkdir -p $resultBaseDir/$date
  resultDir=$resultBaseDir/$date

#for ripe
  apiRipe=/data/salrwais/BPH/Whois/API/RIPE/Data/$date
  bulkRipe=/data/salrwais/BPH/Whois/bulkWhois/RIPE/$date
  if [ ! -e "$apiRipe" ];then
	if [ ! -e ${apiRipe}.7z ];then
	  echo "$apiRipe and ${apiRipe}.7z doesn't exist"
	  date=$(date -d "$date +1day" +"%Y%m%d")
	  continue
	else
	  echo "7z x -o$tempDir ${apiRipe}.7z $date/organisation"
	  7z x -o$tempDir ${apiRipe}.7z $date/organisation
	  sourceDir=$tempDir/$date
	fi
  else
	sourceDir=$apiRipe
  fi
  #if [ ! -e "$bulkRipe" ];then
  #  echo "$bulkRipe doesn't exist"
  #  date=$(date -d "$date +1day" +"%Y%m%d")
  #  continue
  #fi
  #cp -r /data/salrwais/BPH/Whois/bulkWhois/RIPE/$date $tempDir/ripe
  #gzip -d $tempDir/ripe/*.gz
#run unformat script
  #if [ -e $resultDir/org_ripe ];then
  #  echo "bak old org: $resultDir/org_ripe"
  #  mv $resultDir/org_ripe $resultDir/org_ripe_bak
  #fi
  if [ -e $resultDir/asn_ripe ];then
	rm $resultDir/asn_ripe
  fi
  $currDir/convertRipe2Uniform_test.py $sourceDir $resultDir $configFile  $tempDir
  #echo " $currDir/addAsn2InetnumForRipe.sh $date $date"
  #$currDir/addAsn2InetnumForRipe.sh $date $date

  rm -rf $tempDir
  endSec=$(date +"%s")
  echo "time cost is $(($endSec - $startSec))"
  date=$(date -d "$date +1day" +"%Y%m%d")
done
