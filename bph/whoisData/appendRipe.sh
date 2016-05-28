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

echo $startDate $endDate
bulkDataDir="/data/salrwais/BPH/Whois/bulkWhois/RIPE"
keysDir="/data/salrwais/BPH/Whois/API/RIPE/Keys"
resultDataDir="/data/salrwais/BPH/Whois/API/RIPE/Data"
scriptDir="/data/seclab/BPH/Xianghang/bulkData/Scripts/"

date=$startDate
yesterday=$(date -d "$date -1day" +"%Y%m%d")
while [ $date -le $endDate ]
do
  echo $yesterday $date
  #generage changed key list
  echo "start to generate a key list of changed objects"
  echo "$scriptDir/genChangedKeysForRipe.sh $bulkDataDir $yesterday $date $keysDir"
  $scriptDir/genChangedKeysForRipe.sh $bulkDataDir $yesterday $date $keysDir $scriptDir

  #run retrieve process
  rm -rf  $resultDataDir/latest/*
  echo "start to retrieve objects for the key list"
  if [ ! -e $scriptDir/log ]
  then
	mkdir $scriptDir/log
  fi
  logError=$scriptDir/log/logErrorForAppendRipe_$date
  echo "$scriptDir/retrieveRipe.py $scriptDir/appendConfig.cfg 2>$logError"
  $scriptDir/retrieveRipe.py $scriptDir/appendRipeConfig.cfg 2>$logError


  #copy result to current date file
  echo "copy appended objects to $resultDataDir/$date"
  mkdir -p $resultDataDir/$date
  cp -r $resultDataDir/latest/* $resultDataDir/$date 

  #merge data for other objects
  echo "$scriptDir/mergeRipe.py $keysDir $resultDataDir $yesterday $date 0"
  $scriptDir/mergeRipe.py $keysDir $resultDataDir $yesterday $date 0 2>$logError

  echo "copy merged objects to $resultDataDir/latest"
  cp -r $resultDataDir/$date/* $resultDataDir/latest 

  #generate key list for person object
  echo "start to generate keylist for persons"
  echo "$scriptDir/genPersonKeysForRipe.sh $resultDataDir $date $keysDir"
  $scriptDir/genPersonKeysForRipe.sh $resultDataDir $date $keysDir $scriptDir

  #retrieve appended person objects
  logError=$scriptDir/log/logErrorForAppendRipePerson_$date
  echo "$scriptDir/retrieveRipe.py $scriptDir/appendRipePersonConfig.cfg 2>$logError"
  $scriptDir/retrieveRipe.py $scriptDir/appendRipePersonConfig.cfg 2>$logError

  echo "copy appended person objects to $resultDataDir/date"
  cp -r $resultDataDir/latest/* $resultDataDir/$date

  #merge data for other objects
  echo "$scriptDir/mergeRipe.py $keysDir $resultDataDir $yesterday $date "
  $scriptDir/mergeRipe.py $keysDir $resultDataDir $yesterday $date 1 2>$logError

  #copy result to current date file
  echo "copy to $resultDataDir/latest"
  cp -r $resultDataDir/$date/* $resultDataDir/latest 

  yesterday=$date
  date=$(date -d "$date +1day" +"%Y%m%d")
done

