#!/bin/bash
date=$(date +"%Y%m%d")
#if [[ $OSTYPE == "linux-gnu" ]]
#then
#    echo "niaho"
#    yesterday=$(date -d -1day +"%Y%m%d")
#elif [[ $OSTYPE == "darwin14" ]]
#then
#    yesterday=$(date -v-1d +"%Y%m%d")
#else
#    echo "This script cannot be run on this os type"
#    exit
#fi

startDate=$date
endDate=$date

if [[ $# -ge 2 ]]; then
    startDate=$1
	endDate=$2
fi

bulkDataDir="/data/salrwais/BPH/Whois/bulkWhois/LACNIC"
keysDir="/data/salrwais/BPH/Whois/API/LACNIC/Keys"
resultDataDir="/data/salrwais/BPH/Whois/API/LACNIC/Data"
scriptDir="/data/seclab/BPH/Xianghang/bulkData/Scripts/"
formatDir="/data/seclab/BPH/Xianghang/bulkData/Scripts/format"

#try to overwrite default configuration
if [[ $# -ge 3 ]]; then
  bulkDataDir=$3
fi

if [[ $# -ge 4 ]]; then
  keysDir=$4
fi

if [[ $# -ge 5 ]]; then
  resultDataDir=$5
fi

if [[ $# -ge 6 ]]; then
  scriptDir=$6
fi

date=$startDate
yesterday=$(date -d "$date -1day" +"%Y%m%d")
while [ $date -le $endDate ]
do
  echo $yesterday $date
  #generage key list
  echo "start to generate a key list of objects"
  echo "$scriptDir/genChangedKeysForLacnic.sh $bulkDataDir  $keysDir $date"
  $scriptDir/genChangedKeysForLacnic.sh $bulkDataDir  $yesterday $date $keysDir $scriptDir

  #run retrieve process
  rm -rf  $resultDataDir/latest/*
  echo "start to retrieve objects for the key list"
  if [ ! -e $scriptDir/log ]
  then
	mkdir $scriptDir/log
  fi
  logError=$scriptDir/log/logErrorForRetrieveLacnic_$date
  echo "$scriptDir/retrieveLacnic.py $scriptDir/appendLacnicConfig.cfg 2>$logError"
  $scriptDir/retrieveLacnic.py $scriptDir/appendLacnicConfig.cfg 2>$logError

  #copy result to current date file
  echo "copy to $resultDataDir/$date"
  mkdir -p $resultDataDir/$date
  cp -r $resultDataDir/latest/* $resultDataDir/$date 
  
  echo "try to uncompress"
  $scriptDir/uncompress.sh $yesterday $yesterday "LACNIC"
  echo "start to merge person data"
  echo "$scriptDir/mergeLacnic.py $keysDir $resultDataDir $yesterday $date"
  $scriptDir/mergeLacnic.py $keysDir $resultDataDir $yesterday $date

  #copy result from date dir to latest dir
  echo "copy to $resultDataDir/latest"
  cp -r $resultDataDir/$date/* $resultDataDir/latest

  #format into uniform way
  $formatDir/formatLacnic.sh $date $date

  echo "compress $yesterday"
  $scriptDir/compress.sh $yesterday $yesterday "LACNIC"

  yesterday=$date
  date=$(date -d "$date +1day" +"%Y%m%d")
done

