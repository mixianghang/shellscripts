#!/bin/bash
if [ $# -lt 3 ]
then
    echo "Usage sourceDir resultDir date"
    exit 1
fi
sourceDir=$1
resultDir=$2
date=$3
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
objects=("organisation" "irt")
keys=("organisation" "irt")
object="organisation"
index=0
for object in ${objects[@]}
do
    kw=${keys[$index]}
    ((index++))
    grep -E -i  "^$kw:" $tempDir/afrinic.db | sed -r "s/$kw:[ ]+(.*)/\1/g" > $resultDir/$date/${object}_kwlist
done

#person and role
grep -E -i  "^nic-hdl:" $tempDir/afrinic.db | sed -r "s/nic-hdl:[ ]+(.*)/\1/g" > $resultDir/$date/person_role_kwlist
cp -r $resultDir/$date/* $resultDir/latest
rm -rf $tempDir
