#!/bin/bash
resultBaseDir=/data/seclab/BPH/Uniform/
apiDataBaseDir=/data/salrwais/BPH/Whois/API/LACNIC/Data
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
cd $apiDataBaseDir
while [ $date -le $endDate ]
do
  startSec=$(date +"%s")
  tempDir=$currDir/temp
  mkdir -p $tempDir
  mkdir -p $resultBaseDir/$date
  resultDir=$resultBaseDir/$date
#for lacnic
  if [ -e $resultDir/person_lacnic ];then
	echo "$resultDir/person_lacnic exits, delete it"
	rm $resultDir/person_lacnic
  fi
  bulkDir=/data/salrwais/BPH/Whois/bulkWhois/LACNIC/20170101/
  if [ -e ${date}.7z ] && [ ! -e ${date} ];then
	7z x ${date}.7z ${date}/person
  fi
  if [ ! -e $date/person ];then
	echo "$date/person doesn't exist"
	exit 1
  fi
  $currDir/convertLacnic2Uniform_onetime.py $bulkDir $date $resultDir $configFile 
  if [ $? -ne 0 ];then
	echo "convert lacnic to uniform failed for $date"
	exit 1
  fi
  rm -rf $tempDir
  lineNum=$(wc -l <$resultDir/person_lacnic)
  if [ $lineNum -le 65000 ];then
	echo "result linenum is less than 65000: $lineNum"
	exit 1
  fi
  echo "result linenum is $lineNum"
  endSec=$(date +"%s")
  echo "time cost is $(($endSec - $startSec))"
  rm -r $date
  date=$(date -d "$date +1day" +"%Y%m%d")
done
