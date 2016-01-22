#/bin/bash

if [ $# -lt 2  ];then
  echo "Usage: startDate endDate"
  exit 1
fi

startDate=$1
endDate=$2
initDate="20160101"
currDir=$(pwd)
tempDir=$currDir/temp_crossMatchForRipe_$(date +"%Y%m%d_%H%M%S")
bulkDataDir="/data/salrwais/BPH/Whois/bulkWhois/RIPE"
scriptDir="/data/seclab/BPH/Xianghang/bulkData/Scripts"
uniformDir="/data/seclab/BPH/Uniform"
mkdir -p $tempDir

date=$startDate
while [ $date -le $endDate -a $date -lt $initDate ]
do
#generate changed keys
  keyDir=$tempDir/keys
  mkdir -p $keyDir
  $scriptDir/genChangedKeysForRipe.sh $bulkDataDir $date $initDate $keyDir 
#crossMatch and replace
  $scriptDir/crossMatchForRipe.py $keyDir $uniformDir $date $initDate $tempDir/inetnum_ripe
  if [ $? -ne 0 ];then
	exit 1
  fi
  mv $tempDir/inetnum_ripe $uniformDir/$date/inetnum_ripe
  rm -rf $tempDir/*
  date=$(date -d "$date +1day" +"%Y%m%d") 
done
rm -rf $tempDir/
