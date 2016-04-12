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
dataDir=/data/salrwais/BPH/Whois/API/LACNIC/Data
keyDir=/data/salrwais/BPH/Whois/API/LACNIC/Keys
scriptDir=/data/seclab/BPH/Xianghang/bulkData/Scripts

if [[ $# -ge 2 ]]; then
    startDate=$1
	endDate=$2
fi

if [[ $# -ge 5 ]];then
  dataDir=$3
  keyDir=$4
  scriptDir=$5
fi
date=$startDate
yesterday=$(date -d "$date -1day" +"%Y%m%d")
while [ $date -le $endDate ]
do
  echo $yesterday $date $dataDir $keyDir $scriptDir
  $scriptDir/mergeLacnic_onetime.py $keyDir $dataDir $yesterday $date
  yesterday=$date
  date=$(date -d "$date +1day" +"%Y%m%d")
done 
