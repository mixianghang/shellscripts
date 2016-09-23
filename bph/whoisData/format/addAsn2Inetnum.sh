#!/bin/bash
addAsn2InetnumForGivenRegistry(){
  echo "$scriptDir/addAsn2Inetnum.py $formatDir $bgpDir/bpgTable $tempDir $1"
  $scriptDir/addAsn2Inetnum.py $formatDir $bgpDir/bpgTable $tempDir $1
}
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
if [ $# -ge 3 ];then
  registryList=$3
else
  registryList=(ripe arin apnic afrinic)
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
  registry="ripe"
  for registry in ${registryList[@]}
  do
	echo $registry $date
	addAsn2InetnumForGivenRegistry $registry
	if [ ! $? -eq 0 ];then
	  echo "run addAsn2Inetnum.py failed for $date $registry" 
	  continue
	fi
  done
  mv $tempDir/* $formatDir/
  rm -rf $tempDir/*
  date=$(date -d "$date +1day" +"%Y%m%d")
done
rm -rf $tempBaseDir
