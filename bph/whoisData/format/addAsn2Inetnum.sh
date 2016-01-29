#!/bin/bash
formatBaseDir=/data/seclab/BPH/Uniform/
bgpBaseDir=/data/salrwais/BPH/Whois/API/BGP/
currDir=/data/seclab/BPH/Xianghang/bulkData/Scripts/format/
scriptDir=/data/seclab/BPH/Xianghang/bulkData/Scripts/format/
startDate=$(date +"%Y%m%d")
endDate=$(date +"%Y%m%d")
if [ $# -ge 2 ];then
  startDate=$1
  endDate=$2
fi
if [ $# -ge 4 ];then
  startDate=$1
  endDate=$2
  formatBaseDir=$3
  currDir=$4
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

  echo "$scriptDir/addAsn2Inetnum.py $formatDir $bgpDir/bpgTable $tempDir ripe"
  $scriptDir/addAsn2Inetnum.py $formatDir $bgpDir/bpgTable $tempDir ripe
  if [ ! $? -eq 0 ];then
    echo "run addAsn2Inetnum.py failed for $date ripe" 
    date=$(date -d "$date +1day" +"%Y%m%d")
    continue
  fi

  echo "$scriptDir/addAsn2Inetnum.py $formatDir $bgpDir/bpgTable $tempDir apnic"
  $scriptDir/addAsn2Inetnum.py $formatDir $bgpDir/bpgTable $tempDir apnic
  if [ ! $? -eq 0 ];then
    echo "run addAsn2Inetnum.py failed for $date apnic" 
    date=$(date -d "$date +1day" +"%Y%m%d")
    continue
  fi

  echo "$scriptDir/addAsn2Inetnum.py $formatDir $bgpDir/bpgTable $tempDir arin"
  $scriptDir/addAsn2Inetnum.py $formatDir $bgpDir/bpgTable $tempDir arin
  if [ ! $? -eq 0 ];then
    echo "run addAsn2Inetnum.py failed for $date arin" 
    date=$(date -d "$date +1day" +"%Y%m%d")
    continue
  fi

  echo "$scriptDir/addAsn2Inetnum.py $formatDir $bgpDir/bpgTable $tempDir lacnic"
  $scriptDir/addAsn2Inetnum.py $formatDir $bgpDir/bpgTable $tempDir lacnic
  if [ ! $? -eq 0 ];then
    echo "run addAsn2Inetnum.py failed for $date lacnic" 
    date=$(date -d "$date +1day" +"%Y%m%d")
    continue
  fi

  echo "$scriptDir/addAsn2Inetnum.py $formatDir $bgpDir/bpgTable $tempDir afrinic"
  $scriptDir/addAsn2Inetnum.py $formatDir $bgpDir/bpgTable $tempDir afrinic
  if [ ! $? -eq 0 ];then
    echo "run addAsn2Inetnum.py failed for $date afrinic" 
    date=$(date -d "$date +1day" +"%Y%m%d")
    continue
  fi
  mv $tempDir/* $formatDir/
  rm -rf $tempDir/*
  date=$(date -d "$date +1day" +"%Y%m%d")
done
rm -rf $tempBaseDir
