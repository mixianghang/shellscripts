#!/bin/bash
#this is used after ripe format to do missing check and give another chance to fix missing or bad data
#for lacnic, we only check Person. Org are generated from inentum_api data. Even if we got missing keys,
#there is no api for querying the missing ones. Inetnum and asn are retrieved from bulk data.
checkError() {
  if [ $? -ne 0 ];then
	echo "error when $1"
	exit 1
  fi
}

uniformBaseDir=/data/seclab/BPH/Uniform
originConfigFile=$uniformBaseDir/lacnicConfig.cfg
scriptDir=/data/seclab/BPH/Xianghang/bulkData/Scripts
formatDir=$scriptDir/format
apiKeyDir=/data/salrwais/BPH/Whois/API/LACNIC/Keys

if [ $# -lt 2 ];then
  echo "Usage startDate endDate"
  exit 1
fi
startDate=$1
endDate=$2

today=$startDate
objNameList=("person")
objFileList=(person)
objTypeList=("person")
objLen=${#objNameList[@]}

uniformSourceList=(person_formatted_missing)
uniformResultList=(person_lacnic)
while [ $today -le $endDate ]
do
  echo $today
  startSec=$(date +"%s")
  $scriptDir/validity/appendLacnic.sh $today $today person
  checkError "append person from previous day for $today"
  validateDir=$uniformBaseDir/$today/missing/lacnic/validate
  uniformDataDir=$uniformBaseDir/$today
  mkdir -p $validateDir
  subIndex=0
  #checking missing objects for all the types
  while [ $subIndex -lt  $objLen ]
  do
	objName=${objNameList[$subIndex]}
	objFile=${objFileList[$subIndex]}
	objType=${objTypeList[$subIndex]}
	echo "objName: $objName, objFile: $objFile, objType: $objType"
	existKeyFile=$validateDir/${objName}_kwlist_exist
	keyFile=$validateDir/${objName}_kwlist
	missKeyFile=$validateDir/${objName}_kwlist_missing

	#generate exist key file
	grep -Pi "^$objType\t" $uniformDataDir/${objFile}_lacnic | awk -F"\t" '{print $2}' > $existKeyFile
	checkError "generate exist key file"
	echo "got $(wc -l <$existKeyFile) existing keys"

	#generate keyfile
	awk -F"\"|\t" '{print $1}' $apiKeyDir/$today/${objName}_kwlist > $keyFile
	checkError "generate full keylist"
	echo "got $(wc -l <$keyFile) full keys"

	$scriptDir/validity/diffKeys.py $existKeyFile $keyFile $missKeyFile

	if [ $? -ne 0 ];then
	  echo "error when generate missing keys for $objName of $today"
	  exit 1
	fi
	((subIndex++))
  done
#try to requery missing objects for the the types
  sed  "s/DATETOREPLACE/$today/g" $scriptDir/validity/config/appendLacnicConfig.cfg >$validateDir/lacnicConfig.cfg
  $scriptDir/retrieveLacnic.py $validateDir/lacnicConfig.cfg 2>$validateDir/lacnicLogError
  if [ $? -ne 0 ];then
	echo "append missing objects for $today failed"
	exit 1
  fi
#try to format missing objects for all the types
  $formatDir/convertLacnic2Uniform_for_validity.py ./ $validateDir $validateDir $formatDir/uniformFormat.cfg
  if [ $? -ne 0 ];then
	echo "format missing objects for $today failed"
	exit 1
  fi
  i=0 #skip inetnum TODO
  while [ $i -lt ${#uniformSourceList[@]} ]
  do
	uniformSource=${uniformSourceList[$i]}
	uniformResult=${uniformResultList[$i]}
	if [ -e $validateDir/$uniformSource ];then
	  tail -n+2 $validateDir/$uniformSource >>$uniformBaseDir/$today/$uniformResult
	fi
	((i++))
  done
  subIndex=0
  #checking missing objects for all the types
  while [ $subIndex -lt  $objLen ]
  do
	objName=${objNameList[$subIndex]}
	objFile=${objFileList[$subIndex]}
	objType=${objTypeList[$subIndex]}
	echo "objName: $objName, objFile: $objFile, objType: $objType"
	existKeyFile=$validateDir/${objName}_kwlist_exist
	keyFile=$validateDir/${objName}_kwlist
	missKeyFile=$validateDir/${objName}_kwlist_missing

	#generate exist key file
	grep -Pi "^$objType\t" $uniformDataDir/${objFile}_lacnic | awk -F"\t" '{print $2}' > $existKeyFile
	checkError "generate exist key file"
	echo "got $(wc -l <$existKeyFile) existing keys"

	$scriptDir/validity/diffKeys.py $existKeyFile $keyFile $missKeyFile

	if [ $? -ne 0 ];then
	  echo "error when generate missing keys for $objName of $today"
	  exit 1
	fi
	((subIndex++))
  done
  endSec=$(date +"%s")
  echo "time cost is $(($endSec - $startSec))"
  today=$(date -d "$today +1day" +"%Y%m%d")
done

