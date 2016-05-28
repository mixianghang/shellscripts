#!/bin/bash
formatBaseDir=/data/seclab/BPH/Uniform/
bgpBaseDir=/data/salrwais/BPH/Whois/API/BGP/
currDir=/data/seclab/BPH/Xianghang/bulkData/Scripts/format/
scriptDir=/data/seclab/BPH/Xianghang/bulkData/Scripts/format/
if [ $# -ge 3 ];then
  startDate=$1
  endDate=$2
  registry=$3
else
  echo "Usage startDate endDate registry"
  exit 1
fi
tempBaseDir=$currDir/temp_addAsn2Inetnum_$(date +"%Y%m%d_%H%M%S")
date=$startDate
while [ $date -le $endDate ]
do
  tempDir=$tempBaseDir/$date
  formatDir=$formatBaseDir/$date
  bgpDir=$bgpBaseDir/$date
  echo $date
  mkdir -p $tempDir
  mkdir -p $formatDir
  mkdir -p $bgpDir

  echo "$scriptDir/addAsn2Inetnum.py $formatDir $bgpDir/bpgTable $tempDir $registry"
  $scriptDir/addAsn2Inetnum.py $formatDir $bgpDir/bpgTable $tempDir $registry
  if [ ! $? -eq 0 ];then
    echo "run addAsn2Inetnum.py failed for $date $registry" 
    date=$(date -d "$date +1day" +"%Y%m%d")
    continue
  fi
  mv $tempDir/* $formatDir/
  rm -rf $tempDir/*
  date=$(date -d "$date +1day" +"%Y%m%d")
done
rm -rf $tempBaseDir
