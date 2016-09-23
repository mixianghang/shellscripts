#!/bin/bash
checkError() {
  if [ $? -ne 0 ];then
	echo "error when $1"
	exit 1
  fi
}
echoerr() { echo "$@" 1>&2; }
scriptDir=/data/seclab/BPH/Xianghang/bulkData/Scripts
uniformBaseDir=/data/seclab/BPH/Uniform
if [ $# -lt 2 ];then
  echo "Usage : startDate endDate"
  exit 1
fi
if [ $# -ge 3 ];then
  registryList=$3
else
  registryList=(lacnic afrinic ripe apnic arin)
fi
if [ $# -ge 4 ];then
   typeList=$4
else
  typeList=(asn person inetnum org)
fi

startDate=$1
endDate=$2
#typeList=(asn person inetnum org)
today=$startDate
yesterday=$(date -d "$today -1day" +"%Y%m%d")
while [ $today -le $endDate ]
do
  echo $today
  startSec=$(date +"%s")

  registry="lacnic"
  for registry in ${registryList[@]}
  do
	if [[ "$registry" == "afrinic" ]];then
	  echo "validate afrinic $today"
	  $scriptDir/validity/validateAfrinic.sh $today $today
	  checkError "validate afrinic for $today"
	fi
	if [[ "$registry" == "lacnic" ]];then
	  echo "validate lacnic for $today"
	  $scriptDir/validity/validateLacnic.sh $today $today
	  checkError "validate lacnic for $today"
	fi
	if [[ "$registry" == "ripe" ]];then
	  echo "validate ripe for $today"
	  $scriptDir/validity/validateRipe.sh $today $today
	  checkError "validate ripe for $today"
	fi
  done

  registry="lacnic"
  objType="asn"
  for objType in ${typeList[@]}
  do
    for registry in ${registryList[@]}
	do
	  echo $today $registry $objType
	  uniformFile=$uniformBaseDir/$today/${objType}_${registry}
	  if [ ! -e $uniformFile ];then
		echoerr "$uniformFile doesn't exist"
		continue
	  fi

	  checkDir=$uniformBaseDir/$today/missing/${registry}/validate/check
	  mkdir -p $checkDir
	  logFile=$checkDir/${objType}_log
	  if [ -e $logFile ];then
		rm $logFile
	  fi
	  echo $today $registry $objType $uniformFile $logFile
	  $scriptDir/validity/checkUniform.py $uniformFile $objType $registry $logFile
	  if [ $? -ne 0 ];then
		echo "error when checking uniform"
		exit 1
	  fi
	done
  done
  $scriptDir/validity/compressMissingDir.sh $yesterday $yesterday
  checkError "error when compress $yesterday missing dir"
  endSec=$(date +"%s")
  echo "time cost is $(($endSec - $startSec))s"
  yesterday=$today
  today=$(date -d "$today +1day" +"%Y%m%d")
done
