#!/bin/bash
START=$(date +%s)
sleep 2
END=$(date +%s)
echo $START
echo $END
DIFF=$(($END - $START))
echo "time cost is $DIFF"
exit

date=$1
path=/data/salrwais/BPH/Whois/bulkWhois/LACNIC/20151228/
if [ ! -e "/data/salrwais/BPH/Whois/bulkWhois/LACNIC/20151228/" ];then
  echo "$path doesn't exist"
fi
if [ ! -e "/data/salrwais/BPH/Whois/bulkWhois/ARIN/$date/arin.zip" ];then
  echo "/data/salrwais/BPH/Whois/bulkWhois/ARIN/$date/arin.zip doesn't exist"
fi
echo "done"
