#!/bin/bash
#rm -rf /data/salrwais/BPH/Whois/API/AFRINIC/Data/latest/*

currDir=$(pwd)
apiDir="/data/salrwais/BPH/Whois/API/RIPE/Data"
tempDir=$currDir/temp_$(date +"%Y%m%d_%H%M%S")
mkdir -p $tempDir
dates="20160224 20160225 20160324 20160325 20160424 20160425"
date="20160224"
for date in ${dates[@]}
do
  echo ${date}
  file=$apiDir/${date}.7z
  if [ ! -e $file ];then
	echo "$file doesn't exist"
	exit 1
  fi
  7z x $file -o$tempDir $date/person* $date/irt* $date/mntner* $date/role*
done
