#!/bin/bash
startDate=$1
endDate=$2
day=$1
curDir=$(pwd)
diffFile="diff_uniq_keys_${1}_${2}.csv"
echo "diffName, numOfLeft, numOfRight, deleted, appended" > $diffFile
while [ $day -le $endDate ]
  do
	grep -E "(admin-c|tech-c):[ ]+\w+" ${curDir}/apnic.db.inetnum_$day | sed -E 's/(tech-c|admin-c):[ ]+([1-9a-zA-Z\-]+)/\2/g' | sort -u > uniqKeysFromInet_$day
	grep -E "(admin-c|tech-c):[ ]+\w+" ${curDir}/apnic.db.inet6num_$day | sed -E 's/(tech-c|admin-c):[ ]+([0-9a-zA-Z\-]+)/\2/g' | sort -u > uniqKeysFromInet6_$day
	sort -u uniqKeysFromInet6_$day uniqKeysFromInet_$day >uniqKeysFrom_$day
	if [ $day -gt $startDate ]
	then
	  preDay=$((day - 1))
	  diff -iEb uniqKeysFrom_$preDay uniqKeysFrom_$day > uniqKeysCompare_${preDay}_$day
	  deleted=$(grep -E "[0-9]+d[0-9]+" uniqKeysCompare_${preDay}_$day | awk 'BEGIN{FS=",|d"; sum = 0}{if (NF==2) sum += 1; else sum += $2 - $1 + 1} END{print sum}') 
	  appended=$(grep -E "[0-9]+a[0-9]+" uniqKeysCompare_${preDay}_$day | awk 'BEGIN{FS=",|a";sum = 0}{if (NF==2) sum += 1; else sum += $3 - $2 + 1} END{print sum}') 
	  numOfLeft=$(grep -c "" uniqKeysFrom_$preDay)
	  numOfRight=$(grep -c "" uniqKeysFrom_$day)
	  echo "${preDay}_${day}, $numOfLeft, $numOfRight, $deleted, $appended" >> $diffFile
	fi 
	((day++))
  done
