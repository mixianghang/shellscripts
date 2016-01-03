#!/bin/bash
if [ $# -lt 2 ]
then
    echo "Usage sourceDir resultDir"
    exit 1
fi
sourceDir=$1
resultDir=$2
date=$(date +%Y%m%d)
#cmd="grep -E -i  '^$kw:' $sourceDir/$date/ripe.db.$type | sed -r 's/$kw:[ ]+(.*)/\1/g' > $resultDir/$date/${type}_kwlist"
mkdir -p $resultDir/$date
mkdir -p $resultDir/latest
tempDir=$(pwd)/temp/genKwListForLacnic
if [ -e $tempDir ]
then
  rm -rf $tempDir
fi
mkdir -p $tempDir
cp $sourceDir/$date/lacnic.dp $tempDir/
objects=("inetnum")
keys=("inetnum")
object="inetnum"
index=0
for object in ${objects[@]}
do
    kw=${keys[$index]}
    ((index++))
    grep -E -i  "^$kw:" $tempDir/lacnic.dp | sed -r "s/$kw:[ ]+(.*)/\1/g" > $resultDir/$date/${object}_kwlist
done

#generate person kwlist 
grep -E -i "^(owner-c|tech-c|abuse-c):" $sourceDir/$date/$object | awk '{if (NF >= 2) {print $2}}' | sort | uniq > $resultDir/$date/person_kwlist

cp -r $resultDir/$date/* $resultDir/latest
rm -rf $tempDir
