#!/bin/bash
apiDir=/data/salrwais/BPH/Whois/API/
date=$(date +"%Y%m%d")
startDate=$date
endDate=$date
currDir=$(pwd)
if [ $# -ge 2 ];then
  startDate=$1
  endDate=$2
fi
if [ $# -ge 3 ];then
  registryList=$3
else
  registryList=("RIPE" "LACNIC" "AFRINIC")
fi
if [ $# -ge 4 ];then
  apiDir=$4
fi
if [ $# -ge 5 ];then
  currDir=$5
fi
date=$startDate
#registryList=("RIPE" "LACNIC" "AFRINIC")
echo "start to compress for $startDate to $endDate of dir $apiDir"
while [ $date -le $endDate ]
do
  for registry in ${registryList[@]}
  do
    dataDir=$apiDir/$registry/Data/$date
	echo $dataDir
    if [ -e $dataDir ];then
#extract using 7z x rather than 7z e
#besides, to back up, instead of using the following, tar cf - dir | 7z a -si result.7z is recommended, to 
#extract using 7z x -so result.7z | tar xf -
      7z a -t7z -m0=lzma -mx=9 -mfb=64 -md=32m -ms=on ${dataDir}.7z $dataDir
      if [ $? -eq 0 -a -e ${dataDir}.7z ];then
        echo "success compress $dataDir"
        rm -rf $dataDir
      fi
	else
	  echo "dir doesn't exist"
    fi
  done
  date=$(date -d "$date +1day" +"%Y%m%d")
done


