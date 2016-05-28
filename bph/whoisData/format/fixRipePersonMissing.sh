#!/bin/bash
uniformBaseDir=/data/seclab/BPH/Uniform/
apiKeyBaseDir=/data/salrwais/BPH/Whois/API/RIPE/Keys
apiDataBaseDir=/data/salrwais/BPH/Whois/API/RIPE/Data
formatScriptDir=/data/seclab/BPH/Xianghang/bulkData/Scripts/format
configFile=/data/seclab/BPH/Xianghang/bulkData/Scripts/format/uniformFormat.cfg
startDate=20160303
endDate=20160520
today=$startDate
yesterday=$(date -d "$today -1day" +"%Y%m%d")
while [ $today -le $endDate ]
do
  startSec=$(date +"%s")
  echo $today
  othersFile=$uniformBaseDir/$today/others_ripe
  personFile=$uniformBaseDir/$today/person_ripe
  unchangedFile=$uniformBaseDir/$today/unchanged_person_ripe
  missingFile=$uniformBaseDir/$today/missing_person_ripe
  if [ ! -e $personFile ];then
	echo "$personFile doesn't exist"
	exit 1
  fi
  #select out  others types
  $formatScriptDir/fixRipePersonMissing.py 1  $personFile $othersFile
  if [ $? -ne 0 ];then
	echo "select other types failed"
	exit 1
  fi
  rm  $personFile
  #format Person appended
  $formatScriptDir/convertRipe2Uniform_test.py $apiDataBaseDir/$today $uniformBaseDir/$today $configFile
  if [ $? -ne 0 ];then
	echo "format appended person file failed"
	exit 1
  fi
  #select out unchanged 
  $formatScriptDir/fixRipePersonMissing.py 2  $apiKeyBaseDir/$today/person_kwlist_appended $apiKeyBaseDir/$today/person_kwlist_deleted $uniformBaseDir/$yesterday/person_ripe $unchangedFile
  if [ $? -ne 0 ];then
	echo "select unchanged  person file failed"
	exit 1
  fi
  #merge appended person, unchanged persons, others into person_ripe
  cat $othersFile $unchangedFile >>$personFile
  #generate missing key list
  $formatScriptDir/fixRipePersonMissing.py 3  $personFile $apiKeyBaseDir/$today/person_kwlist $missingFile
  if [ $? -ne 0 ];then
	echo "generating missing person file failed"
	exit 1
  fi
  endSec=$(date +"%s")
  rm $unchangedFile
  if [ ! -e $apiDataBaseDir/$today/person ];then
	rm -r $apiDataBaseDir/$today
  fi
  echo "time cost for $today $yesterday is $(($endSec - $startSec))"
  yesterday=$today
  today=$(date -d "$today +1day" +"%Y%m%d")
done
