#!/bin/bash
date=$(date +"%Y%m%d")
if [[ $OSTYPE == "linux-gnu" ]]
then
    echo "niaho"
    yesterday=$(date -d -1day +"%Y%m%d")
elif [[ $OSTYPE == "darwin14" ]]
then
    yesterday=$(date -v-1d +"%Y%m%d")
else
    echo "This script cannot be run on this os type"
    exit
fi

if [[ $# -ge 1 ]]; then
    date=$1
    yesterday=$((date - 1))
fi

bulkDataDir="/data/salrwais/BPH/Whois/bulkWhois/RIPE"
keysDir="/data/salrwais/BPH/API/RIPE/Keys"
resultDataDir="/data/salrwais/BPH/API/RIPE/Data"
scriptDir=$(pwd)

#generage changed key list
echo "start to generate a key list of changed objects"
echo "$scriptDir/genChangedKeysForRipe.sh $bulkDataDir $yesterday $date $keysDir"
$scriptDir/genChangedKeysForRipe.sh $bulkDataDir $yesterday $date $keysDir

#run retrieve process
rm -rf  $resutlDataDir/latest/*
echo "start to retrieve objects for the key list"
if [ ! -e $scriptDir/log ]
then
  mkdir $scriptDir/log
fi
logError=$scriptDir/log/logErrorForAppendRipe_$date
echo "$scriptDir/retrieveRipe.py $scriptDir/appendConfig.cfg 2>$logError"
$scriptDir/retrieveRipe.py $scriptDir/appendConfig.cfg 2>$logError

#copy result to current date file
echo "copy to $resultDataDir/$date"
mkdir -p $resultDataDir/$date
cp -r $resultDataDir/latest/* $resultDataDir/$date 

#generate key list for person object
echo "start to generate keylist for persons"
echo "$scriptDir/genPersonKeysForRipe.sh $resultDataDir/$date $date $keysDir"
$scriptDir/genPersonKeysForRipe.sh $resultDataDir/$date $date $keysDir
