#!/bin/bash
if [ $# -lt 3 ]
then
  echo "Usage sourceDir date resultDir"
  exit 1
fi
sourceDir=$1
date=$2
resultDir=$3

if [ $# -gt 3 ]
then 
  currDir=$4
else
  currDir=$(pwd)
fi
yesterday=$(date -d "$date -1day" +"%Y%m%d")

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
      echo "generate keys from $sourceDir/$date/$object"
      grep -E -i "name=\"(admin-c|tech-c)\".*person" $sourceDir/$date/$object |sed -r 's/.*value=\"(.+)\" .*/\1/g' >>$tempDir/resultList
    fi
    if [ -f $sourceDir/$date/${object}_appended ]
    then
      echo "generate keys from $sourceDir/$date/${object}_appended"
      grep -E -i "name=\"(admin-c|tech-c)\".*person" $sourceDir/$date/${object}_appended |sed -r 's/.*value=\"(.+)\" .*/\1/g' >>$tempDir/resultList
    fi
    ((index++))
done

if [ ! -e $tempDir/resultList ]
then
  echo "no result generated"
  exit 1
fi
if [ -e $resultDir/$yesterday/person_kwlist ]
then
  echo "append old keylsit"
  cat $resultDir/$yesterday/person_kwlist >> $tempDir/resultList
fi
echo "sort and remove duplicates"
sort $tempDir/resultList | uniq > $tempDir/uniqList
if [ -e $resultDir/$yesterday/person_kwlist ]
then
  diff -iEBb $resultDir/$yesterday/person_kwlist $tempDir/uniqList > $tempDir/diffList
  grep -E ">" $tempDir/diffList | sed -r 's/>[ ]+(.*)/\1/g' > $tempDir/appendedList
  grep -E "<" $tempDir/diffList | sed -r 's/<[ ]+(.*)/\1/g' > $tempDir/deletedList
else
  touch $tempDir/appendedList
  touch $tempDir/deletedList
fi
if [ ! -e $resultDir/$date ]
then
  mkdir -p $resultDir/$date
fi
if [ ! -e $resultDir/latest ]
then
  mkdir -p $resultDir/latest
fi

echo "save result to $resultDir/$date/person_kwlist and  $resultDir/latest/person_kwlist"

cp $tempDir/uniqList $resultDir/$date/person_kwlist
cp $tempDir/appendedList $resultDir/$date/person_kwlist_appended
cp $tempDir/deletedList $resultDir/$date/person_kwlist_deleted

cp $tempDir/uniqList $resultDir/latest/person_kwlist
cp $tempDir/appendedList $resultDir/latest/person_kwlist_appended
cp $tempDir/deletedList $resultDir/latest/person_kwlist_deleted

rm -rf $tempDir
