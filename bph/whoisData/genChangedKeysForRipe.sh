#!/bin/bash
if [ $# -lt 4 ]
then
  echo "Usage source date1 date2 resultDir"
  exit 1
fi
sourceDir=$1
date1=$2
date2=$3
resultDir=$4
currDir=$(pwd)
objects=('inetnum' 'inet6num' 'role' 'organisation' 'irt' 'mntner' 'aut-num' 'as-set' 'as-block' 'domain' 'route-set')
keys=('inetnum' 'inet6num' 'nic-hdl' 'organisation' 'irt' 'mntner' 'aut-num' 'as-set' 'as-block' 'domain' 'route-set')

#copy source file and unzip .gz
tempDir=$currDir/temp/genChanged
mkdir -p $tempDir
cp -r $sourceDir/$date1 $sourceDir/$date2 $tempDir
gzip -d $tempDir/$date1/*.gz $tempDir/$date2/*.gz
mkdir -p $resultDir

#loop through objects
object="inetnum"
index=0
for object in "${objects[@]}"
do
    echo $object ${keys[$index]}
    grep -E -i "^${keys[$index]}:|last-modified:" ./$tempDir/$date1/ripe.db.$object | sed -r 's/[^ ]+[ ]+(.*)/\1/g' | awk 'BEGIN{FS=" "; line=""}{line1=$0; if (getline <= 0){ print line1} else {print line1 "\t" $0}}' | sort | uniq >$tempDir/${object}_${date1}
    grep -E -i "^${keys[$index]}:|last-modified:" ./$tempDir/$date2/ripe.db.$object | sed -r 's/[^ ]+[ ]+(.*)/\1/g' | awk 'BEGIN{FS=" "; line=""}{line1=$0; if (getline <= 0){ print line1} else {print line1 "\t" $0}}' | sort | uniq >$tempDir/${object}_${date2}
    diff -iEBb $tempDir/${object}_${date1} $tempDir/${object}_${date1} >  $tempDir/diff_${object}_${date1}_${date2}
#include changed and appended
    grep -E -i "^>" $tempDir/diff_${object}_${date1}_${date2} | sed -r 's/> (.*)/\1/g' | awk 'BEGIN{FS="\t"}{print $1}' >$resultDir/${object}_kwlist_appended
#include changed and deleted
    grep -E -i "^<" $tempDir/diff_${object}_${date1}_${date2} | sed -r 's/< (.*)/\1/g' | awk 'BEGIN{FS="\t"}{print $1}' >$resultDir/${object}_kwlist_deleted
    #rm -rf $tempDir/${object}_${date1}
    #rm -rf $tempDir/${object}_${date2}
    #rm -rf $tempDir/diff_${object}_${date1}_${date2}
    ((index++))
done
#rm -rf $tempDir


