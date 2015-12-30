#!/bin/bash
if [ "$#" -ne 4 ]
then
  echo "usage: delegated, inetnum, inet6num, resultFile"
  exit 1
fi
delegatedFile=$1
inetnumFile=$2
inet6numFile=$3
uncovered=$4
#filter ip address and do unique sort
grep -E -i  "apnic\|\w+\|ipv[46]" $delegatedFile | sed -E '
s/[^\|]+\|[^\|]+\|[^\|]+\|([0-9\.:a-zA-Z]+)\|([0-9]+)\|.*/\1 \2/g' >delegated_retrieved

#filter from inetnumFile for ip address
grep -E -i "^inetnum:[ \t]+" $inetnumFile | awk 'BEGIN{FS=" "}{print $2, $4}' >inetnum_retrieved

#filter from inet6numFile for ip address
grep -E -i "^inet6num:[ \t]+" $inet6numFile | awk 'BEGIN{FS="[ ]+|\/"}{print $2, $3}' >inet6num_retrieved
exit 0


num=0
while read line;
do
  count1=$(grep -E -c -m 1 "^$line$" inetnum_retrieved)
  count2=$(grep -E -c -m 1 "^$line$" inet6num_retrieved)
  if [ $count1 -eq 0 -a $count2 -eq 0 ] 
  then
	echo "$line uncoverred"
	echo $line >>$uncovered
	((num++))
  fi
done <delegated_retrieved
echo "uncoverred prefixes: $num"
