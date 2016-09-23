#!/bin/bash
checkError() {
  if [ $? -ne 0 ];then
	echo "error when $1"
	exit 1
  fi
}
getOtherTypes() {
  #generage changed key list
  #echo "start to generate a key list of changed objects"
  #echo "$scriptDir/genChangedKeysForRipe.sh $bulkDataDir $yesterday $date $keysDir"
  #$scriptDir/genChangedKeysForRipe.sh $bulkDataDir $yesterday $date $keysDir $scriptDir
  #run retrieve process
  #rm -rf  $resultDataDir/latest/*
  echo "start to retrieve objects for the key list"
  if [ ! -e $scriptDir/log ]
  then
	mkdir $scriptDir/log
  fi
  logError=$scriptDir/log/logErrorForAppendRipe_$date
  appendConfig=$scriptDir/appendRipeConfig_olddates.cfg
  sed "s/latest/$date/g" $scriptDir/appendConfig.cfg >$appendConfig
  echo "retrieve objects except for person"
  $scriptDir/retrieveRipe.py $appendConfig  2>$logError
  checkError "retrieve objects except for person"


  #copy result to current date file
  #echo "copy appended objects to $resultDataDir/$date"
  #mkdir -p $resultDataDir/$date
  #cp -r $resultDataDir/latest/* $resultDataDir/$date 

  #merge data for other objects
  echo "merge objects for $date except for person"
  $scriptDir/mergeRipe.py $keysDir $resultDataDir $yesterday $date 0
  checkError "merge all objects except for person for $date"

  #echo "copy merged objects to $resultDataDir/latest"
  #cp -r $resultDataDir/$date/* $resultDataDir/latest 

}
getPersonType() {
  #generate key list for person object
  echo "start to generate keylist for persons"
  $scriptDir/genPersonKeysForRipe.sh $resultDataDir $date $keysDir $scriptDir
  checkError "generate keys for person objects of $date"

  #retrieve appended person objects
  logError=$scriptDir/log/logErrorForAppendRipePerson_$date
  appendRipePersonConfig=$scriptDir/appendRipePersonConfig_olddates.cfg
  sed "s/latest/$date/g" $scriptDir/appendRipePersonConfig.cfg >$appendRipePersonConfig
  echo "append ripe person"
  #$scriptDir/retrieveRipeByTor.py $appendRipePersonConfig $blackList $usedList 2>$logError
  $scriptDir/retrieveRipe.py $appendRipePersonConfig $blackList $usedList 2>$logError
  checkError "generate keys for person objects of $date"

  #echo "copy appended person objects to $resultDataDir/date"
  #cp -r $resultDataDir/latest/person_appended $resultDataDir/$date

  #merge data for other objects
  echo "merge ripe person for $date"
  $scriptDir/mergeRipe.py $keysDir $resultDataDir $yesterday $date 1
  checkError "merge ripe person for $date"
}
date=$(date +"%Y%m%d")
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
blackList=$scriptDir/blackList
usedList=$scriptDir/usedList
if [ -e $blackList ];then
  rm $blackList $usedList
fi
touch $blackList
touch $usedList
while [ $date -le $endDate ]
do
  echo $yesterday $date
  startSec=$(date +"%s")

  getOtherTypes
  checkError "get other type"

  getPersonType
  checkError "get person type"

  $scriptDir/format/formatRipe.sh $date $date
  checkError "format ripe"

  endSec=$(date +"%s")
  echo "time cost for $date is $(($endSec - $startSec))"
  yesterday=$date
  date=$(date -d "$date +1day" +"%Y%m%d")
done

