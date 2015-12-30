#!/bin/bash
startDate=$1
endDate=$2
date=$(date +"%Y_%m_%d_%H_%M_%S")
diffCountFile=diff_inetnum_${startDate}_${endDate}.csv
if [ -f $diffCountFile ]
then
  mv $diffCountFile ${diffCountFile}_before_${date}
  touch $diffCountFile
fi
echo "compare type, changed, deleted, appended, sum, needUpdate, numOfLeft, numOfRight" >> $diffCountFile
while [ $startDate -lt $endDate ]
do
nextDate=$((startDate + 1))
diffNetFile="diff_inet_${startDate}_$nextDate"
diffNet6File="diff_inet6_${startDate}_$nextDate"

numOfLeft=$(grep -c -E "^inet[6]?num" inetnum_$startDate)
numOfRight=$(grep -c -E "^inet[6]?num" inetnum_$nextDate)
changed=$(grep -P "\d+c\d+" $diffNetFile | wc -l)
deleted=$(grep -P "\d+,\d+d\d+" $diffNetFile | sed -r 's/([0-9]+),([0-9]+)d[0-9]+/\1 \2/g' | awk 'BEGIN{sum = 0}{if (($2 - $1 + 1) % 2 != 0) print $0; else sum += ($2 - $1 + 1)/2} END{print sum}')
appended=$(grep -P "\d+a\d+,\d+" $diffNetFile | sed -r 's/[0-9]+a([0-9]+),([0-9]+)/\1 \2/g' | awk 'BEGIN{sum = 0}{if (($2 - $1 + 1) % 2 != 0) print $0; else sum += ($2 - $1 + 1)/2} END{print sum}')
sum=$((changed + deleted + appended))
needUpdate=$((changed + appended))
echo "inet_${startDate}_$nextDate, $changed, $deleted, $appended,$sum,$needUpdate,$numOfLeft, $numOfRight" >> $diffCountFile

numOfLeft=$(grep -c -E "^inet[6]?num" inet6num_$startDate)
numOfRight=$(grep -c -E "^inet[6]?num" inet6num_$nextDate)
changed=$(grep -P "\d+c\d+" $diffNet6File | wc -l)
deleted=$(grep -P "\d+,\d+d\d+" $diffNet6File | sed -r 's/([0-9]+),([0-9]+)d[0-9]+/\1 \2/g' | awk 'BEGIN{sum = 0}{if (($2 - $1 + 1) % 2 != 0) print $0; else sum += ($2 - $1 + 1)/2} END{print sum}')
appended=$(grep -P "\d+a\d+,\d+" $diffNet6File | sed -r 's/[0-9]+a([0-9]+),([0-9]+)/\1 \2/g' | awk 'BEGIN{sum = 0}{if (($2 - $1 + 1) % 2 != 0) print $0; else sum += ($2 - $1 + 1)/2} END{print sum}')
sum=$((changed + deleted + appended))
needUpdate=$((changed + appended))
echo "inet6_${startDate}_$nextDate, $changed, $deleted, $appended,$sum,$needUpdate,$numOfLeft, $numOfRight" >> $diffCountFile
((startDate++))
done
