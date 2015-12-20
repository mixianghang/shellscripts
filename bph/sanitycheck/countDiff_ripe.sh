#!/bin/bash
startDate=$1
endDate=$2
echo "compare type, changed, deleted, appended, sum, needUpdate"
while [ $startDate -lt $endDate ]
do
nextDate=$((startDate + 1))
diffFile="diff_${startDate}_$nextDate"
changed=$(grep -P "\d+c\d+" $diffFile | wc -l)
deleted=$(grep -P "\d+,\d+d\d+" $diffFile | sed -r 's/([0-9]+),([0-9]+)d[0-9]+/\1 \2/g' | awk 'BEGIN{sum = 0}{if (($2 - $1 + 1) % 2 != 0) print $0; else sum += ($2 - $1 + 1)/2} END{print sum}')
appended=$(grep -P "\d+a\d+,\d+" $diffFile | sed -r 's/[0-9]+a([0-9]+),([0-9]+)/\1 \2/g' | awk 'BEGIN{sum = 0}{if (($2 - $1 + 1) % 2 != 0) print $0; else sum += ($2 - $1 + 1)/2} END{print sum}')
sum=$((changed + deleted + appended))
needUpdate=$((changed + appended))
echo "${startDate}_$nextDate, $changed, $deleted, $appended,$sum,$needUpdate"
((startDate++))
done
