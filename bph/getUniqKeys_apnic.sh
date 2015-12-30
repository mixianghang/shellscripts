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
	echo "finish retrieve apnic.db.inetnum_$day"
	grep -E "(admin-c|tech-c):[ ]+\w+" ${curDir}/apnic.db.inet6num_$day | sed -E 's/(tech-c|admin-c):[ ]+([0-9a-zA-Z\-]+)/\2/g' | sort -u > uniqKeysFromInet6_$day
	echo "finish retrieve apnic.db.inet6num_$day"
	sort -u uniqKeysFromInet6_$day uniqKeysFromInet_$day >uniqKeysFrom_$day
	echo "finish retrieve $day"
	if [ $day -gt $startDate ]
	then

	  preDay=$((day - 1))
	  diff -iEb uniqKeysFrom_$preDay uniqKeysFrom_$day > uniqKeysCompare_${preDay}_$day
	  #deleted=$(grep -E "[0-9]+d[0-9]+" uniqKeysCompare_${preDay}_$day | awk 'BEGIN{FS=",|d"; sum = 0}{if (NF==2) sum += 1; else sum += $2 - $1 + 1} END{print sum}') 
	  #appended=$(grep -E "[0-9]+a[0-9]+" uniqKeysCompare_${preDay}_$day | awk 'BEGIN{FS=",|a";sum = 0}{if (NF==2) sum += 1; else sum += $3 - $2 + 1} END{print sum}') 
	  deleted=$(grep -E -c "^<" uniqKeysCompare_${preDay}_$day)
	  appended=$(grep -E -c "^>" uniqKeysCompare_${preDay}_$day)
	  numOfLeft=$(grep -c "" uniqKeysFrom_$preDay)
	  numOfRight=$(grep -c "" uniqKeysFrom_$day)
	  echo "${preDay}_${day}, $numOfLeft, $numOfRight, $deleted, $appended" >> $diffFile
	  echo "finish compare $preDay and $day"

	  diff -iEb uniqKeysFrom_${startDate}_${endDate} uniqKeysFrom_$day > uniqKeysCompare_all_$day
	  #deleted=$(grep -E "[0-9]+d[0-9]+" uniqKeysCompare_all_$day | awk 'BEGIN{FS=",|d"; sum = 0}{if (NF==2) sum += 1; else sum += $2 - $1 + 1} END{print sum}') 
	  #appended=$(grep -E "[0-9]+a[0-9]+" uniqKeysCompare_all_$day | awk 'BEGIN{FS=",|a";sum = 0}{if (NF==2) sum += 1; else sum += $3 - $2 + 1} END{print sum}') 
	  deleted=$(grep -E -c "^<" uniqKeysCompare_all_$day)
	  appended=$(grep -E -c "^>" uniqKeysCompare_all_$day)
	  numOfLeft=$(grep -c "" uniqKeysFrom_${startDate}_${endDate})
	  numOfRight=$(grep -c "" uniqKeysFrom_$day)
	  echo "all_${day}, $numOfLeft, $numOfRight, $deleted, $appended" >> $diffFile
	  grep -E "^>" uniqKeysCompare_all_$day | sed -E 's/>[ ]+(.+)/\1/g' >> uniqKeysFrom_${startDate}_${endDate}
	  sort -u uniqKeysFrom_${startDate}_${endDate} > temp
	  mv temp uniqKeysFrom_${startDate}_${endDate}
	  ukNum=$(wc -l uniqKeysFrom_${startDate}_${endDate})
	  echo "finish compare all and $day, current uk num is $ukNum"
	else
	  cp uniqKeysFrom_$startDate uniqKeysFrom_${startDate}_${endDate}
	fi 
	((day++))
  done
