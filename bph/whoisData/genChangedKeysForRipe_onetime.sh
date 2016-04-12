#!/bin/bash
#only appended and delete keys for types not including person
if [ $# -lt 4 ]
then
  echo "Usage source startDate endDate resultDir"
  exit 1
fi
sourceDir=$1
startDate=$2
endDate=$3
resultDir=$4
if [ $# -gt 4 ]
then 
  currDir=$5
else
  currDir=$(pwd)
fi

objects=('inetnum' 'inet6num' 'role' 'organisation' 'irt' 'mntner' 'aut-num' 'as-set' 'as-block' 'domain' 'route-set')
keys=('inetnum' 'inet6num' 'nic-hdl' 'organisation' 'irt' 'mntner' 'aut-num' 'as-set' 'as-block' 'domain' 'route-set')

date1=$(date -d "$startDate -1day" +"%Y%m%d")
date2=$startDate
while [ $date2 -le $endDate ]
do 
  echo $date1 $date2
#copy source file and unzip .gz
  tempDir=$currDir/temp/genChangedForRipe_$(date +"%H%M%S")
  rm -rf $tempDir
  mkdir -p $tempDir/result
  if [ ! \( -e $sourceDir/$date1 -a -e $sourceDir/$date2 \) ]
  then
	echo "$sourceDir/$date1 or $sourceDir/$date2 doesn't exist"
	exit 1
  fi
  cp -r $sourceDir/$date1 $sourceDir/$date2 $tempDir
  gzip -d $tempDir/$date1/*.gz $tempDir/$date2/*.gz
  mkdir -p $resultDir

#loop through objects
  object="inetnum"
  index=0
  for object in "${objects[@]}"
  do
	  echo $object ${keys[$index]}
	  grep -E -i "^${keys[$index]}:|last-modified:" $tempDir/$date1/ripe.db.$object | sed -r 's/[^ ]+[ ]+(.*)/\1/g' | awk 'BEGIN{FS=" "; line=""}{line1=$0; if (getline <= 0){ print line1} else {print line1 "\t" $0}}' | sort | uniq >$tempDir/${object}_${date1}
	  grep -E -i "^${keys[$index]}:|last-modified:" $tempDir/$date2/ripe.db.$object | sed -r 's/[^ ]+[ ]+(.*)/\1/g' | awk 'BEGIN{FS=" "; line=""}{line1=$0; if (getline <= 0){ print line1} else {print line1 "\t" $0}}' | sort | uniq >$tempDir/${object}_${date2}
	  diff -iEBb $tempDir/${object}_${date1} $tempDir/${object}_${date2} >  $tempDir/diff_${object}_${date1}_${date2}
#include changed and appended
	  grep -E -i "^>" $tempDir/diff_${object}_${date1}_${date2} | sed -r 's/> (.*)/\1/g' | awk 'BEGIN{FS="\t"}{print $1}' >$tempDir/result/${object}_kwlist_appended
#include changed and deleted
	  grep -E -i "^<" $tempDir/diff_${object}_${date1}_${date2} | sed -r 's/< (.*)/\1/g' | awk 'BEGIN{FS="\t"}{print $1}' >$tempDir/result/${object}_kwlist_deleted
	  cp $tempDir/${object}_${date2} $tempDir/result/${object}_kwlist
	  #rm -rf $tempDir/${object}_${date1}
	  #rm -rf $tempDir/${object}_${date2}
	  #rm -rf $tempDir/diff_${object}_${date1}_${date2}
	  ((index++))
  done
  if [ -d "$resultDir/$date2" ]
  then
	  mv $resultDir/$date2 $resultDir/${date2}_bak
  fi
  mkdir $resultDir/$date2
#rm -rf $resultDir/latest
  if [ ! -e $resultDir/latest ]
  then
	mkdir $resultDir/latest
  fi
  cp -r $tempDir/result/* $resultDir/$date2/
  cp -r $tempDir/result/* $resultDir/latest/
  rm -rf $tempDir
  date1=$date2
  date2=$(date -d "$date2 +1day" +"%Y%m%d")
done
