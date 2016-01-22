#!/bin/bash
startDate=$(date +"%Y%m%d")
endDate=$startDate
baseDir="/data/salrwais/BPH/Whois/API/BGP/"
initDir=$
if [ $# -ge 2 ];then
  startDate=$1
  endDate=$2
fi
initDate=$startDate
date=$(date -d "$startDate +1day" +"%Y%m%d")
while [ $date -le $endDate ]
do
  echo $date
  if [ ! -e $baseDir/$initDate/ ];then
	echo "$baseDir/$initDate/ doesn't exist"
	exit 1
  fi
  if [ ! -e $baseDir/$date/ ];then
	echo "$baseDir/$date/ doesn't exist, create it"
	mkdir -p $baseDir/$date
  fi
  echo "cp $baseDir/$initDate/* $baseDir/$date/"
  cp $baseDir/$initDate/* $baseDir/$date/
  date=$(date -d "$date +1day" +"%Y%m%d")
done
