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

startDate=$date
endDate=$date

if [[ $# -ge 2 ]]; then
    startDate=$1
	endDate=$2
fi

bulkDataDir="/data/salrwais/BPH/Whois/bulkWhois/AFRINIC"
keysDir="/data/seclab/BPH/Xianghang/bulkData/AFRINIC/Keys"
resultDataDir="/data/seclab/BPH/Xianghang/bulkData/AFRINIC/Data"
scriptDir="/data/seclab/BPH/Xianghang/bulkData/Scripts/"
apiDir="/data/salrwais/BPH/Whois/API/AFRINIC/Data"
date=$startDate
yesterday=$(date -d "$date -1day" +"%Y%m%d")
while [ $date -le $endDate ]
do
  echo $yesterday $date
  #generage key list
  echo "start to generate a key list of objects"
  echo "$scriptDir/genAppendedKwListForAfrinic.sh $bulkDataDir  $keysDir $date"
  $scriptDir/genAppendedKwListForAfrinic.sh $bulkDataDir  $keysDir $date $scriptDir

  #run retrieve process
  rm -rf  $resultDataDir/latest/*
  echo "start to retrieve objects for the key list"
  if [ ! -e $scriptDir/log_afrinic ]
  then
	mkdir $scriptDir/log_afrinic
  fi
  logError=$scriptDir/log_afrinic/logErrorForRetrieveAfrinic_$date
  echo "$scriptDir/retrieveRipe.py $scriptDir/afrinicPersonConfig.cfg 2>$logError"
  $scriptDir/retrieveRipe.py $scriptDir/afrinicPersonConfig.cfg 2>$logError

  #copy result to current date file
  echo "copy to $resultDataDir/$date"
  mkdir -p $resultDataDir/$date
  cp -r $resultDataDir/latest/* $resultDataDir/$date 
  if [ ! -e $apiDir/$date ];then
	if [ ! -e $apiDir/${date}.7z ];then
	  echo "$apiDir/$date dir or 7z file doesn't exist"
	  exit 1
	fi
	7z x -o$apiDir $apiDir/${date}.7z
  fi
  cat $resultDataDir/$date/person_role >> $apiDir/$date/person_role
  yesterday=$date
  date=$(date -d "$date +1day" +"%Y%m%d")
done

