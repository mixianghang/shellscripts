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
dataDir=/data/salrwais/BPH/Whois/API/RIPE/Data
keyDir=/data/salrwais/BPH/Whois/API/RIPE/Keys
scriptDir=/data/seclab/BPH/Xianghang/bulkData/Scripts
option=0

if [[ $# -ge 2 ]]; then
    startDate=$1
	endDate=$2
fi

if [[ $# -ge 3 ]];then
  option=$3
fi
date=$startDate
yesterday=$(date -d "$date -1day" +"%Y%m%d")
while [ $date -le $endDate ]
do
  echo $yesterday $date
  if [ $option -eq 0 ];then
	echo "merge except operson"
	$scriptDir/mergeRipe.py $keyDir $dataDir $yesterday $date 0
  elif [ $option -eq 1 ];then
    echo "merge only person"
	$scriptDir/mergeRipe.py $keyDir $dataDir $yesterday $date 1
  elif [ $option -eq 2 ];then
    echo "merge all objects"
	$scriptDir/mergeRipe.py $keyDir $dataDir $yesterday $date 0
	$scriptDir/mergeRipe.py $keyDir $dataDir $yesterday $date 1
  fi
  yesterday=$date
  date=$(date -d "$date +1day" +"%Y%m%d")
done 
