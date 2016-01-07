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
yesterday=$((date -1))

if [[ $# -ge 2 ]]; then
    startDate=$1
	endDate=$2
    yesterday=$((startDate - 1))
fi

bulkDataDir="/data/salrwais/BPH/Whois/bulkWhois/LACNIC"
keysDir="/data/salrwais/BPH/Whois/API/LACNIC/Keys"
resultDataDir="/data/salrwais/BPH/Whois/API/LACNIC/Data"
scriptDir="/data/seclab/BPH/Xianghang/bulkData/Scripts/"

date=$startDate
while [ $date -le $endDate ]
do
  echo $yesterday $date
  #generage key list
  echo "start to generate a key list of objects"
  echo "$scriptDir/genKwListForLacnic.sh $bulkDataDir  $keysDir $date"
  $scriptDir/genKwListForLacnic.sh $bulkDataDir  $keysDir $date $scriptDir

  #run retrieve process
  rm -rf  $resultDataDir/latest/*
  echo "start to retrieve objects for the key list"
  if [ ! -e $scriptDir/log ]
  then
	mkdir $scriptDir/log
  fi
  logError=$scriptDir/log/logErrorForRetrieveLacnic_$date
  echo "$scriptDir/retrieveLacnic.py $scriptDir/afrinicConfig.cfg 2>$logError"
  $scriptDir/retrieveLacnic.py $scriptDir/lacnicConfig.cfg 2>$logError

  #copy result to current date file
  echo "copy to $resultDataDir/$date"
  mkdir -p $resultDataDir/$date
  cp -r $resultDataDir/latest/* $resultDataDir/$date 
  ((date++))
  ((yesterday++))
done

