#!/bin/bash
#this is used after ripe format to do missing check and give another chance to fix missing or bad data
checkError() {
  if [ $? -ne 0 ];then
	echo "error when $1"
	exit 1
  fi
}

uniformBaseDir=/data/seclab/BPH/Uniform
originConfigFile=$uniformBaseDir/appendRipeConfig.cfg
scriptDir=/data/seclab/BPH/Xianghang/bulkData/Scripts
formatDir=$scriptDir/format
apiKeyDir=/data/salrwais/BPH/Whois/API/RIPE/Keys

if [ $# -lt 2 ];then
  echo "Usage startDate endDate"
  exit 1
fi
startDate=$1
endDate=$2

today=$startDate
objNameList=(inetnum person irt mntner role organisation aut-num)
objFileList=(inetnum person person person person org asn)
objTypeList=(inetnum person irt mntner role organisation aut-num)
objLen=${#objNameList[@]}

uniformSourceList=(inetnum_formatted_missing person_formatted_missing asn_formatted_missing org_formatted_missing)
uniformResultList=(inetnum_ripe person_ripe asn_ripe org_ripe)
while [ $today -le $endDate ]
do
  echo $today
  startSec=$(date +"%s")
  validateDir=$uniformBaseDir/$today/missing/ripe/validate
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
	grep -Pi "^$objType\t" $uniformDataDir/${objFile}_ripe | awk -F"\t" '{print $2}' > $existKeyFile
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
  sed  "s/DATETOREPLACE/$today/g" $scriptDir/validity/config/appendRipe.cfg >$validateDir/appendRipe.cfg
  $scriptDir/retrieveRipe.py $validateDir/appendRipe.cfg 2>$validateDir/appendLogError
  if [ $? -ne 0 ];then
	echo "append missing objects for $today failed"
	exit 1
  fi
#try to format missing objects for all the types
  $formatDir/convertRipe2Uniform_validity.py $validateDir $validateDir $formatDir/uniformFormat.cfg
  if [ $? -ne 0 ];then
	echo "format missing objects for $today failed"
	exit 1
  fi
  i=1 #skip inetnum TODO
  while [ $i -lt ${#uniformSourceList[@]} ]
  do
	uniformSource=${uniformSourceList[$i]}
	uniformResult=${uniformResultList[$i]}
	if [ -e $validateDir/$uniformSource ];then
	  tail -n+2 $validateDir/$uniformSource >>$uniformBaseDir/$today/$uniformResult
	fi
	((i++))
  done
  endSec=$(date +"%s")
  echo "time cost is $(($endSec - $startSec))"
  today=$(date -d "$today +1day" +"%Y%m%d")
done

