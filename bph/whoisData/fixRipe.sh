#!/bin/bash
bulkDataDir="/data/salrwais/BPH/Whois/bulkWhois/RIPE"
keysDir="/data/salrwais/BPH/Whois/API/RIPE/Keys"
apiDataDir="/data/salrwais/BPH/Whois/API/RIPE/Data"
scriptDir="/data/seclab/BPH/Xianghang/bulkData/Scripts"
formatDir=$scriptDir/format

today=20160417
yesterday=20160416
diffDate=20160501
endDate=20160503
while [ $today -le $endDate ]
do
  echo $yesterday $today
  #uncompress 20160414 20160503
  echo "uncompress for  $yesterday to $today ripe"
  $scriptDir/uncompress.sh $yesterday $today RIPE
  if [ $? -ne 0 ];then
	echo "uncompress error"
	exit 1
  fi

  if [ $today -lt $diffDate ];then
    #merge person for all
    echo "merge person for $today"
	$scriptDir/mergeRipe_all.sh  $today $today 1
	if [ $? -ne 0 ];then
	  echo "merge person for all failed"
	  exit 1
	fi
    #format only person for 0415 to 0430
	$formatDir/formatRipe_test.sh $today $today
	if [ $? -ne 0 ];then
	  echo "format person for $today failed"
	  exit 1
	fi
  else

	echo "merge other objects for $today"
	$scriptDir/mergeRipe_all.sh $today $today 0
	if [ $? -ne 0 ];then
	  echo "merge objects except for person failed for $today"
	  exit 1
	fi

    #format for all objectrs from 0501 to 0503
	$formatDir/formatRipe.sh $today $today
	if [ $? -ne 0 ];then
	  echo "format objects for $today failed"
	  exit 1
	fi

  fi

  yesterday=$today
  today=$(date -d "$today +1day" +"%Y%m%d")
done
#compress $yestoday
$scriptDir/compress.sh 20160415 20160502 RIPE
if [ $? -ne 0 ];then
  echo "compress $yesterday failed"
  exit 1
fi

