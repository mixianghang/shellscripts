#! /bin/bash
startDate=$1
endDate=$2
curDir=$(pwd)
day=$startDate
while [ $day -le $endDate ]
do
  if [ -f ${curDir}/${day}/ripe.db.inetnum.gz ]
  then
  gzip -d ${curDir}/${day}/ripe.db.inetnum.gz
  fi
  if [ -f ${curDir}/${day}/ripe.db.inet6num.gz ]
  then
  gzip -d ${curDir}/${day}/ripe.db.inet6num.gz
  fi
  echo "filte " $day
  grep -E "^(inet[6]?num:|last-modified:)" ${curDir}/${day}/ripe.db.inetnum > $curDir/inetnum_${day}
  grep -E "^(inet[6]?num:|last-modified:)" ${curDir}/${day}/ripe.db.inet6num > $curDir/inet6num_${day}
  ((day++))
done
day=$startDate
while [ $day -lt $endDate ]
do
  nextDay=$(($day + 1))
  echo "comparision of " $day " with " $nextDay
  diff -iEb ${curDir}/inetnum_${day} ${curDir}/inetnum_${nextDay} > $curDir/diff_inet_${day}_${nextDay}
  diff -iEb ${curDir}/inet6num_${day} ${curDir}/inet6num_${nextDay} > $curDir/diff_inet6_${day}_${nextDay}
  ((day++))
done

