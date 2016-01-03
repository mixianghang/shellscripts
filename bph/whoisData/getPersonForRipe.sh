#!/bin/bash
date=$(date +"%Y%m%d")
resutlDataDir="/data/salrwais/BPH/API/RIPE/Data"
scriptDir=$(pwd)

#run retrieve process
echo "start to retrieve person objects for $date"
if [ ! -e $scriptDir/log ]
then
  mkdir $scriptDir/log
fi
logError=$scriptDir/log/logErrorForPersonRipe
echo "$scriptDir/retrieveRipe.py $scriptDir/personConfig.cfg 2>$logError"
$scriptDir/retrieveRipe.py $scriptDir/personConfig.cfg 2>$logError

#copy result to current date file
echo "copy to $resultDataDir and renameto person_$date"
cp  $resultDataDir/latest/person $resultDataDir/person_$date 
