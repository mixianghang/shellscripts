#!/bin/bash
resultBaseDir=/data/seclab/BPH/Uniform/
configFile=/data/seclab/BPH/Xianghang/bulkData/Scripts/format/uniformFormat.cfg
currDir=/data/seclab/BPH/Xianghang/bulkData/Scripts/format/
startDate=$(date +"%Y%m%d")
endDate=$(date +"%Y%m%d")
if [ $# -ge 2 ];then
  startDate=$1
  endDate=$2
fi
if [ $# -ge 5 ];then
  startDate=$1
  endDate=$2
  resultBaseDir=$3
  configFile=$4
  currDir=$5
fi
date=$startDate
while [ $date -le $endDate ]
do
  echo "$date"
  tempDir=$currDir/temp/$date
  mkdir -p $tempDir
  mkdir -p $resultBaseDir/$date
  resultDir=$resultBaseDir/$date

#for arin
#copy and unzip to temp
#  if [ ! -e "/data/salrwais/BPH/Whois/bulkWhois/ARIN/$date/arin.zip" ];then
#	echo "/data/salrwais/BPH/Whois/bulkWhois/ARIN/$date/arin.zip doesn't exist"
#  else
#	unzip -x /data/salrwais/BPH/Whois/bulkWhois/ARIN/$date/arin.zip -d $tempDir/arin
#    #run unformat script
#	$currDir/convertArin2Uniform.py $tempDir/arin $resultDir $configFile
#  fi
#
##for apnic
#  if [ ! -e "/data/salrwais/BPH/Whois/bulkWhois/APNIC/$date" ];then
#	echo "/data/salrwais/BPH/Whois/bulkWhois/APNIC/$date doesn't exist"
#  else
#	cp -r /data/salrwais/BPH/Whois/bulkWhois/APNIC/$date $tempDir/apnic
#	gzip -d $tempDir/apnic/split/*.gz
##run unformat script
#	$currDir/convertApnic2Uniform2.py $tempDir/apnic/split $resultDir $configFile
#  fi
#
##for ripe
#  sourceRipe=/data/salrwais/BPH/Whois/API/RIPE/Data/$date
#  bulkRipe=/data/salrwais/BPH/Whois/bulkWhois/RIPE/$date
#  if [ ! -e "$sourceRipe" -o ! -e "$bulkRipe" ];then
#	echo "$sourceRipe  or $bulkRipe doesn't exist"
#  else
#	cp -r /data/salrwais/BPH/Whois/bulkWhois/RIPE/$date $tempDir/ripe
#	gzip -d $tempDir/ripe/*.gz
##run unformat script
#	$currDir/convertRipe2Uniform.py $sourceRipe $resultDir $configFile  $tempDir/ripe
#  fi
#
##for afrinic
#  mkdir -p $tempDir/afrinic
#  bulkAfrinic=/data/salrwais/BPH/Whois/bulkWhois/AFRINIC/$date/afrinic.db.gz
#  apiDir=/data/salrwais/BPH/Whois/API/AFRINIC/Data/$date/
#  if [ ! -e "$bulkAfrinic" -o ! -e "$apiDir" ];then
#	echo "$bulkAfrinic  or $apiDir doesn't exist"
#  else
#	cp $bulkAfrinic $tempDir/afrinic/
#	gzip -d $tempDir/afrinic/*.gz
#	$currDir/convertAfrinic2Uniform.py $tempDir/afrinic/ $apiDir $resultDir $configFile 
#  fi

#for lacnic
  bulkDir=/data/salrwais/BPH/Whois/bulkWhois/LACNIC/$date/
  apiDir=/data/salrwais/BPH/Whois/API/LACNIC/Data/$date/
  if [ ! -e "$bulkDir" -o ! -e "$apiDir" ];then
	echo "$bulkDir  or $apiDir doesn't exist"
  else
	$currDir/convertLacnic2Uniform.py $bulkDir $apiDir $resultDir $configFile 
	$currDir/convLacnicOrg2Uniform.py $apiDir $resultDir $configFile
	echo "$currDir/preprocessLacnic.sh"
	$currDir/preprocessLacnic.sh $date $date
  fi

  echo "$currDir/addAsn2Inetnum.sh"
  $currDir/addAsn2Inetnum.sh $date $date


  rm -rf $tempDir
  date=$(date -d "$date +1day" +"%Y%m%d")
done
