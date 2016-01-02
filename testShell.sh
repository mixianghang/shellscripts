#!/bin/bash
#if [ "$#" -lt 2 ]
#then
#  echo "usage wrong"
#  exit 1
#fi
#echo $1
#echo $2
#curDir=$(pwd)
#ls -all $curDir

#test shell array
#array1['nihao']=4
#array=("inetnum" "inet6num")
#echo ${array1[*]}
#echo ${array[1]}
#i=0
#for i in ${array[@]}
#do
#    echo $i
#done

#test shell date, can be used on linux rather than mac
#echo $(date -d "-1 day" +%Y%m%d%H%M%S)
#echo $(date -d "tomorrow" +%Y%m%d%H%M%S)
#echo $(date -d "+1 year" +%Y%m%d%H%M%S)

#test shell date on mac
#echo $(date -v-1d +%Y%m%d%H%M%S)
#echo $(date -v-1m +%Y%m%d%H%M%S)

#test dir
dir="bph"
if [ -d $dir/whoisData ]
then
  echo $dir
fi

#test 
#date=$1
#date1=$(date -d "$date -1 day +%Y%m%d%H%M%S")
#echo $date1
