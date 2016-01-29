#!/bin/bash
baseDir=/data/seclab/BPH/Uniform
ripeInit="20160101"
arinInit="20151222"
apnicInit="20151216"
lacnicInit="20160101"
afrinicInit="20160101"
date=$(date +"%Y%m%d")
startDate=$date
endDate=$date
if [ $# -ge 2 ];then
  startDate=$1
  endDate=$2
fi
date=$startDate
while [ $date -le $endDate ]
do
  echo $date
  if [ ! -e $baseDir/$date ];then
	echo "$baseDir/$date doesn't exist, so create it"
	mkdir -p $baseDir/$date
  fi
  ##for arin
  #if [ $date -lt $arinInit ];then
  #  echo "copy arin file form $arinInit directory"
  #  cp -r $baseDir/$arinInit/*_arin $baseDir/$date/
  #fi

  ##for apnic
  #if [ $date -lt $apnicInit ];then
  #  if [ ! -e $baseDir/$date/inetnum_apnic ];then
  #    echo "copy all apnic files from $apnicInit"
  #    cp $baseDir/$apnicInit/*_apnic $baseDir/$date
  #  else
  #    echo "copy apnic_person from $apnicInit"
  #    cp $baseDir/$apnicInit/person_apnic $baseDir/$date
  #  fi
  #fi
  
  #for ripe
  if [ $date -lt $ripeInit ];then
	if [ ! -e $baseDir/$date/inetnum_ripe ];then
	  echo "copy all ripe files from $ripeInit"
	  cp $baseDir/$ripeInit/*_ripe $baseDir/$date
	else
	  echo "copy person and org of ripe from $ripeInit"
	  #cp $baseDir/$ripeInit/person_ripe $baseDir/$date
	  cp $baseDir/$ripeInit/org_ripe $baseDir/$date
	fi
  fi

  #for lacnic
  #if [ $date -lt $lacnicInit ];then
  #  if [ ! -e $baseDir/$date/inetnum_lacnic ];then
  #    echo "copy all lacnic files from $lacnicInit"
  #    cp $baseDir/$lacnicInit/*_lacnic $baseDir/$date/
  #  else
  #    echo "copy only person of lacnic from $lacnicInit"
  #    cp $baseDir/$lacnicInit/person_lacnic $baseDir/$date/
  #  fi
  #fi

  ##for afrinic
  #if [ $date -lt $afrinicInit ];then
  #  echo "copy all afrinic files from $afrinicInit"
  #  cp $baseDir/$afrinicInit/*_afrinic $baseDir/$date 
  #fi
  date=$(date -d "$date +1day" +"%Y%m%d")
done

