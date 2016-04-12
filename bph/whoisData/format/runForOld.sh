#!/bin/bash
resultBaseDir=/data/seclab/BPH/Uniform/
configFile=/data/seclab/BPH/Xianghang/bulkData/Scripts/format/uniformFormat.cfg
currDir=/data/seclab/BPH/Xianghang/bulkData/Scripts/format
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
tempDir_1=$currDir/temp_runforold_$(date +"%Y%m%d_%H%M%S")
while [ $date -le $endDate ]
do
  echo "$date"
  tempDir=$tempDir_1/$date
  echo $tempDir
  mkdir -p $tempDir
  if [ -e $resultBaseDir/$date ];then
	rm -rf $resultBaseDir/$date
  fi
  mkdir -p $resultBaseDir/$date
  resultDir=$resultBaseDir/$date

#for ripe
  bulkRipe=/data/salrwais/BPH/Whois/bulkWhois/RIPE/$date
  if [ ! -e "$bulkRipe" ];then
	echo "$bulkRipe doesn't exist"
  else
	cp -r /data/salrwais/BPH/Whois/bulkWhois/RIPE/$date $tempDir/ripe
	gzip -d $tempDir/ripe/*.gz
#run unformat script
	$currDir/convertRipeOld2Uniform.py $tempDir/ripe $resultDir $configFile
  fi

#for arin
#copy and unzip to temp
  if [ ! -e "/data/salrwais/BPH/Whois/bulkWhois/ARIN/$date/arin.zip" ];then
	echo "/data/salrwais/BPH/Whois/bulkWhois/ARIN/$date/arin.zip doesn't exist"
  else
	unzip -x /data/salrwais/BPH/Whois/bulkWhois/ARIN/$date/arin.zip -d $tempDir/arin
    #run unformat script
	$currDir/convertArin2Uniform.py $tempDir/arin $resultDir $configFile
  fi

#for apnic
  apnicDir=/data/salrwais/BPH/Whois/bulkWhois/APNIC/$date/
  mkdir -p $tempDir/apnic
  if [ ! -e $apnicDir ];then
	echo "$apnicDir doesn't exist"
  else
	if [ -e $apnicDir/apnic.db.inetnum.gz ];then
	  echo "copy from $apnicDir"
	  cp -r $apnicDir/* $tempDir/apnic
	else
	  echo "copy from $apnicDir/split"
	  cp -r $apnicDir/split/* $tempDir/apnic
	fi
	gzip -d $tempDir/apnic/*.gz
#run unformat script
	if [ $? -eq 0 ];then
	  echo "start to run $currDir/convertApnic2Uniform2.py $tempDir/apnic $resultDir $configFile"
	  $currDir/convertApnic2Uniform2.py $tempDir/apnic $resultDir $configFile
	fi
  fi


#for afrinic
  mkdir -p $tempDir/afrinic
  bulkAfrinic=/data/salrwais/BPH/Whois/bulkWhois/AFRINIC/$date/afrinic.db.gz
  apiDir=/data/salrwais/BPH/Whois/API/AFRINIC/Data/$date/
  if [ ! -e "$bulkAfrinic" -o ! -e "$apiDir" ];then
	echo "$bulkAfrinic  or $apiDir doesn't exist"
  else
	cp $bulkAfrinic $tempDir/afrinic/
	gzip -d $tempDir/afrinic/*.gz
	$currDir/convertAfrinic2Uniform.py $tempDir/afrinic/ $apiDir $resultDir $configFile 
  fi

#for lacnic
  bulkDir=/data/salrwais/BPH/Whois/bulkWhois/LACNIC/$date/
  apiDir=/data/salrwais/BPH/Whois/API/LACNIC/Data/$date/
  if [ ! -e "$bulkDir" -o ! -e "$apiDir" ];then
	echo "$bulkDir  or $apiDir doesn't exist"
  else
	$currDir/convertLacnic2Uniform.py $bulkDir $apiDir $resultDir $configFile 
  fi

#complement history
  echo "$currDir/complementHistory.sh $date $date"
  $currDir/complementHistory.sh $date $date
#crossmatching for ripe inetnum
  echo "$currDir/../crossMatchForRipe.sh $date $date"
  $currDir/../crossMatchForRipe.sh $date $date
#add asn for lacnic and afrinic
  echo "$currDir/addAsn2Inetnum.sh"
  $currDir/addAsn2Inetnum.sh $date $date

  rm -rf $tempDir
  date=$(date -d "$date +1day" +"%Y%m%d")
done
