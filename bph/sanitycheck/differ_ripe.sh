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
  echo "filte " $day
  grep -e "inetnum\|last-modified" ${curDir}/${day}/ripe.db.inetnum > $curDir/inetnum_${day}
  ((day++))
done
day=$startDate
while [ $day -lt $endDate ]
do
  nextDay=$(($day + 1))
  echo "comparision of " $day " with " $nextDay
  diff -iEb ${curDir}/inetnum_${day} ${curDir}/inetnum_${nextDay} > $curDir/diff_${day}_${nextDay}
  ((day++))
done

