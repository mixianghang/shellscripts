#!/bin/bash
checkError() {
  if [ $? -ne 0 ];then
	echo "error when $1"
	exit 1
  fi
}
uniformBaseDir=/data/seclab/BPH/Uniform
startDate=$(date +"%Y%m%d")
endDate=$startDate

if [ $# -ge 2 ];then
  startDate=$1
  endDate=$2
fi

currDate=$startDate
while [ $currDate -le $endDate ]
do
  missBaseDir=$uniformBaseDir/$currDate
  missDir=$missBaseDir/missing
  if [ -e $missDir ];then
	7z a $missBaseDir/missing.7z $missDir
	checkError "error when compressing $missDir"
	rm -r $missDir
  fi
  currDate=$(date -d "$currDate +1day" +"%Y%m%d")
done
