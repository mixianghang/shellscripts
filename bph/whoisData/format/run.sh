#!/bin/bash
if [ $# -lt 4 ];then
  echo "Usage: resultDir configFile date currDir"
  exit 1
fi
resultDir=$1
configFile=$2
date=$3
currDir=$4
tempDir=$currDir/temp
mkdir -p $tempDir
mkdir -p $resultDir/$date
resultDir=$resultDir/$date

#for arin
#copy and unzip to temp
#unzip -x /data/salrwais/BPH/Whois/bulkWhois/ARIN/$date/arin.zip -d $tempDir/arin
#
##run unformat script
#$currDir/convertArin2Uniform.py $tempDir/arin $resultDir $configFile
#
##for apnic
#cp -r /data/salrwais/BPH/Whois/bulkWhois/APNIC/$date $tempDir/apnic
#gzip -d $tempDir/apnic/split/*
##run unformat script
#$currDir/convertApnic2Uniform2.py $tempDir/apnic/split $resultDir $configFile

#for ripe
sourceRipe=/data/salrwais/BPH/Whois/API/RIPE/Data/20160101
#run unformat script
$currDir/convertRipe2Uniform.py $sourceRipe $resultDir $configFile

rm -rf $tempDir
