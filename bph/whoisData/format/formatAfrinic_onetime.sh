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
  tempDir=$currDir/temp_formatLacnic_$(date +"%Y%m%d-%H%M%S")
  mkdir -p $tempDir
  mkdir -p $resultBaseDir/$date
  resultDir=$resultBaseDir/$date


#for afrinic
  mkdir -p $tempDir/afrinic
  bulkAfrinic=/data/salrwais/BPH/Whois/bulkWhois/AFRINIC/$date/afrinic.db.gz
  apiDir=/data/salrwais/BPH/Whois/API/AFRINIC/Data/$date
  if [ ! -e "$bulkAfrinic" ];then
    echo "$bulkAfrinic doesn't exist"
    date=$(date -d "$date +1day" +"%Y%m%d")
    continue
  fi
  sourceDir=$apiDir
  if [ ! -e "$apiDir" ];then
    if [ ! -e ${apiDir}.7z ];then
      echo "$apiDir and ${apiDir}.7z doesn't exist"
      date=$(date -d "$date +1day" +"%Y%m%d")
      continue
    else
      7z x -o$tempDir ${apiDir}.7z
      sourceDir=$tempDir/$date
    fi
  else
    sourceDir=$apiDir
  fi
  cp $bulkAfrinic $tempDir/afrinic/
  gzip -d $tempDir/afrinic/*
  if [ -e $resultDir/person_afrinic ];then
    echo "rm old person data $resultDir/person_afrinic"
    rm $resultDir/person_afrinic
  fi
  $currDir/convertAfrinic2Uniform_onetime.py $tempDir/afrinic/ $sourceDir $resultDir $configFile 
  rm -rf $tempDir
  date=$(date -d "$date +1day" +"%Y%m%d")
done
