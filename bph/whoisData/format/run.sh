#!/bin/bash
resultDir=/data/seclab/BPH/Uniform/
configFile=/data/seclab/BPH/Xianghang/bulkData/Scripts/format/uniformFormat.cfg
currDir=/data/seclab/BPH/Xianghang/bulkData/Scripts/format/
date=$(date +"%Y%m%d")
if [ $# -ge 4 ];then
  resultDir=$1
  configFile=$2
  date=$3
  currDir=$4
fi
tempDir=$currDir/temp
mkdir -p $tempDir
mkdir -p $resultDir/$date
resultDir=$resultDir/$date

#for arin
#copy and unzip to temp
unzip -x /data/salrwais/BPH/Whois/bulkWhois/ARIN/$date/arin.zip -d $tempDir/arin

#run unformat script
$currDir/convertArin2Uniform.py $tempDir/arin $resultDir $configFile

#for apnic
cp -r /data/salrwais/BPH/Whois/bulkWhois/APNIC/$date $tempDir/apnic
gzip -d $tempDir/apnic/split/*
#run unformat script
$currDir/convertApnic2Uniform2.py $tempDir/apnic/split $resultDir $configFile

#for ripe
sourceRipe=/data/salrwais/BPH/Whois/API/RIPE/Data/20160101
bulkRipe=/data/salrwais/BPH/Whois/bulkWhois/RIPE/$date
cp -r /data/salrwais/BPH/Whois/bulkWhois/RIPE/$date $tempDir/ripe
gzip -d $tempDir/ripe/*
#run unformat script
$currDir/convertRipe2Uniform.py $sourceRipe $resultDir $configFile  $tempDir/ripe

#for afrinic
mkdir -p $tempDir/afrinic
bulkAfrinic=/data/salrwais/BPH/Whois/bulkWhois/AFRINIC/$date/afrinic.db.gz
apiDir=/data/salrwais/BPH/Whois/API/AFRINIC/Data/$date/
cp $bulkAfrinic $tempDir/afrinic/
gzip -d $tempDir/afrinic/*
$currDir/convertAfrinic2Uniform.py $tempDir/afrinic/ $apiDir $resultDir $configFile 

#for lacnic
bulkDir=/data/salrwais/BPH/Whois/bulkWhois/LACNIC/$date/
apiDir=/data/salrwais/BPH/Whois/API/LACNIC/Data/$date/
$currDir/convertLacnic2Uniform.py $bulkDir $apiDir $resultDir $configFile 



rm -rf $tempDir
