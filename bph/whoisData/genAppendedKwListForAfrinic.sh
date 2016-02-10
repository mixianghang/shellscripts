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

if [ $# -gt 3 ]
then 
  currDir=$4
else
  currDir=$(pwd)
fi

tempDir=$currDir/temp/genKwListForAfrinic
if [ -e $tempDir ]
then
  rm -rf $tempDir
fi
mkdir -p $tempDir
cp $sourceDir/$date/afrinic.db.gz $tempDir/
gzip -d $tempDir/afrinic.db.gz

#generate person kwlist 
grep -E -i "^(owner-c|tech-c|abuse-c|nic-hdl):" $tempDir/afrinic.db | awk '{if (NF >= 2) {print $2}}' | sort | uniq > $resultDir/$date/person_role_new_kwlist
grep -E -i "^(nic-hdl):" $tempDir/afrinic.db | awk '{if (NF >= 2) {print $2}}' | sort | uniq > $resultDir/$date/person_role_old_kwlist
diff -iEBb $resultDir/$date/person_role_old_kwlist $resultDir/$date/person_role_new_kwlist | grep -E "^>.*" | awk '{if (NF >= 2) {print $2}}' | sort | uniq > $resultDir/$date/person_role_kwlist
cp -r $resultDir/$date/person_role_kwlist $resultDir/latest
rm -rf $tempDir
