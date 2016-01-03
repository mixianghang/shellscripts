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
tempDir=$(pwd)/temp/genKwListForAfrinic
if [ -e $tempDir ]
then
  rm -rf $tempDir
fi
mkdir -p $tempDir
cp $sourceDir/$date/afrinic.db.gz $tempDir/
gzip -d $tempDir/afrinic.db.gz
objects=("person" "role" "organisation" "irt")
keys=("nic-hdl" "nic-hdl" "organisation" "irt")
object="person"
index=0
for object in ${objects[@]}
do
    kw=${keys[$index]}
    ((index++))
    grep -E -i  "^$kw:" $tempDir/afrinic.db | sed -r "s/$kw:[ ]+(.*)/\1/g" > $resultDir/$date/${object}_kwlist
done

cp -r $resultDir/$date/* $resultDir/latest
rm -rf $tempDir
