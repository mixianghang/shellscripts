#!/bin/bash
if [ $# -lt 3 ]
then
  echo "Usage sourceDir date resultDir"
  exit 1
fi
sourceDir=$1
date=$2
resultDir=$3
currDir=$(pwd)
objects=('inetnum' 'inet6num' 'role' 'organisation' 'irt' 'mntner' 'aut-num' 'as-set' 'as-block' 'domain' 'route-set')
keys=('inetnum' 'inet6num' 'nic-hdl' 'organisation' 'irt' 'mntner' 'aut-num' 'as-set' 'as-block' 'domain' 'route-set')
#copy source file and unzip .gz
tempDir=$currDir/temp/genPersonKeysForRipe
rm -rf $tempDir
mkdir -p $tempDir
if [ -e $tempDir ]
then
    rm -rf $tempDir
fi
mkdir -p $tempDir
touch $tempDir/resultList

#loop through objects
object="inetnum"
index=0
for object in "${objects[@]}"
do
    if [ -f $sourceDir/$date/$object ]
    then
      grep -E -i "name=\"(admin-c|tech-c)\".*person" $sourceDir/$date/$object |sed -r 's/.*value=\"(.+)\" .*/\1/g' >>$tempDir/resultList
    fi
    if [ -f $sourceDir/$date/$object.appended ]
    then
      grep -E -i "name=\"(admin-c|tech-c)\".*person" $sourceDir/$date/$object.appended |sed -r 's/.*value=\"(.+)\" .*/\1/g' >>$tempDir/resultList
    fi
    ((index++))
done

if [ ! -e $tempDir/resultList ]
then
  echo "no result generated"
  exit 1
fi
if [ -e $resultDir/latest/person_kwlist ]
then
  cat $resultDir/latest/person_kwlist >> $tempDir/resultList
fi
sort $tempDir/resultList | uniq >$tempDir/uniqList
if [ ! -e $resultDir/$date ]
then
  mkdir -p $resultDir/$date
fi
if [ ! -e $resultDir/latest ]
then
  mkdir -p $resultDir/latest
fi

mv $tempDir/uniqList $resultDir/$date/person_kwlist
mv $tempDir/uniqList $resultDir/latest/person_kwlist
rm -rf $tempDir
